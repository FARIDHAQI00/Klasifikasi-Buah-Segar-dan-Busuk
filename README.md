# CekBuah

Website demo untuk menguji foto apel, pisang, dan jeruk dengan model **ResNet50** dari notebook UAS.

## Model

- Artefak: [`backend/model/ResNet50_terbaik.keras`](backend/model/ResNet50_terbaik.keras)
- Manifest kelas, preprocessing, dan SHA-256: [`backend/model/model_manifest.json`](backend/model/model_manifest.json)
- Enam kelas model dipetakan langsung: indeks 0–2 menjadi **Segar**, indeks 3–5 menjadi **Busuk**.
- Notebook melaporkan akurasi test 97,69% pada 2.727 gambar dan 31 gambar busuk tertebak Segar. Hasil foto baru adalah perkiraan visual, jadi periksa buah secara langsung.

## Menjalankan lokal

Gunakan Python 3.12 dan Node.js yang mendukung Vite 8.

Terminal backend:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r backend\requirements.txt
Set-Location backend
python -m uvicorn main:app --reload --port 8000
```

Terminal frontend:

```powershell
Set-Location frontend
npm install
npm run dev
```

Frontend meneruskan `/api/*` ke FastAPI di `http://127.0.0.1:8000`. API menerima JPEG, PNG, atau WebP sampai 4 MB. `POST /api/v1/predict/stream` mengirim riwayat langkah backend dan hasil melalui SSE; `POST /api/v1/predict` tetap tersedia dengan respons JSON. `GET /api/health` memeriksa model.

Riwayat UI mengikuti event aktual: validasi foto, preprocessing RGB 160 × 160, kesiapan model ResNet50, inferensi, lalu pemetaan Segar/Busuk.

Tes backend: `python -m unittest discover -s backend/tests -v`.

## Deploy ke Vercel

1. Impor repo ini ke Vercel dengan root project di root repo. `vercel.json` mengatur frontend Vite, backend FastAPI, dan routing `/api/*`.
2. Deploy preview, lalu cek `/api/health` dan coba foto Segar serta Busuk sebelum mengarahkan domain demo.
3. Paket TensorFlow + model dapat melebihi batas Function standar 500 MB. Jika bundle melewati batas, aktifkan Large Functions pada project Vercel (`VERCEL_SUPPORT_LARGE_FUNCTIONS=1` jika diminta) dan cek cold start serta memori.
4. Request body Vercel dibatasi 4,5 MB; batas upload aplikasi adalah 4 MB.

Preview Vercel perlu dijalankan dari project dan akun Vercel pemilik repo.
