# Tools & Aplikasi per Tahap STLC — Dipetakan ke Project SigmaPay + Panduan CV/Interview

Melengkapi [SDLC_STLC_Concept.md](SDLC_STLC_Concept.md) (6 tahap STLC) dengan **tools yang umum dipakai di industri** pada tiap tahap, dan **jujur menandai** mana yang benar-benar dipakai/disimulasikan di project SigmaPay ini vs mana yang sekadar perlu kamu pahami konsepnya.

> Kenapa kolom "status" penting: interviewer sering minta bukti konkret ("coba tunjukkan board Jira-nya", "boleh lihat collection Postman-nya?"). Lebih aman bilang *"familiar dengan tools X"* daripada mengklaim pernah pakai production kalau kenyataannya belum — sesuai insight yang kamu bawa sendiri di bawah.

## 1. Tools per Tahap STLC (6 Tahap, konsisten dengan SDLC_STLC_Concept.md)

| Tahap STLC | Aktivitas | Tools Umum di Industri | Status di Project SigmaPay Ini |
|---|---|---|---|
| **1. Requirement Analysis** | Review User Story, acceptance criteria, susun RTM | Jira, Confluence, Notion, Google Docs | Disimulasikan via markdown (requirement diwakili narasi di [README](../README.md) & [Test Plan](../01-Test-Plan/Test_Plan_MobileBanking.md)) |
| **2. Test Planning** | Scope, strategy, resource, timeline, risk | Jira, Confluence, Excel/Google Sheets | ✅ Dibuat nyata: [Test_Plan_MobileBanking.md](../01-Test-Plan/Test_Plan_MobileBanking.md) |
| **3. Test Case Design** | Test scenario & test case | TestRail, Zephyr/Xray, Jira, Excel | ✅ Dibuat nyata dalam format CSV (setara Excel/Sheets): [Test_Case_Transfer_QRIS.csv](../03-Test-Case/Test_Case_Transfer_QRIS.csv). TestRail/Zephyr/Xray = tools yang sama fungsinya, belum dipakai hands-on |
| **4. Test Environment Setup** | Siapkan environment, akses sandbox, test data | Docker, Postman, Swagger, Git, Jenkins | Sebagian: struktur environment & test data didokumentasikan di Test Plan §7-8. Docker/Jenkins di luar tanggung jawab manual tester sehari-hari (biasanya disiapkan DevOps) — cukup paham konsepnya |
| **5. Test Execution** | Jalankan test case manual, API testing, (opsional) automation | Postman, Swagger, Selenium, Playwright, Katalon, Appium, Browser DevTools | ✅ Manual execution: [Test_Execution_Report.md](../04-Test-Execution/Test_Execution_Report.md). ✅ API testing: [Postman_API_Test_Notes.md](../06-API-Testing/Postman_API_Test_Notes.md). Automation (Selenium/Playwright/Katalon/Appium) **belum** — masih level "paham konsep" |
| ↳ *Defect Reporting (bagian dari Execution)* | Log bug, severity/priority, retest | Jira, Azure DevOps, ClickUp, Bugzilla | ✅ Disimulasikan gaya Jira: [Bug_Report_Sample.md](../05-Bug-Report/Bug_Report_Sample.md) |
| ↳ *Database Validation (bagian dari Execution)* | Validasi data backend | SQL (PostgreSQL/MySQL), DBeaver | ✅ Dibuat nyata: [SQL_Queries_Validation.sql](../07-SQL-Validation/SQL_Queries_Validation.sql) |
| **6. Test Cycle Closure** | Test summary, defect metrics, sign-off, go/no-go | Jira, Excel, Confluence | ✅ Dibuat nyata: [Test_Summary_Report.md](../08-Test-Summary-Report/Test_Summary_Report.md) |

## 2. Tools Dikelompokkan per Kategori (untuk CV)

| Kategori | Tools |
|---|---|
| **Test Management** | Jira, TestRail, Zephyr/Xray, Azure DevOps |
| **API Testing** | Postman, Swagger/OpenAPI |
| **Automation** | Selenium, Playwright, Katalon, Appium |
| **Database Validation** | SQL, PostgreSQL, MySQL |
| **CI/CD & Version Control** | Git, GitHub/GitLab, Jenkins |
| **Documentation** | Confluence, Google Sheets/Excel, Notion |

**Aturan main untuk CV:** cantumkan hanya tools yang benar-benar bisa kamu jelaskan alurnya kalau ditanya detail saat interview. Untuk QA Analyst/Manual Tester, tidak perlu daftar semua — pilih yang relevan dan bisa dipertanggungjawabkan.

Berdasarkan apa yang **sudah nyata kamu praktikkan lewat project SigmaPay** ini, kombinasi paling jujur dan tetap kuat untuk dicantumkan:

