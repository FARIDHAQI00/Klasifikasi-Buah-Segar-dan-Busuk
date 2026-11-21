"""FastAPI routes for model health, photo validation, prediction, and SSE progress."""
from __future__ import annotations

import io
import json
import logging
import time
import uuid
from typing import Literal

from fastapi import FastAPI, File, HTTPException, Request, UploadFile
from PIL import Image, UnidentifiedImageError
from pydantic import BaseModel
from starlette.concurrency import run_in_threadpool
from starlette.responses import StreamingResponse

from .decision_policy import decide
from .model_loader import load_model, predict, read_manifest
from .preprocessing import prepare_image

MAX_FILE_BYTES = 4 * 1024 * 1024
MAX_BODY_BYTES = 4_500_000
MAX_IMAGE_PIXELS = 20_000_000
ALLOWED_FORMATS = {"JPEG", "PNG", "WEBP"}
logger = logging.getLogger(__name__)

app = FastAPI(
    title="CekBuah API",
    description="API inferensi ResNet50 untuk foto apel, pisang, dan jeruk.",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url=None,
)


class PredictionResponse(BaseModel):
    status: Literal["fresh", "rotten"]
    fruit: str | None
    reason: str
    model_version: str
    policy_version: str


def inspect_image(image_bytes: bytes) -> None:
    try:
        with Image.open(io.BytesIO(image_bytes)) as image:
            if image.format not in ALLOWED_FORMATS:
                raise HTTPException(
                    status_code=415,
                    detail="Gunakan foto JPEG, PNG, atau WebP.",
                )
            width, height = image.size
            if width < 1 or height < 1 or width * height > MAX_IMAGE_PIXELS:
                raise HTTPException(
                    status_code=413,
                    detail="Resolusi foto terlalu besar. Gunakan gambar di bawah 20 megapiksel.",
                )
            image.verify()
    except HTTPException:
        raise
    except (UnidentifiedImageError, OSError, ValueError) as exc:
        raise HTTPException(
            status_code=400,
            detail="File tidak dapat dibaca sebagai gambar. Pilih ulang foto JPEG, PNG, atau WebP.",
        ) from exc


async def read_validated_image(request: Request, file: UploadFile) -> bytes:
    content_length = request.headers.get("content-length")
    if content_length:
        try:
            if int(content_length) > MAX_BODY_BYTES:
                raise HTTPException(
                    status_code=413,
                    detail="Ukuran request terlalu besar. Pilih foto maksimal 4 MB.",
                )
        except ValueError:
            raise HTTPException(status_code=400, detail="Header ukuran request tidak valid.")

    image_bytes = await file.read(MAX_FILE_BYTES + 1)
    await file.close()
    if not image_bytes:
        raise HTTPException(status_code=400, detail="File foto kosong.")
    if len(image_bytes) > MAX_FILE_BYTES:
        raise HTTPException(status_code=413, detail="Ukuran foto maksimal 4 MB.")

    inspect_image(image_bytes)
    return image_bytes


def encode_stream_event(event: dict[str, object]) -> bytes:
    payload = json.dumps(event, ensure_ascii=False, separators=(",", ":"))
    return f"data: {payload}\n\n".encode("utf-8")


@app.get("/api/health")
def health() -> dict[str, object]:
    try:
        load_model()
        return {"status": "ready", "model": "ResNet50", "model_loaded": True}
    except Exception as exc:
        raise HTTPException(status_code=503, detail="Model ResNet50 belum siap.") from exc


@app.get("/api/v1/model-info")
def model_info() -> dict[str, object]:
    manifest = read_manifest()
    return {
        "architecture": manifest["architecture"],
        "model_version": manifest["model_version"],
        "input_size": manifest["input_size"],
        "classes": manifest["classes"],
        "policy_version": manifest["policy_version"],
        "decision_method": manifest["decision_method"],
    }


