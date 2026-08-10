# SauceDemo — Paket Pengujian QA & Otomasi

Paket pengujian yang mencakup login, keranjang belanja, pengurutan produk, dan checkout untuk
situs demo e-commerce SauceDemo, lengkap dengan pengecekan regresi terhadap bug bawaan yang
sudah disiapkan oleh SauceDemo sendiri. Cakupan test yang sama diimplementasikan di tiga
framework automation code-first — Playwright, Cypress, dan Selenium — supaya bisa dipakai
sebagai bahan latihan/perbandingan antar tool, plus panduan untuk Katalon Studio (GUI/low-code)
sebagai opsi ke-4.

**URL Aplikasi:** https://www.saucedemo.com/

Baru pertama kali buka repo ini? Mulai dari
[**docs/00-SDLC-STLC-Overview**](docs/00-SDLC-STLC-Overview/SDLC_STLC_Concept.md) untuk memahami
**kenapa** project ini disusun seperti ini — pemetaan SDLC/STLC, taksonomi jenis testing, dan
tools yang dipakai, semuanya ditautkan langsung ke artefak nyata (Test Plan, test case, hasil
eksekusi, laporan bug) di `docs/00` sampai `docs/10`.

---

## Struktur Repository

Dua akar utama: **`automation/`** (kode test — satu subfolder per framework) dan **`docs/`**
(siklus STLC lengkap `00`–`10`, mengikuti pola project QA lain milik penulis). Konfigurasi shared
(Node/`package.json`) tetap di root supaya `node_modules` tidak terduplikasi tiga kali.

```
Tester-Sauce.com/
├── automation/
│   ├── playwright/
│   │   ├── playwright.config.ts
│   │   └── tests/
│   │       ├── helpers/auth.ts
│   │       ├── auth.spec.ts          # LOGIN-01 s.d. LOGIN-08
│   │       ├── cart.spec.ts          # CART-01 s.d. CART-04
│   │       ├── sort.spec.ts          # SORT-01 s.d. SORT-04
│   │       ├── checkout.spec.ts      # CHK-01 s.d. CHK-05
│   │       └── known-issues.spec.ts  # BUG-001, 003–007
│   ├── cypress/
│   │   ├── cypress.config.ts
│   │   ├── tsconfig.json
│   │   ├── e2e/                      # struktur spec sama persis dengan playwright/tests
│   │   └── support/{e2e.ts,commands.ts}
│   ├── selenium/
│   │   ├── requirements.txt
│   │   └── tests/test_saucedemo.py
│   └── katalon/
│       └── README.md                 # panduan + script Groovy siap-pakai (belum ada project .prj — lihat isinya)
├── docs/
│   ├── 00-SDLC-STLC-Overview/
│   ├── 01-Test-Plan/
│   ├── 02-Test-Scenario/
│   ├── 03-Test-Case/
│   ├── 04-Test-Execution/
│   ├── 05-Bug-Report/
│   ├── 06-API-Testing/           # tidak berlaku untuk project ini — dijelaskan kenapa
│   ├── 07-SQL-Validation/        # tidak berlaku untuk project ini — dijelaskan kenapa
│   ├── 08-Test-Summary-Report/
│   ├── 09-Regression-Checklist/
│   └── 10-Panduan-Kerja-Harian/
├── .github/workflows/ci.yml      # Pipeline CI: job Playwright, Cypress, Selenium paralel
├── .env.example
├── package.json                  # Shared devDependencies (Playwright, Cypress, TypeScript)
└── README.md
```

