# Konsep SDLC & STLC — Dipetakan ke Studi Kasus "SigmaPay" (Transfer & QRIS)

## 1. SDLC (Software Development Life Cycle)

SDLC adalah siklus hidup **pengembangan** software secara keseluruhan (dev, QA, business, ops terlibat semua). QA punya peran di **setiap** fase, bukan cuma pas testing.

| # | Fase SDLC | Yang Terjadi | Peran QA di Fase Ini (Studi Kasus SigmaPay) |
|---|---|---|---|
| 1 | **Requirement Analysis** | BA/PO mengumpulkan kebutuhan bisnis: "User bisa transfer antar bank via BI-FAST" & "User bisa bayar merchant via scan QRIS" | QA review BRD/User Story, cari requirement yang ambigu (misal: "limit transfer harian" — berapa nominalnya? beda per tier user?). Ajukan pertanyaan sebelum development mulai (**shift-left testing**) |
| 2 | **Design (System & UI/UX)** | Tim membuat wireframe, API contract (Swagger/OpenAPI), skema database | QA review design: apakah error state sudah didesain (saldo kurang, QR expired, koneksi timeout)? Mulai siapkan **Test Plan** & **Traceability Matrix** dari sini |
| 3 | **Development (Coding)** | Developer coding fitur transfer & QRIS, termasuk unit test | QA mulai menulis **Test Scenario & Test Case** secara paralel (tidak menunggu development selesai 100%). Setup **test environment** & **test data** |
| 4 | **Testing** | Build pertama masuk ke QA environment | QA melakukan **Smoke Test** → **Functional Test** → **SIT (System Integration Testing)** → regresi → serahkan ke user untuk **UAT** |
| 5 | **Deployment/Release** | Fitur transfer & QRIS naik ke production (biasanya lewat CI/CD, dengan approval) | QA melakukan **smoke test di production** (post-deployment verification) — pastikan transaksi real (nominal kecil) berhasil end-to-end |
| 6 | **Maintenance** | Fitur sudah live, ada bug report dari user, ada fitur tambahan (misal: QRIS cross-border) | QA menangani **regression testing** setiap ada hotfix, serta **monitoring defect trend** dari production |

**Model pengembangan yang relevan:** Karena kedua loker menyebut "Agile/Scrum", asumsikan SDLC berjalan dalam **sprint 2 minggu**, di mana STLC di bawah ini terjadi **berulang setiap sprint**, bukan cuma sekali di akhir project (waterfall).

---

## 2. STLC (Software Testing Life Cycle)

STLC adalah siklus kerja **QA secara spesifik**, biasanya berjalan paralel/nested di dalam fase "Testing" pada SDLC (dan idealnya dimulai sejak fase Requirement).

| # | Fase STLC | Aktivitas | Entry Criteria | Exit Criteria | Deliverable |
|---|---|---|---|---|---|
| 1 | **Requirement Analysis** | QA pelajari User Story: *"Sebagai nasabah, saya ingin transfer ke bank lain via BI-FAST agar dana diterima real-time"* dan *"Sebagai nasabah, saya ingin bayar merchant dengan scan QRIS"*. Identifikasi **testable requirement** vs requirement yang tidak jelas | Requirement/User Story tersedia (walau belum final) | Requirement Traceability Matrix (RTM) awal selesai, semua open question sudah dijawab BA | RTM, daftar clarification question |
| 2 | **Test Planning** | Tentukan scope, strategy, jenis testing (functional, API, SIT, regression), tools, effort estimation, resource, risk | RTM tersedia | Test Plan disetujui Lead/PM | **Test Plan** ([lihat](../01-Test-Plan/Test_Plan_MobileBanking.md)) |
| 3 | **Test Case Design** | Breakdown requirement jadi **Test Scenario** → detail jadi **Test Case** (step, data, expected result), termasuk kasus negatif & edge case | Test Plan disetujui | Test case sudah direview & disetujui | **Test Scenario** & **Test Case** ([lihat](../02-Test-Scenario/Test_Scenario_Transfer_QRIS.md), [lihat](../03-Test-Case/Test_Case_Transfer_QRIS.csv)) |
| 4 | **Test Environment Setup** | Siapkan environment SIT/UAT, dummy account dengan berbagai kondisi saldo, koneksi ke sandbox BI-FAST/QRIS switching, tools (Postman collection, SQL client, JIRA project) | Environment checklist siap | Smoke test environment lolos | Environment ready + smoke test checklist |
| 5 | **Test Execution** | Jalankan test case satu per satu, catat Pass/Fail, ambil **evidence** (screenshot/log), log bug ke JIRA untuk yang Fail, lakukan **retest** setelah fix, lalu **regression test** | Environment siap, build sudah smoke-test | Semua test case dieksekusi, defect kritikal sudah closed/mitigated | **Execution Report**, **Bug Report** ([lihat](../04-Test-Execution/Test_Execution_Report.md), [lihat](../05-Bug-Report/Bug_Report_Sample.md)) |
| 6 | **Test Cycle Closure** | Evaluasi hasil testing: coverage, defect density, defect yang masih open (risk acceptance), keputusan go/no-go | Eksekusi selesai | Sign-off dari QA Lead/stakeholder | **Test Summary Report** ([lihat](../08-Test-Summary-Report/Test_Summary_Report.md)) |

---

## 3. Alur Visual (SDLC ⟷ STLC)

```
SDLC:  Requirement → Design → Development → Testing ─────────────→ Deployment → Maintenance
                                              │
STLC:                          Req. Analysis → Test Planning → Test Case Design →
                                Test Env Setup → Test Execution → Test Cycle Closure
                                                    │
                                        (loop tiap sprint / tiap regression)
```

**Poin penting untuk interview:** SDLC = payung besar seluruh project. STLC = zoom-in ke proses kerja QA. Kandidat yang cuma bisa jawab "STLC itu test planning, design, execution, closure" tanpa bisa mengaitkan ke SDLC & konteks bisnis biasanya dianggap junior. Level 3-5 tahun diharapkan bisa cerita **trade-off**: misal kenapa smoke test dilakukan sebelum functional test, atau kenapa regression test wajib sebelum UAT sign-off.

---

## 4. Level Testing yang Relevan dengan Loker

| Level | Siapa yang Uji | Tujuan | Contoh di SigmaPay |
|---|---|---|---|
| **Unit Testing** | Developer | Validasi fungsi/method individual | Fungsi hitung biaya admin BI-FAST |
| **SIT (System Integration Testing)** | QA | Validasi integrasi antar modul/sistem — termasuk ke switching QRIS & BI-FAST eksternal | Transfer dari SigmaPay → core banking → BI-FAST switching → bank tujuan |
| **Functional Testing** | QA | Validasi fitur sesuai requirement | Form transfer menerima input benar, menolak input salah |
| **Regression Testing** | QA | Pastikan fitur lama tidak rusak setelah ada perubahan | Setelah fix bug QRIS, pastikan fitur transfer & mutasi tetap normal |
| **Smoke Testing** | QA | Cek cepat build baru "layak diuji lebih lanjut" atau tidak | Setelah deploy build baru, cek: bisa login, bisa buka menu transfer, bisa scan QR |
| **UAT (User Acceptance Testing)** | User/Business (didampingi QA) | Validasi dari sudut pandang bisnis/user akhir | Business banking memverifikasi flow transfer sesuai kebutuhan nasabah |
