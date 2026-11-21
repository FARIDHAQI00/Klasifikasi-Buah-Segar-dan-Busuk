# Rencana Website Klasifikasi Buah Segar dan Busuk

**Status:** Demo aktif di Vercel; COCO-SSD Lite menyaring foto, ResNet50 memeriksa crop, dan satu contoh pisang campuran sudah teruji menghasilkan Busuk
**Model website yang ditetapkan:** ResNet50 dari `backend/model/ResNet50_terbaik.keras`
**Repo tujuan:** [FARIDHAQI00/Klasifikasi-Buah-Segar-dan-Busuk](https://github.com/FARIDHAQI00/Klasifikasi-Buah-Segar-dan-Busuk)  
**Notebook acuan:** [UAS_Buah_Cepat_Resume.ipynb di Google Colab](https://colab.research.google.com/drive/16t9E0vxdy2ZF-86ZbjetxU_yVwtDOmON?usp=sharing)

## 1. Tujuan

Membuat website sederhana untuk mengunggah foto apel, pisang, atau jeruk dan mendapat label **Segar** atau **Busuk** langsung dari model ResNet50 hasil notebook.

Prioritas evaluasi adalah mengurangi kasus buah busuk yang diberi hasil segar. Akurasi umum tetap dilaporkan, tetapi tidak cukup sebagai kriteria rilis.

## 2. Temuan dan keputusan dasar

### Dataset dan model

- Notebook memuat enam kelas: freshapples, freshbanana, freshoranges, rottenapples, rottenbanana, dan rottenoranges.
- Pipeline notebook memakai gambar RGB 160 × 160. ResNet50 memakai bobot pretrained ImageNet dengan backbone dibekukan; classifier enam kelas berada pada bagian akhir.
- ResNet50 dipilih notebook berdasarkan akurasi validasi tertinggi, yaitu 98,26%. Akurasi test yang tercatat 97,69%.
- Confusion matrix test mencakup 2.727 gambar. Dengan keputusan argmax enam kelas, 31 dari 1.548 gambar busuk diberi kelas segar: 10 apel busuk diprediksi sebagai apel segar dan 21 jeruk busuk diprediksi sebagai jeruk segar.
- Website memakai COCO-SSD Lite di browser untuk menemukan objek apel, pisang, dan jeruk. ResNet50 tetap menjadi model freshness utama; tiap objek terdeteksi diklasifikasikan terpisah, lalu Busuk menang jika satu objek diprediksi busuk.
- Tidak tersedia dataset lokal non-buah atau buah campuran tambahan. COCO-SSD menjadi gerbang pralatih dan dapat melewatkan target pada foto buram/tertutup; validasi terpisah tetap dibutuhkan sebelum klaim penolakan non-buah yang menyeluruh.
- Bunch pisang yang dideteksi sebagai satu objek dibagi menjadi tiga slice tumpang-tindih sepanjang dimensi terpanjang. Cara ini membantu memeriksa kondisi lokal, tetapi masih dapat melewatkan bercak yang tidak tertangkap di crop; foto satu buah dekat tetap paling sesuai dengan cakupan dataset training.
- Notebook menyimpan model dan hasil run ke Google Drive pada folder UAS_AI/buah_cepat_resume_daf3a93e2d. Artefak yang ditetapkan untuk website sudah disalin ke `backend/model/ResNet50_terbaik.keras`; SHA-256-nya cocok dengan manifest. Jangan mengganti artefak ini dengan model uji lain.

### Split data yang perlu diselaraskan

Konfigurasi preprocessing lokal mencatat jumlah gambar yang berbeda dari output notebook. Website memakai artefak model dan preprocessing yang ditetapkan dari run notebook; pengukuran ulang untuk training berikutnya perlu memakai split yang cocok.

### Keputusan produk

1. Website selalu memuat ResNet50_terbaik.keras. Tidak ada pemilihan atau pergantian arsitektur model saat runtime; model_terpilih.json hanya metadata eksperimen dan bukan ketergantungan aplikasi.
2. Gerbang browser mengembalikan **Foto tidak dikenali** saat tidak ada objek buah target yang terdeteksi.
3. ResNet50 memprediksi setiap crop objek; hasil akhir **Busuk** jika satu crop diprediksi busuk, dan **Segar** jika semua crop diprediksi segar.
4. Website hanya membuat perkiraan visual dari foto. Hasilnya bukan jaminan keamanan atau kelayakan konsumsi.

## 3. Stack dan arsitektur

### Stack

- **Frontend:** React + Vite + TypeScript.
- **Fruit gate:** TensorFlow.js COCO-SSD Lite in the browser; target classes are apple, banana, and orange.
- **Styling:** Tailwind CSS melalui integrasi Vite.
- **Backend:** Python + FastAPI.
- **Inference:** TensorFlow/Keras memuat ResNet50 dalam format .keras.
- **Deployment target:** Vercel Services (Beta). Frontend Vite dan backend FastAPI berada sebagai dua service dalam satu repo dan satu deployment, dengan routing same-origin.
- **Artefak model:** `ResNet50_terbaik.keras` disimpan langsung di `backend/model/` dan dicatat dengan SHA-256 di `backend/model/model_manifest.json`. Dataset, checkpoint training, dan foto pengguna tidak dimasukkan ke repo.

Dokumentasi stack dan deploy: [React](https://react.dev/learn), [Vite](https://vite.dev/guide/), [Tailwind CSS untuk Vite](https://tailwindcss.com/docs/installation/using-vite), [Vite di Vercel](https://vercel.com/docs/frameworks/frontend/vite), [FastAPI di Vercel](https://vercel.com/kb/guide/ship-a-fastapi-app-on-vercel), [Vercel Services](https://vercel.com/docs/services), dan [batas Vercel Functions](https://vercel.com/docs/functions/limitations).

### Target deploy Vercel

- Gunakan satu Vercel Project yang terhubung ke root repo GitHub ini. `vercel.json` memakai format `services` saat ini; frontend Vite dan backend FastAPI dibangun terpisah lalu dirutekan melalui satu domain. Vercel Services tersedia dalam Beta; ikuti pilihan framework/preset yang ditawarkan dashboard saat impor.
- Service frontend memakai root frontend/ dan membangun React/Vite menjadi asset statis. Service backend memakai root backend/ dan mengekspos instance FastAPI bernama app melalui entrypoint main:app.
- COCO-SSD Lite berjalan di browser dan mengunduh bobot detektor saat pertama dipakai. Foto pengguna diperiksa lokal; hanya crop objek buah terdeteksi yang dikirim ke backend. Dependensi detector berada di frontend statis, tidak menambah ukuran Python Function Vercel.
- File `vercel.json` di root mendefinisikan service dan rewrite: `/api/*` menuju backend, sedangkan path lain menuju frontend. Service backend menerima path `/api/...` asli. Karena satu deployment memiliki satu origin, frontend memanggil `/api/v1/predict` tanpa konfigurasi CORS lintas domain.
- Hubungkan GitHub ke Vercel agar branch main menjadi deployment produksi dan pull request mendapat preview deployment. Gunakan vercel dev untuk memeriksa routing lokal bila konfigurasi Services sudah dipasang.
- FastAPI dijalankan oleh Python Runtime sebagai Vercel Function. Model dimuat sekali per instance Function yang masih hidup; cold start berikutnya mungkin memuat ulang model. Jangan mengandalkan memori proses untuk menyimpan state permanen.
- Sebelum fitur lengkap, buat spike kelayakan deploy yang membangun backend beserta TensorFlow dan ResNet50, lalu ukur ukuran bundle, cold start, RAM, dan latency inference pada plan Vercel yang akan dipakai.
- Batas request body Vercel Function adalah 4,5 MB. MVP membatasi file gambar hingga 4 MB dan juga memeriksa total Content-Length; upload di atas batas dikembalikan sebagai error yang jelas, tidak diteruskan ke prediksi.
- Bundle Python standar dibatasi hingga 500 MB tanpa kompresi. Large Functions hingga 5 GB tersedia sebagai Beta pada Fluid Compute; project yang belum terdaftar mungkin perlu mengaktifkan `VERCEL_SUPPORT_LARGE_FUNCTIONS=1` di environment Vercel. Pilih paket standar bila cukup; bila melampaui batas, ukur Large Functions di preview terlebih dahulu. Memori Function Hobby adalah 2 GB/1 vCPU; ukur apakah TensorFlow dan inference cocok pada resource tersebut.
- Bobot ResNet50 ikut berada di repo dan dibundel bersama backend. Verifikasi SHA-256 sebelum pemuatan. Ukur bundle backend pada build preview; bila melewati batas standar 500 MB, aktifkan Large Functions/Fluid Compute sebelum deployment atau pindahkan API inference ke runtime Python container yang sesuai. Jangan mengunduh model dari Google Drive pada setiap prediksi.
- Pin Python 3.12 dan versi TensorFlow/Keras yang kompatibel dengan model Colab. Verifikasi impor dan pemuatan model pada runtime Vercel sebelum mengerjakan seluruh UI.
- Jika bundle, cold start, atau pemakaian RAM tidak layak pada akun Vercel, frontend tetap dideploy di Vercel dan API inference dipindahkan ke layanan Python yang mendukung container/model menetap. Frontend memakai URL backend melalui environment variable dan API hanya mengizinkan origin website tersebut.

Contoh bentuk routing di vercel.json:

    {
      "services": {
        "frontend": { "root": "frontend/" },
        "backend": { "root": "backend/", "entrypoint": "main:app" }
      },
      "rewrites": [
        { "source": "/api/(.*)", "destination": { "service": "backend" } },
        { "source": "/(.*)", "destination": { "service": "frontend" } }
      ]
    }

### Alur request

1. Pengguna memilih foto dan melihat pratinjau.
2. COCO-SSD Lite mencari apel, pisang, atau jeruk di browser. Jika tidak ditemukan, UI menampilkan **Foto tidak dikenali** dan berhenti.
3. Browser memotong tiap objek terdeteksi dan mengirimkan daftar sebagai multipart `files` ke POST /api/v1/predict/stream.
4. FastAPI memeriksa format, ukuran, dimensi, dan integritas setiap potongan.
5. Backend menjalankan preprocessing yang sama dengan notebook untuk tiap potongan.
6. ResNet50 menghasilkan skor enam kelas sesuai urutan label untuk tiap potongan.
7. Backend mengirim event SSE saat tiap langkah dimulai dan selesai. Hasil gabungan menjadi Busuk jika satu potongan busuk; jika semua segar, hasilnya Segar.
8. Frontend menampilkan hasil, jenis buah bila cukup jelas, serta keterangan singkat.

### Kontrak API awal

- GET /api/health — memeriksa aplikasi dan status model siap.
- GET /api/v1/model-info — mengembalikan versi model, ukuran input, kelas, dan versi kebijakan.
- POST /api/v1/predict/stream — menerima satu `file` atau beberapa `files` dan mengirim event riwayat proses serta hasil melalui SSE.
- POST /api/v1/predict — endpoint JSON langsung untuk klien non-streaming.

Contoh respons berhasil:

    {
      "status": "fresh",
      "fruit": "Apel",
      "reason": "Perkiraan visual dari model ResNet50.",
      "model_version": "resnet50-terbaik-v1",
      "policy_version": "fruit-regions-any-rotten-v1"
    }

Website menampilkan nama kelas, tanpa mengubah skor menjadi persentase keyakinan.

### Preprocessing dan pemetaan label

Urutan kelas harus sama persis dengan model:

| Indeks | Kelas model | Jenis | Kondisi |
|---:|---|---|---|
| 0 | freshapples | Apel | Segar |
| 1 | freshbanana | Pisang | Segar |
| 2 | freshoranges | Jeruk | Segar |
| 3 | rottenapples | Apel | Busuk |
| 4 | rottenbanana | Pisang | Busuk |
| 5 | rottenoranges | Jeruk | Busuk |

Model mengeluarkan enam skor sesuai urutan tabel untuk setiap crop. API tidak mengirim skor tersebut ke pengguna. Decision policy memilih argmax tiap crop, lalu menggabungkan keputusan secara konservatif.

- Indeks 0–2 (kelas segar) menghasilkan **Segar**.
- Indeks 3–5 (kelas busuk) menghasilkan **Busuk**.
- Output model invalid menghasilkan error API.

Fungsi preprocessing harus mengikuti implementasi notebook: decoding RGB, resize TensorFlow ke 160 × 160, lalu tf.keras.applications.resnet50.preprocess_input pada nilai gambar 0–255. Karena preprocessing berada di luar model .keras pada notebook, perubahan library atau urutan operasi harus diverifikasi sebelum deploy.

## 4. Kebijakan hasil demo

- Setiap crop dipetakan dengan argmax: kelas 0–2 **Segar**, kelas 3–5 **Busuk**.
- Hasil foto menjadi **Busuk** bila sedikitnya satu crop terdeteksi busuk.
- Jika output model tidak terbaca, API mengembalikan error.
- Notebook mencatat 31 foto busuk terprediksi segar. Hasil website adalah perkiraan visual, bukan kepastian untuk semua foto baru.
- Model dilatih untuk apel, pisang, dan jeruk; antarmuka tidak menjanjikan hasil tepat untuk objek atau buah di luar kelas tersebut.

## 5. Catatan evaluasi model

- Notebook mencatat akurasi 97,69% serta 31 foto busuk yang salah diberi kelas Segar.
- Periksa contoh foto nyata dan hasil per kelas untuk menentukan kebutuhan training ulang.
- Hasil website adalah perkiraan visual model, bukan jaminan untuk semua foto.

## 6. Ruang lingkup MVP

### Termasuk

- Satu halaman responsif untuk mengunggah satu foto.
- Pratinjau, hapus/ganti foto, indikator proses, hasil, dan pesan error.
- Dukungan awal JPEG, PNG, dan WebP dengan ukuran file maksimal 4 MB agar total request tetap di bawah batas payload Vercel Function 4,5 MB.
- Deteksi browser untuk menolak foto yang tidak memiliki objek target terdeteksi, dengan hasil **Foto tidak dikenali**.
- Crop per objek buah dan agregasi **Busuk** jika salah satu region diprediksi busuk.
- Prediksi jenis buah dan kondisi Segar/Busuk melalui API.
- Status runtime **Segar**, **Busuk**, dan **Foto tidak dikenali**.
- Tidak menyimpan gambar pengguna atau membuat riwayat akun.
- README berisi cara menjalankan lokal, menyiapkan artefak model, dan deploy.

### Tidak termasuk MVP

- Registrasi pengguna, database, riwayat prediksi, dashboard admin, batch upload, dan API publik berbayar.
- Training model dari website.
- Klaim bahwa foto dapat memastikan kondisi bagian dalam atau keamanan pangan.

## 7. Struktur repo yang dituju

    website-klasifikasi-buah/
      PLAN.md
      README.md
      vercel.json
      frontend/
        src/
          fruitDetector.ts
        public/
        vite.config.ts
        package.json
      backend/
        main.py
        app/
          api.py
          model_loader.py
          preprocessing.py
          decision_policy.py
        requirements.txt
        .python-version
        model/
          ResNet50_terbaik.keras
          model_manifest.json
      .gitignore

File `.keras` terpilih dicommit di `backend/model/` karena diminta sebagai artefak aplikasi. Model lain, dataset, hasil checkpoint, hasil ekstraksi, dan foto pengguna tidak dicommit. Hash SHA-256 dan versi artefak dicatat di `backend/model/model_manifest.json`.

## 8. Roadmap build

| Tahap | Pekerjaan | Hasil dan kriteria selesai |
|---|---|---|
| 0. Bekukan sumber dan artefak | Tetapkan `backend/model/ResNet50_terbaik.keras` sebagai satu-satunya model aplikasi; simpan SHA-256, kelas, preprocessing, versi TensorFlow, serta metrik run yang sama di manifest. | Selesai; backend hanya membaca artefak ini dan hash-nya cocok. Tidak ada model selector atau fallback arsitektur. |
| 1. Pemetaan label | Jalankan argmax enam kelas untuk tiap region dan agregasi any-rotten-wins. | Selesai; tes unit memastikan satu region Busuk membuat hasil keseluruhan Busuk. |
| 2. Modul inference | Pindahkan preprocessing dan pemanggilan model ke modul Python yang dapat menerima gambar dan mengeluarkan skor serta status. Muat model sekali per proses. | Selesai; hash diverifikasi sebelum model dimuat dan preprocessing dicocokkan dengan notebook. |
| 3. API | Implementasikan health, model-info, single image, region batch; validasi upload dan error; batasi ukuran/jumlah pixel; jangan simpan gambar. | Kode menerima `file` atau `files`; batch inference memakai model yang sama. Perlu smoke test API batch pada runtime TensorFlow. |
| 4. Frontend | Buat React SPA dengan COCO-SSD Lite gate, crop buah, upload batch, riwayat langkah aktual, hasil, dan error. | Production build lulus. Browser gate dicoba pada foto pisang dan non-buah yang diberikan; sampel ini belum cukup untuk mengukur cakupan deteksi umum. |
| 5. Integrasi lokal/produksi | Periksa frontend, routing /api, preprocessing, label, batch response, dan alur error. | Tujuh tes kebijakan lulus. Runtime TensorFlow/FastAPI tidak tersedia di mesin lokal, tetapi endpoint produksi health/model-info siap; UI produksi menolak sampel non-buah dan mengirim tiga crop foto pisang campuran hingga hasil Busuk/Pisang. |
| 6. Deploy Vercel | Hubungkan repo, atur frontend/backend Services, routing, artefak model, dan periksa hasil deployment. | Selesai untuk commit `7fed7e7`; status deployment Vercel sukses dan root serta API produksi merespons. |
| 7. Verifikasi demo dan dokumentasi | Cek health, deteksi buah/non-buah, batch crop, label, dan versi model pada deployment aktif. | Selesai pada `https://klasifikasibuah.vercel.app`: sampel non-buah berhenti di browser; foto pisang campuran menghasilkan **Busuk/Pisang**; riwayat keenam tahap tampil tanpa error konsol. Ini uji contoh, bukan jaminan 100% pada semua foto. |

Demo sudah bisa dipakai untuk presentasi pada sampel yang tersedia. Pengujian foto tambahan akan membantu menemukan batas detektor dan model, tetapi tidak mengubah hasil contoh produksi yang sudah terverifikasi.

## 9. Risiko dan mitigasi

| Risiko | Mitigasi |
|---|---|
| Busuk diberi label Segar | Risiko ini tercatat di evaluasi notebook (31 kasus); tampilkan hasil sebagai perkiraan visual dan kumpulkan contoh foto untuk peningkatan model. |
| Split lokal dan Colab berbeda | Pilih satu manifest final dan simpan hash; hitung ulang evaluasi untuk model yang sama dengan split tersebut. |
| Preprocessing berubah | Gunakan fungsi preprocessing yang identik dengan notebook dan verifikasi pada kumpulan gambar acuan. |
| Foto di luar dataset | COCO-SSD Lite menolak foto bila tidak menemukan apel/pisang/jeruk. Model umum ini dapat salah deteksi atau luput; uji dengan contoh nyata sebelum klaim cakupan penuh. |
| Campuran segar dan busuk | Kotak pisang dibagi tiga dan hasil Busuk menang bila satu slice diprediksi busuk. COCO dapat meleset dari bercak atau crop tidak cukup menampilkannya; kasus lokal tetap bisa terlewat. |
| Artefak model besar atau hilang | Simpan hanya model ResNet50 terpilih (95,157,337 bytes) di `backend/model/`, pin hash SHA-256, dan verifikasi saat backend start. Jangan commit dataset/checkpoint. |
| Kebocoran foto pengguna | Jangan simpan upload; hapus data gambar dari memori setelah request selesai; jangan mencatat file ke log. |
| Batas Vercel Function | Ukur bundle, payload, RAM, cold start, dan latency pada preview; gunakan Large Functions bila sesuai atau pindahkan hanya API inference ke layanan Python container jika tetap tidak layak. |
| Perubahan/ketidaktersediaan fitur Beta Vercel Services | Verifikasi opsi Services di dashboard saat impor; jika tidak tersedia, siapkan dua project Vercel atau backend Python terpisah tanpa mengubah frontend. |
| Ketidakcocokan TensorFlow dengan runtime Python | Pin Python 3.12 dan dependency; buat uji pemuatan model sebagai bagian spike sebelum membangun seluruh aplikasi. |

## 10. Kriteria selesai

Demo aktif di `https://klasifikasibuah.vercel.app`. Pada foto yang diuji, gate browser menolak non-buah dan ResNet50 mengembalikan **Busuk/Pisang** untuk foto pisang setengah busuk. Model tetap perkiraan visual; deteksi atau bercak busuk pada foto lain dapat terlewat.

