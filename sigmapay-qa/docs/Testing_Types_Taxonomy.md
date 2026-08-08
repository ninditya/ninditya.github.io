# Taksonomi Jenis Testing — Dilengkapi & Dipetakan ke Studi Kasus SigmaPay

Catatan awal kamu sudah benar sebagai kerangka. Di bawah ini dilengkapi bagian yang sering ditanyakan saat interview tapi belum ada di catatan (Smoke, Regression, Sanity, sub-jenis Performance, dll), plus contoh konkret dari project [SigmaPay](../README.md) supaya tidak sekadar hafalan.

## 1. Berdasarkan Tujuan

### Functional Testing
Menguji **apakah fitur bekerja sesuai requirement** — fokus ke "what", bukan "how".
- Contoh umum: checkout berhasil, validasi form.
- Contoh SigmaPay: transfer dengan saldo cukup berhasil ([TC-TRF-001](../03-Test-Case/Test_Case_Transfer_QRIS.csv)), field nominal negatif ditolak ([TC-TRF-012](../03-Test-Case/Test_Case_Transfer_QRIS.csv)).

### Non-Functional Testing
Menguji **kualitas sistem**, bukan fitur itu sendiri:

| Jenis | Definisi | Contoh SigmaPay |
|---|---|---|
| **Performance — Load Testing** | Sistem diuji pada beban normal-hingga-puncak sesuai ekspektasi | 1.000 user transfer bersamaan saat jam gajian |
| **Performance — Stress Testing** | Beban di luar kapasitas, untuk menemukan *breaking point* | 10.000 transaksi QRIS/detik saat event diskon merchant |
| **Performance — Spike/Soak Testing** | Lonjakan mendadak / beban berkelanjutan dalam waktu lama | Lonjakan transaksi menjelang tengah malam awal bulan (gajian) |
| **Security Testing** | Cek celah dasar sebelum masuk ke pentest formal | SQL injection di field catatan transfer ([TC-TRF-020](../03-Test-Case/Test_Case_Transfer_QRIS.csv)), IDOR di endpoint status transaksi (lihat [API Testing Notes](../06-API-Testing/Postman_API_Test_Notes.md) poin 4) |
| **Usability Testing** | Apakah user awam mudah memahami alur & pesan error | Apakah pesan "Saldo tidak mencukupi" jelas dibaca nasabah non-teknis |
| **Compatibility Testing** | Aplikasi berjalan normal di berbagai **browser** (untuk versi Web) dan **device/OS/versi** (untuk versi Mobile) | Relevan karena loker minta *Web, Mobile, dan API testing* — cek SigmaPay Web di Chrome/Safari/Edge, dan SigmaPay Mobile di Android/iOS versi lama vs baru |
| **Reliability/Recovery Testing** | Sistem pulih dengan baik setelah gangguan | Berkaitan langsung dengan [BUG-SGP-002 & BUG-SGP-003](../05-Bug-Report/Bug_Report_Sample.md) — koneksi putus & timeout switching BI-FAST |

> Catatan: Performance & Security formal biasanya tim terpisah (lihat "Out of Scope" di [Test Plan](../01-Test-Plan/Test_Plan_MobileBanking.md)), tapi manual tester tetap wajib paham konsepnya dan melakukan *sanity check* dasarnya sendiri.

## 2. Berdasarkan Level (V-Model)

Sudah dibahas detail di [SDLC_STLC_Concept.md](SDLC_STLC_Concept.md) §4. Ringkas + relasinya ke V-Model:

```
Requirement  ⟷  Acceptance Testing (UAT)
Design       ⟷  System Testing
Arsitektur   ⟷  Integration Testing (SIT)
Code         ⟷  Unit Testing
```

| Level | Siapa | Fokus | Contoh SigmaPay |
|---|---|---|---|
| Unit | Developer | Function/class/module individual | Fungsi hitung biaya admin BI-FAST |
| Integration (SIT) | QA | Aliran data antar modul/sistem eksternal | SigmaPay → core banking → switching BI-FAST → bank tujuan |
| System | QA | Sistem utuh, functional + non-functional | Seluruh alur transfer dari login s.d. e-receipt |
| Acceptance (UAT) | User/Business | Validasi sesuai kebutuhan bisnis | Business banking verifikasi flow transfer sesuai kebutuhan nasabah |

