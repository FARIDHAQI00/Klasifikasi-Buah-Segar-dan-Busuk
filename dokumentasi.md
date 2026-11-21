# Dokumentasi Proyek CekBuah

Dokumen ini menjelaskan peran setiap berkas utama, alur foto dari browser sampai hasil, hubungan pipeline website dengan notebook training, serta cara menjalankan dan men-deploy aplikasi.

## Ringkasan

CekBuah adalah demo klasifikasi kondisi apel, pisang, dan jeruk menggunakan satu foto dan artefak `ResNet50_terbaik.keras`. Backend FastAPI menjalankan preprocessing dan inference; frontend React mengirim foto, menampilkan tahapan proses, lalu menampilkan label **Segar** atau **Busuk**.

Website menggunakan keputusan enam kelas langsung dari `argmax`. Tidak ada confidence percentage atau batas tambahan di UI. Foto tidak disimpan dan riwayat hanya berlaku pada permintaan yang sedang berjalan.

## Struktur dan Tanggung Jawab Berkas

### Frontend

| Berkas | Tanggung jawab |
| --- | --- |
| `frontend/index.html` | Metadata halaman, warna browser, favicon, dan mount point React. |
| `frontend/src/main.tsx` | Membuat root React dan memasang `App` serta stylesheet global. |
| `frontend/src/App.tsx` | Upload dan preview foto, validasi sisi klien, permintaan SSE, riwayat proses, hasil, dan error. |
| `frontend/src/styles.css` | Token warna, tipografi, background orb, layout responsif, status hasil, dan animasi. |
| `frontend/src/vite-env.d.ts` | Deklarasi tipe frontend Vite dan impor CSS. |
| `frontend/public/favicon.svg` | Ikon tab browser yang memakai bentuk Lucide `ShoppingBasket`, sama dengan ikon header CekBuah. |
| `frontend/public/cekbuah-orb.svg` | Ilustrasi orb kaca, sorot lavender, garis orbit, dan flare untuk background hero. |
| `frontend/vite.config.ts` | Plugin React/Tailwind dan proxy `/api` untuk development lokal. |
| `frontend/package.json` | Dependensi dan perintah frontend. |
| `frontend/package-lock.json` | Versi dependensi frontend yang dikunci oleh npm. |
| `frontend/tsconfig.json` | Referensi konfigurasi TypeScript frontend. |
| `frontend/tsconfig.app.json` | Pemeriksaan TypeScript untuk aplikasi React. |
| `frontend/tsconfig.node.json` | Pemeriksaan TypeScript untuk konfigurasi Vite. |

### Backend dan model

| Berkas | Tanggung jawab |
| --- | --- |
| `backend/main.py` | Entry point FastAPI untuk runtime Vercel. |
| `backend/app/__init__.py` | Penanda package aplikasi backend. |
| `backend/app/api.py` | Endpoint health/model info/prediksi, validasi request dan gambar, serta SSE tahapan dan hasil. |
| `backend/app/preprocessing.py` | Decode RGB, resize 160×160, konversi float32, dan preprocessing ResNet50. |
| `backend/app/model_loader.py` | Memeriksa hash, memuat model satu kali per proses, dan menjalankan inference. |
| `backend/app/decision_policy.py` | Memilih kelas dengan `argmax` lalu menentukan jenis buah dan label Segar/Busuk. |
| `backend/model/ResNet50_terbaik.keras` | Satu-satunya artefak model yang digunakan website. |
| `backend/model/model_manifest.json` | Sumber nilai hash, kelas, ukuran input, versi, preprocessing, dan catatan evaluasi model. JSON dipertahankan tanpa komentar agar valid. |
| `backend/requirements.txt` | Dependensi Python runtime FastAPI, Pillow, multipart, TensorFlow, dan Uvicorn. |
| `backend/tests/test_preprocessing.py` | Pemeriksaan preprocessing format JPEG/PNG/WebP dan nilai RGB ResNet50. |
| `backend/tests/test_decision_policy.py` | Pemeriksaan pemetaan enam kelas, tie, dan output skor invalid. |

