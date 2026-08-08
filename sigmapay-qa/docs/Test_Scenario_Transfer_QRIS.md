# Test Scenario — Fund Transfer & QRIS Payment

Test Scenario adalah level "high-level" sebelum di-breakdown jadi Test Case detail. Dikelompokkan per modul, mencakup **Positive**, **Negative**, dan **Edge Case** — ini bagian yang paling sering ditanyakan saat interview: *"kemungkinan-kemungkinan apa saja yang bisa terjadi?"*

> Skenario di bawah ini sudah disinkronkan dengan [SigmaPay Prototype Scope](../SigmaPay%20Prototype%20Scope/SigmaPay%20QA%20Workbench.dc.html) — prototype interaktif 30 layar yang mengimplementasikan skenario-skenario ini secara nyata, termasuk toggle build buggy/fixed untuk tiap bug.

## Modul 1: Fund Transfer (Intrabank & Interbank/BI-FAST)

### Positive Scenario
| ID | Skenario |
|---|---|
| TS-TRF-01 | Transfer intrabank dengan saldo cukup berhasil, saldo pengirim berkurang & penerima bertambah sesuai nominal |
| TS-TRF-02 | Transfer interbank via BI-FAST dengan saldo cukup berhasil, dana diterima real-time |
| TS-TRF-03 | Transfer ke Virtual Account berhasil, status settlement sesuai |
| TS-TRF-04 | User dapat melihat rincian biaya admin sebelum konfirmasi transfer |
| TS-TRF-05 | User menerima notifikasi & bukti transfer (e-receipt) setelah transaksi sukses |
| TS-TRF-06 | User dapat melakukan transfer terjadwal (scheduled transfer) |
| TS-TRF-07 | Riwayat transfer tersimpan dan muncul di menu mutasi |

### Negative Scenario
| ID | Skenario |
|---|---|
| TS-TRF-08 | Transfer ditolak saat saldo tidak mencukupi |
| TS-TRF-09 | Transfer ditolak saat nominal melebihi limit transaksi harian |
| TS-TRF-10 | Transfer ditolak saat nomor rekening tujuan tidak valid/tidak ditemukan |
| TS-TRF-11 | Transfer ditolak saat rekening tujuan dalam status diblokir/dormant |
| TS-TRF-12 | Transfer gagal ditangani dengan baik saat OTP salah 3x (akun terkunci sementara) |
| TS-TRF-13 | Transfer gagal saat sesi aplikasi timeout di tengah proses konfirmasi |
| TS-TRF-14 | Sistem menolak input nominal negatif atau nol |
| TS-TRF-15 | Sistem menolak input karakter non-numerik pada field nominal |
| TS-TRF-16 | Transfer ke rekening sendiri (nomor sama) **ditolak** dengan pesan "Rekening tujuan sama dengan rekening Anda. Gunakan menu Pindah Buku." — business rule ini sudah final (dikonfirmasi lewat [SigmaPay Prototype Scope](../SigmaPay%20Prototype%20Scope/SigmaPay%20QA%20Workbench.dc.html)), fitur "Pindah Buku" sendiri belum ada di scope sprint ini |

### Edge Case / Kemungkinan Kritis (khas Banking)
| ID | Skenario | Kenapa Penting |
|---|---|---|
| TS-TRF-17 | **Double debit**: user tap tombol "Transfer" dua kali cepat (double click) — pastikan hanya 1 transaksi tereksekusi | Bug klasik yang menyebabkan kerugian finansial nasabah |
| TS-TRF-18 | **Status ambigu**: koneksi terputus setelah request transfer terkirim ke server tapi sebelum response diterima user — cek apakah saldo terdebit tapi UI menampilkan "gagal" (perlu rekonsiliasi) | Menyebabkan komplain nasabah "uang hilang" |
| TS-TRF-19 | Transfer ke BI-FAST saat sandbox/switching eksternal timeout — pastikan sistem melakukan **reversal otomatis** atau status "pending" yang jelas | Uang keluar tapi tidak sampai ke tujuan |
| TS-TRF-20 | Transfer dilakukan tepat saat pukul 23:59:59 mendekati cut-off harian — cek perhitungan limit harian tidak reset di tengah transaksi | Bug boundary/waktu |
| TS-TRF-21 | Input nominal dengan banyak digit desimal / nominal sangat besar (misal Rp 999.999.999.999) — cek validasi & tidak overflow | Data validation & security |
| TS-TRF-22 | Field "Berita Transfer/Catatan" diisi dengan script/SQL injection payload (`' OR '1'='1`, `<script>alert(1)</script>`) | Basic security hygiene yang QA wajib cek meski bukan pentest formal |

## Modul 2: QRIS Payment

### Positive Scenario
| ID | Skenario |
|---|---|
| TS-QRIS-01 | Scan QRIS statis milik merchant valid, input nominal, bayar berhasil |
| TS-QRIS-02 | Scan QRIS dinamis (nominal sudah tertera dari merchant), bayar berhasil tanpa input manual |
| TS-QRIS-03 | Setelah bayar, status "Berhasil" muncul di app & merchant menerima notifikasi pembayaran |
| TS-QRIS-04 | User dapat melihat & mengunduh bukti pembayaran QRIS |

### Negative Scenario
| ID | Skenario |
|---|---|
| TS-QRIS-05 | Pembayaran ditolak saat QR code sudah kedaluwarsa (expired) |
| TS-QRIS-06 | Pembayaran ditolak saat QR code rusak/tidak terbaca (invalid format) |
| TS-QRIS-07 | Pembayaran ditolak saat saldo tidak cukup |
| TS-QRIS-08 | Pembayaran ditolak saat nominal melebihi **Rp 10.000.000 per transaksi** — ini limit **per transaksi**, bukan akumulasi harian seperti limit transfer (beda mekanisme, jangan disamakan saat design test case) |
| TS-QRIS-09 | Sistem menolak scan QR dari sumber yang tidak dikenali/bukan format QRIS nasional |

### Edge Case
| ID | Skenario | Kenapa Penting |
|---|---|---|
| TS-QRIS-10 | User scan QRIS tapi menutup aplikasi sebelum konfirmasi final — cek saldo tidak terpotong | Kegagalan transaksi harus fail-safe (tidak merugikan nasabah) |
| TS-QRIS-11 | Merchant ID pada QR tidak match dengan Merchant ID di sistem backend saat settlement | Uang terbayar tapi salah merchant — kasus nyata di industri |
| TS-QRIS-12 | Dua device melakukan scan QR statis yang sama secara bersamaan (concurrent payment) — pastikan tidak terjadi race condition pada saldo | Concurrency bug |
| TS-QRIS-13 | Pembayaran QRIS lintas bank/switching berbeda — cek waktu settlement dan status "pending" ditampilkan dengan jelas ke user | UX kejelasan status, bukan cuma fungsi |

## Modul 3: Non-Fungsional Ringan (tetap bagian tanggung jawab manual QA)

| ID | Skenario |
|---|---|
| TS-NFR-01 | Waktu respons transfer intrabank tidak lebih dari 5 detik (sanity check, bukan load test formal) |
| TS-NFR-02 | Data sensitif (nomor rekening, saldo) tidak muncul di log aplikasi/API response yang tidak perlu |
| TS-NFR-03 | Aplikasi tetap dapat digunakan (graceful degradation) saat koneksi lambat/berpindah dari WiFi ke seluler di tengah transaksi |
