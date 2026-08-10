# Tools & Aplikasi per Tahap STLC — Dipetakan ke Project SauceDemo + Panduan CV/Interview

Melengkapi [SDLC_STLC_Concept.md](SDLC_STLC_Concept.md) (6 tahap STLC) dengan tools yang benar-benar
dipakai di project ini. Beda dengan portofolio manual-testing yang biasanya menandai automation
sebagai "familiar with the concept", **di project ini automation-nya nyata ditulis dan dijalankan**
— jadi kolom status di bawah kebanyakan ✅, bukan "belum".

## 1. Tools per Tahap STLC

| Tahap STLC | Aktivitas | Tools Umum di Industri | Status di Project SauceDemo Ini |
|---|---|---|---|
| **1. Requirement Analysis** | Eksplorasi aplikasi, susun requirement dari observasi | Jira, Confluence, Notion, browser DevTools | ✅ Nyata: requirement direkonstruksi lewat eksplorasi manual & dicatat di [Test_Plan_SauceDemo.md](../01-Test-Plan/Test_Plan_SauceDemo.md) §1-2 |
| **2. Test Planning** | Scope, strategy, environment, exit criteria | Jira, Confluence, Excel | ✅ Nyata: [Test_Plan_SauceDemo.md](../01-Test-Plan/Test_Plan_SauceDemo.md) lengkap |
| **3. Test Case Design** | Test case + langsung jadi test script | TestRail, Zephyr/Xray, Jira, Excel | ✅ Nyata, dua lapis: dokumen [Test_Case_SauceDemo.csv](../03-Test-Case/Test_Case_SauceDemo.csv) (setara Excel/Sheets) **dan** implementasi kodenya langsung di 3 framework |
| **4. Test Environment Setup** | Config runner, browser, dependency, env var | Docker, Git, Jenkins/GitHub Actions | ✅ Nyata: [automation/playwright/playwright.config.ts](../../automation/playwright/playwright.config.ts), [automation/cypress/cypress.config.ts](../../automation/cypress/cypress.config.ts), [automation/selenium/requirements.txt](../../automation/selenium/requirements.txt), [.env.example](../../.env.example) |
| **5. Test Execution** | Jalankan test, otomasi UI | Selenium, Playwright, Cypress, Katalon, Appium | ✅ **Playwright**: dijalankan nyata ke situs live, 26/29 lulus (3 kegagalan disengaja — verifikasi bug bawaan; termasuk 3 test case baru hasil validasi test case manual eksternal). ✅ **Selenium**: dijalankan nyata, 7/7 lulus (subset smoke test). ⚠️ **Cypress**: 23/26 lulus untuk test lama (dijalankan nyata di Cypress Test Runner) — pass rate sama persis dengan Playwright untuk test yang sama, tapi 2 dari 6 hasil `known-issues` berbeda antar keduanya; 3 test case terbaru sudah lolos type-check tapi belum dieksekusi (lihat [Test_Execution_Report.md §4 & §7](../04-Test-Execution/Test_Execution_Report.md#4-detail-hasil--known-issues-verifikasi-bug-bawaan-playwright-vs-cypress)). ⚠️ **Katalon**: panduan + script Groovy siap-pakai ada di [`automation/katalon/README.md`](../../automation/katalon/README.md), tapi belum ada project `.prj` yang dibuat/dijalankan — Katalon Studio adalah aplikasi desktop GUI yang tidak bisa dijalankan dari sesi development (CLI, tersandbox) yang dipakai membangun repo ini |
| ↳ *Defect Reporting* | Log bug, severity, status, retest | Jira, Azure DevOps | ✅ Nyata, gaya laporan bug: [Bug_Report_SauceDemo.md](../05-Bug-Report/Bug_Report_SauceDemo.md) — termasuk status "reproduksi ulang" per tanggal, bukan cuma daftar statis |
| ↳ *API Testing* | Validasi endpoint backend | Postman, Swagger | ❌ Tidak berlaku — SauceDemo tidak punya API publik untuk diuji (lihat Out of Scope di [Test_Plan_SauceDemo.md](../01-Test-Plan/Test_Plan_SauceDemo.md) §4) |
| ↳ *Database Validation* | Validasi data backend | SQL, DBeaver | ❌ Tidak berlaku — aplikasi client-side murni, tidak ada akses database |
| **6. Test Cycle Closure** | Summary, defect metrics, sign-off | Jira, Excel, Confluence | ⚠️ Sebagian: ringkasan status defect ada di bagian atas [Bug_Report_SauceDemo.md](../05-Bug-Report/Bug_Report_SauceDemo.md), tapi laporan closure formal (coverage %, rekomendasi) belum dibuat terpisah |

> **Catatan jujur soal Cypress (sudah selesai):** selama proses membangun project ini, `cypress
> run` sempat dicoba dijalankan di sesi development yang tersandbox dan gagal start — bukan
> karena kode testnya salah, tapi karena lingkungan sandbox tersebut mengganti proses binary
> Electron (yang dipakai Cypress sebagai test runner) dengan stub lain. Kode divalidasi lewat
> type-check saat itu (lolos, 0 error), lalu **dijalankan sungguhan oleh pemilik project di
> Cypress Test Runner miliknya sendiri** — hasilnya 23/26 lulus, pass rate identik dengan
> Playwright. Detail lengkap termasuk 2 hasil yang berbeda dari Playwright (BUG-003, BUG-007) ada
> di [Test_Execution_Report.md §4](../04-Test-Execution/Test_Execution_Report.md#4-detail-hasil--known-issues-verifikasi-bug-bawaan-playwright-vs-cypress).
> Setelahnya, 3 test case baru ditambahkan (LOGIN-08, CHK-04, CHK-05, lihat
> [Test_Execution_Report.md §7](../04-Test-Execution/Test_Execution_Report.md)) — sudah lolos
> type-check, menunggu dijalankan ulang di Cypress untuk melengkapi datanya jadi 29/29.

## 2. Tools Dikelompokkan per Kategori (untuk CV)

| Kategori | Tools |
|---|---|
| **Automation (Web E2E, code-first)** | Playwright, Cypress, Selenium (WebDriver) |
| **Automation (Web E2E, GUI/low-code)** | Katalon Studio — lihat [`automation/katalon/README.md`](../../automation/katalon/README.md) |
| **Bahasa & Runtime** | TypeScript, Python (pytest), Groovy (Katalon) |
| **Test Management / Dokumentasi** | Markdown, CSV (setara Excel/Sheets), GitHub |
| **CI/CD** | GitHub Actions |
| **Dependency & Environment** | npm, pip, `webdriver-manager`, virtualenv |

**Tidak relevan untuk project ini** (bukan berarti tidak dikuasai secara umum, hanya tidak
dipakai di sini karena scope-nya): API testing (Postman), SQL/database validation, mobile
testing (Appium) — SauceDemo adalah aplikasi web murni tanpa backend yang bisa diakses dan tidak
punya versi mobile.

**Aturan main untuk CV:** karena automation di project ini benar-benar dijalankan dan hasilnya
bisa ditunjukkan (bukan cuma diklaim), aman mencantumkan Playwright, Cypress, dan Selenium
sebagai **hands-on**, bukan sekadar "familiar with the concept". Ini melengkapi portofolio QA
manual (kalau ada) yang biasanya lebih kuat di sisi Test Planning/Test Case Design/Defect
Management gaya Jira tapi automation-nya masih level konsep — dua jenis project ini saling
menutupi kekurangan satu sama lain kalau ditunjukkan bersamaan.

**Khusus Katalon:** karena project-nya belum benar-benar dibuat & dijalankan di Katalon Studio
(baru panduan + script Groovy), yang jujur dicantumkan di CV adalah **"familiar with Katalon
Studio, siap onboarding"** — persis prinsip yang sama dipakai di portofolio QA manual lain milik
penulis untuk tools yang belum sempat dipraktikkan hands-on. Statusnya bisa naik jadi "hands-on"
begitu project-nya benar-benar dibuat & dijalankan mengikuti [panduan](../../automation/katalon/README.md)
tersebut.

## 3. Kenapa 3 Framework Sekaligus (Bukan 1 Saja)?

Umumnya di industri, tim hanya memakai **satu** framework automation utama. Menulis di tiga
sekaligus (Playwright, Cypress, Selenium) untuk test case yang identik bukan praktik industri
standar — ini sengaja dilakukan di project ini sebagai **latihan perbandingan tool**, supaya bisa
menjawab pertanyaan interview seperti "kenapa pilih Playwright dibanding Selenium?" dengan
pengalaman langsung, bukan hafalan dari artikel:

| Aspek | Playwright | Cypress | Selenium |
|---|---|---|---|
| Bahasa di project ini | TypeScript | TypeScript | Python |
| Model eksekusi | Node.js, multi-browser engine bawaan | Electron sebagai test runner, driver browser bawaan | WebDriver protocol, butuh driver eksternal (di sini via `webdriver-manager`) |
| Auto-wait | Bawaan di setiap assertion | Bawaan di setiap `cy.` command | Perlu `WebDriverWait` eksplisit (terlihat jelas di [test_saucedemo.py](../../automation/selenium/tests/test_saucedemo.py)) |
| Kecepatan setup di project ini | Cepat — satu `npx playwright install` | Cepat untuk kode, tapi binary Electron-nya besar (~600MB) | Perlu venv + `ChromeDriverManager` terpisah |
| Kesan setelah dipakai di project ini | Config & assertion paling ringkas | API paling "enak dibaca", tapi runner-nya Electron jadi kurang ramah lingkungan headless/sandbox tertentu | Paling verbose tapi paling universal (dukungan browser/bahasa terluas di industri) |

## 4. Template Jawaban Interview (Versi Jujur, Berbasis Project Ini)

Kalau ditanya *"Pengalaman automation testing kamu apa?"*:

> "Saya membangun test automation suite untuk aplikasi e-commerce demo SauceDemo, mencakup
> login (termasuk 6 akun uji dengan perilaku berbeda), keranjang belanja, pengurutan produk, dan
> alur checkout 3 langkah — saya implementasikan di tiga framework berbeda sekaligus: Playwright,
> Cypress, dan Selenium, dengan test case yang sama supaya bisa membandingkan langsung
> trade-off-nya. Saya juga membangun test khusus untuk memverifikasi ulang bug-bug bawaan yang
> memang sengaja disiapkan situs ini untuk latihan QA, dan dari situ saya menemukan bahwa
> beberapa bug yang sebelumnya tercatat aktif ternyata sudah tidak reproduksi lagi — jadi suite
> ini bukan cuma menjalankan test yang lolos, tapi juga aktif mendeteksi perubahan perilaku
> aplikasi dari waktu ke waktu. Saya juga menemukan bahwa Playwright dan Cypress memberi hasil
> berbeda untuk satu bug spesifik (satu framework menangkap alert JavaScript, satu lagi tidak) —
> dari situ saya belajar kalau dua tool automation bisa berinteraksi dengan halaman yang sama
> secara teknis berbeda (simulasi event JS vs kontrol browser native), yang penting dipahami
> supaya tidak salah menyimpulkan 'bug hilang' padahal itu keterbatasan tool-nya. Semua terhubung
> ke pipeline CI di GitHub Actions supaya jalan otomatis setiap ada perubahan."

Kalimat ini aman karena semuanya bisa langsung ditunjukkan (hasil run, kode, CI config) kalau
diminta bukti konkret saat interview.
