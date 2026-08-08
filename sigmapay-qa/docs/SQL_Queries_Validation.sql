-- ============================================================
-- SQL Validation Queries — SigmaPay Mobile Banking (Dummy Schema)
-- Digunakan QA untuk memvalidasi data di level database setelah
-- eksekusi test case UI/API, bukan cuma percaya tampilan di layar.
--
-- Bagian A disinkronkan PERSIS dengan skema yang didemokan di tab
-- "SQL" pada SigmaPay Prototype Scope (SigmaPay QA Workbench.dc.html):
--   accounts(account_no, holder, balance)
--   transactions(trx_id, type, amount, status, created_at)
--   status yang benar-benar dipakai: SUCCESS, PENDING, REVERSED
--   (transaksi yang DITOLAK/GAGAL tidak pernah di-INSERT ke tabel
--   ini di prototype — hanya percobaan yang settle yang tercatat.
--   Ini catatan penting untuk audit trail perbankan, lihat §B.6)
--
-- Bagian B adalah skema lanjutan yang direkomendasikan untuk sistem
-- production sesungguhnya (di luar apa yang dimodelkan prototype
-- yang sengaja ringan) — dipakai untuk validasi yang lebih dalam.
-- ============================================================


-- ============================================================
-- BAGIAN A — Skema Inti (persis seperti tab SQL di prototype)
-- ============================================================

-- A.1 Cek saldo terkini akun tertentu — query identik dengan tab SQL prototype
SELECT account_no, holder, balance
FROM accounts
WHERE account_no = '8801 2345 6789'; -- Andi Prasetyo (User A)

-- A.2 Cek riwayat transaksi terbaru — query identik dengan tab SQL prototype
SELECT trx_id, type, amount, status, created_at
FROM transactions
ORDER BY created_at DESC;

-- A.3 Validasi TIDAK ADA duplikasi transaksi akibat double tap (BUG-SGP-001)
-- Prototype mendeteksi duplikat dengan kombinasi (type, amount, destination) — lihat dupResult di tab SQL
SELECT type, amount, destination_account, COUNT(*) AS jumlah_transaksi,
       array_agg(trx_id) AS trx_ids
FROM transactions
WHERE account_no = '8801 2345 6789'
  AND created_at >= NOW() - INTERVAL '5 minutes'
GROUP BY type, amount, destination_account
HAVING COUNT(*) > 1;
-- Build v1.4.0-QA (buggy) mereproduksi TC-TRF-015 → 1 baris duplikat muncul di sini.
-- Build v1.5.0-FIX → wajib 0 rows (idempotency key mencegah insert kedua).


-- ============================================================
-- BAGIAN B — Skema Lanjutan (rekomendasi untuk production,
-- melengkapi apa yang tidak dimodelkan di prototype ringan)
-- ============================================================

-- B.4 Rekonsiliasi status vs saldo aktual (BUG-SGP-002 — status "Gagal" di UI
-- padahal saldo sudah terdebit dan backend mencatat SUCCESS)
SELECT t.trx_id, t.status AS status_di_backend, a.balance AS saldo_terkini,
       t.amount, t.created_at
FROM transactions t
JOIN accounts a ON a.account_no = t.account_no
WHERE t.trx_id = :trx_id; -- ambil trx_id dari log API di tab "API" pada prototype

-- B.5 Cari transaksi PENDING yang belum di-REVERSED melewati SLA (BUG-SGP-003)
SELECT trx_id, type, amount, status, created_at,
       NOW() - created_at AS durasi_pending
FROM transactions
WHERE status = 'PENDING'
  AND created_at < NOW() - INTERVAL '15 minutes'
ORDER BY created_at ASC;
-- Build v1.5.0-FIX: 0 rows (scheduler auto-reversal mengubah status jadi REVERSED setelah SLA).
-- Build v1.4.0-QA: baris tetap PENDING tanpa batas waktu — reproduksi lewat kondisi jaringan
-- "Switching BI-FAST timeout" di panel kiri prototype.

-- B.6 Validasi tidak ada transaksi QRIS SUCCESS yang dibayar setelah QR expired (BUG-SGP-004)
-- CATATAN SKEMA: prototype saat ini TIDAK menyimpan qr_expiry_time/paid_at di tabel transactions —
-- ini gap skema nyata yang perlu ditambahkan sebagai bagian dari fix BUG-SGP-004, bukan cuma
-- perbaikan di kode aplikasi. Query ini mengasumsikan kolom tersebut sudah ditambahkan:
SELECT trx_id, type, amount, status, paid_at, qr_expiry_time
FROM transactions
WHERE type LIKE 'QRIS%'
  AND status = 'SUCCESS'
  AND paid_at > qr_expiry_time;
-- Expected setelah fix: 0 rows

-- B.7 Validasi kecocokan Merchant ID QR vs Master Merchant (BUG-SGP-005)
-- CATATAN SKEMA: butuh tabel `merchants` terpisah (belum ada di skema minimal prototype)
SELECT t.trx_id, t.merchant_id AS merchant_id_di_qr,
       m.merchant_id AS merchant_id_terdaftar, m.merchant_name
FROM transactions t
LEFT JOIN merchants m ON m.merchant_id = t.merchant_id
WHERE t.type LIKE 'QRIS%'
  AND m.merchant_id IS NULL;
-- Jika ada row hasil: berarti ada transaksi tersettle ke Merchant ID yang TIDAK terdaftar

-- B.8 Validasi jurnal double-entry (debit = kredit) — sanity check akuntansi dasar
-- Prototype memakai heuristik sederhana (ledgerResult: "ada PENDING = tidak seimbang");
-- versi production sesungguhnya butuh tabel ledger_entries double-entry seperti ini:
SELECT trx_id,
       SUM(CASE WHEN entry_type = 'DEBIT' THEN amount ELSE 0 END) AS total_debit,
       SUM(CASE WHEN entry_type = 'CREDIT' THEN amount ELSE 0 END) AS total_credit
FROM ledger_entries
WHERE trx_id = :trx_id
GROUP BY trx_id
HAVING SUM(CASE WHEN entry_type = 'DEBIT' THEN amount ELSE 0 END)
     <> SUM(CASE WHEN entry_type = 'CREDIT' THEN amount ELSE 0 END);
-- Expected: 0 rows (jika ada row = data tidak balance, red flag serius)

-- B.9 Cek log audit trail untuk setiap percobaan OTP gagal (TC-TRF-010)
-- CATATAN SKEMA: butuh tabel auth_attempt_logs terpisah — penting untuk kepatuhan audit perbankan,
-- apalagi mengingat prototype MEMBUKTIKAN bahwa transaksi yang gagal/ditolak tidak pernah
-- masuk ke tabel `transactions` sama sekali (lihat catatan header file ini). Percobaan OTP gagal
-- WAJIB tetap tercatat di tabel audit terpisah meski transaksinya sendiri tidak pernah terjadi.
SELECT account_no, attempt_type, is_success, attempted_at
FROM auth_attempt_logs
WHERE account_no = '8801 2345 6789'
  AND attempt_type = 'OTP'
ORDER BY attempted_at DESC
LIMIT 5;

-- B.10 Validasi data sensitif tidak tersimpan dalam bentuk plain text
-- (sanity check keamanan dasar yang wajib QA cek meski bukan pentest formal)
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'accounts'
  AND column_name IN ('pin', 'password', 'otp_code');
-- Pastikan kolom sensitif ini disimpan ter-hash/ter-enkripsi di level aplikasi,
-- bukan hanya mengandalkan nama kolom untuk menilai — cross-check dengan tim dev.
