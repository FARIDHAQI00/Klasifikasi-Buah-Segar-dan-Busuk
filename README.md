# CekBuah

Website demo untuk menguji foto apel, pisang, dan jeruk dengan model **ResNet50** dari notebook UAS.

## Artefak model

- Model yang dipakai: [`backend/model/ResNet50_terbaik.keras`](backend/model/ResNet50_terbaik.keras)
- Manifest, urutan kelas, preprocessing, dan SHA-256: [`backend/model/model_manifest.json`](backend/model/model_manifest.json)
- Aplikasi tidak memilih arsitektur lain dan tidak mengunduh model saat request.
- Dataset, checkpoint training, dan foto pengunjung tidak disimpan di repo atau server.

## Kebijakan hasil saat ini

Notebook mencatat akurasi test 97,69% pada 2.727 gambar, tetapi argmax mentah memberi label kelas segar kepada 31 gambar busuk. Karena arsip gambar validation lokal yang tersedia terpotong, ambang aman belum dapat dikalibrasi dari data yang sesuai. Sampai gerbang false-fresh lulus, backend hanya dapat mengeluarkan **Busuk** atau **Perlu diperiksa**; hasil yang mengarah ke kelas segar tidak akan ditampilkan sebagai **Segar**.

Untuk mengaktifkan **Segar** pada iterasi mendatang, siapkan split validation lengkap yang dipakai run model ini, tetapkan ambang tanpa melihat test, lalu evaluasi sekali di test terkunci. Jika ada satu saja false-fresh pada kriteria rilis, status otomatis Segar harus tetap mati. Saat ini API memakai kelas argmax: kelas busuk menghasilkan **Busuk**, sedangkan kelas segar menghasilkan **Perlu diperiksa**. Backend tidak mengklaim mengenali gambar non-buah atau jenis buah di luar apel, pisang, dan jeruk.

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

Frontend Vite meneruskan `/api/*` ke `http://127.0.0.1:8000`. API menerima JPEG, PNG, atau WebP sampai 4 MB melalui `POST /api/v1/predict`. `GET /api/health` memuat dan memeriksa model; `GET /api/v1/model-info` menampilkan metadata model dan kebijakan.

Jalankan regression tests backend dari root repo setelah memasang dependensi:

```powershell
python -m unittest discover -s backend/tests -v
```

Tes ini memeriksa pemetaan enam kelas, status fallback aman, skor invalid, format gambar, ukuran tensor, dan preprocessing ResNet50.

## Deploy ke Vercel

1. Impor repo GitHub ini sebagai satu project Vercel dengan root project di root repo. [`vercel.json`](vercel.json) mendeklarasikan service frontend Vite dan backend FastAPI, mengarahkan `/api/*` ke backend, dan path lainnya ke frontend. Ikuti preset/framework Services yang ditawarkan dashboard.
2. Vercel Services tersedia sebagai Beta. Jalankan `vercel dev --local` untuk memeriksa routing Services lokal, lalu buat deployment preview sebelum production.
3. Pada preview, periksa `/api/health`, unggah foto di bawah 4 MB, dan catat ukuran bundle Python, cold start, memori, serta waktu inference.
4. Paket Python standar memiliki batas 500 MB tanpa kompresi. Jika bundel TensorFlow + model melampauinya, aktifkan Large Functions (maksimum 5 GB pada Fluid Compute Beta); untuk project yang meminta opt-in, tambahkan `VERCEL_SUPPORT_LARGE_FUNCTIONS=1` pada Environment Variables. Request body Vercel Function tetap dibatasi 4,5 MB.
5. Promosikan ke production hanya setelah preview berfungsi dan gerbang false-fresh untuk model ini dinyatakan lulus. Sampai saat itu UI menjelaskan bahwa status Segar otomatis terkunci.

File repo menyiapkan routing dan source, tetapi project Vercel, deployment preview, pengukuran runtime, serta environment variable Large Functions (bila diminta) masih perlu disiapkan di akun Vercel. Jangan mengaktifkan produksi sebelum gerbang keselamatan model terpenuhi.
