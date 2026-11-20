import { useEffect, useRef, useState } from "react";
import {
  Camera,
  CircleAlert,
  CircleCheck,
  ImagePlus,
  LoaderCircle,
  RotateCcw,
  ScanLine,
  ShieldCheck,
  ShoppingBasket,
  TriangleAlert,
  Upload,
  X,
} from "lucide-react";

const MAX_FILE_BYTES = 4 * 1024 * 1024;
const ACCEPTED_TYPES = new Set(["image/jpeg", "image/png", "image/webp"]);
const PROCESS_STEPS = [
  { id: "validation", label: "Validasi format dan ukuran foto" },
  { id: "preprocessing", label: "Preprocessing RGB · 160 × 160" },
  { id: "model", label: "Menyiapkan model ResNet50" },
  { id: "inference", label: "Inferensi enam kelas" },
  { id: "label", label: "Pemetaan label Segar/Busuk" },
] as const;

type ProcessingStepId = (typeof PROCESS_STEPS)[number]["id"];
type ProcessingStatus = "pending" | "running" | "complete" | "error";
type ProcessingLogItem = {
  id: ProcessingStepId;
  label: string;
  status: ProcessingStatus;
  durationMs?: number;
};

const PROCESSING_STATUS_LABELS: Record<ProcessingStatus, string> = {
  pending: "Menunggu",
  running: "Berjalan",
  complete: "Selesai",
  error: "Gagal",
};

type ResultStatus = "fresh" | "rotten";

type Prediction = {
  status: ResultStatus;
  fruit: string | null;
  reason: string;
  model_version: string;
  policy_version: string;
};

function isPrediction(value: unknown): value is Prediction {
  if (!value || typeof value !== "object") return false;
  const result = value as Record<string, unknown>;
  return (
    (result.status === "fresh" || result.status === "rotten") &&
    (result.fruit === null || typeof result.fruit === "string") &&
    typeof result.reason === "string" &&
    typeof result.model_version === "string" &&
    typeof result.policy_version === "string"
  );
}

function responseDetail(value: unknown): string | undefined {
  if (!value || typeof value !== "object") return undefined;
  const detail = (value as Record<string, unknown>).detail;
  return typeof detail === "string" ? detail : undefined;
}

function createProcessingLog(): ProcessingLogItem[] {
  return PROCESS_STEPS.map((step) => ({ ...step, status: "pending" }));
}

function isProcessingStepId(value: unknown): value is ProcessingStepId {
  return PROCESS_STEPS.some((step) => step.id === value);
}

function isProcessingEventStatus(value: unknown): value is Exclude<ProcessingStatus, "pending"> {
  return value === "running" || value === "complete" || value === "error";
}

async function readPredictionStream(
  response: Response,
  onStep: (
    step: ProcessingStepId,
    status: Exclude<ProcessingStatus, "pending">,
    durationMs?: number,
  ) => void,
): Promise<Prediction> {
  if (!response.body) throw new Error("Log proses tidak tersedia dari server.");

  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";
  let prediction: Prediction | null = null;

  const handleEvent = (frame: string) => {
    const data = frame
      .split("\n")
      .filter((line) => line.startsWith("data:"))
      .map((line) => line.slice(5).trimStart())
      .join("\n");
    if (!data) return;

    let value: unknown;
    try {
      value = JSON.parse(data);
    } catch {
      throw new Error("Format log proses dari server tidak valid.");
    }
    if (!value || typeof value !== "object") {
      throw new Error("Log proses dari server tidak dikenali.");
    }

    const event = value as Record<string, unknown>;
    if (
      event.type === "step" &&
      isProcessingStepId(event.step) &&
      isProcessingEventStatus(event.status)
    ) {
      const durationMs =
        typeof event.duration_ms === "number" && Number.isFinite(event.duration_ms)
          ? event.duration_ms
          : undefined;
      onStep(event.step, event.status, durationMs);
      return;
    }
    if (event.type === "result" && isPrediction(event.result)) {
      prediction = event.result;
      return;
    }
    if (event.type === "error") {
      throw new Error(
        typeof event.detail === "string" ? event.detail : "Model gagal memproses foto.",
      );
    }
    throw new Error("Log proses dari server tidak dikenali.");
  };

  try {
    let done = false;
    while (!done) {
      const chunk = await reader.read();
      done = chunk.done;
      buffer += decoder.decode(chunk.value, { stream: !done }).replace(/\r\n/g, "\n");
      let frameEnd = buffer.indexOf("\n\n");
      while (frameEnd >= 0) {
        handleEvent(buffer.slice(0, frameEnd));
        buffer = buffer.slice(frameEnd + 2);
        frameEnd = buffer.indexOf("\n\n");
      }
    }
    if (buffer.trim()) handleEvent(buffer);
  } catch (streamError) {
    await reader.cancel().catch(() => undefined);
    throw streamError;
  } finally {
    reader.releaseLock();
  }

  if (!prediction) throw new Error("Server belum mengirim hasil prediksi.");
  return prediction;
}

