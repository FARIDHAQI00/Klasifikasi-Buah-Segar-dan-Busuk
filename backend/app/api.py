from __future__ import annotations

import io
from typing import Literal

from fastapi import FastAPI, File, HTTPException, Request, UploadFile
from PIL import Image, UnidentifiedImageError
from pydantic import BaseModel

from .decision_policy import decide
from .model_loader import load_model, predict, read_manifest
from .preprocessing import prepare_image

MAX_FILE_BYTES = 4 * 1024 * 1024
MAX_BODY_BYTES = 4_500_000
MAX_IMAGE_PIXELS = 20_000_000
ALLOWED_FORMATS = {"JPEG", "PNG", "WEBP"}

app = FastAPI(
    title="CekBuah API",
    description="API inferensi ResNet50 untuk foto apel, pisang, dan jeruk.",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url=None,
)


class PredictionResponse(BaseModel):
    status: Literal["rotten", "review"]
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
        "fresh_auto_label_enabled": manifest["fresh_auto_label_enabled"],
    }


@app.post("/api/v1/predict", response_model=PredictionResponse)
async def classify_image(
    request: Request,
    file: UploadFile = File(..., description="Foto apel, pisang, atau jeruk"),
) -> PredictionResponse:
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
    try:
        tensor = prepare_image(image_bytes)
        scores = predict(tensor)
    except Exception as exc:
        raise HTTPException(
            status_code=503,
            detail="Model belum dapat memproses foto. Coba lagi beberapa saat.",
        ) from exc

    decision = decide(scores)
    manifest = read_manifest()
    return PredictionResponse(
        status=decision.status,
        fruit=decision.fruit,
        reason=decision.reason,
        model_version=manifest["model_version"],
        policy_version=manifest["policy_version"],
    )