### Root dan deployment

| Berkas | Tanggung jawab |
| --- | --- |
| `vercel.json` | Definisi layanan frontend/backend Vercel dan rewrite `/api/*`; JSON tidak mendukung komentar. |
| `README.md` | Petunjuk ringkas menjalankan dan deploy aplikasi. |
| `dokumentasi.md` | Peta berkas, workflow klasifikasi, kecocokan notebook, endpoint, dan catatan model. |
| `PRODUCT.md` | Batasan dan tujuan produk demo. |
| `PLAN.md` | Rencana build, keputusan teknis, serta status kesiapan deploy. |
| `DESIGN.md` | Sistem visual, token, layout, komponen, dan aksesibilitas. |
| `.impeccable/cekbuah-surface.md` | Arah desain dan batasan konten untuk halaman CekBuah. |
| `.impeccable/cekbuah-quality-bar.md` | Kriteria visual yang berasal dari referensi pengguna. |
| `.impeccable/design.json` | Sidecar desain untuk editor/tooling; JSON tidak mendukung komentar. |
| `.gitignore` | Mengabaikan hasil build, cache, environment, dan file data lokal. |

File JSON dan model biner tidak diberi komentar di dalamnya karena akan merusak formatnya; fungsi file tersebut dicatat di tabel ini. Berkas kode Python, TypeScript/TSX, CSS, HTML, SVG, dan daftar dependensi memiliki komentar atau docstring pembuka.

## Kecocokan dengan Notebook

