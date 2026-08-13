# Medika Nusantara — Synthetic Workforce Dataset

Deliverable 3, case study Product Manager (AI-Native), Rakamin Workforce Intelligence Platform.

Semua data di sini sintetis. Tidak ada data karyawan nyata. Generator deterministik, seed `20260807`, jalankan ulang untuk hasil identik.

```bash
python generate_medika_data.py ./output
```

## Isi

| File | Isi |
|---|---|
| `generate_medika_data.py` | Generator, sekaligus dokumentasi eksekutabel dari seluruh logika |
| `dataset_a_messy.csv` / `.json` | Union naif 3 sistem, 820 baris untuk 200 manusia |
| `dataset_b_clean.csv` / `.json` | Hasil contextualization layer, 1 baris per orang |
| `ground_truth.csv` | Kebenaran yang ditanam generator. Tidak pernah dilihat pipeline |
| `resolution_audit.csv` | Jejak audit identity resolution per orang |
| `role_taxonomy.json` | 10 peran kanonik, 14 skill, kamus varian title |
| `comparison_metrics.json` | Seluruh angka pembanding A vs B |

`ground_truth.csv` ada supaya klaim pipeline bisa diukur, bukan diasumsikan. Ini juga yang memungkinkan over-split identity resolution dihitung, bukan ditebak.

## Angka utama

| Metrik | Nilai |
|---|---|
| Baris Dataset A | 820 |
| Manusia sebenarnya | 200 |
| Job title mentah berbeda | 70 |
| Fill rate skill HRIS | 44,5 persen (kosong 55,5 persen) |
| Grup terbentuk oleh analisis naif | 219 |
| Orang hasil resolusi | 232 (over-split 32, 16 persen) |
| Flag review Dataset B | 44,4 persen |
| Konflik tanggal masuk | 90 |
| Mutasi tercatat sebagai terminasi | 10 |
| Baris performa pra-2022 tidak valid | 132 |

## Messiness yang diinjeksi, dan alasannya

1. **Fragmentasi title.** 10 peran kanonik muncul sebagai 70 string berbeda. Analisis naif membentuk 219 grup dari 200 orang, artinya rata-rata grup kurang dari satu orang. Setiap agregasi per-peran yang perusahaan ini buat hari ini sudah salah sebelum AI menyentuhnya.
2. **Kekosongan skill 55,5 persen, dan tidak acak.** Fill rate ditentukan tier adopsi HRIS cabang: tinggi 0,85, menengah 0,55, rendah 0,15. Skill sebenarnya diambil dari distribusi identik untuk semua cabang. Ini mekanisme yang paling menentukan di seluruh dataset.
3. **ID tidak nyambung.** `EMP-xxxx`, `candidate_xxx`, `moodle_xxxxx`. Kolom `payroll_id` sengaja ada di skema dan dibiarkan kosong, supaya yang hilang terlihat eksplisit.
4. **Varian nama.** Muhammad/Muhamad/M., pembalikan urutan, inisial, kapital penuh, spasi ganda. String equality tidak cukup, probabilistic matching wajib.
5. **Konflik tanggal.** ATS mencatat tanggal offer, HRIS mencatat tanggal masuk, selisih 7 sampai 75 hari.
6. **Coverage ATS parsial.** Workable diasumsikan diadopsi 2023, jadi karyawan lama tidak punya record ATS sama sekali.
7. **Skala rating tidak seragam.** 1-5, 1-4, dan A-D antar cabang. Perbandingan performa lintas cabang tidak valid tanpa harmonisasi.
8. **Performa pra-2022 tidak reliable.** Digenerate di luar rentang skala yang berlaku, supaya alasan pembuangannya bisa dibuktikan.
9. **Mutasi tercatat sebagai terminasi lalu rehire.** 10 kasus, employee ID baru, cabang berbeda. Ini kontaminasi label attrition, dan alasan utama attrition prediction ditunda ke Fase 2.

## Logika inferensi skill

Empat status, dengan provenance melekat di setiap record. Tidak pernah ada nilai nol yang disamarkan sebagai fakta.

| Status | Confidence | Sumber |
|---|---|---|
| `declared` | 1,00 | Tertulis di field skill HRIS |
| `evidenced` | 0,90 | Ada completion kursus LMS yang memetakan ke skill tersebut |
| `inferred` | 0,55 | Skill wajib peran, hanya jika orang tersebut punya minimal satu sinyal lain |
| `unknown` | 0,00 | Tidak ada sinyal apa pun. Tidak diimputasi, tetap dibiarkan sebagai lubang |

