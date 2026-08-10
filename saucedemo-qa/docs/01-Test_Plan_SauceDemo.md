# Test Plan — SauceDemo (Login & Checkout)

**Aplikasi:** https://www.saucedemo.com/
**Status:** Aktif

## 1. Pendahuluan

### a. Gambaran Umum
SauceDemo adalah situs e-commerce demo yang digunakan untuk latihan QA. Situs ini memiliki alur
login yang dibatasi oleh enam akun uji khusus (masing-masing sudah disiapkan dengan
perilaku/bug yang berbeda), katalog produk dengan fitur pengurutan, alur tambah/hapus item ke
keranjang, dan checkout tiga langkah (Your Information → Overview → Complete).

### b. Tujuan
Memastikan login, keranjang belanja, pengurutan, dan checkout berjalan dengan benar untuk alur
normal (positive case), memastikan skenario negatif/edge case (kredensial salah, field kosong,
data checkout tidak lengkap, akun terkunci) ditangani dengan pesan error yang sesuai, serta
memastikan bug bawaan yang memang sengaja disiapkan oleh situs ini (lihat
[Bug Report](../05-Bug-Report/Bug_Report_SauceDemo.md)) tetap terdokumentasi dan bisa
diverifikasi ulang lewat automation.

## 2. Item Pengujian

| # | Fitur | Item Uji |
|---|-------|----------|
| 1 | Login | Kredensial valid, kredensial tidak valid, username case-sensitive, username kosong, password kosong, akun terkunci, logout |
| 2 | Keranjang | Tambah ke keranjang, hapus dari halaman inventory, hapus dari halaman keranjang, tombol continue shopping |
| 3 | Pengurutan | Name (A–Z), Name (Z–A), Price (low–high), Price (high–low) |
| 4 | Checkout | Satu item, beberapa item, field wajib kosong (First Name / Last Name / Postal Code) |
| 5 | Bug bawaan | Bug yang sudah disiapkan pada akun `problem_user`, `error_user`, `visual_user`, `performance_glitch_user` |

## 3. In Scope Testing
Login, Keranjang Belanja, Pengurutan, Checkout (Your Information / Overview / Complete), serta
pengecekan regresi terhadap akun-akun bug bawaan milik SauceDemo.

## 4. Out of Scope Testing

| Fitur | Alasan |
|-------|--------|
| Register | Situs ini tidak memiliki fitur registrasi |
| Proses pembayaran | SauceDemo tidak memiliki payment gateway sungguhan — checkout menggunakan data pembayaran/pengiriman dummy yang tetap |
| Validasi alamat | Tidak ada validasi alamat sungguhan; hanya pengecekan field wajib diisi |
| Pengujian API | SauceDemo adalah demo yang seluruhnya berjalan di sisi client (client-rendered) dan tidak memiliki API publik untuk diuji |

## 5. Pendekatan Pengujian
Regresi otomatis diimplementasikan di tiga framework — Playwright (utama), Cypress, dan Selenium
(subset smoke test) — dengan cakupan test case yang sama, dijalankan pada Chromium/Chrome
headless. Keenam akun uji bawaan SauceDemo masing-masing diuji minimal satu kali supaya bug yang
sudah diketahui/disiapkan tetap bisa terus diverifikasi ulang, tidak hanya ditemukan lewat
pengujian manual.

## 6. Lingkungan Pengujian
- Website: https://www.saucedemo.com/
- Browser: Chromium (dikelola Playwright) / Electron+Chrome (Cypress) / Chrome (Selenium via
  webdriver-manager)
- Akun uji: `standard_user`, `locked_out_user`, `problem_user`, `performance_glitch_user`,
  `error_user`, `visual_user` — password `secret_sauce` untuk semua akun

## 7. Deliverable Pengujian
- Test Plan (dokumen ini)
- Test Scenario: [`02-Test-Scenario/Test_Scenario_SauceDemo.md`](../02-Test-Scenario/Test_Scenario_SauceDemo.md)
- Paket test otomatis: [`automation/playwright/`](../../automation/playwright) (Playwright), [`automation/cypress/`](../../automation/cypress) (Cypress),
  [`automation/selenium/`](../../automation/selenium) (Selenium)
- Katalog test case: [`03-Test-Case/Test_Case_SauceDemo.csv`](../03-Test-Case/Test_Case_SauceDemo.csv)
- Laporan eksekusi: [`04-Test-Execution/Test_Execution_Report.md`](../04-Test-Execution/Test_Execution_Report.md)
- Laporan bug: [`05-Bug-Report/Bug_Report_SauceDemo.md`](../05-Bug-Report/Bug_Report_SauceDemo.md)
- Test Summary & Regression Checklist: [`08-Test-Summary-Report/`](../08-Test-Summary-Report/Test_Summary_Report.md), [`09-Regression-Checklist/`](../09-Regression-Checklist/Regression_Test_Checklist.md)
- Pipeline CI: [`.github/workflows/ci.yml`](../../.github/workflows/ci.yml)

## 8. Referensi
Perilaku bug bawaan dikonfirmasi langsung terhadap akun-akun uji yang didokumentasikan oleh
SauceDemo sendiri, serta telah dicek ulang dari hasil latihan test plan/bug report manual
sebelumnya untuk situs yang sama.