| Folder docs/ | Isi | Fase STLC Terkait |
|---|---|---|
| [00-SDLC-STLC-Overview](docs/00-SDLC-STLC-Overview/SDLC_STLC_Concept.md) | Konsep SDLC & STLC dipetakan ke project ini, taksonomi jenis testing, tools & perbandingan Playwright/Cypress/Selenium | — (konsep dasar) |
| [01-Test-Plan](docs/01-Test-Plan/Test_Plan_SauceDemo.md) | Scope, in/out of scope, pendekatan, environment, deliverable | Test Planning |
| [02-Test-Scenario](docs/02-Test-Scenario/Test_Scenario_SauceDemo.md) | Skenario uji level tinggi per fitur, jembatan antara Test Plan dan Test Case | Test Case Design |
| [03-Test-Case](docs/03-Test-Case/Test_Case_SauceDemo.csv) | 27 test case detail (langkah, data uji, expected result) — bisa dibuka di Excel/Google Sheets | Test Case Design |
| [04-Test-Execution](docs/04-Test-Execution/Test_Execution_Report.md) | Hasil eksekusi **nyata** (bukan simulasi) per framework, termasuk breakdown test yang disengaja gagal | Test Execution |
| [05-Bug-Report](docs/05-Bug-Report/Bug_Report_SauceDemo.md) | 7 bug bawaan SauceDemo, lengkap status reproduksi per tanggal verifikasi | Test Execution → Defect Management |
| [06-API-Testing](docs/06-API-Testing/API_Testing_Not_Applicable.md) | **Tidak berlaku** untuk project ini — dijelaskan kenapa, bukan dilewati diam-diam | Test Execution (API layer) |
| [07-SQL-Validation](docs/07-SQL-Validation/SQL_Validation_Not_Applicable.md) | **Tidak berlaku** untuk project ini — dijelaskan kenapa | Test Execution (DB layer) |
| [08-Test-Summary-Report](docs/08-Test-Summary-Report/Test_Summary_Report.md) | Ringkasan siklus testing, defect density, coverage gap, dan rekomendasi | Test Cycle Closure |
| [09-Regression-Checklist](docs/09-Regression-Checklist/Regression_Test_Checklist.md) | Checklist ringkas untuk dipakai tiap kali suite dijalankan ulang | Regression Testing |
| [10-Panduan-Kerja-Harian](docs/10-Panduan-Kerja-Harian/Panduan_Kerja_QA_Automation.md) | **Bukan simulasi** — ritme kerja nyata memaintain suite automation seperti ini, termasuk hambatan nyata yang ditemukan saat membangunnya | — (panduan operasional, di luar STLC) |

---

## Akun Uji

Akun-akun ini sudah dipublikasikan langsung oleh SauceDemo di halaman login-nya, jadi tidak ada
yang bersifat rahasia di sini — data ini hanya dikumpulkan di `.env` supaya test tidak
menuliskan string yang sama berulang-ulang di banyak tempat.

