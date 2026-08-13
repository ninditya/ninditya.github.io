# QA Portfolio Project — Mobile Banking "SigmaPay" (Fund Transfer & QRIS Payment)

Project simulasi kerja QA Manual Tester untuk aplikasi **Mobile Banking dummy bernama "SigmaPay"**, fokus pada modul **Fund Transfer (Intrabank/Interbank/BI-FAST)** dan **QRIS Payment**. Dibuat untuk melatih & mendemonstrasikan skill set yang diminta di lowongan QA Engineer domain Banking:

- Manual Testing (Web, Mobile, API)
- Test Plan, Test Scenario, Test Case, Test Script, Test Evidence, Test Report
- Functional Testing, SIT, UAT, Regression Testing, Smoke Testing
- Defect Management (gaya JIRA)
- API Testing (gaya Postman)
- Basic SQL untuk validasi database
- Core Banking Backend (AS400/IBM i + DB2 for i) — konsep & pola verifikasi batch job
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
| [05-Bug-Report](05-Bug-Report/Bug_Report_Sample.md) | 7 sample bug report gaya JIRA, lengkap severity/priority (termasuk 1 bug di lapisan core banking AS400) | Test Execution → Defect Management |
| [06-API-Testing](06-API-Testing/Postman_API_Test_Notes.md) | Dokumentasi API testing (Postman) untuk endpoint Transfer & QRIS. Dilengkapi [latihan tambahan di public dummy API](06-API-Testing/Public_Dummy_API_Practice_Notes.md) (restful-booker, Swagger Petstore) — ditandai jujur terpisah dari simulasi SigmaPay | Test Execution (API layer) |
| [07-SQL-Validation](07-SQL-Validation/SQL_Queries_Validation.sql) | Query SQL untuk validasi data backend setelah transaksi | Test Execution (DB layer) |
| [08-Test-Summary-Report](08-Test-Summary-Report/Test_Summary_Report.md) | Laporan akhir siklus testing + rekomendasi go-live | Test Cycle Closure |
| [09-Regression-Checklist](09-Regression-Checklist/Regression_Test_Checklist.md) | Checklist regresi ringkas untuk dipakai tiap ada bug fix/release baru | Regression Testing |
| [10-Panduan-Kerja-Harian](10-Panduan-Kerja-Harian/Panduan_Kerja_QA_Manual_Banking.md) | **Bukan simulasi** — gambaran nyata kerja harian/mingguan/per-sprint kalau kamu diterima di posisi ini: onboarding, ritme sprint, deliverable, jalur eskalasi, tantangan lapangan, ekspektasi 30/60/90 hari | — (panduan operasional, di luar STLC) |
| [11-AS400-Core-Banking](11-AS400-Core-Banking/AS400_Concepts_Primer.md) | Lapisan **core banking backend** SigmaPay: konsep AS400/IBM i + DB2 for i, test case verifikasi batch job EOD, query validasi DB2 for i, checklist monitoring job — ditandai jujur sebagai belajar mandiri, bukan pengalaman production | Test Execution (core banking layer) |
| [12-Automation-Appium](12-Automation-Appium/README.md) | Automation suite (Appium + WebdriverIO + Mocha + Chai) yang menguji [SigmaPay Bank Demo](<SigmaPay Bank Demo/README.md>) sebagai mobile web — Page Object Model, 4 spec file (login/transfer/QRIS/bug regression). Kode lengkap, **belum pernah dieksekusi** terhadap Appium/emulator sungguhan (lihat catatan jujur di README-nya) | Test Execution (automation) |
| [SigmaPay Prototype Scope](<SigmaPay Prototype Scope/SigmaPay QA Workbench.dc.html>) | **Sumber kebenaran tunggal (source of truth)** — prototype interaktif 30 layar yang mengimplementasikan app SigmaPay + workbench QA di sampingnya (test case per layar, log API, tab SQL, tab Defect), dengan toggle build **v1.4.0-QA (buggy)** vs **v1.5.0-FIX**. Semua dokumen 00-09 di atas sudah disinkronkan terhadap data & business rule konkret di file ini | — (living scope, bukan deliverable STLC) |
| [SigmaPay Bank Demo](<SigmaPay Bank Demo/README.md>) | **Target automation** — aplikasi web statis (HTML/CSS/JS murni, tanpa tooling khusus) dengan 10 akun uji ala saucedemo.com (happy path, akun terkunci, saldo kosong, delay buatan, & 6 persona yang masing-masing mereproduksi satu bug dari `05-Bug-Report`), locator `data-testid` stabil di setiap elemen — siap dipakai latihan Selenium/Playwright/Cypress | — (system-under-test, bukan deliverable STLC) |

## Tentang folder "SigmaPay Prototype Scope"

Folder ini berisi prototype interaktif (`SigmaPay QA Workbench.dc.html` + `ios-frame.jsx` + `support.js` + design system di `_ds/`) yang dibangun dengan tooling prototyping khusus (terlihat dari struktur `x-dc`/`dc-runtime`-nya) — **bukan format HTML statis biasa**, jadi kemungkinan besar perlu dibuka lewat tool yang sama yang membuatnya, bukan sekadar double-click di browser.

