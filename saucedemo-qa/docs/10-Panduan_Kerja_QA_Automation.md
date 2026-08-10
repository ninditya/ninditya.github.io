# Panduan Kerja QA Automation Engineer — Berbasis Pengalaman Project Ini

**Bukan simulasi teori** — gambaran nyata ritme kerja kalau berperan sebagai QA
Automation/SDET yang memaintain suite seperti [Tester-Sauce.com](../../README.md) ini, ditulis dari
pengalaman langsung membangun & menjalankannya, termasuk hambatan nyata yang muncul (bukan
skenario ideal di atas kertas).

## 1. Onboarding ke Project Automation Baru (Minggu Pertama)

Kalau baru gabung ke tim dan diberi akses ke repo seperti ini, urutan wajar untuk cepat paham:

1. **Baca [`00-SDLC-STLC-Overview`](../00-SDLC-STLC-Overview/SDLC_STLC_Concept.md) dulu** —
   pahami *kenapa* struktur project-nya begini sebelum baca kode.
2. **Baca [`01-Test-Plan`](../01-Test-Plan/Test_Plan_SauceDemo.md)** — scope, out-of-scope, dan
   environment yang dipakai.
3. **Clone, install, dan jalankan sendiri** sebelum menyentuh kode:
   ```bash
   npm install
   npx playwright install chromium
   npx playwright test
   ```
   Kalau langkah ini gagal di mesin sendiri, itu sinyal paling awal ada masalah environment yang
   harus diselesaikan duluan — jangan mulai nulis test baru di atas fondasi yang belum jalan.
4. **Baca 2-3 file spec yang sudah ada** (mis. [`auth.spec.ts`](../../automation/playwright/tests/auth.spec.ts))
   sebelum menulis test case baru, supaya pola penamaan/struktur konsisten.

## 2. Ritme Kerja Reguler

| Ritme | Aktivitas |
|---|---|
| **Setiap ada perubahan kode/push** | CI ([`ci.yml`](../../.github/workflows/ci.yml)) jalan otomatis — cek hasilnya, jangan tunggu ditanya orang lain |
| **Mingguan/berkala** | Jalankan [Regression Checklist](../09-Regression-Checklist/Regression_Test_Checklist.md) secara sadar, bukan cuma percaya CI hijau — kadang perlu dicek manual detail perubahan status bug seperti di siklus 2026-08-10 |
| **Setiap ada fitur/area baru untuk diuji** | Mulai dari Test Scenario dulu ([`02-Test-Scenario`](../02-Test-Scenario/Test_Scenario_SauceDemo.md)), baru turun ke Test Case detail — jangan langsung nulis kode tanpa breakdown |
| **Setiap CI merah** | Triase dulu sebelum panik: apakah ini bug aplikasi (baik), test flaky (perlu diperbaiki), atau memang perubahan yang disengaja di `known-issues.spec.ts` (lihat §3 di bawah)? |

## 3. Skill Paling Sering Dipakai Sehari-hari (Bukan yang Paling Sering Disebut di Textbook)

Dari pengalaman langsung membangun project ini, yang paling sering benar-benar dipakai:

- **Triase kegagalan test**: dari 3 kegagalan Playwright di suite ini, semuanya harus dicek satu
  per satu — apakah itu defect aplikasi (BUG-001, 003, 005 — memang masih terjadi) atau justru
  kabar baik (BUG-004, 006, 007 — ternyata sudah tidak terjadi). Tanpa investigasi ini, "3 test
  gagal" gampang disalahartikan sebagai automation yang rusak.
- **Baca error message Playwright/Cypress/pytest dengan teliti** — locator yang tidak ditemukan,
  timeout, vs assertion mismatch itu tiga penyebab berbeda dengan cara debug berbeda.
- **Menjaga 3 framework tetap sinkron**: kalau selector SauceDemo berubah, ketiganya
  (`automation/playwright/`, `automation/cypress/`, `automation/selenium/`) harus diupdate bareng — gampang lupa salah satu kalau
  tidak disiplin.
- **Debugging environment, bukan cuma kode test**: contoh nyata dari project ini — `cypress run`
  sempat gagal bukan karena kode salah, tapi karena binary Electron-nya diblokir sandbox
  lingkungan development. Skill mendiagnosis "ini kode atau ini environment?" penting dan jarang
  diajarkan eksplisit.

## 4. Jalur Eskalasi (Kapan Lapor, ke Siapa)

| Situasi | Eskalasi |
|---|---|
| Test gagal karena bug aplikasi yang genuine baru | Laporkan sebagai defect baru — update [Bug Report](../05-Bug-Report/Bug_Report_SauceDemo.md) dengan format yang sama |
| Test gagal karena selector berubah (bukan bug) | Perbaiki kode test, bukan laporkan sebagai bug — tapi catat kalau perubahannya cukup besar (indikasi UI di-redesign) |
| CI gagal terus-menerus tanpa jelas sebabnya (flaky) | Jangan langsung tambah `retry`/`timeout` lebih besar sebagai solusi instan — cari akar masalahnya dulu (race condition? elemen animasi? network lambat?) |
| Framework/tool baru mau ditambahkan | Diskusikan dulu apakah benar-benar perlu — project ini sengaja pakai 3 framework untuk *latihan perbandingan*, bukan pola yang disarankan untuk project produksi (lihat [STLC_Tools_Mapping.md §3](../00-SDLC-STLC-Overview/STLC_Tools_Mapping.md)) |

## 5. Tantangan Nyata yang Muncul di Project Ini (Bukan Skenario Rekaan)

- **Binary Electron diblokir sandbox** saat mencoba menjalankan Cypress — solusinya bukan
  memaksakan install ulang berkali-kali, tapi investigasi akar masalah (cek `codesign`, `spctl`,
  coba jalankan binary langsung dengan `--version`) sampai ketemu bahwa masalahnya di level
  environment, bukan instalasi.
- **Data bug bawaan yang "basi"**: dokumentasi awal (dari referensi bug report lama) mencatat 7
  bug aktif, tapi setelah dijalankan ulang, 3 di antaranya sudah tidak reproduksi. Pelajarannya:
  **jangan pernah percaya dokumentasi lama tanpa verifikasi ulang** — ini persis kenapa
  regression testing itu penting, bukan basa-basi teori.
- **CSV dengan koma & kutip di dalam sel** — [`Test_Case_SauceDemo.csv`](../03-Test-Case/Test_Case_SauceDemo.csv)
  perlu escaping yang benar (RFC 4180) supaya tidak rusak saat dibuka di Excel/Google Sheets;
  divalidasi dengan `python3 -m csv` sebelum dianggap selesai, bukan cuma "keliatannya benar".

## 6. Ekspektasi 30/60/90 Hari (Kalau Ini Project Kerja Sungguhan)

| Periode | Ekspektasi |
|---|---|
| **30 hari** | Bisa menjalankan & membaca hasil ketiga framework tanpa bantuan, paham struktur `00`-`10`, mulai kontribusi test case kecil (mis. tambah kasus edge case baru di area yang sudah ada) |
| **60 hari** | Bisa triase kegagalan CI secara mandiri, tahu kapan sesuatu itu bug vs flaky vs environment issue, mulai usulkan perbaikan struktur (mis. multi-browser project, smoke tag) |
| **90 hari** | Bisa onboarding orang baru lain ke project ini, punya opini berdasar soal trade-off Playwright vs Cypress vs Selenium dari pengalaman langsung (bukan cuma baca artikel), dan proaktif menutup gap yang sudah diakui di [Test Summary Report §4](../08-Test-Summary-Report/Test_Summary_Report.md) |
