# QA Portfolio Project — Mobile Banking "SigmaPay" (Fund Transfer & QRIS Payment)

Project simulasi kerja QA Manual Tester untuk aplikasi **Mobile Banking dummy bernama "SigmaPay"**, fokus pada modul **Fund Transfer (Intrabank/Interbank/BI-FAST)** dan **QRIS Payment**. Dibuat untuk melatih & mendemonstrasikan skill set yang diminta di lowongan QA Engineer domain Banking:

- Manual Testing (Web, Mobile, API)
- Test Plan, Test Scenario, Test Case, Test Script, Test Evidence, Test Report
- Functional Testing, SIT, UAT, Regression Testing, Smoke Testing
- Defect Management (gaya JIRA)
- API Testing (gaya Postman)
- Basic SQL untuk validasi database
- Agile/Scrum

## Kenapa domain ini?

Loker "Tester Manual – Can Join Immediately" dan "QA Manual (ASAP/Banking)" secara eksplisit memprioritaskan pengalaman di **Digital Banking, Internet/Mobile Banking, Core Banking, Payment, Transfer, QRIS, Virtual Account, Loan, CASA**. Project ini dibuat supaya langsung "nyambung" saat dibahas di interview — kamu bisa cerita end-to-end proses testing-nya, bukan cuma teori.

## Struktur Project

| Folder | Isi | Fase STLC Terkait |
|---|---|---|
| [00-SDLC-STLC-Overview](00-SDLC-STLC-Overview/SDLC_STLC_Concept.md) | Penjelasan konsep SDLC & STLC, dipetakan ke aktivitas QA nyata di studi kasus ini. Termasuk [Taksonomi Jenis Testing](00-SDLC-STLC-Overview/Testing_Types_Taxonomy.md) dan [Tools per Tahap STLC + Panduan CV/Interview](00-SDLC-STLC-Overview/STLC_Tools_Mapping.md) | — (konsep dasar) |
| [01-Test-Plan](01-Test-Plan/Test_Plan_MobileBanking.md) | Test Plan lengkap (scope, strategy, environment, risk) | Test Planning |
| [02-Test-Scenario](02-Test-Scenario/Test_Scenario_Transfer_QRIS.md) | Daftar skenario uji level tinggi, termasuk edge case & negative case | Test Case Design |
| [03-Test-Case](03-Test-Case/Test_Case_Transfer_QRIS.csv) | 27 Test Case detail (langkah, data uji, expected result) — bisa dibuka di Excel/Google Sheets | Test Case Design |
| [04-Test-Execution](04-Test-Execution/Test_Execution_Report.md) | Simulasi hasil eksekusi test case (Pass/Fail) + test evidence | Test Execution |
| [05-Bug-Report](05-Bug-Report/Bug_Report_Sample.md) | 6 sample bug report gaya JIRA, lengkap severity/priority | Test Execution → Defect Management |
| [06-API-Testing](06-API-Testing/Postman_API_Test_Notes.md) | Dokumentasi API testing (Postman) untuk endpoint Transfer & QRIS | Test Execution (API layer) |
| [07-SQL-Validation](07-SQL-Validation/SQL_Queries_Validation.sql) | Query SQL untuk validasi data backend setelah transaksi | Test Execution (DB layer) |
| [08-Test-Summary-Report](08-Test-Summary-Report/Test_Summary_Report.md) | Laporan akhir siklus testing + rekomendasi go-live | Test Cycle Closure |
| [09-Regression-Checklist](09-Regression-Checklist/Regression_Test_Checklist.md) | Checklist regresi ringkas untuk dipakai tiap ada bug fix/release baru | Regression Testing |
| [10-Panduan-Kerja-Harian](10-Panduan-Kerja-Harian/Panduan_Kerja_QA_Manual_Banking.md) | **Bukan simulasi** — gambaran nyata kerja harian/mingguan/per-sprint kalau kamu diterima di posisi ini: onboarding, ritme sprint, deliverable, jalur eskalasi, tantangan lapangan, ekspektasi 30/60/90 hari | — (panduan operasional, di luar STLC) |
| [SigmaPay Prototype Scope](<SigmaPay Prototype Scope/SigmaPay QA Workbench.dc.html>) | **Sumber kebenaran tunggal (source of truth)** — prototype interaktif 30 layar yang mengimplementasikan app SigmaPay + workbench QA di sampingnya (test case per layar, log API, tab SQL, tab Defect), dengan toggle build **v1.4.0-QA (buggy)** vs **v1.5.0-FIX**. Semua dokumen 00-09 di atas sudah disinkronkan terhadap data & business rule konkret di file ini | — (living scope, bukan deliverable STLC) |

## Tentang folder "SigmaPay Prototype Scope"

Folder ini berisi prototype interaktif (`SigmaPay QA Workbench.dc.html` + `ios-frame.jsx` + `support.js` + design system di `_ds/`) yang dibangun dengan tooling prototyping khusus (terlihat dari struktur `x-dc`/`dc-runtime`-nya) — **bukan format HTML statis biasa**, jadi kemungkinan besar perlu dibuka lewat tool yang sama yang membuatnya, bukan sekadar double-click di browser.

Fungsinya di project ini: jadi **spesifikasi hidup**. Semua nama akun, nomor rekening, nominal, business rule (mis. limit QRIS per transaksi vs limit transfer harian, pesan error "Pindah Buku" untuk transfer ke rekening sendiri), dan logika ke-6 bug (BUG-SGP-001 s.d. 006) diambil dari sana dan disinkronkan ke seluruh dokumen `01` s.d. `09`. Kalau ke depan prototype-nya berubah, dokumen di sini perlu di-sync ulang mengikuti — bilang saja kalau butuh sinkronisasi ulang.

## Cara pakai project ini saat interview

1. Mulai dari `00-SDLC-STLC-Overview` untuk menjelaskan **kenapa** kamu melakukan tahapan tersebut (interviewer suka nanya "kamu ngapain aja dari requirement sampai release?").
2. Tunjukkan `01-Test-Plan` sebagai bukti kamu bisa **merencanakan** testing, bukan cuma eksekusi.
3. Tunjukkan alur `02 → 03 → 04 → 05` sebagai bukti siklus **design case → eksekusi → temukan bug → laporkan bug**.
4. Tunjukkan `06` dan `07` sebagai bukti kamu bisa testing di luar UI (API & Database) — ini pembeda kandidat junior vs kandidat 3-5 tahun pengalaman.
5. Tutup dengan `08` sebagai bukti kamu paham **exit criteria** dan bisa membuat keputusan/rekomendasi rilis (soft skill yang dicari untuk level "3-5 tahun pengalaman").

## Catatan

Semua data (nomor rekening, nominal, ID transaksi) adalah **dummy/fiktif**, dibuat murni untuk simulasi latihan, tidak merepresentasikan sistem bank sungguhan manapun.
