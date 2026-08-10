# SQL / Database Validation — Tidak Berlaku untuk Project Ini

Sama seperti [`06-API-Testing`](../06-API-Testing/API_Testing_Not_Applicable.md), folder ini
tetap dibuat untuk menjaga penomoran tahap STLC tetap lengkap dan mudah ditelusuri, bukan diisi
konten yang dipaksakan.

## Alasan

SauceDemo tidak memberi akses apa pun ke lapisan database — tidak ada kredensial, tidak ada
endpoint yang mengekspos data mentah, dan checkout hanya menampilkan data dummy statis
("SauceCard #31337", "Free Pony Express Delivery!") yang sama untuk semua transaksi, bukan hasil
tulis/baca database sungguhan yang bisa divalidasi silang.

Ini konsisten dengan Out of Scope di
[Test Plan §4](../01-Test-Plan/Test_Plan_SauceDemo.md#4-out-of-scope-testing) — khususnya poin
"Proses pembayaran" dan "Validasi alamat" yang memang tidak punya backend nyata di baliknya.

## Kalau Suatu Saat Dibutuhkan

Untuk aplikasi dengan database sungguhan, tahap ini biasanya berisi query SQL untuk
memvalidasi data pasca-transaksi (misalnya: `SELECT` saldo/status pesanan setelah checkout
dibandingkan dengan hasil di UI) — melengkapi hasil UI testing dengan validasi di level data,
bukan cuma percaya tampilan layar.