Syarat "minimal satu sinyal lain" pada `inferred` adalah keputusan desain yang disengaja. Mengimputasi orang yang sama sekali tidak punya jejak akan membuat cabang ber-adopsi rendah terlihat normal, sehingga menyembunyikan masalah tepat di tempat masalahnya berada. Sistem lebih baik mengatakan "saya tidak tahu" daripada menebak dengan percaya diri.

## Identity resolution

Cascade empat tingkat. Tanpa Oracle Payroll tidak ada roster otoritatif, sehingga HRIS dipromosikan menjadi system of record secara default. Itu asumsi berisiko dan dicatat sebagai risiko, bukan disembunyikan.

| Tier | Aturan | Confidence | Hasil |
|---|---|---|---|
| T1 | NIK atau email korporat identik | 1,00 / 0,98 | Auto-merge |
| T2 | Nama ternormalisasi + tanggal lahir | 0,92 | Auto-merge |
| T3a | Fuzzy nama ≥ 0,965, cabang sama | 0,88 | Auto-merge |
| T3b | Fuzzy nama 0,86 sampai 0,965 | 0,70 | Antrean review |
| T4 | Hanya di HRIS, tanpa korroborasi | 0,85 | Auto, ditandai belum terkorroborasi |
| T4 | Hanya di ATS/LMS, tanpa jangkar HRIS | 0,45 | Antrean review |

Normalisasi nama memakai token sort supaya "Wijaya, Ahmad Budi" dan "Ahmad Budi Wijaya" bertemu. Blocking per cabang dipakai untuk menekan ruang perbandingan, tapi kecocokan tanggal lahir mengalahkan blocking, karena justru pola itu yang menandai mutasi antar cabang.

Record tunggal di HRIS tidak diperlakukan sebagai anomali. Itu kondisi normal bagi mayoritas populasi yang masuk sebelum ATS diadopsi. Menandainya untuk review akan membanjiri antrean dengan kasus yang tidak butuh manusia.

## Temuan headline

Skill sebenarnya digenerate dari distribusi identik untuk semua tier adopsi HRIS. Karena itu, setiap perbedaan antar tier di Dataset A adalah artefak pencatatan.

**Rata-rata gap score per tier adopsi HRIS**

| Tier adopsi | Dataset A | Dataset B |
|---|---|---|
| Tinggi | 0,504 | 0,486 |
| Menengah | 0,647 | 0,527 |
| Rendah | 0,965 | 0,553 |
| **Rentang** | **0,461** | **0,067** |

Rentang menyusut 85 persen. Di Dataset A, cabang dengan pencatatan terburuk terlihat sebagai cabang dengan krisis skill terparah. Mereka bukan.

**Perbandingan tingkat individu, 30 orang teratas**

| Metrik | Nilai |
|---|---|
| Kesepakatan A dan B | 10 dari 30 |
| Salah di-flag (muncul di A, tidak di B) | 20 |
| Terlewat (muncul di B, tidak di A) | 20 |

20 dari 30 orang yang akan dikirim ke program reskilling berdasarkan Dataset A adalah orang yang record HRIS-nya kosong, bukan orang yang punya gap skill. Anggaran pelatihan terbakar untuk menyelesaikan masalah pencatatan. Sementara itu 20 orang dengan gap nyata tidak pernah terlihat.

111 dari 200 orang di roster punya skor kebutuhan identik tertinggi karena nol skill tercatat. Sistem apa adanya tidak punya dasar apa pun untuk memilih 30 di antara mereka. Prototype menampilkan angka ini secara eksplisit.

## Implikasi untuk skenario Day 75

Case menanyakan apa yang dilakukan ketika model attrition menunjukkan akurasi 82 persen tapi tiga manajer HR menyatakan hasilnya terasa salah. Dataset ini memberi jawaban mekanistiknya, bukan sekadar dugaan.

Karena kekosongan berkorelasi dengan cabang, model apa pun yang dilatih di atas Dataset A akan menemukan sinyal kuat dan stabil pada kelengkapan record. Sinyal itu nyata, bisa direplikasi, dan menghasilkan akurasi tinggi pada test set. Yang dipelajari model adalah higienitas pencatatan cabang, bukan risiko tenaga kerja.

Manajer HR benar. Modelnya yang salah. Dan 82 persen adalah gejala, bukan bukti.
