# Test Plan — SigmaPay Mobile Banking: Modul Fund Transfer & QRIS Payment

| Field | Detail |
|---|---|
| Dokumen | Test Plan |
| Versi | 1.0 |
| Project | SigmaPay Mobile Banking |
| Modul | Fund Transfer (Intrabank, Interbank/BI-FAST, Virtual Account) & QRIS Payment |
| Disusun oleh | QA Engineer |
| Sprint | Sprint 14 (Simulasi) |

## 1. Pendahuluan

Dokumen ini menjelaskan pendekatan pengujian untuk fitur **Fund Transfer** dan **QRIS Payment** pada aplikasi SigmaPay Mobile Banking, sebelum dirilis ke production.

## 2. Tujuan Testing

- Memastikan seluruh alur transfer dana (intrabank, interbank via BI-FAST, ke Virtual Account) berjalan sesuai requirement.
- Memastikan alur pembayaran QRIS (statis & dinamis) berjalan sesuai requirement, termasuk validasi merchant.
- Memastikan data transaksi konsisten antara **aplikasi (UI)**, **API/backend**, dan **database**.
- Memastikan tidak ada regresi pada fitur existing (login, saldo, mutasi) akibat perubahan di modul ini.

## 3. Scope

### In Scope
- Functional Testing: Transfer Intrabank, Transfer Interbank (BI-FAST), Transfer ke Virtual Account, QRIS Payment (scan & pay)
- Negative Testing: saldo tidak cukup, limit transaksi, input tidak valid, sesi timeout
- API Testing: endpoint `POST /transfer`, `POST /qris/pay`, `GET /transaction/status`
- Database Validation: mutasi saldo, log transaksi, status settlement
- Regression Testing: modul Login, Cek Saldo, Riwayat Mutasi
- SIT: integrasi ke simulator/sandbox BI-FAST & QRIS Switching
- Smoke Testing: setiap build baru masuk QA environment
- UAT Support: pendampingan business user saat UAT

### Out of Scope
- Performance/Load Testing (ditangani tim Performance terpisah)
- Security Penetration Testing (ditangani tim Security)
- Automation Testing (fase ini manual — automation candidate untuk regression suite di sprint berikutnya)

## 4. Test Strategy

| Jenis Testing | Kapan Dilakukan | Metode |
|---|---|---|
| Smoke Testing | Setiap build baru diterima QA | Manual, checklist 10 kasus kritikal |
| Functional Testing | Setelah smoke test lolos | Manual, mengacu ke Test Case |
| API Testing | Paralel dengan functional testing UI | Postman |
| Database Validation | Setelah transaksi dieksekusi | SQL query manual via DB client |
| SIT | Setelah functional testing modul selesai | Manual, environment terhubung sandbox eksternal |
| Regression Testing | Setelah bug fix / sebelum rilis | Manual, mengacu ke Regression Checklist |
| UAT | Setelah SIT selesai & defect kritikal closed | Business user, didampingi QA |

## 5. Entry Criteria

- Build sudah di-deploy ke QA environment tanpa error deployment.
- Smoke test 10 kasus kritikal **Pass**.
- Test Case sudah direview & disetujui.
- Test data (dummy account, dummy merchant QRIS) sudah tersedia.

## 6. Exit Criteria

- Minimal 95% test case telah dieksekusi.
- Tidak ada defect **Critical/Blocker** yang masih Open.
- Defect **Major** yang open sudah mendapat persetujuan risk acceptance dari Product Owner.
- Test Summary Report sudah disetujui QA Lead.

## 7. Test Environment

| Komponen | Detail |
|---|---|
| Aplikasi | SigmaPay Mobile (Android/iOS) versi QA build |
| API | `https://api-qa.sigmapay.dummy` (dummy) |
| Database | PostgreSQL — schema `sigmapay_qa` (dummy) |
| Sandbox eksternal | BI-FAST Simulator, QRIS Switching Simulator |
| Tools | JIRA (defect tracking), Postman (API testing), DBeaver (SQL client), Excel/Sheets (test case management) |
| Device | Min. 1 Android real device, 1 iOS real device/simulator |

## 8. Test Data

> Sinkron dengan [SigmaPay Prototype Scope](../SigmaPay%20Prototype%20Scope/SigmaPay%20QA%20Workbench.dc.html) — prototype interaktif yang mengimplementasikan persis data di bawah ini, sehingga jadi acuan tunggal (single source of truth) untuk seluruh dokumen di project ini.

### Akun Uji

