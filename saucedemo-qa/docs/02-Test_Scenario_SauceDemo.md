# Test Scenario — SauceDemo (Login & Checkout)

Level di atas [Test Case](../03-Test-Case/Test_Case_SauceDemo.csv): skenario di bawah ini
menjawab "area besar apa yang perlu diuji dan kenapa", sebelum diturunkan jadi langkah detail
per test case. Setiap skenario dipetakan ke [Test Plan §2](../01-Test-Plan/Test_Plan_SauceDemo.md#2-item-pengujian)
dan diimplementasikan sebagai kode di [`automation/playwright/`](../../automation/playwright), [`automation/cypress/`](../../automation/cypress), dan
[`automation/selenium/`](../../automation/selenium).

| Scenario ID | Fitur | Deskripsi Skenario | Test Case Terkait | Prioritas |
|---|---|---|---|---|
| SCN-LOGIN-01 | Login | Verifikasi login berhasil untuk kombinasi kredensial valid (termasuk beda case → gagal, karena username case-sensitive) | LOGIN-01, LOGIN-03 | Tinggi |
| SCN-LOGIN-02 | Login | Verifikasi login ditolak dengan pesan error yang sesuai untuk kredensial tidak valid/kosong | LOGIN-02, LOGIN-04, LOGIN-05 | Tinggi |
| SCN-LOGIN-03 | Login | Verifikasi akun yang dikunci (locked-out) selalu ditolak walau kredensialnya benar | LOGIN-06 | Tinggi |
| SCN-LOGIN-04 | Login | Verifikasi logout mengakhiri sesi dan mengembalikan user ke halaman login | LOGIN-07 | Sedang |
| SCN-LOGIN-05 | Login | Verifikasi halaman yang butuh sesi (cart) tidak bisa diakses langsung tanpa login — session/access control dasar | LOGIN-08 | Sedang |
| SCN-CART-01 | Keranjang | Verifikasi item bisa ditambahkan ke keranjang dan badge/tombol memperbarui status dengan benar | CART-01 | Tinggi |
| SCN-CART-02 | Keranjang | Verifikasi item bisa dihapus dari keranjang, baik dari halaman inventory maupun halaman cart | CART-02, CART-03 | Sedang |
| SCN-CART-03 | Keranjang | Verifikasi navigasi "Continue Shopping" mengembalikan user ke katalog produk | CART-04 | Rendah |
| SCN-SORT-01 | Pengurutan | Verifikasi seluruh 4 opsi sort (Name A-Z/Z-A, Price low-high/high-low) menghasilkan urutan yang benar | SORT-01, SORT-02, SORT-03, SORT-04 | Sedang |
| SCN-CHECKOUT-01 | Checkout | Verifikasi checkout berhasil sampai halaman konfirmasi, untuk satu maupun banyak item sekaligus | CHK-01, CHK-02 | Tinggi |
| SCN-CHECKOUT-02 | Checkout | Verifikasi checkout diblokir dengan pesan error yang sesuai saat salah satu field wajib (First Name/Last Name/Postal Code) kosong | CHK-03 | Tinggi |
| SCN-CHECKOUT-03 | Checkout | Dokumentasikan karakteristik validasi input form checkout (karakter spesial diterima tanpa ditolak) dan verifikasi perhitungan total harga (subtotal + tax) benar | CHK-04, CHK-05 | Rendah–Sedang |
| SCN-REGRESSION-01 | Regresi Bug Bawaan | Verifikasi ulang 7 bug yang sengaja disiapkan SauceDemo pada akun `problem_user`, `error_user`, `visual_user`, `performance_glitch_user` — apakah masih reproduksi atau sudah berubah perilakunya | BUG-001, BUG-003, BUG-004, BUG-005, BUG-006, BUG-007 | Tinggi |

## Skenario yang Sengaja Tidak Dibuat

Konsisten dengan Out of Scope di [Test Plan §4](../01-Test-Plan/Test_Plan_SauceDemo.md#4-out-of-scope-testing):
tidak ada skenario untuk Register, proses pembayaran sungguhan, validasi alamat, maupun API
testing — karena SauceDemo memang tidak memiliki fitur/lapisan tersebut untuk diuji.

## Catatan Desain

Skenario di atas sengaja dikelompokkan per **fitur**, bukan per **jenis testing** (functional vs
non-functional dsb) — pengelompokan jenis testing dengan contoh konkretnya sudah dibahas
terpisah di [Testing_Types_Taxonomy.md](../00-SDLC-STLC-Overview/Testing_Types_Taxonomy.md) supaya
dokumen ini tetap fokus jadi jembatan antara Test Plan (scope besar) dan Test Case (langkah
detail), bukan mengulang taksonomi yang sama.
