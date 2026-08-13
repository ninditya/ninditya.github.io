# Automation Suite — Appium + WebdriverIO + Mocha + Chai

Suite automation UI untuk [`SigmaPay Bank Demo`](<../SigmaPay Bank Demo/README.md>), pakai stack yang sering diminta di loker QA banking: **Appium** (server automation), **Mocha** (test runner), **Chai** (assertion library). Client library yang bicara ke Appium adalah **WebdriverIO** (`webdriverio`, dipakai dalam mode *standalone/programmatic* — bukan lewat `@wdio/cli`) karena itu cara resmi Node.js berkomunikasi dengan Appium server; `wd` (client lama) sudah deprecated.

> **Catatan jujur:** kode di folder ini **sudah ditulis lengkap tapi belum pernah dijalankan** terhadap Appium server/emulator sungguhan (lingkungan development saat ini tidak punya Android SDK/Xcode/Appium terpasang). Locator (`data-testid`) dan alur bisnis diverifikasi manual dengan membaca ulang source `SigmaPay Bank Demo/*.html` dan `assets/app.js` baris per baris supaya seakurat mungkin, tapi **belum ada bukti hasil eksekusi (screenshot/report) yang bisa ditunjukkan**. Kalau ditanya di interview, jawab jujur: "saya tulis test suite-nya lengkap dengan page object pattern, tapi belum sempat eksekusi end-to-end di emulator" — bukan "sudah saya jalankan dan semua pass". Ikuti [Setup & Run](#setup--run) untuk memverifikasi sendiri.

## Kenapa Appium untuk web statis?

`SigmaPay Bank Demo` adalah HTML/CSS/JS statis, bukan app native — jadi Appium dipakai dalam mode **Mobile Web Testing** (fitur resmi Appium): mengarahkan `browserName` ke Chrome (Android) atau Safari (iOS) tanpa APK/IPA apa pun. Ini valid dan memang salah satu use case utama Appium, tapi kalau tujuannya murni web testing tanpa kebutuhan device/emulator, `WebdriverIO`/`Selenium`/`Playwright` langsung ke browser desktop jauh lebih ringan setup-nya — Appium baru bernilai tambah kalau memang butuh menguji perilaku di viewport/browser mobile sungguhan (device fragmentation, seperti yang biasanya jadi alasan tim banking pakai Appium).

## Arsitektur

```
Mocha (test runner) ─┬─ Page Objects (pageobjects/*.js)
                      │        │
                      │        ▼
                      └─ WebdriverIO client ──WebDriver protocol──► Appium Server ──► Chrome/Safari (emulator/simulator)
                                                                                              │
Chai (assertion)  ◄── hasil getText()/isDisplayed()/dst.                                     ▼
                                                                                     SigmaPay Bank Demo
                                                                                   (http-server, localhost:8080)
```

## Struktur Folder

| Path | Isi |
|---|---|
| `config/capabilities.js` | Koneksi ke Appium server + capabilities (Android/Chrome atau iOS/Safari, pilih via env var) |
| `helpers/driver.js` | Start/stop sesi WebdriverIO, base URL, reset state (`sessionStorage.clear()`) |
| `helpers/format.js` | Replika `formatRupiah()` dari app supaya assertion saldo tidak hardcode string |
| `pageobjects/*.js` | Page Object Model — satu class per halaman, locator berbasis `data-testid` |
| `test/01-login.spec.js` | Login: normal, password salah, akun terkunci, akun lambat (loading state) |
| `test/02-transfer.spec.js` | Transfer: sukses, saldo tidak cukup, rekening sendiri, rekening diblokir, rekening tidak ditemukan |
| `test/03-qris.spec.js` | QRIS: bayar sukses, QR expired ditolak, Merchant ID mismatch ditolak, limit per transaksi |
| `test/04-bug-regression.spec.js` | Mendokumentasikan 6 persona "bug" (double debit, status ambigu, dst.) — assertion sengaja membuktikan bug-nya terjadi, bukan salah tulis |

## Setup & Run

### Prasyarat
1. Node.js 18+
2. Salah satu dari:
   - **Android**: Android Studio + 1 AVD (emulator) yang sudah dijalankan, `ANDROID_HOME` ter-set
   - **iOS** (khusus macOS): Xcode + 1 Simulator
3. Appium 2.x + driver yang sesuai (belum termasuk otomatis di `npm install` — Appium driver di-install lewat CLI Appium sendiri, bukan npm package biasa)

### Langkah

```bash
cd "12-Automation-Appium"
npm install

# Sekali saja, install driver Appium sesuai platform:
npx appium driver install uiautomator2   # untuk Android
# atau
npx appium driver install xcuitest       # untuk iOS

# Terminal 1 — serve SigmaPay Bank Demo sebagai static server
npm run serve:app

# Terminal 2 — jalankan Appium server
npm run appium

# Terminal 3 — pastikan emulator/simulator sudah menyala, lalu jalankan test
npm test
```

### Environment Variables

| Variabel | Default | Keterangan |
|---|---|---|
| `MOBILE_PLATFORM` | `android` | `android` atau `ios` |
| `APPIUM_HOST` | `127.0.0.1` | Host Appium server |
| `APPIUM_PORT` | `4723` | Port Appium server |
| `DEVICE_NAME` | `Android Emulator` / `iPhone 15` | Nama device/AVD/simulator |
| `PLATFORM_VERSION` | `13.0` / `17.0` | Versi OS emulator/simulator |
| `APP_BASE_URL` | `http://10.0.2.2:8080` (Android) / `http://127.0.0.1:8080` (iOS) | URL tempat `SigmaPay Bank Demo` di-serve |

> **Gotcha yang perlu diketahui:** dari dalam Android emulator, `localhost` menunjuk ke emulator itu sendiri — harus pakai `10.0.2.2` untuk menjangkau mesin host (sudah di-default-kan di `helpers/driver.js`, tapi kalau pakai real device di jaringan yang sama, override `APP_BASE_URL` dengan IP LAN mesin host).

## Cakupan Test vs Dokumen Lain

| Spec | Setara dengan |
|---|---|
| `01-login.spec.js` | Prasyarat login di seluruh `TC-TRF-*` (`03-Test-Case`) |
| `02-transfer.spec.js` | TC-TRF-001 (transfer sukses), TC-TRF-014 (transfer ke rekening sendiri) |
| `03-qris.spec.js` | TC-QRIS-004 (QR expired), TC-QRIS-009 (Merchant ID mismatch) |
| `04-bug-regression.spec.js` | BUG-SGP-001, 002, 003, 004, 005, 006 (`05-Bug-Report/Bug_Report_Sample.md`) — versi implementasi standalone di Bank Demo, bukan reproduksi identik dari prototype `.dc.html` |

## Batasan yang Perlu Disadari

- **Belum dieksekusi** terhadap Appium/emulator sungguhan — lihat catatan jujur di atas.
- Test di `04-bug-regression.spec.js` yang melibatkan double-click cepat (`nasabah_dobel_transaksi`) bergantung pada timing race condition di sisi client — bisa jadi *flaky* tergantung kecepatan WebDriver round-trip vs `setTimeout` 400ms di kode aplikasi; kalau flaky, coba perbesar `getDriver().pause(...)` di spec tersebut atau jalankan ulang.
- Tidak ada backend/API sungguhan di baliknya (state di `sessionStorage`) — ini murni UI automation, bukan API automation. Untuk API testing, lihat [`06-API-Testing`](../06-API-Testing/Postman_API_Test_Notes.md).
- Sama seperti folder lain di project ini: **jangan klaim ini sebagai pengalaman production Appium** — posisikan sebagai "saya bangun sendiri test suite-nya dari nol, termasuk page object pattern & reset state strategy", bukan "saya maintain automation suite ini di tempat kerja".