function formatFileSize(bytes: number) {
  return `${(bytes / 1024 / 1024).toFixed(2)} MB`;
}

function formatDuration(durationMs: number) {
  if (durationMs < 1000) return `${Math.max(1, Math.round(durationMs))} ms`;
  return `${(durationMs / 1000).toLocaleString("id-ID", { maximumFractionDigits: 1 })} dtk`;
}

function App() {
  const inputRef = useRef<HTMLInputElement>(null);
  const [file, setFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState("");
  const [prediction, setPrediction] = useState<Prediction | null>(null);
  const [error, setError] = useState("");
  const [isDragging, setIsDragging] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [stepHistory, setStepHistory] = useState<ProcessingLogItem[]>([]);

  useEffect(() => {
    return () => {
      if (previewUrl) URL.revokeObjectURL(previewUrl);
    };
  }, [previewUrl]);

  function chooseFile(nextFile: File | undefined) {
    if (!nextFile) return;
    if (!ACCEPTED_TYPES.has(nextFile.type)) {
      setError("Format belum didukung. Pilih foto JPEG, PNG, atau WebP.");
      return;
    }
    if (nextFile.size > MAX_FILE_BYTES) {
      setError("Ukuran foto melebihi 4 MB. Pilih foto yang lebih kecil.");
      return;
    }

    setFile(nextFile);
    setPreviewUrl(URL.createObjectURL(nextFile));
    setPrediction(null);
    setError("");
    setStepHistory([]);
  }

  function removeFile() {
    setFile(null);
    setPreviewUrl("");
    setPrediction(null);
    setError("");
    setStepHistory([]);
    if (inputRef.current) inputRef.current.value = "";
  }

  function handleDrop(event: React.DragEvent<HTMLLabelElement>) {
    event.preventDefault();
    setIsDragging(false);
    chooseFile(event.dataTransfer.files[0]);
  }

  async function submitImage(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!file || isLoading) return;

    setStepHistory(createProcessingLog());
    setIsLoading(true);
    setError("");
    setPrediction(null);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("/api/v1/predict/stream", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        const payload: unknown = await response.json().catch(() => null);
        if ([400, 413, 415].includes(response.status)) {
          setStepHistory((current) =>
            current.map((step) =>
              step.id === "validation" ? { ...step, status: "error" } : step,
            ),
          );
        }
        if (response.status === 413) {
          throw new Error("Foto terlalu besar untuk diproses. Pilih foto maksimal 4 MB.");
        }
        throw new Error(responseDetail(payload) || "Foto belum dapat diproses. Coba pilih gambar lain.");
      }

      const result = await readPredictionStream(response, (stepId, status, durationMs) => {
        setStepHistory((current) =>
          current.map((step) =>
            step.id === stepId ? { ...step, status, durationMs } : step,
          ),
        );
      });
      setPrediction(result);
    } catch (requestError) {
      setError(
        requestError instanceof Error
          ? requestError.message
          : "Terjadi kendala saat menghubungi model. Coba lagi.",
      );
    } finally {
      setIsLoading(false);
    }
  }

  const resultTitle = prediction?.status === "rotten" ? "Busuk" : "Segar";

  return (
    <div className="site-shell">
      <a className="skip-link" href="#main-content">
        Langsung ke pemeriksaan
      </a>

      <header className="topbar page-width">
        <a className="brand" href="#main-content" aria-label="CekBuah, beranda">
          <span className="brand-mark" aria-hidden="true">
            <ShoppingBasket size={21} strokeWidth={2.2} />
          </span>
          <span>CekBuah</span>
        </a>
        <nav className="top-nav" aria-label="Navigasi utama">
          <a href="#alur">Cara kerja</a>
          <a href="#catatan">Batas hasil</a>
        </nav>
      </header>

      <main id="main-content">
        <section className="hero page-width" aria-labelledby="hero-title">
          <div className="hero-copy">
            <div className="market-label">
              <span className="market-label__seal" aria-hidden="true">
                <ScanLine size={18} />
              </span>
              Pemeriksaan visual buah
            </div>
            <h1 id="hero-title">Cek kondisi buah sebelum dibawa pulang.</h1>
            <p className="hero-description">
              Unggah satu foto apel, pisang, atau jeruk. Model ResNet50 membaca pola
              visualnya dan memberi hasil yang bisa ditinjau kembali.
            </p>

            <div className="fruit-list" aria-label="Jenis buah yang didukung">
              <span>Apel</span>
              <span>Pisang</span>
              <span>Jeruk</span>
            </div>

            <p className="privacy-note">
              <ShieldCheck size={18} strokeWidth={1.9} aria-hidden="true" />
              Foto diproses untuk prediksi dan tidak disimpan.
            </p>
          </div>

          <form className="inspection-panel" onSubmit={submitImage}>
            <div className="panel-heading">
              <div>
                <h2>Periksa satu buah</h2>
                <p>Gunakan foto yang terang dan memperlihatkan permukaannya.</p>
              </div>
              <span className="model-stamp">ResNet50</span>
            </div>

            {!file ? (
              <label
                className={`dropzone${isDragging ? " dropzone--active" : ""}`}
                htmlFor="fruit-image"
                onDragOver={(event) => {
                  event.preventDefault();
                  setIsDragging(true);
                }}
                onDragLeave={() => setIsDragging(false)}
                onDrop={handleDrop}
              >
                <input
                  ref={inputRef}
                  className="visually-hidden"
                  id="fruit-image"
                  type="file"
                  accept="image/jpeg,image/png,image/webp"
                  aria-label="Pilih foto buah"
                  onChange={(event) => {
                    chooseFile(event.currentTarget.files?.[0]);
                    event.currentTarget.value = "";
                  }}
                />
                <span className="upload-symbol" aria-hidden="true">
                  <ImagePlus size={25} strokeWidth={1.8} />
                </span>
                <span className="dropzone-title">Letakkan foto di sini</span>
                <span className="dropzone-support">atau pilih dari perangkat</span>
                <span className="choose-file-button">Pilih foto</span>
                <span className="dropzone-limit">JPG, PNG, atau WebP · maks. 4 MB</span>
              </label>
            ) : (
              <div className="selected-image">
                <div className="preview-frame">
                  <img src={previewUrl} alt={`Pratinjau ${file.name}`} />
                  <button
                    className="remove-image"
                    type="button"
                    onClick={removeFile}
                    aria-label="Hapus foto yang dipilih"
                    disabled={isLoading}
                  >
                    <X size={18} />
                  </button>
                </div>
                <div className="file-meta">
                  <div className="file-meta__text">
                    <strong title={file.name}>{file.name}</strong>
                    <span>{formatFileSize(file.size)}</span>
                  </div>
                  <button
                    className="replace-button"
                    type="button"
                    onClick={() => inputRef.current?.click()}
                    disabled={isLoading}
                  >
                    <RotateCcw size={15} aria-hidden="true" />
                    Ganti foto
                  </button>
                  <input
                    ref={inputRef}
                    className="visually-hidden"
                    type="file"
                    accept="image/jpeg,image/png,image/webp"
                    aria-label="Ganti foto buah"
                    onChange={(event) => {
                      chooseFile(event.currentTarget.files?.[0]);
                      event.currentTarget.value = "";
                    }}
                  />
                </div>
              </div>
            )}

            {error && (
              <div className="inline-error" role="alert">
                <CircleAlert size={18} aria-hidden="true" />
                <span>{error}</span>
              </div>
            )}

            {file && (
              <button className="submit-button" type="submit" disabled={isLoading}>
                {isLoading ? (
                  <>
                    <LoaderCircle className="spinner" size={18} aria-hidden="true" />
                    Sedang memeriksa
                  </>
                ) : (
                  <>
                    <Camera size={18} aria-hidden="true" />
                    Periksa kesegaran
                  </>
                )}
              </button>
            )}

            {stepHistory.length > 0 && (
              <section
                className={`step-history${isLoading ? " step-history--active" : ""}`}
                aria-label="Riwayat proses backend dan model"
                aria-live={isLoading ? "polite" : "off"}
                aria-atomic="false"
              >
                <div className="step-history__heading">
                  <h3>Riwayat proses</h3>
                  <span className={`step-history__summary${error ? " step-history__summary--error" : ""}`}>
                    {isLoading ? "Berjalan" : error ? "Terhenti" : "Selesai"}
                  </span>
                </div>
                <ol className="step-history__list">
                  {stepHistory.map((step, index) => (
                    <li key={step.id} className={`step-history__item step-history__item--${step.status}`}>
                      <span className="step-history__marker" aria-hidden="true">
                        {step.status === "complete" ? (
                          <CircleCheck size={17} />
                        ) : step.status === "running" ? (
                          <LoaderCircle className="spinner" size={17} />
                        ) : step.status === "error" ? (
                          <CircleAlert size={17} />
                        ) : (
                          index + 1
                        )}
                      </span>
                      <span className="step-history__label">{step.label}</span>
                      <span className="step-history__status">
                        {step.durationMs !== undefined && step.status !== "pending"
                          ? `${PROCESSING_STATUS_LABELS[step.status]} · ${formatDuration(step.durationMs)}`
                          : PROCESSING_STATUS_LABELS[step.status]}
                      </span>
                    </li>
                  ))}
                </ol>
              </section>
            )}

            {prediction && (
              <section
                className={`result-panel result-panel--${prediction.status}`}
                aria-labelledby="result-title"
                aria-live="polite"
              >
                <div className="result-heading">
                  <span className="result-icon" aria-hidden="true">
                    {prediction.status === "rotten" ? (
                      <TriangleAlert size={21} />
                    ) : (
                      <CircleCheck size={21} />
                    )}
                  </span>
                  <div>
                    <p className="result-label">Hasil pemeriksaan</p>
                    <h3 id="result-title">{resultTitle}</h3>
                  </div>
                </div>
                {prediction.fruit && (
                  <p className="fruit-detected">Jenis yang dikenali: {prediction.fruit}</p>
                )}
                <p className="result-reason">{prediction.reason}</p>
                <div className="result-footer">
                  <span>{prediction.model_version}</span>
                  <button type="button" onClick={removeFile}>
                    <RotateCcw size={14} aria-hidden="true" />
                    Coba foto lain
                  </button>
                </div>
              </section>
            )}

          </form>
        </section>

        <section className="process-section page-width" id="alur" aria-labelledby="process-title">
          <div className="section-heading">
            <h2 id="process-title">Dari foto sampai hasil.</h2>
            <p>Alur singkat agar setiap hasil mudah dipahami.</p>
          </div>
          <div className="process-steps">
            <article className="process-step">
              <span className="step-icon" aria-hidden="true">
                <Upload size={19} />
              </span>
              <div>
                <h3>Unggah satu foto</h3>
                <p>Pilih satu apel, pisang, atau jeruk dengan permukaan terlihat.</p>
              </div>
            </article>
            <article className="process-step">
              <span className="step-icon" aria-hidden="true">
                <ScanLine size={19} />
              </span>
              <div>
                <h3>ResNet50 membaca pola</h3>
                <p>Ukuran dan preprocessing mengikuti notebook training.</p>
              </div>
            </article>
            <article className="process-step">
              <span className="step-icon" aria-hidden="true">
                <CircleCheck size={19} />
              </span>
              <div>
                <h3>Tinjau hasilnya</h3>
                <p>Lihat perkiraan kondisi buah dari hasil klasifikasi.</p>
              </div>
            </article>
          </div>
        </section>

        <section className="limits-section page-width" id="catatan" aria-labelledby="limits-title">
          <div className="limits-icon" aria-hidden="true">
            <ShieldCheck size={22} />
          </div>
          <div>
            <h2 id="limits-title">Hasil model adalah perkiraan visual.</h2>
            <p>Periksa kondisi buah secara langsung sebelum dikonsumsi.</p>
          </div>
        </section>
      </main>

      <footer className="footer page-width">
        <span>CekBuah</span>
        <span>Demo klasifikasi buah · model ResNet50</span>
      </footer>
    </div>
  );
}

export default App;