@app.post("/api/v1/predict", response_model=PredictionResponse)
async def classify_image(
    request: Request,
    file: UploadFile = File(..., description="Foto apel, pisang, atau jeruk"),
) -> PredictionResponse:
    image_bytes = await read_validated_image(request, file)
    try:
        tensor = prepare_image(image_bytes)
        scores = predict(tensor)
        decision = decide(scores)
    except Exception as exc:
        raise HTTPException(
            status_code=503,
            detail="Model belum dapat memproses foto. Coba lagi beberapa saat.",
        ) from exc
    manifest = read_manifest()
    return PredictionResponse(
        status=decision.status,
        fruit=decision.fruit,
        reason=decision.reason,
        model_version=manifest["model_version"],
        policy_version=manifest["policy_version"],
    )


@app.post("/api/v1/predict/stream")
async def classify_image_stream(
    request: Request,
    file: UploadFile = File(..., description="Foto apel, pisang, atau jeruk"),
) -> StreamingResponse:
    request_id = uuid.uuid4().hex[:12]

    def step_event(
        step: str,
        status: str,
        duration_ms: float | None = None,
    ) -> bytes:
        event: dict[str, object] = {
            "type": "step",
            "step": step,
            "status": status,
            "request_id": request_id,
        }
        if duration_ms is not None:
            event["duration_ms"] = round(duration_ms, 1)
        logger.info(
            "prediction_step request_id=%s step=%s status=%s duration_ms=%s",
            request_id,
            step,
            status,
            round(duration_ms, 1) if duration_ms is not None else "-",
        )
        return encode_stream_event(event)

    async def event_stream():
        current_step = "validation"
        step_started = time.perf_counter()

        try:
            yield step_event(current_step, "running")
            image_bytes = await read_validated_image(request, file)
            yield step_event(
                current_step, "complete", (time.perf_counter() - step_started) * 1000
            )

            current_step = "preprocessing"
            step_started = time.perf_counter()
            yield step_event(current_step, "running")
            tensor = await run_in_threadpool(prepare_image, image_bytes)
            yield step_event(
                current_step, "complete", (time.perf_counter() - step_started) * 1000
            )

            current_step = "model"
            step_started = time.perf_counter()
            yield step_event(current_step, "running")
            await run_in_threadpool(load_model)
            yield step_event(
                current_step, "complete", (time.perf_counter() - step_started) * 1000
            )

            current_step = "inference"
            step_started = time.perf_counter()
            yield step_event(current_step, "running")
            scores = await run_in_threadpool(predict, tensor)
            yield step_event(
                current_step, "complete", (time.perf_counter() - step_started) * 1000
            )

            current_step = "label"
            step_started = time.perf_counter()
            yield step_event(current_step, "running")
            decision = decide(scores)
            manifest = read_manifest()
            result = PredictionResponse(
                status=decision.status,
                fruit=decision.fruit,
                reason=decision.reason,
                model_version=manifest["model_version"],
                policy_version=manifest["policy_version"],
            )
            yield step_event(
                current_step, "complete", (time.perf_counter() - step_started) * 1000
            )
            logger.info(
                "prediction_result request_id=%s status=%s fruit=%s",
                request_id,
                result.status,
                result.fruit,
            )
            yield encode_stream_event(
                {"type": "result", "request_id": request_id, "result": result.model_dump()}
            )
        except HTTPException as exc:
            duration_ms = (time.perf_counter() - step_started) * 1000
            logger.warning(
                "prediction_validation_failed request_id=%s status=%s",
                request_id,
                exc.status_code,
            )
            yield step_event(current_step, "error", duration_ms)
            yield encode_stream_event(
                {"type": "error", "detail": str(exc.detail), "request_id": request_id}
            )
        except Exception:
            duration_ms = (time.perf_counter() - step_started) * 1000
            logger.exception(
                "prediction_failed request_id=%s step=%s", request_id, current_step
            )
            yield step_event(current_step, "error", duration_ms)
            yield encode_stream_event(
                {
                    "type": "error",
                    "detail": "Model belum dapat memproses foto. Coba lagi beberapa saat.",
                    "request_id": request_id,
                }
            )

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache, no-transform",
            "X-Accel-Buffering": "no",
        },
    )
