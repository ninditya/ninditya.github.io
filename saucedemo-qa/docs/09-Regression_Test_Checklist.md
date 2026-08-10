# Regression Test Checklist — SauceDemo

Checklist ringkas untuk dipakai setiap kali suite ini dijalankan ulang (rilis baru, curiga ada
perubahan perilaku situs, atau sekadar jadwal berkala). Tujuannya cepat dipakai tanpa perlu buka
dokumen lain dulu — detail lengkap tiap test case ada di
[`03-Test-Case/Test_Case_SauceDemo.csv`](../03-Test-Case/Test_Case_SauceDemo.csv).

## 1. Perintah Cepat

```bash
# Playwright (utama)
npx playwright test --config=automation/playwright/playwright.config.ts

# Cypress
npx cypress run --project automation/cypress

# Selenium (subset smoke test)
pytest automation/selenium/tests --disable-warnings -v
```

## 2. Checklist per Area

### Login
- [ ] LOGIN-01 — Login valid berhasil masuk ke `/inventory.html`
- [ ] LOGIN-02 — Kredensial salah menampilkan error yang benar
- [ ] LOGIN-03 — Username beda case tetap ditolak
- [ ] LOGIN-04 — Username kosong diblokir
- [ ] LOGIN-05 — Password kosong diblokir
- [ ] LOGIN-06 — Akun `locked_out_user` selalu ditolak
- [ ] LOGIN-07 — Logout kembali ke halaman login
- [ ] LOGIN-08 — Akses cart tanpa login diarahkan ke halaman login

### Keranjang Belanja
- [ ] CART-01 — Add to cart mengubah tombol & badge
- [ ] CART-02 — Remove dari inventory menghapus badge
- [ ] CART-03 — Remove dari halaman cart menghapus item
- [ ] CART-04 — Continue Shopping kembali ke inventory

### Pengurutan
- [ ] SORT-01 — Name (A to Z)
- [ ] SORT-02 — Name (Z to A)
- [ ] SORT-03 — Price (low to high)
- [ ] SORT-04 — Price (high to low)

### Checkout
- [ ] CHK-01 — Checkout satu item sampai konfirmasi
- [ ] CHK-02 — Checkout banyak item sampai konfirmasi
- [ ] CHK-03 — Ketiga variasi field wajib kosong diblokir dengan benar
- [ ] CHK-04 — Karakter spesial diterima tanpa validasi format
- [ ] CHK-05 — Perhitungan total harga (subtotal + tax) benar

### Regresi Bug Bawaan (`known-issues.spec.ts` / `.cy.ts`)
- [ ] BUG-001 (`problem_user`) — catat apakah masih terjadi
- [ ] BUG-003 (`error_user`) — catat apakah masih terjadi
- [ ] BUG-004 (`error_user`) — catat apakah masih terjadi
- [ ] BUG-005 (`error_user`) — catat apakah masih terjadi
- [ ] BUG-006 (`error_user`) — catat apakah masih terjadi
- [ ] BUG-007 (`performance_glitch_user`) — catat apakah masih terjadi

> Bagian ini **paling penting untuk selalu dicek manual hasilnya**, bukan cuma dilihat
> pass/fail-nya — kalau status berubah (reproduksi ↔ tidak reproduksi), update
> [`05-Bug-Report/Bug_Report_SauceDemo.md`](../05-Bug-Report/Bug_Report_SauceDemo.md) dengan
> tanggal verifikasi yang baru, seperti yang terjadi di siklus 2026-08-10.

## 3. Setelah Regresi Selesai

1. Bandingkan hasil dengan run sebelumnya di
   [`04-Test-Execution/Test_Execution_Report.md`](../04-Test-Execution/Test_Execution_Report.md) —
   apakah ada test yang berubah status (baru gagal / baru lulus)?
2. Kalau ada perubahan status bug bawaan, update tabel & tanggal di
   [`05-Bug-Report/Bug_Report_SauceDemo.md`](../05-Bug-Report/Bug_Report_SauceDemo.md).
3. Kalau ada selector yang berubah di SauceDemo (test gagal karena elemen tidak ditemukan, bukan
   karena bug), update kode test di `automation/playwright/`, `automation/cypress/`, dan `automation/selenium/` — jaga ketiganya
   tetap konsisten satu sama lain.
4. Perbarui ringkasan di
   [`08-Test-Summary-Report/Test_Summary_Report.md`](../08-Test-Summary-Report/Test_Summary_Report.md)
   kalau ada perubahan signifikan pada coverage atau defect density.

## 4. Kapan Checklist Ini Dipakai

- Sebelum menandai suite "siap dipakai" oleh orang lain (mis. demo interview).
- Setelah menambah test case baru — pastikan tidak merusak test case lama.
- Berkala (mis. bulanan), untuk mendeteksi drift perilaku SauceDemo seperti yang ditemukan di
  siklus 2026-08-10 (3 dari 7 bug bawaan ternyata sudah berubah status tanpa ada perubahan apa
  pun dari sisi kita).
