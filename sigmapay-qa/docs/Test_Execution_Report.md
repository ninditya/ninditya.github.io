# Test Execution Report — Cycle 1 (SIT)

| Field | Detail |
|---|---|
| Project | SigmaPay Mobile Banking |
| Modul | Fund Transfer & QRIS Payment |
| Build | v1.4.0-QA |
| Tanggal Eksekusi | 03 – 05 Agustus 2026 |
| Environment | QA (api-qa.sigmapay.dummy) |
| Executor | QA Engineer |

## 1. Ringkasan Eksekusi

| Total TC | Passed | Failed | Blocked | Not Executed | Pass Rate |
|---|---|---|---|---|---|
| 30 | 24 | 6 | 0 | 0 | 80% |

> Catatan: Pass rate 80% pada Cycle 1 masih di bawah exit criteria (95%). Diperlukan **Cycle 2 (Retest)** setelah 6 defect di bawah ini diperbaiki developer.

## 2. Smoke Test (Pre-condition sebelum Cycle 1)

| Item | Status |
|---|---|
| Login berhasil | Pass |
| Menu Transfer dapat diakses | Pass |
| Menu Scan QRIS dapat diakses | Pass |
| Saldo tampil dengan benar | Pass |
| Riwayat mutasi dapat diakses | Pass |

Smoke test **Pass** → build dilanjutkan ke Functional Testing.

## 3. Hasil Eksekusi per Test Case

| Test Case ID | Judul Singkat | Status | Defect Terkait | Evidence |
|---|---|---|---|---|
| TC-TRF-001 | Transfer intrabank saldo cukup | Pass | - | evidence/TC-TRF-001.png |
| TC-TRF-002 | Transfer interbank BI-FAST | Pass | - | evidence/TC-TRF-002.png |
| TC-TRF-003 | Transfer ke Virtual Account | Pass | - | evidence/TC-TRF-003.png |
| TC-TRF-004 | Rincian biaya admin tampil | Pass | - | evidence/TC-TRF-004.png |
| TC-TRF-005 | Notifikasi & e-receipt | Pass | - | evidence/TC-TRF-005.png |
| TC-TRF-006 | Saldo tidak cukup ditolak | Pass | - | evidence/TC-TRF-006.png |
| TC-TRF-007 | Melebihi limit harian ditolak | Pass | - | evidence/TC-TRF-007.png |
| TC-TRF-008 | Rekening tujuan tidak valid | Pass | - | evidence/TC-TRF-008.png |
| TC-TRF-009 | Rekening tujuan diblokir | Pass | - | evidence/TC-TRF-009.png |
| TC-TRF-010 | OTP salah 3x terkunci | Pass | - | evidence/TC-TRF-010.png |
| TC-TRF-011 | Sesi timeout saat konfirmasi | Pass | - | evidence/TC-TRF-011.png |
| TC-TRF-012 | Validasi nominal negatif/nol | **Fail** | BUG-SGP-006 | evidence/TC-TRF-012.png |
| TC-TRF-013 | Validasi nominal non-numerik | Pass | - | evidence/TC-TRF-013.png |
| TC-TRF-014 | Transfer ke rekening sendiri | Pass | - | evidence/TC-TRF-014.png |
| TC-TRF-015 | Cegah double debit | **Fail** | BUG-SGP-001 | evidence/TC-TRF-015.png |
| TC-TRF-016 | Status ambigu saat koneksi putus | **Fail** | BUG-SGP-002 | evidence/TC-TRF-016.png |
| TC-TRF-017 | Reversal otomatis timeout BI-FAST | **Fail** | BUG-SGP-003 | evidence/TC-TRF-017.png |
| TC-TRF-018 | Boundary waktu cut-off limit | Pass | - | evidence/TC-TRF-018.png |
| TC-TRF-019 | Validasi nominal ekstrem besar | Pass | - | evidence/TC-TRF-019.png |
| TC-TRF-020 | Input berbahaya field catatan | Pass | - | evidence/TC-TRF-020.png |
| TC-QRIS-001 | Bayar QRIS statis | Pass | - | evidence/TC-QRIS-001.png |
| TC-QRIS-002 | Bayar QRIS dinamis | Pass | - | evidence/TC-QRIS-002.png |
| TC-QRIS-003 | Status sukses konsisten | Pass | - | evidence/TC-QRIS-003.png |
| TC-QRIS-004 | QR expired ditolak | **Fail** | BUG-SGP-004 | evidence/TC-QRIS-004.png |
| TC-QRIS-005 | QR rusak ditolak | Pass | - | evidence/TC-QRIS-005.png |
| TC-QRIS-006 | Saldo tidak cukup ditolak | Pass | - | evidence/TC-QRIS-006.png |
| TC-QRIS-007 | Melebihi limit QRIS harian | Pass | - | evidence/TC-QRIS-007.png |
| TC-QRIS-008 | Saldo aman jika app ditutup paksa | Pass | - | evidence/TC-QRIS-008.png |
| TC-QRIS-009 | Validasi Merchant ID saat settlement | **Fail** | BUG-SGP-005 | evidence/TC-QRIS-009.png |
| TC-QRIS-010 | Concurrent payment QR sama | Pass | - | evidence/TC-QRIS-010.png |

> Folder `evidence/` bersifat placeholder — pada praktik nyata berisi screenshot/screen-recording/log request-response sebagai bukti eksekusi (test evidence) yang dilampirkan ke tiket JIRA & laporan.

## 4. Defect Summary (Ringkas — detail di [05-Bug-Report](../05-Bug-Report/Bug_Report_Sample.md))

| Defect ID | Severity | Modul | Status |
|---|---|---|---|
| BUG-SGP-001 | Critical | Transfer | Open |
| BUG-SGP-002 | Critical | Transfer | Open |
| BUG-SGP-003 | Major | Transfer | Open |
| BUG-SGP-004 | Critical | QRIS | Open |
| BUG-SGP-005 | Major | QRIS | Open |
| BUG-SGP-006 | Minor | Transfer | Open |

## 5. Rekomendasi

- **Blocker untuk rilis**: BUG-SGP-001, 002, 004 (Critical, berhubungan langsung dengan integritas dana nasabah) — wajib fix sebelum lanjut ke UAT.
- BUG-SGP-003 & 005 (Major) — disarankan fix sebelum rilis, atau minimal mitigasi + monitoring manual di production.
- BUG-SGP-006 (Minor) — dapat masuk backlog rilis berikutnya jika disetujui Product Owner (risk acceptance), tidak memblok rilis.
- Setelah fix, lanjutkan ke **Cycle 2: Retest defect + Regression Test** (lihat [Regression Checklist](../09-Regression-Checklist/Regression_Test_Checklist.md)).