Notebook yang diperiksa adalah salinan lokal `outputs/UAS_Buah_Cepat_Resume.ipynb`, sesuai judul pada screenshot. Notebook Colab yang dibagikan pengguna ada di [tautan ini](https://colab.research.google.com/drive/16t9E0vxdy2ZF-86ZbjetxU_yVwtDOmON?usp=sharing). Link Colab tidak dapat dibaca langsung oleh pemeriksa web, sehingga perbandingan dilakukan pada salinan notebook lokal.

| Operasi | Notebook | Website | Cocok? |
| --- | --- | --- | --- |
| Urutan kelas | `freshapples`, `freshbanana`, `freshoranges`, `rottenapples`, `rottenbanana`, `rottenoranges` | Urutan yang sama di `model_manifest.json` dan `decision_policy.py` | Ya |
| Decode | `tf.io.decode_image(..., channels=3, expand_animations=False)` | `prepare_image()` memakai parameter yang sama | Ya |
| Resize | `tf.image.resize(image, (160, 160))` | Bilinear, antialias off; sama dengan default notebook | Ya |
| Input preprocessing | `tf.keras.applications.resnet50.preprocess_input(x)` sesudah float32 RGB 0–255 | Pemanggilan yang sama pada tensor resize | Ya |
| Model | ImageNet ResNet50 dibekukan, Global Average Pooling, Dropout 0.3, Dense 6 softmax | Model tersimpan dijalankan dengan `training=False`; lapisan berada di dalam artefak yang sama | Ya |
| Keputusan kelas | `np.argmax(probability, axis=1)` | `np.argmax()` di `decision_policy.py` | Ya |
| Augmentasi | Flip dan perubahan brightness hanya pada dataset training | Tidak diterapkan saat prediksi foto website | Benar; augmentasi training tidak boleh dijalankan pada inference |

Jadi transformasi tensor, model, urutan kelas, dan metode keputusan website sudah mengikuti notebook. Tidak perlu mengubah bobot atau preprocessing. Perbedaan tambahan adalah langkah operasional website: validasi file dan memastikan model siap dimuat.

### Arti lima tahap di riwayat

1. **Validasi format dan ukuran foto** — pemeriksaan request website; tahap ini tidak mengubah tensor model.
2. **Preprocessing ResNet50 · RGB 160 × 160** — satu baris riwayat yang merangkum decode, resize, float32, dan `preprocess_input` notebook.
3. **Menyiapkan model ResNet50** — memastikan artefak terverifikasi dan siap; model dimuat malas sekali per proses, lalu dipakai ulang.
4. **Inferensi ResNet50 · enam kelas** — forward pass model yang mencakup lapisan ResNet50, pooling, dropout mode inference, dan softmax.
5. **Argmax · label Segar/Busuk** — memilih skor terbesar, mencari buah, lalu memetakan indeks kelas ke Segar atau Busuk.

Backend mengirim event `running` dan `complete` ketika masuk/keluar dari tiap kelompok tahap. Frontend menampilkan event secara berurutan dan menahan status berjalan minimal 240 ms agar langkah yang sangat cepat tetap terlihat. Angka durasi di setiap baris tetap durasi terukur backend; jeda UI tidak mengubah waktu yang ditampilkan atau hasil model.

### Pemetaan kelas

| Indeks | Kelas notebook | Hasil UI |
| ---: | --- | --- |
| 0 | `freshapples` | Segar · Apel |
| 1 | `freshbanana` | Segar · Pisang |
| 2 | `freshoranges` | Segar · Jeruk |
| 3 | `rottenapples` | Busuk · Apel |
| 4 | `rottenbanana` | Busuk · Pisang |
| 5 | `rottenoranges` | Busuk · Jeruk |

## Alur Workflow Klasifikasi

```text
Pilih foto
  → frontend/src/App.tsx: cek tipe/ukuran dan tampilkan preview
  → POST /api/v1/predict/stream dengan multipart field `file`
  → backend/app/api.py: validasi format, ukuran, resolusi, dan integritas gambar
  → backend/app/preprocessing.py: decode RGB → resize 160×160 → float32 → ResNet50 preprocess_input
  → backend/app/model_loader.py: cocokkan SHA-256, muat/cache model, jalankan forward pass
  → backend/app/decision_policy.py: argmax 6 skor → buah + Segar/Busuk
  → backend/app/api.py: kirim event SSE setiap tahap dan event hasil
  → frontend/src/App.tsx: tampilkan riwayat terurut dan hasil akhir
```

Semua event dan hasil hanya berlaku untuk request saat itu. Foto tidak ditulis ke disk atau database.

## API

| Method | Path | Fungsi |
| --- | --- | --- |
| `GET` | `/api/health` | Memastikan model dapat dimuat. |
| `GET` | `/api/v1/model-info` | Menampilkan arsitektur, versi, kelas, input, dan metode keputusan. |
| `POST` | `/api/v1/predict/stream` | Prediksi dan event proses melalui SSE; digunakan UI. |
| `POST` | `/api/v1/predict` | Prediksi JSON tanpa riwayat SSE. |

Foto dibatasi JPEG/PNG/WebP sampai 4 MB. API juga menolak gambar tidak valid atau lebih dari 20 megapiksel.

## Menjalankan Lokal

Backend:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r backend\requirements.txt
Set-Location backend
python -m uvicorn main:app --reload --port 8000
```

Frontend di terminal lain:

```powershell
Set-Location frontend
npm install
npm run dev
```

Frontend meneruskan `/api/*` ke `http://127.0.0.1:8000`. Build produksi frontend:

```powershell
npm run build
```

## Deploy Vercel

Import root repository ke project Vercel. `vercel.json` mengarahkan frontend Vite dan backend FastAPI serta meneruskan `/api/*`. Gunakan preview deployment untuk mencoba health check dan upload sebelum mengalihkan domain. Periksa batas ukuran function Vercel karena TensorFlow dan model cukup besar; batas upload aplikasi adalah 4 MB.

## Catatan Evaluasi dan Batasan

Pada evaluasi test notebook, 31 dari 1.548 gambar busuk terprediksi segar oleh `argmax` mentah. UI hanya menampilkan label dan tidak menampilkan persentase. Hasil model tidak menjamin 100% dan kasus buah campuran/bercak lokal bisa terlewat oleh klasifikasi satu foto. Periksa buah secara langsung.
