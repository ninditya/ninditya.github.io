# Bug Report — Gaya JIRA (Sample Defect dari Cycle 1)

Format mengikuti field standar JIRA: Summary, Environment, Steps to Reproduce, Expected vs Actual, Severity, Priority, Attachment.

> **Semua 6 bug di bawah ini bisa direproduksi langsung** di [SigmaPay Prototype Scope](../SigmaPay%20Prototype%20Scope/SigmaPay%20QA%20Workbench.dc.html): pastikan toggle build di kanan atas di-set ke **v1.4.0-QA** (kondisi buggy, default), jalankan steps to reproduce di perangkat simulasi, lalu cek tab **Defect** di panel kanan untuk melihat status "TEREPRODUKSI". Pindahkan toggle ke **v1.5.0-FIX** dan ulangi langkah yang sama untuk memverifikasi retest ("RETEST PASS") — ini setara dengan siklus retest Cycle 2 di [Test Execution Report](../04-Test-Execution/Test_Execution_Report.md). Untuk BUG-SGP-002 dan BUG-SGP-003, aktifkan dulu kondisi jaringan yang sesuai di panel kiri ("Koneksi putus setelah submit" / "Switching BI-FAST timeout") sebelum menjalankan transaksi.

---

### BUG-SGP-001

| Field | Detail |
|---|---|
| Summary | [Transfer] Double debit terjadi saat tombol "Kirim" ditekan dua kali secara cepat |
| Module | Fund Transfer – Intrabank |
| Severity | **Critical** |
| Priority | **P1** |
| Environment | QA – Android build v1.4.0-QA, device Pixel 6 |
| Reported By | QA Engineer |
| Related Test Case | TC-TRF-015 |
| Status | Open |

**Steps to Reproduce**
1. Login sebagai User A (saldo Rp 5.000.000)
2. Buka menu Transfer Intrabank, isi tujuan User B, nominal Rp 300.000
3. Di halaman konfirmasi, tap tombol "Kirim" dua kali secara berurutan dengan cepat (< 1 detik)

**Expected Result**
Hanya 1 transaksi tereksekusi. Saldo User A berkurang tepat Rp 300.000 (+ admin fee).

**Actual Result**
Tercatat 2 transaksi terpisah dengan Transaction ID berbeda. Saldo User A terpotong 2x (Rp 600.000 + 2x admin fee).

**Root Cause Analysis (dugaan awal QA)**
Tidak ada debounce/disable pada tombol submit setelah tap pertama, dan tidak ada idempotency key pada request API `POST /transfer`.

**Rekomendasi**
Disable tombol submit segera setelah tap pertama + implementasi idempotency key di sisi backend.

---

### BUG-SGP-002

| Field | Detail |
|---|---|
| Summary | [Transfer] Status transaksi menampilkan "Gagal" di UI padahal saldo sudah terdebit saat koneksi terputus |
| Module | Fund Transfer – Intrabank |
| Severity | **Critical** |
| Priority | **P1** |
| Environment | QA – iOS build v1.4.0-QA |
| Reported By | QA Engineer |
| Related Test Case | TC-TRF-016 |
| Status | Open |

**Steps to Reproduce**
1. Login sebagai User A
2. Isi form transfer Rp 250.000, submit
3. Aktifkan Airplane Mode tepat setelah tombol "Kirim" ditekan (mensimulasikan request terkirim tapi response tidak diterima)
4. Nonaktifkan Airplane Mode, buka menu Riwayat Mutasi & cek saldo

**Expected Result**
Status transaksi di aplikasi konsisten dengan kondisi saldo aktual di database. Jika saldo terdebit, status harus "Berhasil" (bukan "Gagal"), atau ada mekanisme rekonsiliasi otomatis.

**Actual Result**
Aplikasi menampilkan "Transfer Gagal, silakan coba lagi", padahal query database menunjukkan saldo sudah terpotong dan transaksi berstatus SUCCESS di backend.

**Dampak Bisnis**
Berisiko tinggi menyebabkan user mencoba transfer ulang (duplikasi) dan komplain "uang hilang" ke Call Center.

**Rekomendasi**
Implementasi mekanisme **query status transaksi** otomatis di sisi client setelah timeout, bukan langsung asumsi gagal.

---

### BUG-SGP-003

| Field | Detail |
|---|---|
| Summary | [Transfer] Tidak ada reversal otomatis saat switching BI-FAST timeout, saldo tertahan tanpa status jelas |
| Module | Fund Transfer – Interbank (BI-FAST) |
| Severity | **Major** |
| Priority | **P2** |
| Environment | QA – Sandbox BI-FAST Simulator (simulated timeout) |
| Reported By | QA Engineer |
| Related Test Case | TC-TRF-017 |
| Status | Open |