Fungsinya di project ini: jadi **spesifikasi hidup**. Semua nama akun, nomor rekening, nominal, business rule (mis. limit QRIS per transaksi vs limit transfer harian, pesan error "Pindah Buku" untuk transfer ke rekening sendiri), dan logika ke-6 bug (BUG-SGP-001 s.d. 006) diambil dari sana dan disinkronkan ke seluruh dokumen `01` s.d. `09`. Kalau ke depan prototype-nya berubah, dokumen di sini perlu di-sync ulang mengikuti — bilang saja kalau butuh sinkronisasi ulang.

## Tentang folder "SigmaPay Bank Demo"

Ini pasangan dari "SigmaPay Prototype Scope" di atas, tapi dengan tujuan berbeda: kalau Prototype Scope adalah *spesifikasi hidup* yang perlu tooling khusus untuk dibuka, folder ini adalah **HTML/CSS/JS statis biasa** — tanpa dependency, langsung bisa dibuka di browser atau di-*serve* dengan static server apa pun, dan dirancang supaya **bisa langsung dipakai jadi target automation** (Selenium/Playwright/Cypress), mengikuti pola situs latihan seperti saucedemo.com: 10 akun login, masing-masing sengaja punya perilaku berbeda (lihat [`SigmaPay Bank Demo/README.md`](<SigmaPay Bank Demo/README.md>) untuk daftar lengkap & referensi locator `data-testid`).

## Tentang folder "11-AS400-Core-Banking"

Banyak loker QA Banking mensyaratkan familiaritas dengan **AS400/IBM i** karena banyak bank di Indonesia menjalankan core banking (ledger, rekening, batch EOD) di platform ini. Folder ini menambahkan lapisan itu ke narasi arsitektur SigmaPay: mobile app + API (yang sudah dibangun di `06-API-Testing`) berperan sebagai *channel layer*, sementara AS400/DB2 for i berperan sebagai *system of record*. Isinya: primer konsep, test case verifikasi batch job, query gaya DB2 for i, dan checklist monitoring job — **semuanya ditandai eksplisit sebagai hasil belajar mandiri untuk portfolio, bukan pengalaman hands-on production AS400 sungguhan** (lihat tabel kejujuran di [AS400_Concepts_Primer.md §4](11-AS400-Core-Banking/AS400_Concepts_Primer.md#4-status-kejujuran-mengikuti-pola-stlc_tools_mappingmd)).

## Tentang folder "12-Automation-Appium"

Implementasi automation nyata (bukan cuma "familiar with the concept") untuk `SigmaPay Bank Demo`, pakai stack **Appium + WebdriverIO + Mocha + Chai** dalam mode *mobile web testing* (drive Chrome/Safari di emulator/simulator, tanpa APK/IPA karena target-nya web statis). Page Object Model per halaman, 4 spec file mencakup login, transfer, QRIS, dan regresi 6 persona "bug". **Kode-nya lengkap dan sudah disinkronkan ke locator `data-testid` sungguhan di source Bank Demo, tapi belum pernah dijalankan end-to-end terhadap Appium server/emulator sungguhan** — lihat [README folder ini](12-Automation-Appium/README.md) untuk cara setup & verifikasi sendiri, dan catatan kejujuran soal ini di interview.

## Cara pakai project ini saat interview

1. Mulai dari `00-SDLC-STLC-Overview` untuk menjelaskan **kenapa** kamu melakukan tahapan tersebut (interviewer suka nanya "kamu ngapain aja dari requirement sampai release?").
2. Tunjukkan `01-Test-Plan` sebagai bukti kamu bisa **merencanakan** testing, bukan cuma eksekusi.
3. Tunjukkan alur `02 → 03 → 04 → 05` sebagai bukti siklus **design case → eksekusi → temukan bug → laporkan bug**.
4. Tunjukkan `06` dan `07` sebagai bukti kamu bisa testing di luar UI (API & Database) — ini pembeda kandidat junior vs kandidat 3-5 tahun pengalaman.
5. Tutup dengan `08` sebagai bukti kamu paham **exit criteria** dan bisa membuat keputusan/rekomendasi rilis (soft skill yang dicari untuk level "3-5 tahun pengalaman").
6. Kalau ditanya soal automation, buka `SigmaPay Bank Demo` langsung di browser dan tunjukkan kamu bisa merancang **test data & test target-nya sendiri** (bukan cuma jalankan skrip di aplikasi orang lain) — poin pembeda dibanding kandidat yang cuma pernah latihan di situs demo publik. Lanjutkan dengan `12-Automation-Appium` untuk menunjukkan kode automation-nya sendiri (Page Object Model, Appium + Mocha + Chai) — tapi jujur bilang kalau belum sempat eksekusi end-to-end di emulator sungguhan.
7. Kalau ditanya soal core banking/AS400, buka `11-AS400-Core-Banking` untuk menunjukkan kamu paham *apa* yang perlu divalidasi di lapisan core banking (batch job, rekonsiliasi ledger, DB2 for i) dan *kenapa* — pakai template jawaban jujur di [AS400_Concepts_Primer.md §5](11-AS400-Core-Banking/AS400_Concepts_Primer.md#5-template-jawaban-interview-versi-jujur), jangan klaim ini pengalaman production.

## Catatan

Semua data (nomor rekening, nominal, ID transaksi) adalah **dummy/fiktif**, dibuat murni untuk simulasi latihan, tidak merepresentasikan sistem bank sungguhan manapun.
