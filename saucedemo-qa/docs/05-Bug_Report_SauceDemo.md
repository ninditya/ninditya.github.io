# Laporan Bug — Paket Pengujian QA SauceDemo

**Aplikasi:** https://www.saucedemo.com/
**Catatan:** SauceDemo memang sengaja menyiapkan setiap bug di bawah ini pada akun uji tertentu
supaya orang yang belajar QA punya bug sungguhan untuk ditemukan. Setiap bug diverifikasi ulang
lewat test otomatis di [`known-issues.spec.ts`](../../automation/playwright/tests/known-issues.spec.ts)
(Playwright) dan [`known-issues.cy.ts`](../../automation/cypress/e2e/known-issues.cy.ts) (Cypress) —
dan, jika disebutkan, juga di paket Selenium — sehingga setiap kali dijalankan ulang, perubahan
perilaku SauceDemo akan langsung ketahuan. Karena sekarang ada hasil nyata dari dua framework
sekaligus, tabel di bawah membedakan status **konsisten** (sama di kedua framework — sinyal
kuat/bisa dipercaya) dari status **framework-dependent** (beda hasil — perlu dibaca catatannya).

**Terakhir diverifikasi:** 2026-08-10, dijalankan otomatis langsung ke situs live (Playwright dari
sesi development, Cypress dari Cypress Test Runner milik pemilik project — lihat
[Test_Execution_Report.md §4](../04-Test-Execution/Test_Execution_Report.md#4-detail-hasil--known-issues-verifikasi-bug-bawaan-playwright-vs-cypress)
untuk detail lengkapnya).

| ID | Playwright | Cypress | Kesimpulan |
|----|---|---|---|
| BUG-001 | ✅ Ya | ✅ Ya | **Konsisten** — masih terjadi |
| BUG-002 | Belum diotomasi (hanya bisa dicek visual) | Belum diotomasi | — |
| BUG-003 | ✅ Ya | ❌ Tidak | ⚠️ **Framework-dependent** — lihat catatan di bawah |
| BUG-004 | ❌ Tidak | ❌ Tidak | **Konsisten** — sudah tidak terjadi lagi |
| BUG-005 | ✅ Ya | ✅ Ya | **Konsisten** — masih terjadi |
| BUG-006 | ❌ Tidak | ❌ Tidak | **Konsisten** — sudah tidak terjadi lagi |
| BUG-007 | ❌ Tidak | ✅ Ya | ⚠️ **Framework-dependent** — kemungkinan besar ambang batas waktu yang terlalu ketat, lihat catatan di bawah |

---

## BUG-001 — Gambar Produk Tidak Menampilkan Gambar yang Benar (`problem_user`)

| Kolom | Detail |
|-------|--------|
| **Area** | Katalog produk |
| **Severity** | Sedang |
| **Akun** | `problem_user` / `secret_sauce` |
| **Status** | Masih terjadi per 2026-08-10 — **konsisten di Playwright dan Cypress** |
| **Pengecekan otomatis** | `known-issues.spec.ts` (Playwright) — BUG-001; `known-issues.cy.ts` (Cypress) — BUG-001 |

**Langkah Reproduksi:**
1. Login sebagai `problem_user`.
2. Periksa gambar produk di halaman inventory.

**Diharapkan:** Setiap kartu produk menampilkan gambarnya masing-masing yang benar.
**Kenyataan:** Semua kartu produk menampilkan gambar yang sama dan salah.

---

## BUG-002 — Halaman Dashboard Memiliki Beberapa Masalah Komponen UI (`visual_user`)

| Kolom | Detail |
|-------|--------|
| **Area** | UI / Tampilan |
| **Severity** | Sedang |
| **Akun** | `visual_user` / `secret_sauce` |
| **Pengecekan otomatis** | Tidak ada — pergeseran tampilan (visual drift) tidak bisa dicek lewat assertion berbasis DOM biasa; perlu ditinjau manual atau lewat visual-regression testing |

**Langkah Reproduksi:**
1. Login sebagai `visual_user`.
2. Periksa komponen-komponen halaman (ikon hamburger, ikon keranjang, harga item, posisi tombol
   "Add to cart").

**Diharapkan:** Semua komponen UI tampil di posisi dan nilai yang benar.
**Kenyataan:** Beberapa komponen bergeser posisinya atau menampilkan nilai yang salah (misalnya
harga yang membengkak, ikon/tombol yang posisinya bergeser).

---

## BUG-003 — Fitur Sort Menampilkan Error JavaScript (`error_user`)

| Kolom | Detail |
|-------|--------|
| **Area** | Katalog produk / Pengurutan |
| **Severity** | Tinggi |
| **Akun** | `error_user` / `secret_sauce` |
| **Status** | ⚠️ Framework-dependent per 2026-08-10 — terjadi di Playwright, **tidak** terjadi di Cypress pada run yang sama harinya |
| **Pengecekan otomatis** | `known-issues.spec.ts` — BUG-003 (Playwright, FAIL/bug terdeteksi); `known-issues.cy.ts` — BUG-003 (Cypress, PASS/bug tidak terdeteksi) |

**Langkah Reproduksi:**
1. Login sebagai `error_user`.
2. Ubah pilihan di dropdown sort.

**Diharapkan:** Daftar item terurut ulang sesuai pilihan yang dipilih.
**Kenyataan (Playwright):** Sort tidak memperbarui daftar; muncul dialog alert: "Sorting is
broken! This error has been reported to Backtrace."
**Kenyataan (Cypress):** Alert tidak muncul sama sekali pada run yang sama harinya.

**Catatan analisis:** dugaan penyebab paling masuk akal adalah perbedaan cara Playwright dan
Cypress men-trigger event `change` pada elemen `<select>` — Playwright mengemulasi input lebih
dekat ke perilaku browser asli (lewat Chrome DevTools Protocol), Cypress mensimulasikan event
lewat JavaScript. Kemungkinan logika broken-sort di `error_user` hanya terpicu oleh salah satu
jenis event tersebut. Ini bukan bug di test-nya — kedua framework melaporkan yang benar-benar
terjadi di sesinya masing-masing; kesimpulannya, bug ini **tidak konsisten muncul di semua cara
interaksi**, bukan benar-benar hilang.

---

## BUG-004 — Tombol Add to Cart Tidak Berfungsi di Sebagian Item (`error_user`)

| Kolom | Detail |
|-------|--------|
| **Area** | Keranjang belanja |
| **Severity** | Tinggi |
| **Akun** | `error_user` / `secret_sauce` |
| **Status** | Sudah tidak terjadi lagi per 2026-08-10 — semua tombol Add to cart dalam kondisi aktif, **konsisten di Playwright, Cypress, dan Selenium** |
| **Pengecekan otomatis** | `known-issues.spec.ts` (Playwright) — BUG-004; `known-issues.cy.ts` (Cypress) — BUG-004; `test_saucedemo.py::test_error_user_add_to_cart_all_items` (Selenium) |

**Langkah Reproduksi:**
1. Login sebagai `error_user`.
2. Klik "Add to cart" pada beberapa item.

**Diharapkan:** Semua tombol "Add to cart" bisa diklik dan menambahkan itemnya.
**Kenyataan:** Sebagian tombol berfungsi; sebagian lagi tidak bisa diklik.

---

## BUG-005 — Field Last Name Tidak Bisa Diisi Saat Checkout (`error_user`)

| Kolom | Detail |
|-------|--------|
| **Area** | Checkout: Your Information |
| **Severity** | Tinggi |
| **Akun** | `error_user` / `secret_sauce` |
| **Status** | Masih terjadi per 2026-08-10 — **konsisten di Playwright dan Cypress** |
| **Pengecekan otomatis** | `known-issues.spec.ts` (Playwright) — BUG-005; `known-issues.cy.ts` (Cypress) — BUG-005 |

**Langkah Reproduksi:**
1. Login sebagai `error_user`, tambahkan item, lanjut ke checkout.
2. Coba isi field Last Name.

**Diharapkan:** Field Last Name menerima input.
**Kenyataan:** Field tidak menerima input apa pun.

---

## BUG-006 — Tidak Bisa Menyelesaikan Alur Checkout (`error_user`)

| Kolom | Detail |
|-------|--------|
| **Area** | Checkout: Overview |
| **Severity** | Tinggi |
| **Akun** | `error_user` / `secret_sauce` |
| **Status** | Sudah tidak terjadi lagi per 2026-08-10 — tombol Finish dalam kondisi aktif dan bisa diklik, **konsisten di Playwright dan Cypress** |
| **Pengecekan otomatis** | `known-issues.spec.ts` (Playwright) — BUG-006; `known-issues.cy.ts` (Cypress) — BUG-006 |

**Langkah Reproduksi:**
1. Login sebagai `error_user`, tambahkan item, lanjutkan checkout sampai ke langkah Overview.
2. Klik "Finish".

**Diharapkan:** Pesanan selesai; pengguna sampai di halaman konfirmasi.
**Kenyataan:** Tombol "Finish" tidak bisa diklik.

---

## BUG-007 — Dashboard Memiliki Respons yang Lambat (`performance_glitch_user`)

| Kolom | Detail |
|-------|--------|
| **Area** | Performa |
| **Severity** | Sedang |
| **Akun** | `performance_glitch_user` / `secret_sauce` |
| **Status** | ⚠️ Framework-dependent per 2026-08-10 — dashboard termuat **dalam** batas waktu 5 detik di Playwright, tapi **melewati** batas waktu di Cypress pada run yang sama harinya |
| **Pengecekan otomatis** | `known-issues.spec.ts` (Playwright, PASS/< 5 detik); `known-issues.cy.ts` (Cypress, FAIL/> 5 detik) — BUG-007 |

**Langkah Reproduksi:**
1. Login sebagai `performance_glitch_user`.

**Diharapkan:** Pengalihan ke halaman inventory berjalan mulus tanpa delay yang terasa.
**Kenyataan:** Delay bawaan `performance_glitch_user` masih ada, dan durasinya berada **tepat di
sekitar ambang batas 5 detik** yang dipakai test ini — cukup dekat sehingga hasilnya bisa
berpindah pass/fail tergantung overhead runner yang dipakai (Cypress Test Runner mode GUI/
interaktif punya overhead lebih besar daripada Playwright headless, jadi lebih rentan melewati
ambang batas).

**Catatan analisis:** ini kemungkinan besar bukan berarti delay-nya "berubah", melainkan ambang
batas 5 detik di test ini **terlalu ketat/mepet** untuk dijadikan pass/fail biner yang stabil
lintas framework. Rekomendasi: naikkan ambang batas (mis. 8-10 detik) atau ukur delta relatif
terhadap waktu load `standard_user` alih-alih angka absolut.
