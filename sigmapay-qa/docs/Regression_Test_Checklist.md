# Regression Test Checklist — SigmaPay Mobile Banking

Checklist ringkas untuk dieksekusi **setiap ada bug fix atau rilis baru**, memastikan fitur yang sudah berjalan tidak rusak akibat perubahan di modul lain. Dipetakan ke fase **Maintenance (SDLC)** / **regresi berulang tiap sprint (STLC)**.

## Cara Pakai

- Jalankan checklist ini **sebelum** setiap rilis ke production, dan setiap kali ada hotfix defect Critical/Major.
- Jika modul yang di-fix menyentuh Ledger/Saldo, wajib jalankan seluruh section **Fund Transfer** + **Saldo & Mutasi**, bukan cuma modul yang di-fix.
- Tandai ✅ Pass / ❌ Fail / ⏭️ Skip (dengan alasan) di kolom Status.
- Kolom **ID** memakai skema `REG-XX` yang sama dengan yang direferensikan di [SigmaPay Prototype Scope](../SigmaPay%20Prototype%20Scope/SigmaPay%20QA%20Workbench.dc.html) — item bertanda ✅ di kolom "Live di Prototype" bisa langsung dieksekusi interaktif di sana; sisanya perlu environment SIT/UAT sesungguhnya.

## 1. Login & Autentikasi

| ID | Item | Live di Prototype | Status |
|---|---|---|---|
| REG-01 | Login dengan kredensial valid berhasil | ✅ | |
| REG-02 | Login dengan PIN/password salah ditolak | ✅ | |
| REG-03 | Biometric login (jika tersedia) tetap berfungsi | N/A — belum diimplementasikan di build ini (lihat Profil: "Biometric login: Nonaktif") | |
| REG-04 | Sesi otomatis logout setelah idle sesuai kebijakan | ✅ (tombol "Paksa sesi timeout" di panel kiri) | |

## 2. Saldo & Riwayat Mutasi

| ID | Item | Live di Prototype | Status |
|---|---|---|---|
| REG-05 | Saldo yang tampil di Home sesuai dengan database | ✅ | |
| REG-06 | Riwayat mutasi menampilkan transaksi terbaru dengan urutan tanggal benar | ✅ | |
| REG-07 | Detail transaksi pada mutasi dapat dibuka & datanya lengkap | ✅ | |
| REG-08 | Filter mutasi (per tanggal/jenis transaksi) berfungsi normal | — (belum ada fitur filter di prototype) | |

## 3. Fund Transfer

| ID | Item | Live di Prototype | Status |
|---|---|---|---|
| REG-09 | Transfer intrabank normal tetap berhasil | ✅ | |
| REG-10 | Transfer interbank (BI-FAST) normal tetap berhasil | ✅ | |
| REG-11 | Transfer ke Virtual Account tetap berhasil | ✅ | |
| REG-12 | Validasi saldo tidak cukup tetap berfungsi | ✅ (pakai akun Citra Dewi, saldo Rp 0) | |
| REG-13 | Validasi limit transaksi harian tetap berfungsi | ✅ (toggle "Akumulasi hari ini Rp 49.000.000" di panel kiri) | |
| REG-14 | Tidak ada double debit saat tap cepat berulang (regresi BUG-SGP-001) | ✅ (toggle build v1.5.0-FIX, tap 2x cepat di S11) | |
| REG-15 | Status transaksi tetap konsisten saat simulasi koneksi terputus (regresi BUG-SGP-002) | ✅ (toggle kondisi jaringan "Koneksi putus setelah submit") | |

## 4. QRIS Payment

| ID | Item | Live di Prototype | Status |
|---|---|---|---|
| REG-16 | Scan & bayar QRIS statis tetap berhasil | ✅ ("Kopi Kalibrata") | |
| REG-17 | Scan & bayar QRIS dinamis tetap berhasil | ✅ ("Toko Serba Ada") | |
| REG-18 | QR expired tetap ditolak backend (regresi BUG-SGP-004) | ✅ ("Warung Sate Pak Har", build v1.5.0-FIX) | |
| REG-19 | Validasi Merchant ID tetap berjalan (regresi BUG-SGP-005) | ✅ ("Laundry Ekspress", build v1.5.0-FIX) | |
| REG-20 | Bukti pembayaran QRIS tetap dapat diunduh | ✅ (tombol "Unduh/bagikan bukti" di layar e-receipt) | |

## 5. API Layer (Sanity Check via Postman Collection)

| ID | Item | Live di Prototype | Status |
|---|---|---|---|
| REG-21 | `POST /transfer` mengembalikan response sesuai kontrak (status code & schema) | ✅ (lihat tab "API" di panel kanan) | |
| REG-22 | `POST /qris/pay` menolak QR expired dengan errorCode `QR_EXPIRED` | ✅ (build v1.5.0-FIX, lihat tab API) | |
| REG-23 | `GET /transaction/status` tidak bisa diakses lintas user (IDOR check) | — (endpoint ini tidak dimodelkan penuh di prototype, tetap wajib diuji manual via Postman) | |

## 6. Database Sanity Check

| ID | Item | Live di Prototype | Status |
|---|---|---|---|
| REG-24 | Tidak ada transaksi duplikat (jalankan [SQL Query A.3](../07-SQL-Validation/SQL_Queries_Validation.sql)) | ✅ (tab "SQL" di panel kanan, baris "Query #3") | |
| REG-25 | Tidak ada transaksi "Pending" yang melewati SLA (jalankan [SQL Query B.5](../07-SQL-Validation/SQL_Queries_Validation.sql)) | Sebagian — prototype hanya menampilkan simulasi status, query lengkap dijalankan manual | |
| REG-26 | Ledger debit = kredit untuk seluruh transaksi hari berjalan (jalankan [SQL Query B.8](../07-SQL-Validation/SQL_Queries_Validation.sql)) | Sebagian — prototype pakai heuristik sederhana ("ada PENDING = tidak seimbang"), bukan double-entry penuh | |

## Ringkasan Hasil

| Total Item | Pass | Fail | Skip |
|---|---|---|---|
| 26 | | | |

**Keputusan:** Rilis dapat dilanjutkan jika seluruh item **Critical path** (REG-09 s.d. REG-15, REG-24 s.d. REG-26) berstatus Pass. Kegagalan pada item tersebut = **blocker rilis**.
