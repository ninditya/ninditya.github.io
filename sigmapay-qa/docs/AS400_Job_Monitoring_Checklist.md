# AS400/IBM i Job Monitoring Checklist — SigmaPay Core Banking

Checklist untuk QA jalankan **setiap pagi setelah batch EOD selesai**, dan **setiap kali ada PTF/patch** di-apply ke library core banking. Mengikuti pola [09-Regression-Checklist](../09-Regression-Checklist/Regression_Test_Checklist.md) — ✅ Pass / ❌ Fail / ⏭️ Skip.

> Command AS400 di bawah ini dikutip dari dokumentasi publik IBM i (bukan hasil praktik langsung) — lihat catatan kejujuran di [AS400_Concepts_Primer.md §4](AS400_Concepts_Primer.md#4-status-kejujuran-mengikuti-pola-stlc_tools_mappingmd).

## 1. Status Job Batch EOD

| ID | Item | Command Referensi | Status |
|---|---|---|---|
| AS4-01 | Job `SGPEOD01` selesai tanpa *abnormal end* | `WRKACTJOB SBS(QBATCH)` | |
| AS4-02 | Job log tidak berisi pesan severity tinggi (CPF/MCH) | `WRKJOBLOG` / `DSPJOBLOG JOB(SGPEOD01)` | |
| AS4-03 | Tidak ada job dalam status `*MSGW` (menunggu respons manual) | `WRKACTJOB` — kolom Status | |
| AS4-04 | Job selesai dalam batas waktu SLA batch window (mis. sebelum jam 05:00) | Bandingkan `start_time`/`end_time` di `BATCH_CTL` ([Query #2](DB2_for_i_Validation_Queries.sql)) | |

## 2. Job Queue & Antrian

| ID | Item | Command Referensi | Status |
|---|---|---|---|
| AS4-05 | Job queue `QBATCH` tidak menumpuk/backlog | `WRKJOBQ QBATCH` | |
| AS4-06 | Tidak ada job yang di-*hold* tanpa alasan jelas | `WRKJOBQ` — kolom Status (`HLD`) | |

## 3. Output & Laporan

| ID | Item | Command Referensi | Status |
|---|---|---|---|
| AS4-07 | Spool file laporan EOD tersedia di output queue | `WRKOUTQ SGPEODRPT` | |
| AS4-08 | Isi laporan tidak kosong/corrupt, jumlah baris sesuai jumlah transaksi | Buka spool file + [Query #4](DB2_for_i_Validation_Queries.sql) untuk cross-check | |

## 4. Integritas Data Pasca-Batch

| ID | Item | Command Referensi | Status |
|---|---|---|---|
| AS4-09 | Batch untuk tanggal proses hari ini berstatus `COMPLETE`, hanya 1 kali (bukan rerun) | [Query #2 & #3](DB2_for_i_Validation_Queries.sql) — regresi BUG-SGP-008 | |
| AS4-10 | Tidak ada entri LEDGER dobel (accrual/reconciliation) | [Query #3](DB2_for_i_Validation_Queries.sql) | |
| AS4-11 | Saldo di `ACCOUNTS` cocok dengan tampilan aplikasi mobile | [Query #1](DB2_for_i_Validation_Queries.sql) vs UI Home | |
| AS4-12 | Tidak ada dua instance job batch dengan nama sama berstatus `RUNNING` bersamaan | [Query #7](DB2_for_i_Validation_Queries.sql) | |

## 5. Setelah PTF/Patch (tambahan, tidak rutin harian)

| ID | Item | Command Referensi | Status |
|---|---|---|---|
| AS4-13 | Smoke test fungsi dasar core banking (login, cek saldo, 1x transfer) tetap berjalan | Lihat [TC-AS400-008](AS400_Batch_Test_Cases.csv) | |
| AS4-14 | Versi PTF yang ter-apply sesuai rencana rilis (tidak ada PTF lain yang ikut ter-apply tanpa sepengetahuan QA) | `DSPPTF` (Display PTF) | |

## Ringkasan Hasil

| Total Item | Pass | Fail | Skip |
|---|---|---|---|
| 14 | | | |

**Keputusan:** Batch EOD dianggap sehat jika seluruh item section 1 dan 4 (AS4-01 s.d. AS4-04, AS4-09 s.d. AS4-12) **Pass**. Kegagalan pada item tersebut = **blocker** untuk membuka akses transaksi hari itu (channel bergantung pada saldo yang sudah final di-batch).