| Akun | Nama | No. Rekening | Saldo | Bisa Login? | Catatan |
|---|---|---|---|---|---|
| User A | Andi Prasetyo | 8801 2345 6789 | Rp 5.000.000 | Ya | Akun utama untuk skenario transfer normal |
| User B | Budi Santoso | 8801 9988 7766 | Rp 1.000.000 | Tidak | Hanya sebagai rekening tujuan (penerima) |
| User C | Citra Dewi | 8801 5544 3322 | Rp 0 | Ya | Skenario saldo tidak cukup |
| User D | Dian Kusuma | 8801 1122 3344 | Rp 750.000 | Tidak (diblokir) | Skenario rekening tujuan tidak aktif/diblokir |

- **PIN** untuk semua akun uji: `123456` (6 digit). PIN salah ditolak (REG-02).
- **OTP** sandbox: `246810` (6 digit). Salah 3x → transaksi terkunci sementara ([TC-TRF-010](../03-Test-Case/Test_Case_Transfer_QRIS.csv)).
- **Batas idle sesi**: 5 menit → auto logout (REG-04).

### Bank Tujuan (BI-FAST)

| Nama Bank | Kode |
|---|---|
| Bank XYZ | 014 |
| Bank ABC | 008 |
| Bank Nusantara | 451 |

### Virtual Account

| Field | Nilai |
|---|---|
| Nomor VA valid | 88081234567890 |
| Penyedia | PLN Prabayar |
| Tagihan | Rp 250.000 |
| Biaya admin | Rp 0 |

### QR Uji QRIS

| Merchant | Jenis | Nominal | Kondisi |
|---|---|---|---|
| Kopi Kalibrata | Statis, NMID ID1023456789012 | Input manual | Valid |
| Toko Serba Ada | Dinamis | Rp 75.000 | Valid |
| Warung Sate Pak Har | Dinamis | Rp 45.000 | **Expired** (5 menit lalu) → [TC-QRIS-004](../03-Test-Case/Test_Case_Transfer_QRIS.csv) |
| Laundry Ekspress | Dinamis | Rp 120.000 | **Merchant ID mismatch** → [TC-QRIS-009](../03-Test-Case/Test_Case_Transfer_QRIS.csv) |
| QR tidak dikenali | - | - | Format rusak/bukan QRIS nasional → [TC-QRIS-005](../03-Test-Case/Test_Case_Transfer_QRIS.csv) |

### Biaya & Limit

| Item | Nilai |
|---|---|
| Biaya admin — Intrabank | Rp 1.000 |
| Biaya admin — BI-FAST (interbank) | Rp 2.500 |
| Biaya admin — Virtual Account | Rp 0 |
| Biaya admin — QRIS | Rp 0 |
| Limit transfer harian (akumulasi) | Rp 50.000.000 |
| Limit QRIS **per transaksi** (bukan akumulasi harian) | Rp 10.000.000 |

### Payload Uji Keamanan Dasar (field Berita Transfer)

| Payload | Kegunaan |
|---|---|
| `<script>alert(1)</script>` | Uji XSS — lihat [TC-TRF-020](../03-Test-Case/Test_Case_Transfer_QRIS.csv) |
| `' OR '1'='1` | Uji SQL Injection — lihat [TC-TRF-020](../03-Test-Case/Test_Case_Transfer_QRIS.csv) |

## 9. Roles & Responsibilities

| Role | Tanggung Jawab |
|---|---|
| QA Engineer | Design test case, eksekusi testing, log & retest defect, buat laporan |
| Developer | Fix defect, deploy build ke QA environment |
| Product Owner | Klarifikasi requirement, approve risk acceptance |
| Business User | UAT |

## 10. Risk & Mitigation

| Risiko | Dampak | Mitigasi |
|---|---|---|
| Sandbox BI-FAST/QRIS tidak stabil | SIT tertunda | Siapkan mock response sebagai fallback, koordinasi H-1 dengan tim eksternal |
| Requirement limit transaksi belum final | Test case salah asumsi | Freeze requirement sebelum test case design dimulai, minta sign-off BA |
| Waktu testing mepet (rilis ASAP) | Coverage tidak maksimal | Prioritaskan test case berdasarkan **risk-based testing** — modul uang keluar (debit) diprioritaskan dari modul kosmetik UI |

## 11. Deliverables

- Test Plan (dokumen ini)
- Test Scenario & Test Case
- Test Execution Report + Evidence
- Bug Report
- Test Summary Report
