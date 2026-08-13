-- ============================================================
-- DB2 for i Validation Queries — SigmaPay Core Banking (AS400/IBM i)
-- Ditulis dengan gaya sintaks DB2 for i (qualified library.table,
-- dijalankan via STRSQL/ACS "Run SQL Scripts"), MELENGKAPI
-- 07-SQL-Validation/SQL_Queries_Validation.sql (skema Postgres,
-- lapisan channel/API) dengan lapisan core banking di AS400.
--
-- CATATAN JUJUR: query di file ini belum pernah dijalankan di
-- AS400/DB2 for i sungguhan — ditulis berdasarkan dokumentasi
-- publik sintaks DB2 for i untuk kebutuhan portfolio. Skema
-- (SIGMAPRD.ACCOUNTS, SIGMAPRD.LEDGER, SIGMAPRD.BATCH_CTL) adalah
-- desain dummy yang konsisten dengan narasi arsitektur di
-- 01-Test-Plan/Test_Plan_MobileBanking.md, bukan skema production.
-- ============================================================


-- ============================================================
-- 1. Cek saldo akun langsung dari core banking (bandingkan
--    dengan tampilan aplikasi setelah batch EOD selesai)
-- ============================================================
SELECT account_no, holder, balance, last_batch_date
FROM SIGMAPRD.ACCOUNTS
WHERE account_no = '8801 2345 6789'; -- Andi Prasetyo (User A)
-- Catatan sintaks DB2 for i: qualifikasi library.table (SIGMAPRD.ACCOUNTS)
-- dipakai eksplisit di sini; alternatifnya pakai *LIBL (library list)
-- kalau SIGMAPRD sudah ada di library list koneksi STRSQL.


-- ============================================================
-- 2. Cek status batch job EOD untuk tanggal proses tertentu
--    (dipakai TC-AS400-001, TC-AS400-003)
-- ============================================================
SELECT job_name, process_date, status, start_time, end_time
FROM SIGMAPRD.BATCH_CTL
WHERE job_name = 'SGPEOD01'
  AND process_date = CURRENT DATE;
-- status: 'C' = COMPLETE, 'R' = RUNNING, 'E' = ERROR
-- Expected setelah EOD normal: tepat 1 baris, status = 'C'


-- ============================================================
-- 3. Deteksi batch rerun yang menyebabkan entri LEDGER dobel
--    (BUG-SGP-008 — reproduksi query, lihat 05-Bug-Report)
-- ============================================================
SELECT account_no, entry_type, amount, process_date,
       COUNT(*) AS jumlah_entri
FROM SIGMAPRD.LEDGER
WHERE process_date = CURRENT DATE
  AND entry_type = 'INTEREST_ACCRUAL'
GROUP BY account_no, entry_type, amount, process_date
HAVING COUNT(*) > 1;
-- Expected: 0 rows. Kalau BUG-SGP-008 terjadi (job di-rerun tanpa
-- guard clause), akan muncul baris dengan jumlah_entri = 2.


-- ============================================================
-- 4. Rekonsiliasi total transaksi harian: channel API vs core banking
--    (dipakai TC-AS400-002, TC-AS400-010)
-- ============================================================
SELECT COUNT(*) AS total_transaksi_ledger
FROM SIGMAPRD.LEDGER
WHERE process_date = CURRENT DATE;
-- Bandingkan manual dengan jumlah transaksi dari log API middleware
-- (lihat 06-API-Testing/Postman_API_Test_Notes.md) — harus sama persis.


-- ============================================================
-- 5. Cek transaksi yang masuk mendekati cut-off time masuk ke
--    batch tanggal yang benar (dipakai TC-AS400-004)
-- ============================================================
SELECT trx_id, account_no, amount, submitted_at, process_date
FROM SIGMAPRD.LEDGER
WHERE submitted_at BETWEEN
      TIMESTAMP(CURRENT DATE, TIME('22:55:00')) AND
      TIMESTAMP(CURRENT DATE + 1 DAY, TIME('00:05:00'))
ORDER BY submitted_at;
-- Cek manual: transaksi submitted_at < cut-off (23:00) harus
-- punya process_date = hari yang sama; setelah cut-off = H+1.


-- ============================================================
-- 6. Validasi journaling/audit trail perubahan tabel ACCOUNTS
--    (konsep DB2 for i: journal receiver mencatat setiap perubahan)
-- ============================================================
-- CATATAN KONSEP (belum dipraktikkan): DB2 for i mendukung "journaling"
-- (perintah CL: STRJRNPF) yang mencatat setiap perubahan row ke journal
-- receiver, dipakai untuk audit trail & recovery. Query di bawah ini
-- mengasumsikan kolom ROW CHANGE TIMESTAMP aktif di tabel ACCOUNTS
-- (fitur DB2 for i untuk melacak kapan sebuah baris terakhir berubah):
SELECT account_no, balance, ROW CHANGE TIMESTAMP AS last_changed
FROM SIGMAPRD.ACCOUNTS
WHERE account_no = '8801 2345 6789'
  AND ROW CHANGE TIMESTAMP > CURRENT TIMESTAMP - 1 DAY;
-- Berguna untuk memastikan hanya batch job resmi yang mengubah
-- saldo dalam 24 jam terakhir, bukan proses lain yang tidak terduga.


-- ============================================================
-- 7. Sanity check: tidak ada job batch yang overlap (dua job
--    dengan job_name sama berstatus RUNNING bersamaan)
-- ============================================================
SELECT job_name, COUNT(*) AS jumlah_running
FROM SIGMAPRD.BATCH_CTL
WHERE status = 'R'
GROUP BY job_name
HAVING COUNT(*) > 1;
-- Expected: 0 rows. Kalau ada baris, berarti ada risiko race condition
-- dua instance job batch berjalan bersamaan terhadap tabel yang sama.
