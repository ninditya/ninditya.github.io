# Konsep SDLC & STLC — Dipetakan ke Project SauceDemo (Login & Checkout Automation)

## 0. Konteks Project Ini (Beda dari Simulasi Biasa)

SauceDemo (https://www.saucedemo.com/) adalah situs demo publik yang **sudah jadi** — bukan
aplikasi yang sedang kita kembangkan dari nol. Jadi mapping SDLC di bawah ini sedikit berbeda
dari studi kasus simulasi pada umumnya:

- **Requirement tidak datang dari BRD/User Story resmi** — direkonstruksi lewat eksplorasi
  aplikasi langsung (reverse requirement). Ini justru skenario yang **sangat umum di dunia
  nyata**: testing sistem vendor/legacy/pihak ketiga tanpa dokumentasi lengkap.
- **"Development" di project ini bukan development SauceDemo**, melainkan development
  **test automation suite**-nya — kode Playwright/Cypress/Selenium di
  [`automation/playwright/`](../../automation/playwright), [`automation/cypress/`](../../automation/cypress), dan [`automation/selenium/`](../../automation/selenium).
- Semua hasil eksekusi di dokumen ini adalah **hasil run sungguhan**, bukan simulasi/asumsi —
  termasuk temuan bahwa 3 dari 7 bug bawaan yang tercatat di
  [`05-Bug-Report/Bug_Report_SauceDemo.md`](../05-Bug-Report/Bug_Report_SauceDemo.md) ternyata **sudah tidak reproduksi lagi** per
  2026-08-10, ditemukan lewat regression run yang benar-benar dijalankan.

## 1. SDLC (Software Development Life Cycle)

| # | Fase SDLC | Yang Terjadi (Umum) | Peran QA di Project Ini (Studi Kasus SauceDemo) |
|---|---|---|---|
| 1 | **Requirement Analysis** | BA/PO mengumpulkan kebutuhan bisnis | Tidak ada BA — QA (saya) mengeksplorasi aplikasi langsung: cek halaman login (6 akun uji beda perilaku), alur cart, sort, dan checkout 3 langkah, lalu menuliskan hasilnya sebagai requirement di [Test Plan](../01-Test-Plan/Test_Plan_SauceDemo.md) §1-2 |
| 2 | **Design (System & UI/UX)** | Tim membuat wireframe, API contract, skema database | Tidak ada design doc resmi (aplikasi pihak ketiga). QA cukup mengamati desain yang sudah ada: field error state (`[data-test="error"]`), pesan error spesifik per skenario, struktur URL per langkah checkout — semua dicatat sebagai referensi selector di kode test |
| 3 | **Development (Coding)** | Developer coding fitur | Untuk project ini, "development" = menulis **test automation** di 3 framework paralel: [`automation/playwright/tests/`](../../automation/playwright/tests) (Playwright/TypeScript), [`automation/cypress/e2e/`](../../automation/cypress/e2e) (Cypress/TypeScript), [`automation/selenium/tests/`](../../automation/selenium/tests) (Selenium/Python) |
| 4 | **Testing** | Build masuk ke QA environment | Suite dijalankan langsung ke situs live `https://www.saucedemo.com/`. Hasil nyata: **Playwright 26/29 lulus**, **Cypress 23/26 lulus** (3 test terbaru menyusul), **Selenium 7/7 lulus** (3 "kegagalan" Playwright/Cypress memang disengaja — itu adalah pengecekan bug bawaan yang seharusnya gagal, lihat §4 di bawah) |
| 5 | **Deployment/Release** | Fitur naik ke production lewat CI/CD | Tidak ada deployment aplikasi (SauceDemo sudah live). Yang "di-deploy" di sini adalah **pipeline CI**-nya sendiri: [`.github/workflows/ci.yml`](../../.github/workflows/ci.yml) menjalankan Playwright + Cypress + Selenium otomatis di setiap push/PR ke `main` |
| 6 | **Maintenance** | Ada bug report, ada fitur tambahan | Regression run berkala jadi cara **memantau drift** — bukan cuma nunggu bug baru. Bukti konkret: saat suite dijalankan ulang, ternyata BUG-004, BUG-006, dan BUG-007 (yang sebelumnya tercatat aktif) **sudah tidak reproduksi**, sementara BUG-001, BUG-003, BUG-005 masih. Ini didokumentasikan dengan tanggal di [`05-Bug-Report/Bug_Report_SauceDemo.md`](../05-Bug-Report/Bug_Report_SauceDemo.md) |

**Model pengembangan yang relevan:** Karena tidak ada sprint/rilis fitur baru (target ujinya
statis), siklus yang relevan di sini adalah **regression cycle** — STLC di bawah berulang setiap
kali suite dijalankan ulang (manual atau lewat CI), bukan per sprint pengembangan fitur.

---

## 2. STLC (Software Testing Life Cycle)

| # | Fase STLC | Aktivitas di Project Ini | Entry Criteria | Exit Criteria | Deliverable (Nyata, Bisa Dibuka) |
|---|---|---|---|---|---|
| 1 | **Requirement Analysis** | Eksplorasi SauceDemo: 6 akun uji (`standard_user`, `locked_out_user`, `problem_user`, `performance_glitch_user`, `error_user`, `visual_user`), alur login, cart, sort, checkout 3 langkah | Akses ke `https://www.saucedemo.com/` | Fitur & scope teridentifikasi, in-scope vs out-of-scope jelas | [Test Plan §1-4](../01-Test-Plan/Test_Plan_SauceDemo.md) |
| 2 | **Test Planning** | Tentukan scope, pendekatan (3 framework automation), environment, exit criteria | Requirement teridentifikasi | Test Plan lengkap | [`01-Test-Plan/Test_Plan_SauceDemo.md`](../01-Test-Plan/Test_Plan_SauceDemo.md) |
| 3 | **Test Case Design** | Breakdown jadi test case per area (Login, Cart, Sort, Checkout, Known Issues/bug bawaan), termasuk negative case & edge case, langsung diimplementasikan sebagai kode | Test Plan siap | Test case terdokumentasi & terimplementasi di kode | [`03-Test-Case/Test_Case_SauceDemo.csv`](../03-Test-Case/Test_Case_SauceDemo.csv) (27 test case) + spec di [`automation/playwright/tests/`](../../automation/playwright/tests), [`automation/cypress/e2e/`](../../automation/cypress/e2e), [`automation/selenium/tests/`](../../automation/selenium/tests) |
| 4 | **Test Environment Setup** | Setup 3 runner automation (browser, dependency, config, env var) | Test case siap ditulis | Environment bisa menjalankan suite | [`automation/playwright/playwright.config.ts`](../../automation/playwright/playwright.config.ts), [`automation/cypress/cypress.config.ts`](../../automation/cypress/cypress.config.ts), [`automation/selenium/requirements.txt`](../../automation/selenium/requirements.txt), [`.env.example`](../../.env.example) |
| 5 | **Test Execution** | Jalankan suite, catat Pass/Fail nyata, verifikasi ulang status bug bawaan dengan tanggal | Environment siap | Suite tereksekusi, hasil tercatat | Hasil run nyata (lihat §1 tabel SDLC baris 4) + [`05-Bug-Report/Bug_Report_SauceDemo.md`](../05-Bug-Report/Bug_Report_SauceDemo.md) (status reproduksi per bug + tanggal verifikasi) |
| 6 | **Test Cycle Closure** | Evaluasi coverage & status defect | Eksekusi selesai | — | **Belum ada dokumen closure formal terpisah** (mis. Test Summary Report dengan rekomendasi go/no-go). Ringkasan status paling dekat saat ini ada di bagian atas [`05-Bug-Report/Bug_Report_SauceDemo.md`](../05-Bug-Report/Bug_Report_SauceDemo.md). Ini gap yang jujur diakui — kandidat pengembangan lanjutan project |

> Kenapa baris ke-6 ditandai "belum ada", bukan dibuat-buat: SauceDemo bukan project rilis
> berkelanjutan yang butuh keputusan go/no-go bisnis, jadi Test Summary Report formal memang
> belum krusial di sini — beda dengan studi kasus simulasi rilis produk. Kalau butuh, ini gampang
> ditambahkan sebagai file baru di folder ini.

---

## 3. Alur Visual (SDLC ⟷ STLC)

```
SDLC:  Requirement → Design → Dev (tulis automation) → Testing ──────→ CI (tiap push) → Maintenance
                                                          │                                  │
STLC:                          Req. Analysis → Test Planning → Test Case Design →           │
                                Test Env Setup → Test Execution → Test Cycle Closure          │
                                                    │                                         │
                                        (regression run berulang) ◄───────────────────────────┘
```

---

## 4. Level Testing yang Relevan dengan Project Ini

| Level | Berlaku di Project Ini? | Alasan / Contoh |
|---|---|---|
| **Unit Testing** | ❌ Tidak berlaku | SauceDemo bukan kode kita — tidak ada akses ke unit/function internalnya |
| **Integration Testing (SIT)** | ❌ Tidak berlaku | SauceDemo adalah aplikasi client-side monolitik demo, tidak ada modul/sistem eksternal terpisah untuk diintegrasikan (lihat "Out of Scope" di [Test Plan §4](../01-Test-Plan/Test_Plan_SauceDemo.md)) |
| **System / E2E Testing** | ✅ Ini level utama project ini | Seluruh alur diuji end-to-end lewat browser sungguhan: login → cart → sort → checkout, di 3 framework automation |
| **Regression Testing** | ✅ Inti dari project ini | Setiap kali suite dijalankan ulang, otomatis jadi regression check — termasuk terhadap 7 bug bawaan di `known-issues.spec.ts` / `known-issues.cy.ts` |
| **UAT (User Acceptance Testing)** | ⚠️ Mirip secara konsep | Tidak ada "user bisnis" sungguhan, tapi `known-issues.spec.ts`/`.cy.ts` berfungsi seperti acceptance check: memverifikasi perilaku yang "seharusnya benar" dari sudut pandang pengguna, dan sengaja gagal kalau aplikasi tidak memenuhi itu |

**Poin penting:** project ini secara jujur **sempit tapi dalam** di level System/Regression
Testing dengan automation lintas 3 tool, dibanding project simulasi manual testing yang lebih
luas cakupan levelnya (unit s.d. UAT) tapi eksekusinya manual. Dua jenis project ini saling
melengkapi kalau ditunjukkan bersamaan saat interview — satu membuktikan kemampuan manual/STLC
penuh, satu lagi membuktikan kemampuan automation lintas tool yang benar-benar jalan.
