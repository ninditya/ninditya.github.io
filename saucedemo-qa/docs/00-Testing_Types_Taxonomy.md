# Taksonomi Jenis Testing — Dipetakan ke Project SauceDemo

Melengkapi [SDLC_STLC_Concept.md](SDLC_STLC_Concept.md) dengan definisi tiap jenis testing, plus
contoh konkret dari test case & bug nyata di project ini — supaya tidak sekadar hafalan definisi.

## 1. Berdasarkan Tujuan

### Functional Testing
Menguji **apakah fitur bekerja sesuai requirement** — fokus ke "what", bukan "how".
- Positive case: login berhasil dengan kredensial benar ([LOGIN-01](../03-Test-Case/Test_Case_SauceDemo.csv)),
  checkout satu/banyak item berhasil sampai konfirmasi ([CHK-01, CHK-02](../03-Test-Case/Test_Case_SauceDemo.csv)).
- Negative case: username/password kosong ([LOGIN-04, LOGIN-05](../03-Test-Case/Test_Case_SauceDemo.csv)), field
  checkout wajib kosong ([CHK-03](../03-Test-Case/Test_Case_SauceDemo.csv)), akun terkunci ditolak
  ([LOGIN-06](../03-Test-Case/Test_Case_SauceDemo.csv)).

### Non-Functional Testing
Menguji **kualitas sistem**, bukan fitur itu sendiri:

| Jenis | Definisi | Contoh di Project Ini |
|---|---|---|
| **Performance** | Waktu respons sistem dalam batas wajar | [BUG-007](../05-Bug-Report/Bug_Report_SauceDemo.md) — dashboard `performance_glitch_user` diuji harus termuat < 5 detik. Ini satu-satunya sisi performa yang diuji; load/stress testing skala besar tidak relevan untuk demo site statis |
| **Security** | Cek celah dasar akses | Sebagian besar **tidak berlaku** — tidak ada API/backend untuk diserang (lihat Out of Scope di [Test_Plan_SauceDemo.md](../01-Test-Plan/Test_Plan_SauceDemo.md)). Yang paling dekat: [LOGIN-06](../03-Test-Case/Test_Case_SauceDemo.csv) memverifikasi akun terkunci benar-benar tidak bisa login meski kredensialnya valid — access control dasar, bukan security testing formal |
| **Usability** | Apakah tampilan & pesan error mudah dipahami | [BUG-002](../05-Bug-Report/Bug_Report_SauceDemo.md) — `visual_user` menampilkan komponen UI yang bergeser/salah (harga membengkak, ikon bergeser). Sengaja **tidak diotomasi** karena drift tampilan lebih tepat dicek visual/manual, bukan lewat assertion DOM biasa |
| **Compatibility** | Aplikasi berjalan normal di berbagai browser | **Gap yang jujur diakui**: saat ini hanya Chromium (Playwright) dan Chrome (Selenium/Cypress) yang dijalankan — `automation/playwright/playwright.config.ts` cuma punya satu project `chromium`. Menambah Firefox/WebKit adalah pengembangan lanjutan paling mudah dari sini |
| **Reliability/Recovery** | Sistem tidak crash & pulih dengan baik dari error | [BUG-003](../05-Bug-Report/Bug_Report_SauceDemo.md) — sort di akun `error_user` memicu dialog alert JavaScript "Sorting is broken!" alih-alih gagal dengan baik (graceful degradation) |

## 2. Berdasarkan Level

