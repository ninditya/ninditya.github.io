# Panduan Kerja Nyata — Kalau Kamu Diterima sebagai QA Manual Tester (Banking, Kontrak)

Ini **bukan** materi interview — ini gambaran realistis apa yang akan kamu kerjakan hari ke hari, minggu ke minggu, kalau diterima di salah satu dari 3 loker yang kamu share (Tester Manual Banking / QA Manual Banking, kontrak, ASAP, 3-5 tahun). Disusun berdasarkan detail konkret di job description-nya: SIT/UAT/Regression/Smoke, JIRA/Azure DevOps, Postman/Swagger, SQL, Agile/Scrum, prioritas domain Transfer/QRIS/VA/Loan/CASA.

## 1. Realita Posisi Ini (Baca Dulu Sebelum Masuk)

- **Kontrak + "Can Join Immediately"** = kemungkinan besar kamu **menggantikan tester yang keluar** atau **menambah kapasitas tim yang sudah berjalan lama** — bukan project baru dari nol. Artinya: sistemnya sudah ada, requirement lama sudah ada (mungkin tidak terdokumentasi rapi), dan kamu harus cepat "nyambung" ke konteks yang berjalan, bukan mulai dari requirement analysis kosong seperti di project simulasi SigmaPay.
- **Klien Banking** = proses lebih formal/ketat dibanding startup: ada kebutuhan **audit trail** (test evidence wajib lengkap karena bisa diaudit OJK/internal audit bank), ada **change management** yang lebih birokratis (approval berlapis sebelum deploy), dan **data nasabah asli tidak boleh dipakai untuk testing** — selalu data dummy/masking.
- **Vendor (Sigma Global Teknologi) yang di-outsource ke bank** = kamu kemungkinan bekerja di lokasi/tim campuran (vendor + internal bank), dengan dua rantai komando: PM/Lead dari vendor untuk urusan administratif, tapi requirement & sign-off tetap dari pihak bank.

## 2. Minggu Pertama (Onboarding) — Checklist Realistis

| Hari | Yang Biasanya Terjadi | Yang Perlu Kamu Lakukan Aktif |
|---|---|---|
| Hari 1-2 | Akun dibuat: email, JIRA/Azure DevOps, akses VPN, akses environment SIT/UAT | Pastikan **semua akses berfungsi** hari itu juga — akses lambat adalah alasan #1 tester baru telat produktif |
| Hari 2-3 | Knowledge transfer dari tester lama (jika ada) atau dari BA/Dev Lead | Minta: (a) daftar modul yang sudah pernah ditest, (b) existing test case repository, (c) daftar bug yang masih open, (d) akses ke dokumentasi API (Swagger) |
| Hari 3-5 | Mulai di-assign ticket kecil dulu (biasanya regression atau bug retest, bukan langsung fitur besar) | Pelajari **existing regression checklist** tim (kalau belum ada, ini kesempatan kamu menunjukkan value — usulkan buat, mirip [09-Regression-Checklist](../09-Regression-Checklist/Regression_Test_Checklist.md) di project ini) |
| Minggu 1 selesai | Ikut Sprint Planning/Refinement pertama kamu | Jangan cuma dengar — mulai tanya pertanyaan klarifikasi requirement, ini yang membedakan tester junior vs senior |

## 3. Ritme Kerja Harian (Daily Cycle — Realistis Sprint Berjalan)

```
09.00  Daily Standup (Scrum) — laporkan: kemarin ngetest apa, hari ini rencana apa, ada blocker apa
09.15  Cek papan JIRA/Azure DevOps — ticket mana yang statusnya "Ready for Test"
09.30  Eksekusi test case untuk ticket yang masuk, ambil evidence (screenshot/log) sambil jalan
       — bukan dikumpulkan di akhir, karena kalau lupa capture, harus reproduce ulang
11.00  Retest bug yang kemarin di-fix developer (prioritas tinggi — jangan numpuk di akhir sprint)
13.00  Lanjut eksekusi / API testing via Postman untuk endpoint terkait ticket hari ini
15.00  Log bug baru yang ditemukan (severity/priority jelas, steps to reproduce presisi —
       lihat format di [05-Bug-Report](../05-Bug-Report/Bug_Report_Sample.md))
16.00  Update status semua ticket yang dikerjakan hari ini di JIRA/Azure DevOps sebelum pulang
       — status yang telat di-update = sumber miskomunikasi paling umum di tim QA-Dev
```