> **STLC, Test Planning, Test Case Design, SIT, UAT, Smoke Testing, Regression Testing, API Testing (Postman), Defect Management (gaya Jira), Database Validation (SQL)**

Selenium/Playwright/Katalon boleh disebut sebagai **"familiar with the concept, siap onboarding"** — bukan "hands-on production experience" — kecuali kamu memang sudah pernah pakai langsung.

## 3. Posisi Katalon dalam STLC (Termasuk Konteks Mobile Banking)

Katalon relevan terutama di tahap **Test Execution**, mencakup Web UI automation, API testing, dan Mobile testing sekaligus (satu tool untuk tiga jenis testing — ini nilai jual utamanya dibanding Selenium yang web-only atau Appium yang mobile-only).

| Tahap STLC | Peran Katalon |
|---|---|
| Requirement Analysis | Tidak langsung — hanya jadi input untuk desain automated test case |
| Test Planning | Menentukan scope mana yang layak diotomasi (biasanya: regression suite berulang, bukan fitur yang masih sering berubah) |
| Test Case Design | Membuat test case & test script di dalam Katalon |
| Environment Setup | Konfigurasi target browser/device/API endpoint |
| **Test Execution** | **Menjalankan automated test** — ini peran utamanya |
| Defect Reporting | Bisa diintegrasikan ke Jira untuk auto-log hasil gagal |
| Test Closure | Menghasilkan execution report & pass/fail metrics otomatis |

### Khusus konteks Mobile Banking

Untuk mobile banking, Katalon **bukan satu-satunya tools** — kombinasi realistis: **UI/Mobile automation (Katalon/Appium) + API testing (Postman) + Database validation (SQL) + device coverage (Android Studio/Xcode/BrowserStack)**.

Contoh alur automated test yang relevan untuk modul di project ini:
```
Login → OTP → Cek Saldo → Transfer/Scan QRIS → Konfirmasi → Cek Riwayat Mutasi
```
Katalon menjalankan alur UI-nya, sementara Postman tetap dipakai terpisah untuk memvalidasi API di baliknya (`POST /transfer`, `POST /qris/pay` — lihat [API Testing Notes](../06-API-Testing/Postman_API_Test_Notes.md)).

> Catatan implementasi di project ini: seluruh test case di [03-Test-Case](../03-Test-Case/Test_Case_Transfer_QRIS.csv) saat ini masih **manual**. Kandidat kuat untuk diotomasi lebih dulu dengan Katalon/Selenium/Playwright adalah suite di [09-Regression-Checklist](../09-Regression-Checklist/Regression_Test_Checklist.md), karena regression test paling sering diulang tiap rilis — nilai ROI automation paling tinggi di situ. Ini bisa jadi pengembangan lanjutan project kalau kamu mau praktik hands-on beneran.

## 4. Template Jawaban Interview (Versi Jujur, Berbasis Project Ini)

Kalau ditanya *"Tools apa yang kamu pakai dalam STLC?"*:

> "Saya membangun sendiri sebuah project simulasi QA manual testing untuk aplikasi mobile banking, mencakup seluruh siklus STLC — mulai dari Test Plan, Test Scenario, dan Test Case, eksekusi manual dengan pencatatan hasil dan evidence, defect reporting dengan format menyerupai Jira, API testing menggunakan Postman untuk endpoint transfer dan QRIS, sampai validasi data di level database pakai SQL, dan ditutup dengan Test Summary Report untuk keputusan go/no-go. Untuk automation tools seperti Katalon atau Selenium, saya paham konsep dan alurnya dalam STLC, dan siap onboarding cepat kalau tim menggunakan tools tersebut."

Kalimat ini **aman** karena tidak mengklaim pengalaman production yang tidak kamu miliki, tapi tetap menunjukkan pemahaman menyeluruh + bukti konkret (project ini) yang bisa langsung kamu tunjukkan kalau diminta.

**Prinsip yang perlu terus dipegang:** jangan klaim pernah testing aplikasi mobile banking *production* kalau yang kamu punya adalah project simulasi/latihan seperti SigmaPay ini. Selalu jelas bedanya: *"saya latihan lewat project sendiri"* vs *"saya pernah kerjakan di production"* — interviewer berpengalaman biasanya menggali lebih dalam dan ketidakjujuran di titik ini gampang ketahuan.

---

*Catatan: beberapa gambar tangkapan layar Katalon yang kamu lampirkan berasal dari link sesi ChatGPT (`images.openai.com`) yang bersifat sementara/tidak persisten, jadi tidak saya sertakan di file ini — kalau butuh visual Katalon di portfolio, lebih baik pakai screenshot dari instalasi Katalon kamu sendiri saat benar-benar mencobanya.*