| Username | Perilaku |
|----------|----------|
| `standard_user` | Alur normal, tanpa bug |
| `locked_out_user` | Login selalu ditolak |
| `problem_user` | Ada bug UI/gambar bawaan — lihat [BUG-001](docs/05-Bug-Report/Bug_Report_SauceDemo.md#bug-001--gambar-produk-tidak-menampilkan-gambar-yang-benar-problem_user) |
| `performance_glitch_user` | Ada bug dashboard lambat bawaan — lihat [BUG-007](docs/05-Bug-Report/Bug_Report_SauceDemo.md#bug-007--dashboard-memiliki-respons-yang-lambat-performance_glitch_user) |
| `error_user` | Ada bug bawaan pada sort/keranjang/checkout — lihat [BUG-003 sampai BUG-006](docs/05-Bug-Report/Bug_Report_SauceDemo.md) |
| `visual_user` | Ada bug tampilan (layout) bawaan — lihat [BUG-002](docs/05-Bug-Report/Bug_Report_SauceDemo.md#bug-002--halaman-dashboard-memiliki-beberapa-masalah-komponen-ui-visual_user) |

Password untuk semua akun: `secret_sauce`

### Setup Lokal

```bash
cp .env.example .env
npm install
```

Playwright/Cypress tidak otomatis membaca file `.env`. Export variabel-variabel berikut sebelum
menjalankan test jika ingin mengganti nilai default:

```bash
export TEST_USERNAME="standard_user"
export TEST_PASSWORD="secret_sauce"
```

Cypress hanya membaca env var berawalan `CYPRESS_` (prefix-nya otomatis dibuang), jadi untuk
mengganti password khusus di Cypress gunakan `CYPRESS_TEST_PASSWORD` sebagai gantinya.

---

## Cakupan Pengujian

| ID | Area | Deskripsi |
|----|------|-----------|
| LOGIN-01 | Login | Kredensial valid berhasil masuk ke halaman inventory |
| LOGIN-02 | Login | Kredensial tidak valid menampilkan pesan error yang sesuai |
| LOGIN-03 | Login | Username bersifat case-sensitive (peka huruf besar/kecil) |
| LOGIN-04 | Login | Username kosong diblokir dengan pesan error wajib diisi |
| LOGIN-05 | Login | Password kosong diblokir dengan pesan error wajib diisi |
| LOGIN-06 | Login | Akun yang terkunci (locked-out) selalu ditolak |
| LOGIN-07 | Login | Logout mengembalikan pengguna ke halaman login |
| LOGIN-08 | Login | Akses halaman cart tanpa login diarahkan ke halaman login |
| CART-01 | Keranjang | Add to cart mengubah status tombol dan memperbarui badge |
| CART-02 | Keranjang | Remove dari halaman inventory menghapus badge |
| CART-03 | Keranjang | Remove dari halaman keranjang menghapus item dari daftar |
| CART-04 | Keranjang | Continue Shopping kembali ke halaman inventory |
| SORT-01 | Pengurutan | Name (A to Z) |
| SORT-02 | Pengurutan | Name (Z to A) |
| SORT-03 | Pengurutan | Price (low to high) |
| SORT-04 | Pengurutan | Price (high to low) |
| CHK-01 | Checkout | Satu item, alur lengkap sampai selesai |
| CHK-02 | Checkout | Beberapa item, alur lengkap sampai selesai |
| CHK-03 | Checkout | First Name / Last Name / Postal Code kosong masing-masing diblokir |
| CHK-04 | Checkout | Karakter spesial diterima tanpa validasi format (karakteristik demo site) |
| CHK-05 | Checkout | Perhitungan total harga (subtotal + tax) di checkout overview benar |
| BUG-001 | Bug bawaan | `problem_user` — gambar produk tidak sesuai |
| BUG-003 | Bug bawaan | `error_user` — sort menampilkan error JavaScript |
| BUG-004 | Bug bawaan | `error_user` — tombol Add to cart tidak berfungsi di sebagian item |
| BUG-005 | Bug bawaan | `error_user` — field Last Name tidak bisa diisi |
| BUG-006 | Bug bawaan | `error_user` — tombol Finish tidak bisa diklik |
| BUG-007 | Bug bawaan | `performance_glitch_user` — dashboard lambat |

Katalog lengkap manual/otomatis: [docs/03-Test-Case/Test_Case_SauceDemo.csv](docs/03-Test-Case/Test_Case_SauceDemo.csv)

---

## Menjalankan Test

### Prasyarat
- Node.js 18+ dan npm
- Python 3.11+ dan pip

Semua perintah `npm`/`npx` di bawah dijalankan dari **root repo** — `package.json` dan
`node_modules` sengaja hanya ada satu set di root, dipakai bersama oleh Playwright dan Cypress.

### 1. Playwright

```bash
npm install
npx playwright install chromium
npm test
```

`npm test` setara dengan `npx playwright test --config=automation/playwright/playwright.config.ts`.

Menjalankan satu file test tertentu:
```bash
npx playwright test --config=automation/playwright/playwright.config.ts automation/playwright/tests/checkout.spec.ts
```

Melihat laporan HTML:
```bash
npm run test:report
```

### 2. Cypress

```bash
npm install
npm run cypress:run
```

`npm run cypress:run` setara dengan `npx cypress run --project automation/cypress`.

Membuka Cypress dalam mode interaktif (Test Runner GUI):
```bash
npm run cypress:open
```

Menjalankan satu file test tertentu:
```bash
npx cypress run --project automation/cypress --spec automation/cypress/e2e/checkout.cy.ts
```

> Cypress Test Runner adalah aplikasi Electron (butuh tampilan GUI). Jika dijalankan di
> lingkungan headless/sandbox yang tidak mendukung peluncuran binary Electron, `cypress run`
> tidak akan bisa start — jalankan dari terminal biasa di mesin lokal, bukan dari lingkungan
> tersandbox.

### 3. Selenium

```bash
cd automation/selenium
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cd ../..
npm run test:selenium
```

`npm run test:selenium` setara dengan `pytest automation/selenium/tests --disable-warnings -v`.

> Virtualenv Python bersifat **spesifik ke path absolut tempat ia dibuat** — kalau folder
> `automation/selenium/` dipindah lagi di kemudian hari, buat ulang venv-nya (`rm -rf venv &&
> python3 -m venv venv`) alih-alih memindahkannya, supaya tidak muncul `ModuleNotFoundError`.

### 4. Katalon Studio (opsional, GUI)

Berbeda dari 3 framework di atas: Katalon Studio adalah aplikasi desktop, bukan `npm`/`pip`
package, jadi tidak ada satu perintah CLI untuk "menjalankan semuanya". Ikuti panduan lengkap +
script Groovy siap-tempel di [`automation/katalon/README.md`](automation/katalon/README.md).

---

## CI/CD

GitHub Actions menjalankan Playwright, Cypress, dan Selenium secara paralel pada setiap push/PR
ke `main` — masing-masing mengarah ke path `automation/<framework>/` yang sesuai. Job Playwright
dan Cypress mengunggah laporan/artifact-nya (retensi 7 hari). Detail: [`.github/workflows/ci.yml`](.github/workflows/ci.yml).
Katalon **belum** masuk CI — GitHub-hosted runner tidak punya Katalon Runtime Engine terinstall,
dan `katalonc` sendiri belum pernah diverifikasi jalan di project ini (lihat
[`automation/katalon/README.md`](automation/katalon/README.md) §7).

---

## Dokumentasi

Lihat tabel folder `docs/` di atas untuk daftar lengkap `00-SDLC-STLC-Overview` sampai
`10-Panduan-Kerja-Harian`. Yang paling sering dibuka:

| File | Isi |
|------|-----|
| [docs/00-SDLC-STLC-Overview/SDLC_STLC_Concept.md](docs/00-SDLC-STLC-Overview/SDLC_STLC_Concept.md) | Pemetaan SDLC & 6 tahap STLC ke project ini, termasuk level testing yang relevan |
| [docs/01-Test-Plan/Test_Plan_SauceDemo.md](docs/01-Test-Plan/Test_Plan_SauceDemo.md) | Ruang lingkup, pendekatan, lingkungan, dan deliverable pengujian |
| [docs/03-Test-Case/Test_Case_SauceDemo.csv](docs/03-Test-Case/Test_Case_SauceDemo.csv) | Katalog lengkap test case |
| [docs/04-Test-Execution/Test_Execution_Report.md](docs/04-Test-Execution/Test_Execution_Report.md) | Hasil eksekusi nyata per framework |
| [docs/05-Bug-Report/Bug_Report_SauceDemo.md](docs/05-Bug-Report/Bug_Report_SauceDemo.md) | Bug bawaan SauceDemo, satu per akun uji, dipetakan ke pengecekan otomatis yang memverifikasinya |
| [docs/08-Test-Summary-Report/Test_Summary_Report.md](docs/08-Test-Summary-Report/Test_Summary_Report.md) | Ringkasan akhir siklus testing & rekomendasi |
# test-plan-sauce-demo-qa-automation-suite
