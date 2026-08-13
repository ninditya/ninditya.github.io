# SigmaPay Bank Demo — Web Target untuk Latihan QA Automation

Ini adalah **aplikasi web statis** (HTML/CSS/JavaScript murni, tanpa framework, tanpa build step) yang dibuat khusus jadi **target/system-under-test** untuk latihan manual & automation testing — mengikuti pola situs latihan populer seperti [saucedemo.com](https://www.saucedemo.com/): beberapa akun login, masing-masing sengaja punya perilaku berbeda supaya bisa dipakai latihan eksplorasi, bug hunting, dan penulisan skrip Selenium/Playwright/Cypress.

**Catatan jujur:** ini adalah aplikasi tiruan yang saya bangun sendiri untuk latihan portofolio, bukan aplikasi produksi sungguhan dan bukan pengalaman kerja di bank. Semua data (nama, nomor rekening, saldo) fiktif. Logikanya murni client-side (state disimpan di `sessionStorage` browser) — tidak ada backend/API sungguhan di baliknya.

Berbeda dari [SigmaPay Prototype Scope](../prototype.html) (prototype interaktif yang butuh tooling khusus untuk dibuka), folder ini adalah **HTML statis biasa** — bisa langsung dibuka di browser atau di-serve dengan static server apa pun, dan locator-nya (`data-testid`) stabil untuk automation.

## Cara menjalankan

Opsi 1 — buka langsung:
```
buka index.html di browser
```

Opsi 2 — via static server lokal (disarankan, supaya path relatif & fetch berperilaku seperti web sungguhan):
```bash
cd "SigmaPay Bank Demo"
python3 -m http.server 8080
# lalu buka http://localhost:8080
```

Tidak ada instalasi dependency apa pun.

## Daftar Akun Uji

Password sama untuk semua akun: **`Sigma123!`**. PIN transaksi untuk semua akun: **`123456`**.

| Username | Nama | Saldo Awal | Perilaku |
|---|---|---:|---|
| `nasabah_normal` | Rangga Wibisono | Rp 5.000.000 | Happy path — semua fitur berjalan normal |
| `nasabah_terkunci` | — | — | Login **selalu ditolak**: "Akun terkunci" (setara `locked_out_user` di saucedemo) |
| `nasabah_saldo_kosong` | Melati Suryani | Rp 0 | Untuk skenario saldo tidak cukup |
| `nasabah_lambat` | Bram Setiawan | Rp 2.500.000 | Setiap aksi (login, kirim transfer, bayar QRIS) delay ~3 detik — untuk uji loading state/timeout |
| `nasabah_dobel_transaksi` | Yusuf Hakim | Rp 3.000.000 | **Bug**: tombol "Kirim" tidak ter-disable setelah diklik → double-click cepat = dobel debit |
| `nasabah_status_ambigu` | Farah Amelia | Rp 2.000.000 | **Bug**: saldo benar-benar terpotong & tercatat "Berhasil" di database, tapi UI menampilkan pesan "Transfer Gagal" (harus dicek ke menu Mutasi untuk ketahuan) |
| `nasabah_interbank_macet` | Galih Purnomo | Rp 3.500.000 | **Bug**: transfer interbank (BI-FAST) memotong saldo tapi status macet di "Diproses" selamanya, tidak ada reversal otomatis |
| `nasabah_qris_kadaluwarsa` | Nadia Kirana | Rp 1.500.000 | **Bug**: QR yang sudah kedaluwarsa (`QRIS003`) tetap bisa dibayar, padahal untuk akun lain QR ini otomatis diblokir |
| `nasabah_qris_merchant_salah` | Wulan Ardianti | Rp 1.800.000 | **Bug**: QR dengan Merchant ID tidak sesuai (`QRIS004`) tetap diproses tanpa peringatan, padahal untuk akun lain transaksi ini otomatis dibatalkan |
| `nasabah_nominal_negatif` | Doni Saputra | Rp 4.000.000 | **Bug**: field nominal transfer menerima angka negatif tanpa validasi |

Keenam akun "Bug" di atas selaras secara tematik dengan BUG-SGP-001–006 di [Bug_Report_Sample.md](../docs/Bug_Report_Sample.html), tapi ini implementasi standalone yang terpisah (bukan reproduksi identik dari prototype `.dc.html`).

Data transfer & QRIS lain yang tersedia untuk latihan:

| Nomor Rekening Tujuan | Nama | Status |
|---|---|---|
| `8802 0000 0001` | Toko Sinar Jaya | Diblokir (untuk uji "rekening tujuan diblokir") |
| nomor selain yang terdaftar | — | "Rekening tidak ditemukan" |
| rekening akun sendiri yang login | — | Ditolak, "Gunakan menu Pindah Buku" |

| Kode QR | Merchant | Tipe |
|---|---|---|
| `QRIS001` | Kedai Kopi Nusantara | Dinamis, Rp 25.000 |
| `QRIS002` | Toko Sembako Makmur | Statis, nominal manual |
| `QRIS003` | Percetakan Warna Digital | Statis, **kedaluwarsa** |
| `QRIS004` | Toko Elektronik Jaya | Dinamis, Rp 450.000, **Merchant ID tidak cocok** |

Limit QRIS: Rp 10.000.000 per transaksi (berlaku untuk semua akun).

## Referensi Locator (`data-testid`)

Setiap elemen interaktif punya atribut `data-testid` yang stabil, tidak bergantung teks/CSS class — praktik yang sama dipakai saucedemo.com supaya skrip automation tidak flaky. Contoh yang paling sering dipakai:

| Halaman | Locator | Keterangan |
|---|---|---|
| Login | `input-username`, `input-password`, `btn-login`, `login-error` | |
| Semua halaman (setelah login) | `nav-dashboard`, `nav-transfer`, `nav-qris`, `nav-mutasi`, `nav-profil`, `btn-logout` | Topbar |
| Beranda | `saldo-value`, `account-no`, `quick-transfer`, `quick-qris`, `quick-mutasi`, `quick-profil` | |
| Transfer | `select-jenis-transfer`, `input-rekening-tujuan`, `btn-cek-rekening`, `inquiry-result`, `input-nominal`, `btn-lanjut-transfer`, `input-pin`, `btn-kirim-transfer`, `transfer-result-success` / `transfer-result-error` / `transfer-result-pending` | |
| QRIS | `qr-item-QRIS001` (dst.), `input-qris-nominal`, `input-qris-pin`, `btn-bayar-qris`, `qris-result-success` | |
| Mutasi | `mutasi-item-0`, `mutasi-status-0`, `mutasi-amount-0` (index berurutan) | |
| Profil | `btn-reset-demo`, `btn-logout-profil` | |

Lihat langsung source HTML untuk daftar lengkap — semua elemen form & tombol sudah diberi `data-testid`.

## Ide Skenario Latihan Automation

- **Positive**: login `nasabah_normal` → transfer intrabank → verifikasi saldo di Beranda & entri di Mutasi konsisten.
- **Negative**: login `nasabah_saldo_kosong` → coba transfer → assert pesan "Saldo tidak mencukupi" & saldo tidak berubah.
- **Locked account**: login `nasabah_terkunci` dengan password benar → assert tetap ditolak.
- **Bug hunting**: login `nasabah_dobel_transaksi` → gunakan `page.click()` dua kali berturut-turut tanpa delay pada `btn-kirim-transfer` → assert jumlah entri di Mutasi (harus 1, kalau bug muncul jadi 2).
- **Data-state mismatch**: login `nasabah_status_ambigu` → lakukan transfer → assert pesan di layar vs. status yang benar-benar tersimpan di Mutasi (mendemonstrasikan pentingnya verifikasi lewat lebih dari satu sumber, bukan cuma percaya pesan UI).
- **Loading state**: login `nasabah_lambat` → assert elemen `loading-spinner` muncul selama proses, lalu hilang setelah selesai (butuh explicit wait, bukan `sleep` statis — latihan bagus untuk membedakan wait strategy yang stabil vs. flaky).
- **Reset antar test run**: gunakan tombol `btn-reset-demo` di Profil (atau cukup buka tab/incognito baru — state disimpan di `sessionStorage`, otomatis bersih per sesi) supaya test case idempotent.

## Batasan yang Perlu Disadari

- Tidak ada backend/API sungguhan — cocok untuk **UI automation**, bukan API testing. Untuk latihan API testing, lihat [Postman_API_Test_Notes.md](../docs/Postman_API_Test_Notes.html) (berbasis endpoint hipotetis) atau platform seperti Parabank yang memang menyediakan REST API asli.
- State reset begitu tab ditutup (`sessionStorage`) — bukan database sungguhan, jadi tidak ada validasi lintas-device/lintas-browser.
- Dibuat untuk latihan pribadi, bukan diklaim sebagai pengalaman kerja nyata saat wawancara — posisikan sebagai "saya membangun target aplikasi + skenario ujinya sendiri untuk latihan automation", bukan "saya pernah testing aplikasi bank ini di tempat kerja".