## 4. Ritme Kerja per Sprint (Asumsi 2 Minggu, Agile/Scrum)

| Fase Sprint | Aktivitas QA | Terkait STLC |
|---|---|---|
| **Sprint Planning (H1)** | Ikut estimasi effort testing per User Story, tandai yang butuh SIT dengan sistem eksternal (BI-FAST/QRIS switching) sebagai higher risk | Test Planning |
| **Refinement/Requirement Walkthrough (H1-H2)** | Ajukan clarifying question ke BA/PO **sebelum** development selesai (shift-left) — misal soal limit transaksi, business rule rekening diblokir | Requirement Analysis |
| **Paralel dengan Development (H2-H5)** | Mulai tulis test scenario & test case dari requirement yang sudah fix, tidak menunggu build jadi | Test Case Design |
| **Build Masuk QA (H5 dst, biasanya beberapa kali per sprint)** | Smoke test dulu → kalau lolos baru functional test penuh → API test paralel → SQL validation untuk transaksi kritikal | Test Execution |
| **Bug Fixing Cycle (H6-H8)** | Retest bug, regression test area terdampak (bukan cuma area yang di-fix) | Test Execution (Regression) |
| **Menjelang Sprint Review (H9)** | Regression penuh, pastikan tidak ada Critical/Major open, siapkan demo bareng Dev jika diminta | Test Cycle Closure |
| **Sprint Review & Retro (H10)** | Demo hasil ke stakeholder, di retro: usulkan perbaikan proses (misal: butuh data test lebih variatif, environment sering down, dll) | Test Cycle Closure |

> Kalau ada rilis ke **UAT**, biasanya berjalan **di luar** sprint cycle biasa — kamu akan diminta mendampingi user bisnis bank, menerjemahkan temuan mereka (sering ditulis awam, tidak presisi) menjadi bug report yang bisa dikerjakan developer.

## 5. Deliverable yang Harus Kamu Hasilkan, dan Untuk Siapa

| Deliverable | Untuk Siapa | Kapan |
|---|---|---|
| Test Case (update dari existing repo, bukan bikin dari nol tiap kali) | Tim QA lain (reuse), Dev (acuan expected behavior) | Setiap ada User Story baru |
| Bug Report dengan evidence lengkap | Developer (fix), Dev Lead (prioritas), kadang di-review internal audit bank | Setiap ketemu defect |
| Test Execution Evidence (screenshot/log per test case) | Wajib untuk **audit compliance** perbankan — bukan sekadar formalitas | Setiap eksekusi |
| Test Summary Report per rilis | PM/Lead, kadang dipresentasikan ke pihak bank untuk keputusan go-live | Akhir tiap cycle SIT/UAT |
| Regression checklist yang terus diperbarui | Tim QA (dipakai berulang tiap rilis) | Living document, update tiap sprint |

## 6. Kolaborasi & Jalur Eskalasi (Siapa Dihubungi Kalau...)