## 3. Berdasarkan Teknik

| Teknik | Definisi | Relevansi untuk Role Manual Tester |
|---|---|---|
| **Black Box** | Fokus input-output, tidak peduli source code | Ini yang **paling sering dipakai** manual tester — sesuai loker "Manual Testing" |
| **White Box** | Menguji logika di dalam code, lihat coverage (branch, path) | Biasanya dev/SDET; tester cukup paham dasarnya untuk diskusi root cause dengan dev |
| **Gray Box** | Kombinasi — tester tahu sedikit "isi dalam" sistem (skema DB, API contract) tanpa baca full source code | **Paling representatif untuk loker ini** — kamu diminta bisa SQL & API testing meski tidak baca source code aplikasi. Lihat [SQL Validation](../07-SQL-Validation/SQL_Queries_Validation.sql) & [API Testing Notes](../06-API-Testing/Postman_API_Test_Notes.md) |

## 4. Kategori Tambahan — Sering Ditanyakan Saat Interview, Eksplisit Diminta di Loker

| Jenis | Definisi | Beda dengan yang Mirip |
|---|---|---|
| **Smoke Testing** | Cek cepat: build baru layak diuji lanjut atau tidak (contoh: bisa login, buka menu transfer, buka scan QRIS) | Dangkal tapi luas cakupannya — lihat [Test Execution Report §2](../04-Test-Execution/Test_Execution_Report.md) |
| **Sanity Testing** | Cek sempit & dalam pada satu area yang baru saja di-fix | Beda dari Smoke: Sanity fokus ke 1 fitur spesifik, bukan seluruh aplikasi |
| **Regression Testing** | Pastikan fitur lama tidak rusak akibat perubahan di area lain | Lihat [Regression Checklist](../09-Regression-Checklist/Regression_Test_Checklist.md) |
| **Retesting** | Menguji ulang **defect yang sama** setelah di-fix developer | Beda dari Regression: Retesting hanya cek bug itu sendiri, Regression cek area sekitarnya yang mungkin ikut terdampak |
| **Exploratory Testing** | Testing tanpa script formal, mengandalkan pengalaman & intuisi tester untuk mencari bug tak terduga | Cara BUG-SGP-001 (double debit) & BUG-SGP-011 semacamnya sering ditemukan di dunia nyata — bukan dari test case yang sudah ditulis, tapi dari "insting" mencoba tap dua kali |
| **Ad-hoc Testing** | Testing random tanpa dokumentasi formal | Informal, biasanya dilakukan saat waktu sempit menjelang rilis |

## 5. Ringkasan: Jenis Testing Apa yang Menemukan Bug Apa (SigmaPay)

Tabel ini bagus untuk dijelaskan saat interview — menunjukkan kamu paham **kapan pakai teknik apa**, bukan cuma hafal definisi.

| Bug | Ditemukan Lewat Jenis Testing |
|---|---|
| [BUG-SGP-001](../05-Bug-Report/Bug_Report_Sample.md) — Double debit | Edge case functional testing (bisa juga lewat exploratory testing) |
| [BUG-SGP-002](../05-Bug-Report/Bug_Report_Sample.md) — Status ambigu saat koneksi putus | Non-functional: Reliability/Recovery Testing |
| [BUG-SGP-003](../05-Bug-Report/Bug_Report_Sample.md) — Tidak ada reversal otomatis | SIT (Integration Testing) — gagal di titik integrasi ke switching eksternal |
| [BUG-SGP-004](../05-Bug-Report/Bug_Report_Sample.md) — QR expired tetap diproses | Negative functional testing + Gray Box (validasi API, bukan cuma UI) |
| [BUG-SGP-005](../05-Bug-Report/Bug_Report_Sample.md) — Merchant ID tidak divalidasi | Gray Box Testing (butuh paham skema data merchant) + Integration Testing |
| [BUG-SGP-006](../05-Bug-Report/Bug_Report_Sample.md) — Validasi nominal negatif | Black Box functional testing (basic input validation) |
