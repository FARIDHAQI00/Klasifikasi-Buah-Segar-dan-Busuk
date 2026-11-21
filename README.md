# CekBuah

Website demo untuk menguji foto apel, pisang, dan jeruk dengan model **ResNet50** dari notebook UAS.

Demo aktif: [klasifikasibuah.vercel.app](https://klasifikasibuah.vercel.app). Deployment dan alur klasifikasi pada sampel yang tersedia sudah dicek.

Lihat [`dokumentasi.md`](dokumentasi.md) untuk peta berkas, workflow klasifikasi, dan pengecekan kesesuaian dengan notebook.

## Model

- Artefak: [`backend/model/ResNet50_terbaik.keras`](backend/model/ResNet50_terbaik.keras)
- Manifest kelas, preprocessing, dan SHA-256: [`backend/model/model_manifest.json`](backend/model/model_manifest.json)
- Gerbang COCO-SSD Lite di browser mendeteksi apel, pisang, atau jeruk lalu memotong tiap objek untuk dinilai ResNet50.
- Tiap potongan memakai enam kelas ResNet50. Kotak pisang dibagi menjadi tiga slice tumpang-tindih; jika satu potongan diprediksi Busuk, hasil foto menjadi **Busuk**.
- Jika tidak ada buah target terdeteksi, foto berhenti di browser dan ditampilkan sebagai **Foto tidak dikenali**.
- Pada data test notebook, 31 dari 1.548 gambar busuk tertebak Segar oleh `argmax` mentah. Hasil foto baru adalah perkiraan visual, jadi periksa buah secara langsung.

Detektor COCO-SSD adalah model objek umum dengan 80 kelas, termasuk apple, banana, dan orange. Gerbang ini menolak foto saat tak ada objek buah target terdeteksi; deteksi model umum tetap dapat luput pada foto buram, tertutup, atau sangat jauh. Untuk buah campuran, keputusan Busuk menang bila salah satu potongan objek yang terdeteksi diprediksi busuk.

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

Frontend meneruskan `/api/*` ke FastAPI di `http://127.0.0.1:8000`. COCO-SSD memeriksa foto di browser dan hanya potongan buah terdeteksi yang dikirim ke backend. API menerima JPEG, PNG, atau WebP sampai 4 MB per berkas. `POST /api/v1/predict/stream` menerima satu `file` atau beberapa `files`, mengirim riwayat backend dan hasil melalui SSE; `POST /api/v1/predict` tetap tersedia dengan respons JSON untuk satu foto. `GET /api/health` memeriksa model.

Riwayat UI mengikuti proses aktual: deteksi buah di browser, validasi, preprocessing RGB 160 × 160 per potongan, kesiapan model, inferensi per potongan, lalu agregasi hasil.

Tes backend: `python -m unittest discover -s backend/tests -v`.

## Deploy ke Vercel

1. Impor repo ini ke Vercel dengan root project di root repo. `vercel.json` mengatur frontend Vite, backend FastAPI, dan routing `/api/*`.
2. Deploy preview, lalu cek `/api/health` dan coba foto Segar serta Busuk sebelum mengarahkan domain demo.
3. Paket TensorFlow + model dapat melebihi batas Function standar 500 MB. Jika bundle melewati batas, aktifkan Large Functions pada project Vercel (`VERCEL_SUPPORT_LARGE_FUNCTIONS=1` jika diminta) dan cek cold start serta memori.
4. Request body Vercel dibatasi 4,5 MB; batas upload aplikasi adalah 4 MB.

Preview Vercel perlu dijalankan dari project dan akun Vercel pemilik repo.
