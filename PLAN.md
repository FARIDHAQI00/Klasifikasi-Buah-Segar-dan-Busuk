# Rencana Website Klasifikasi Buah Segar dan Busuk

**Status:** dokumen perencanaan; implementasi aplikasi belum dimulai  
**Model kandidat yang dipilih:** ResNet50  
**Repo tujuan:** [FARIDHAQI00/Klasifikasi-Buah-Segar-dan-Busuk](https://github.com/FARIDHAQI00/Klasifikasi-Buah-Segar-dan-Busuk)  
**Notebook acuan:** [UAS_Buah_Cepat_Resume.ipynb di Google Colab](https://colab.research.google.com/drive/16t9E0vxdy2ZF-86ZbjetxU_yVwtDOmON?usp=sharing)

## 1. Tujuan

Membuat website sederhana untuk mengunggah foto apel, pisang, atau jeruk dan mendapat perkiraan kondisi segar atau busuk dari model ResNet50 hasil notebook. Sistem harus memiliki hasil ketiga, **Perlu diperiksa**, agar gambar yang tidak meyakinkan tidak dipaksa menjadi segar atau busuk.

Prioritas evaluasi adalah mengurangi kasus buah busuk yang diberi hasil segar. Akurasi umum tetap dilaporkan, tetapi tidak cukup sebagai kriteria rilis.

## 2. Temuan dan keputusan dasar

### Dataset dan model

- Notebook memuat enam kelas: freshapples, freshbanana, freshoranges, rottenapples, rottenbanana, dan rottenoranges.
- Pipeline notebook memakai gambar RGB 160 × 160. ResNet50 memakai bobot pretrained ImageNet dengan backbone dibekukan; classifier enam kelas berada pada bagian akhir.
- ResNet50 dipilih notebook berdasarkan akurasi validasi tertinggi, yaitu 98,26%. Akurasi test yang tercatat 97,69%.
- Confusion matrix test mencakup 2.727 gambar. Dengan keputusan argmax enam kelas, 31 dari 1.548 gambar busuk diberi kelas segar: 10 apel busuk diprediksi sebagai apel segar dan 21 jeruk busuk diprediksi sebagai jeruk segar.
- Jadi model mentah dari notebook **belum lulus** kriteria rilis aman untuk label Segar. Ambang keputusan yang dikalibrasi mungkin memperbaiki perilaku ini, tetapi hasilnya harus dibuktikan pada test terkunci dan foto baru.
- Notebook menyimpan model dan hasil run ke Google Drive pada folder UAS_AI/buah_cepat_resume_daf3a93e2d. File model produksi perlu diambil dan diverifikasi sebelum integrasi; file model uji di folder lokal tidak boleh dianggap sebagai artefak final.

### Split data yang perlu diselaraskan

Konfigurasi preprocessing lokal mencatat 8.720 gambar train, 2.181 validation, dan 2.698 test. Output notebook Colab menunjukkan 2.727 gambar pada test. Ini menandakan pembagian yang tercatat lokal dan run notebook tidak identik. Sebelum build inference, tetapkan manifest dan model yang menjadi acuan, lalu simpan hash serta versinya. Jangan menggabungkan metrik dari split yang berbeda.

### Keputusan produk

1. ResNet50 menjadi satu-satunya model kandidat untuk MVP.
2. Hasil website memiliki tiga status: **Segar**, **Busuk**, dan **Perlu diperiksa**.
3. Tidak mengaktifkan status otomatis Segar sampai ambang dan evaluasi risiko melewati gerbang rilis.
4. Website hanya membuat perkiraan visual dari foto. Hasilnya bukan jaminan keamanan atau kelayakan konsumsi.

## 3. Stack dan arsitektur

### Stack

- **Frontend:** React + Vite + TypeScript.
- **Styling:** Tailwind CSS melalui integrasi Vite.
- **Backend:** Python + FastAPI.
- **Inference:** TensorFlow/Keras memuat ResNet50 dalam format .keras.
- **Deployment target:** Vercel. Frontend Vite dan backend FastAPI ditempatkan sebagai dua service dalam satu repo dan satu deployment Vercel, dengan routing same-origin.
- **Artefak model:** berkas model disimpan terpisah dari source code, misalnya pada release atau penyimpanan artefak yang dikonfigurasi saat deploy. Dataset, checkpoint training, dan foto pengguna tidak dimasukkan ke repo.

Dokumentasi stack dan deploy: [React](https://react.dev/learn), [Vite](https://vite.dev/guide/), [Tailwind CSS untuk Vite](https://tailwindcss.com/docs/installation/using-vite), [Vite di Vercel](https://vercel.com/docs/frameworks/frontend/vite), [FastAPI di Vercel](https://vercel.com/kb/guide/ship-a-fastapi-app-on-vercel), [Vercel Services](https://vercel.com/docs/services), dan [batas Vercel Functions](https://vercel.com/docs/functions/limitations).

### Target deploy Vercel

- Gunakan satu Vercel Project yang terhubung ke repo GitHub ini. Vercel Services membangun frontend dan backend secara terpisah dalam satu project, lalu merutekan keduanya melalui satu domain. Fitur Services saat ini berstatus beta; konfirmasi ketersediaan dan pengaturannya pada akun sebelum deploy.
- Service frontend memakai root frontend/ dan membangun React/Vite menjadi asset statis. Service backend memakai root backend/ dan mengekspos instance FastAPI bernama app melalui entrypoint main:app.
- File vercel.json di root mendefinisikan service dan rewrite: /api/* menuju backend, sedangkan path lain menuju frontend. Karena satu deployment memiliki satu origin, frontend memanggil /api/v1/predict tanpa konfigurasi CORS lintas domain.
- Hubungkan GitHub ke Vercel agar branch main menjadi deployment produksi dan pull request mendapat preview deployment. Gunakan vercel dev untuk memeriksa routing lokal bila konfigurasi Services sudah dipasang.
- FastAPI dijalankan oleh Python Runtime sebagai Vercel Function. Model dimuat sekali per instance Function yang masih hidup; cold start berikutnya mungkin memuat ulang model. Jangan mengandalkan memori proses untuk menyimpan state permanen.
- Sebelum fitur lengkap, buat spike kelayakan deploy yang membangun backend beserta TensorFlow dan ResNet50, lalu ukur ukuran bundle, cold start, RAM, dan latency inference pada plan Vercel yang akan dipakai.
- Batas request body Vercel Function adalah 4,5 MB. MVP membatasi file gambar hingga 4 MB dan juga memeriksa total Content-Length; upload di atas batas dikembalikan sebagai error yang jelas, tidak diteruskan ke prediksi.
- Bundle Python standar dibatasi hingga 500 MB tanpa kompresi. Large Functions hingga 5 GB tersedia sebagai beta pada Fluid Compute. Pilih paket standar bila cukup; bila melampaui batas, evaluasi Large Functions di preview terlebih dahulu. Catat bahwa memori Function pada Hobby adalah 2 GB/1 vCPU; ukur apakah TensorFlow dan inference cocok pada resource tersebut.
- Pilih strategi artefak ResNet50 setelah spike: sertakan bobot pada artefak deployment jika ukuran bundle masih memenuhi batas, atau ambil dari private model storage satu kali per cold start dan verifikasi SHA-256. Jangan mengunduh model dari Google Drive pada setiap prediksi.
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
2. Browser mengirim file sebagai multipart request ke POST /api/v1/predict.
3. FastAPI memeriksa format file, ukuran unggahan, dimensi, dan apakah gambar dapat dibaca.
4. Backend mengubah gambar ke RGB, resize ke 160 × 160, lalu menerapkan preprocessing ResNet50 yang sama dengan notebook.
5. Model menghasilkan skor enam kelas. Backend menggabungkan skor tiga kelas segar dan tiga kelas busuk.
6. Decision policy memakai ambang yang sudah ditetapkan dari validation. Jika foto tidak jelas, skor tidak cukup, atau input di luar cakupan, API mengembalikan Perlu diperiksa.
7. Frontend menampilkan hasil, jenis buah bila cukup jelas, serta keterangan singkat.

### Kontrak API awal

- GET /health — memeriksa aplikasi dan status model siap.
- GET /api/v1/model-info — mengembalikan versi model, ukuran input, kelas, dan versi ambang.
- POST /api/v1/predict — menerima satu gambar dan mengembalikan status.

Contoh respons berhasil:

    {
      "status": "review",
      "fruit": "jeruk",
      "scores": {
        "fresh": 0.42,
        "rotten": 0.58
      },
      "reason": "skor belum melewati ambang keputusan",
      "model_version": "resnet50-v1",
      "policy_version": "safety-v1"
    }

Nilai skor softmax tidak otomatis dianggap probabilitas yang terkalibrasi. Persentase tidak ditampilkan sebagai kepastian sebelum kalibrasi diperiksa.

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

Backend menghitung:

- P_segar = skor indeks 0 + 1 + 2.
- P_busuk = skor indeks 3 + 4 + 5.

Fungsi preprocessing harus mengikuti implementasi notebook: decoding RGB, resize TensorFlow ke 160 × 160, lalu tf.keras.applications.resnet50.preprocess_input pada nilai gambar 0–255. Karena preprocessing berada di luar model .keras pada notebook, perubahan library atau urutan operasi harus diverifikasi sebelum deploy.

## 4. Kebijakan keputusan yang mengutamakan risiko

Softmax argmax akan menjadi baseline pembanding, bukan keputusan final. Ambang untuk status Busuk dan Segar dikalibrasi memakai data validation saja. Test tidak dipakai berulang kali untuk memilih ambang.

- **Busuk:** dipilih saat skor agregat busuk melewati ambang yang sudah dikalibrasi.
- **Segar:** hanya boleh dipilih saat skor dan pemeriksaan input melewati aturan yang telah disetujui.
- **Perlu diperiksa:** dipilih untuk hasil yang ambigu, input rusak, kualitas gambar rendah, jenis buah yang tidak didukung, atau kondisi yang tidak dikenal model.

Ambang tinggi dapat membuat lebih banyak foto masuk ke Perlu diperiksa. Karena itu, laporan selalu menyertakan jumlah dan persentase foto yang otomatis diputuskan (coverage), serta jumlah salah busuk-ke-segar. Ambang tidak boleh dilonggarkan hanya untuk menaikkan coverage tanpa mengukur kembali risiko.

Model machine learning tidak dapat menjamin nol kesalahan pada semua foto baru. Jika syaratnya adalah tidak boleh salah menyebut busuk sebagai segar pada pengujian, kegagalan gerbang tersebut berarti status Segar otomatis tidak dirilis. Foto ambigu diarahkan ke pemeriksaan manusia.

## 5. Rencana evaluasi dan gerbang rilis

### Metrik utama

1. Jumlah dan rasio buah busuk yang diprediksi segar (false-fresh rate).
2. Recall busuk gabungan dan recall untuk apel, pisang, serta jeruk busuk.
3. Precision status Segar.
4. Coverage: proporsi foto yang mendapat status otomatis dibandingkan Perlu diperiksa.
5. Akurasi enam kelas, macro-F1, confusion matrix, dan waktu inferensi sebagai metrik pendukung.

### Urutan evaluasi

1. Bekukan manifest train, validation, dan test serta versi model.
2. Kalibrasi ambang dan periksa metrik keselamatan hanya dengan validation.
3. Simpan ambang dan versi kebijakan sebelum menjalankan evaluasi final.
4. Evaluasi sekali pada test terkunci; laporkan seluruh metrik, termasuk false-fresh per jenis buah.
5. Uji tambahan pada foto kamera nyata: variasi cahaya, jarak, latar, sudut, satu/beberapa buah, buah rusak sebagian, dan gambar non-buah.
6. Jika test masih menghasilkan busuk-ke-segar, rilis diblokir untuk status Segar otomatis. Tinjau kesalahan dan siapkan data tambahan atau training ulang. Jangan mengubah ambang berdasarkan hasil test lalu mengklaim test yang sama sebagai evaluasi independen.

### Syarat kandidat untuk rilis

- Model, pemetaan label, dan preprocessing cocok dengan artefak notebook.
- Tidak ada error file atau kegagalan backend yang berubah menjadi status Segar.
- Ambang dibekukan dari validation.
- Gerbang false-fresh pada test terkunci terpenuhi; target usulan adalah nol kasus busuk-ke-segar pada test tersebut.
- Coverage dan jumlah Perlu diperiksa dilaporkan agar kebijakan tidak terlihat aman hanya karena hampir semua gambar ditolak.
- Pengujian foto nyata selesai dan hasilnya dicatat.
- Jika gerbang gagal, aplikasi tetap boleh berjalan sebagai demo dengan status Segar otomatis dimatikan dan setiap kasus yang tidak pasti diarahkan ke pemeriksaan manual.

## 6. Ruang lingkup MVP

### Termasuk

- Satu halaman responsif untuk mengunggah satu foto.
- Pratinjau, hapus/ganti foto, indikator proses, hasil, dan pesan error.
- Dukungan awal JPEG, PNG, dan WebP dengan ukuran file maksimal 4 MB agar total request tetap di bawah batas payload Vercel Function 4,5 MB.
- Prediksi jenis buah dan kondisi melalui API.
- Tiga status hasil dan kebijakan keselamatan.
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
        public/
        vite.config.ts
        package.json
      backend/
        main.py
        app/
          inference.py
          preprocessing.py
          decision_policy.py
          schemas.py
        requirements.txt
        .python-version
      ml/
        labels.json
        preprocessing.json
        model_manifest.json
      artifacts/
        README.md
      .gitignore

Folder artifacts hanya menyimpan petunjuk cara memperoleh model atau konfigurasi lokal; file .keras, dataset, hasil checkpoint, dan foto pengguna tidak dicommit. Hash SHA-256 dan versi artefak dicatat di model_manifest.json.

## 8. Roadmap build

| Tahap | Pekerjaan | Hasil dan kriteria selesai |
|---|---|---|
| 0. Bekukan sumber dan uji kelayakan Vercel | Pastikan split Colab atau split lokal yang akan menjadi acuan; ambil model ResNet50 final; verifikasi kelas, preprocessing, versi TensorFlow, hash artefak, ukuran bundle, cold start, RAM, serta status dukungan Services pada akun. | Satu manifest, satu model, satu konfigurasi inference, dan bukti backend bisa dibangun di Vercel. |
| 1. Gerbang keselamatan | Kalibrasi ambang dari validation, hitung false-fresh, recall busuk per buah, coverage; jalankan evaluasi final pada test terkunci. | Keputusan rilis tercatat. Jika ada false-fresh pada target test, Segar otomatis tetap mati. |
| 2. Modul inference | Pindahkan preprocessing dan pemanggilan model ke modul Python yang dapat menerima gambar dan mengeluarkan skor serta status. Muat model sekali saat startup. | Backend inference dapat direproduksi dan memakai versi label/ambang yang tercatat. |
| 3. API | Implementasikan health, model-info, dan predict; validasi upload dan error; batasi ukuran dan jumlah piksel; jangan simpan gambar. | Respons API konsisten untuk foto valid, rusak, terlalu besar, dan ambigu. |
| 4. Frontend | Buat React SPA: upload/drag-drop, pratinjau, progress, hasil tiga status, error, dan tampilan ponsel. | Alur upload sampai hasil dapat dipakai tanpa mengirim ulang foto secara tidak sengaja. |
| 5. Integrasi lokal | Jalankan frontend dan API bersama; periksa routing /api, preprocessing, label, respons, serta kebijakan status pada skenario normal dan gagal. | Demo end-to-end sesuai kontrak API dan tidak pernah mengubah kegagalan menjadi Segar. |
| 6. Deploy preview Vercel | Konfigurasikan Vercel Services, root frontend/backend, entrypoint FastAPI, routing, ukuran upload, dan artefak model. Deploy preview dari branch kerja sebelum main. | URL preview dapat memuat model dan menerima gambar dalam batas payload; ukuran bundle, cold/warm start, RAM, latency, dan error dicatat. |
| 7. Deploy produksi dan dokumentasi | Setelah preview serta gerbang keselamatan lolos, promosikan branch main ke produksi. Pastikan health check, model version, threshold version, dan langkah rollback tercatat. | Website live di Vercel; versi model/ambang dapat diperiksa dan deployment dapat dipulihkan bila perlu. |

Estimasi awal: sekitar 5–7 hari kerja untuk MVP bila artefak siap, spike Vercel lulus, dan threshold lulus. Pengumpulan label/foto tambahan atau training ulang memperpanjang estimasi; hasil baseline saat ini menunjukkan pekerjaan gerbang keselamatan kemungkinan perlu perhatian sebelum rilis.

## 9. Risiko dan mitigasi

| Risiko | Mitigasi |
|---|---|
| Busuk diberi label segar | Ambang berbasis validation, status Perlu diperiksa, gerbang false-fresh pada test, dan larangan rilis Segar otomatis bila gagal. |
| Split lokal dan Colab berbeda | Pilih satu manifest final dan simpan hash; hitung ulang evaluasi untuk model yang sama dengan split tersebut. |
| Preprocessing berubah | Gunakan fungsi preprocessing yang identik dengan notebook dan verifikasi pada kumpulan gambar acuan. |
| Foto di luar dataset | Batasi dukungan ke apel, pisang, dan jeruk; arahkan foto tidak dikenal/ambigu ke Perlu diperiksa; lakukan uji foto kamera. |
| Artefak model besar atau hilang | Jangan simpan dataset/model/checkpoint besar dalam riwayat Git; simpan di storage artefak dan verifikasi SHA-256. |
| Kebocoran foto pengguna | Jangan simpan upload; hapus data gambar dari memori setelah request selesai; jangan mencatat file ke log. |
| Batas Vercel Function | Ukur bundle, payload, RAM, cold start, dan latency pada preview; gunakan Large Functions bila sesuai atau pindahkan hanya API inference ke layanan Python container jika tetap tidak layak. |
| Perubahan/ketidaktersediaan fitur beta Vercel Services | Verifikasi fitur di akun sebelum konfigurasi; siapkan opsi dua project Vercel atau backend Python terpisah tanpa mengubah frontend. |
| Ketidakcocokan TensorFlow dengan runtime Python | Pin Python 3.12 dan dependency; buat uji pemuatan model sebagai bagian spike sebelum membangun seluruh aplikasi. |

## 10. Kriteria selesai

MVP dinyatakan siap didemokan saat website dapat menerima foto, mengembalikan salah satu dari tiga status, menggunakan ResNet50 dan preprocessing yang benar, memvalidasi file, serta mencatat versi model dan ambang. Status Segar otomatis hanya aktif setelah gerbang keselamatan yang ditetapkan terpenuhi. Jika tidak, website harus menyatakan Perlu diperiksa untuk hasil yang tidak lolos dan tidak mengklaim jaminan nol kesalahan.