| Situasi | Hubungi Siapa | Catatan |
|---|---|---|
| Requirement ambigu/tidak jelas | Business Analyst / Product Owner | Jangan asumsi sendiri lalu bikin test case salah arah — tanya dulu, dokumentasikan jawabannya |
| Developer tidak setuju itu bug ("itu emang gitu by design") | Bawa evidence konkret (screenshot, log, hasil query SQL) ke Dev Lead kalau tidak selesai di level developer | Ini kenapa evidence & SQL validation penting — bukan cuma klaim dari mulut |
| Sandbox eksternal (BI-FAST/QRIS switching) down/tidak stabil | Tim infra/vendor eksternal, eskalasi lewat PM kalau menghambat sprint | Realistis sering terjadi — integrasi pihak ketiga di luar kendali tim internal |
| Akses environment/VPN bermasalah | IT Support/DevOps internal | Jangan tunda lapor — makin lama makin menghambat testing hari itu |
| Deadline mepet, tidak semua bisa ditest | PM/Lead — diskusikan **risk-based prioritization**, bukan diam-diam skip testing tanpa bilang siapa-siapa | Prioritaskan modul yang menyentuh uang keluar (debit) dulu, baru kosmetik UI |

## 7. Tantangan Nyata yang Kemungkinan Kamu Hadapi

| Tantangan | Kenapa Sering Terjadi di Konteks Ini | Cara Menghadapinya |
|---|---|---|
| Dokumentasi requirement lama tidak lengkap/hilang | Sistem sudah berjalan lama, tester/BA sebelumnya sudah keluar | Reverse-engineer dari behavior sistem yang ada + tanya user bisnis yang paling paham |
| Environment SIT sering tidak stabil, data test terbatas | Environment banking biasanya dipakai bergantian banyak tim, tidak didedikasikan untuk QA saja | Siapkan test data sendiri di awal sprint, jangan menunggu sampai H-1 eksekusi |
| Data nasabah tidak boleh dipakai, harus masking/dummy | Kepatuhan data privasi & regulasi perbankan | Selalu pastikan test data policy sebelum mulai — tanya di minggu pertama |
| Regression manual memakan waktu besar tiap rilis | Automation belum ada/minim (sesuai loker: automation cuma "nice to have") | Usulkan mulai automasi bagian regression paling sering diulang — nilai tambah besar untuk kontrak kamu |
| Tekanan waktu tinggi karena status kontrak "ASAP" | Perusahaan butuh kapasitas cepat, biasanya karena backlog testing menumpuk | Fokus risk-based testing di awal, jangan coba test 100% coverage sempurna di bawah tekanan waktu — komunikasikan trade-off ke PM |
| User bisnis (UAT) melaporkan "bug" pakai bahasa awam/tidak presisi | User bisnis bank biasanya bukan orang teknis | Selalu klarifikasi ulang jadi steps to reproduce yang presisi sebelum diteruskan ke developer |

## 8. Metrik yang Biasanya Dipakai untuk Menilai Performa Kamu

| Metrik | Arti |
|---|---|
| **Defect Leakage Rate** | Berapa banyak bug lolos ke production yang harusnya ketemu saat testing — makin rendah makin baik |
| **Test Case Execution Rate** | Persentase test case yang berhasil dieksekusi sesuai timeline sprint |
| **Defect Turnaround Time** | Seberapa cepat kamu retest bug setelah developer bilang "sudah fix" |
| **On-time Delivery** | Apakah testing selesai sesuai jadwal rilis, tanpa jadi bottleneck tim |

## 9. Ekspektasi Realistis 30-60-90 Hari

| Periode | Ekspektasi |
|---|---|
| **30 hari pertama** | Sudah bisa mandiri eksekusi test case existing, familiar dengan modul utama (Transfer, QRIS minimal), sudah kontribusi minimal 1 bug report berkualitas per minggu |
| **60 hari** | Sudah bisa design test case sendiri dari requirement baru tanpa banyak bimbingan, mulai dipercaya pegang modul tertentu secara independen |
| **90 hari** | Dianggap kontributor penuh — bisa diajak diskusi risk-based prioritization saat deadline mepet, mulai dilibatkan di keputusan go/no-go rilis |

---

*Dokumen ini melengkapi bukan menggantikan simulasi project di folder 00-09 — project SigmaPay tetap berguna untuk latihan **bagaimana** membuat Test Plan/Case/Bug Report yang baik. Dokumen ini menjawab pertanyaan berbeda: **apa yang harus kamu lakukan setiap hari** kalau posisi ini benar-benar kamu jalani.*
