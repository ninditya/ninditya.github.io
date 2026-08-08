# Test Summary Report — SigmaPay Mobile Banking (Fund Transfer & QRIS)

| Field | Detail |
|---|---|
| Project | SigmaPay Mobile Banking |
| Modul | Fund Transfer & QRIS Payment |
| Periode Testing | 03 – 08 Agustus 2026 |
| Build Final | v1.4.2-QA |
| Disusun oleh | QA Engineer |
| Status Dokumen | Final — untuk sign-off |

## 1. Ringkasan Eksekusi (Seluruh Cycle)

| Cycle | Fokus | Total TC | Pass | Fail | Pass Rate |
|---|---|---|---|---|---|
| Cycle 1 (SIT) | Functional + Negative + Edge Case | 30 | 24 | 6 | 80% |
| Cycle 2 (Retest + Regression) | Retest 6 defect + 12 TC regresi (Login, Saldo, Mutasi) | 18 | 17 | 1 | 94% |
| Cycle 3 (Final Regression) | Retest 1 sisa defect + smoke ulang | 3 | 3 | 0 | 100% |
| **Total Akhir** | | **51 eksekusi** | **44** | **7** (semua sudah closed) | **100% pada eksekusi terakhir** |

## 2. Status Defect Akhir

| Defect ID | Severity | Status Akhir | Catatan |
|---|---|---|---|
| BUG-SGP-001 | Critical | **Closed** | Idempotency key diimplementasikan, tervalidasi via SQL query #3 (tidak ada duplikasi) |
| BUG-SGP-002 | Critical | **Closed** | Mekanisme query status otomatis setelah timeout sudah berjalan |
| BUG-SGP-003 | Major | **Closed** | Auto-reversal job berjalan dalam SLA 15 menit |
| BUG-SGP-004 | Critical | **Closed** | Validasi expiry QR dipindah ke backend, tervalidasi via SQL query #6 |
| BUG-SGP-005 | Major | **Closed** | Validasi Merchant ID terhadap master data ditambahkan |
| BUG-SGP-006 | Minor | **Closed** | Validasi client-side untuk nominal negatif ditambahkan |
| BUG-SGP-007 *(ditemukan saat regresi Cycle 2)* | Minor | **Closed** | Riwayat mutasi salah urut tanggal setelah perubahan format tanggal — di luar scope awal, ditemukan dari regression testing |

## 3. Defect Density & Analisis

- Total defect ditemukan: **7** dari 2 modul utama (Transfer, QRIS) + 1 modul terdampak (Mutasi).
- **Critical: 3 (43%)** — seluruhnya terkait **integritas dana** (double debit, status ambigu, validasi expiry). Ini menegaskan pentingnya edge case testing di domain banking, bukan cuma happy path.
- **Major: 2 (29%)**, **Minor: 2 (28%)**.
- Modul **Transfer** menyumbang defect terbanyak (5 dari 7) — wajar karena kompleksitas alur (integrasi eksternal BI-FAST, validasi limit, concurrency).

## 4. Coverage

| Area | Status |
|---|---|
| Functional Testing (UI) | 100% test case dieksekusi |
| API Testing | Endpoint utama (`/transfer`, `/qris/pay`, `/transaction/status`) tervalidasi termasuk negative case & IDOR check |
| Database Validation | 10 query validasi dijalankan, seluruh temuan kritikal terbukti dari sisi data, bukan asumsi UI |
| Regression Testing | Modul Login, Cek Saldo, Riwayat Mutasi — 1 defect baru ditemukan & closed |
| SIT (integrasi BI-FAST & QRIS Switching) | Tervalidasi via sandbox, termasuk skenario timeout |
| UAT | Terjadwal setelah dokumen ini disetujui — di luar tanggung jawab langsung QA namun QA mendampingi |

## 5. Exit Criteria — Evaluasi

| Kriteria | Target | Aktual | Terpenuhi? |
|---|---|---|---|
| Test case dieksekusi | ≥ 95% | 100% | ✅ |
| Defect Critical open | 0 | 0 | ✅ |
| Defect Major open | 0 atau risk-accepted | 0 | ✅ |
| Test Summary Report disetujui | Ya | Menunggu sign-off | ⏳ |

## 6. Rekomendasi Go/No-Go

**Rekomendasi: GO** untuk lanjut ke tahap UAT dan rilis terbatas (soft launch), dengan catatan:

1. Monitoring ketat pada modul Transfer & QRIS di 2 minggu pertama pasca rilis (mengingat riwayat defect Critical di area ini).
2. Siapkan **rollback plan** khusus untuk skenario reversal BI-FAST, mengingat kompleksitas integrasi eksternal.
3. Regression suite yang sudah dibuat (lihat [Regression Checklist](../09-Regression-Checklist/Regression_Test_Checklist.md)) disarankan menjadi kandidat prioritas untuk **diotomasi** di sprint berikutnya (nice-to-have di job desc: Selenium/Katalon/Cypress/Playwright) agar regresi tidak lagi manual setiap rilis.

## 7. Lessons Learned

- Kasus **double debit** dan **status ambigu saat koneksi terputus** tidak akan ditemukan hanya dengan happy-path testing — memperkuat pentingnya **risk-based & edge-case testing** khususnya di domain finansial.
- Validasi di level **API dan Database**, bukan hanya UI, terbukti krusial untuk membuktikan root cause ke developer secara presisi (lihat BUG-SGP-004 dan BUG-SGP-005).
- Regression testing manual pada 3 cycle memakan waktu signifikan — kandidat kuat untuk automation di iterasi berikutnya.