Sudah dibahas di [SDLC_STLC_Concept.md §4](SDLC_STLC_Concept.md#4-level-testing-yang-relevan-dengan-project-ini).
Ringkasnya: project ini murni di level **System/E2E** dan **Regression**, karena SauceDemo adalah
target uji pihak ketiga tanpa akses ke unit/integration layer-nya.

## 3. Berdasarkan Teknik

| Teknik | Definisi | Relevansi di Project Ini |
|---|---|---|
| **Black Box** | Fokus input-output, tidak peduli source code | **Satu-satunya teknik yang dipakai di sini** — semua test case ditulis murni dari observasi perilaku aplikasi (klik, isi form, baca hasil), tanpa pernah melihat source code SauceDemo |
| **White Box** | Menguji logika internal, code coverage | ❌ Tidak berlaku — tidak ada akses ke source code SauceDemo |
| **Gray Box** | Tahu sedikit "isi dalam" (skema DB, API contract) tanpa baca full source | ❌ Tidak berlaku di sini — beda dengan project QA manual berbasis backend (SQL/API), SauceDemo tidak expose lapisan itu sama sekali |

## 4. Kategori Tambahan — Sering Ditanyakan Saat Interview

| Jenis | Definisi | Contoh/Status di Project Ini |
|---|---|---|
| **Smoke Testing** | Cek cepat: build/situs layak diuji lanjut atau tidak | Secara konsep, [LOGIN-01](../03-Test-Case/Test_Case_SauceDemo.csv) (login standar berhasil) berfungsi sebagai smoke check dasar. Belum ada subset yang ditandai eksplisit sebagai "smoke suite" terpisah (mis. lewat tag) — pengembangan lanjutan yang gampang ditambahkan |
| **Sanity Testing** | Cek sempit & dalam pada satu area yang baru saja berubah | Ini persis yang terjadi saat memverifikasi ulang [BUG-004, BUG-006, BUG-007](../05-Bug-Report/Bug_Report_SauceDemo.md) satu per satu setelah dicurigai perilakunya berubah, tanpa perlu menjalankan seluruh suite |
| **Regression Testing** | Pastikan fitur lama tidak rusak setelah ada perubahan | Inti dari `known-issues.spec.ts` / `known-issues.cy.ts` — dijalankan ulang untuk memastikan bug bawaan masih (atau sudah tidak) muncul |
| **Retesting** | Menguji ulang temuan yang sama setelah "diperbaiki" | Bukan retest atas fix kita sendiri (SauceDemo bukan kode kita), tapi prinsipnya sama: retest berkala terhadap [BUG-001 s.d. BUG-007](../05-Bug-Report/Bug_Report_SauceDemo.md) untuk memastikan statusnya masih akurat — dan terbukti berguna, karena 3 di antaranya sudah berubah status |
| **Exploratory Testing** | Testing tanpa script formal, mengandalkan pengalaman tester | Tahap awal sebelum test case ditulis: eksplorasi manual struktur halaman SauceDemo (id/class selector, pesan error persis, URL tiap step checkout) sebelum dituangkan jadi kode test terstruktur |
| **Ad-hoc Testing** | Testing random tanpa dokumentasi formal | Tidak diterapkan formal di project ini — semua temuan langsung didokumentasikan, bukan dibiarkan ad-hoc |

## 5. Ringkasan: Bug Apa Ditemukan/Diverifikasi Lewat Jenis Testing Apa

| Bug | Jenis Testing | Status Reproduksi (2026-08-10) |
|---|---|---|
| [BUG-001](../05-Bug-Report/Bug_Report_SauceDemo.md) — Gambar produk salah (`problem_user`) | Functional Testing (negative/visual assertion pada `src` gambar) | ✅ Masih terjadi |
| [BUG-002](../05-Bug-Report/Bug_Report_SauceDemo.md) — Komponen UI bergeser (`visual_user`) | Usability Testing (manual/visual, belum diotomasi) | Tidak dicek otomatis |
| [BUG-003](../05-Bug-Report/Bug_Report_SauceDemo.md) — Sort memicu alert JS (`error_user`) | Reliability/Recovery Testing | ✅ Masih terjadi |
| [BUG-004](../05-Bug-Report/Bug_Report_SauceDemo.md) — Add to cart gagal sebagian (`error_user`) | Functional Testing | ❌ Sudah tidak terjadi |
| [BUG-005](../05-Bug-Report/Bug_Report_SauceDemo.md) — Field Last Name tidak bisa diisi (`error_user`) | Functional Testing | ✅ Masih terjadi |
| [BUG-006](../05-Bug-Report/Bug_Report_SauceDemo.md) — Tombol Finish tidak bisa diklik (`error_user`) | Functional Testing | ❌ Sudah tidak terjadi |
| [BUG-007](../05-Bug-Report/Bug_Report_SauceDemo.md) — Dashboard lambat (`performance_glitch_user`) | Performance Testing | ❌ Sudah tidak terjadi (di ambang batas 5 detik) |

Tabel ini bagus dijelaskan saat interview karena menunjukkan bukan cuma "saya tahu jenis-jenis
testing", tapi **kapan tiap jenis itu benar-benar dipakai dan apa hasilnya** — termasuk jujur soal
temuan yang berubah dari waktu ke waktu, bukan status statis yang dihafal sekali lalu tidak
pernah dicek ulang.