**Steps to Reproduce**
1. Lakukan transfer interbank Rp 400.000 ke bank tujuan
2. Simulasikan sandbox switching BI-FAST tidak memberikan response (timeout)
3. Cek status transaksi di aplikasi setelah 60 detik

**Expected Result**
Sistem melakukan reversal otomatis (saldo dikembalikan) dalam waktu wajar, ATAU status berubah menjadi "Pending – sedang diproses" yang jelas dengan estimasi waktu penyelesaian.

**Actual Result**
Status tetap "Diproses" tanpa batas waktu jelas; saldo tetap terpotong; tidak ada job/scheduler yang melakukan reversal otomatis setelah threshold timeout terlampaui.

**Rekomendasi**
Tambahkan scheduled job untuk auto-reversal jika status "Pending" melebihi SLA tertentu (misal 15 menit), plus notifikasi ke user.

---

### BUG-SGP-004

| Field | Detail |
|---|---|
| Summary | [QRIS] Pembayaran tetap dapat diproses meskipun QR code sudah kedaluwarsa (expired) |
| Module | QRIS Payment |
| Severity | **Critical** |
| Priority | **P1** |
| Environment | QA – Merchant QRIS Simulator |
| Reported By | QA Engineer |
| Related Test Case | TC-QRIS-004 |
| Status | Open |

**Steps to Reproduce**
1. Generate QR dinamis dengan masa berlaku 5 menit dari sisi merchant simulator
2. Tunggu hingga QR melewati masa berlaku (> 5 menit)
3. Scan QR yang sudah expired tersebut dari aplikasi SigmaPay
4. Lanjutkan hingga tahap pembayaran

**Expected Result**
Sistem menolak pemrosesan dan menampilkan pesan "QR sudah kedaluwarsa" sebelum tahap pembayaran.

**Actual Result**
Aplikasi tidak melakukan validasi masa berlaku QR di sisi client maupun saat hit API `POST /qris/pay`; pembayaran berhasil diproses dan saldo terpotong meski QR sudah expired.

**Dampak Bisnis**
Berpotensi menyebabkan sengketa dana antara nasabah dan merchant karena transaksi terjadi di luar validitas QR yang disepakati (berisiko terhadap kepatuhan standar QRIS Bank Indonesia).

**Rekomendasi**
Validasi `expiry_time` pada QR wajib dicek baik di client (UX cepat) maupun di backend (source of truth) sebelum eksekusi pembayaran.

---

### BUG-SGP-005

| Field | Detail |
|---|---|
| Summary | [QRIS] Tidak ada validasi kecocokan Merchant ID antara QR dan data settlement backend |
| Module | QRIS Payment |
| Severity | **Major** |
| Priority | **P2** |
| Environment | QA – Merchant QRIS Simulator |
| Reported By | QA Engineer |
| Related Test Case | TC-QRIS-009 |
| Status | Open |

**Steps to Reproduce**
1. Siapkan QR dengan Merchant ID yang dimodifikasi (tidak sesuai data terdaftar di backend, disimulasikan via test data)
2. Scan & lakukan pembayaran

**Expected Result**
Sistem menolak transaksi atau menandai sebagai anomali sebelum dana disettle ke merchant yang salah.

**Actual Result**
Transaksi tetap diproses dan dana disettle berdasarkan Merchant ID pada QR tanpa cross-check ke data merchant terdaftar di backend.

**Rekomendasi**
Tambahkan validasi Merchant ID pada QR terhadap master data merchant sebelum proses settlement final.

---

### BUG-SGP-006

| Field | Detail |
|---|---|
| Summary | [Transfer] Field nominal menerima input negatif tanpa validasi |
| Module | Fund Transfer – Form Input |
| Severity | **Minor** |
| Priority | **P3** |
| Environment | QA – Web build v1.4.0-QA |
| Reported By | QA Engineer |
| Related Test Case | TC-TRF-012 |
| Status | Open |

**Steps to Reproduce**
1. Buka form transfer
2. Masukkan nominal "-100000" pada field nominal
3. Tekan tombol lanjut

**Expected Result**
Sistem menolak input dan menampilkan pesan validasi.

**Actual Result**
Sistem menerima input, tombol "Lanjut" tetap aktif, dan error baru muncul di halaman konfirmasi dengan pesan yang tidak informatif ("Terjadi kesalahan").

**Rekomendasi**
Tambahkan validasi input di level form (client-side) agar error lebih cepat & jelas bagi user, tidak menunggu response API.
