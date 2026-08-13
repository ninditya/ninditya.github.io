const { expect } = require("chai");
const { startSession, endSession, resetAppState, getDriver } = require("../helpers/driver");
const { formatRupiah } = require("../helpers/format");
const LoginPage = require("../pageobjects/LoginPage");
const QrisPage = require("../pageobjects/QrisPage");

async function loginAs(username, password) {
  await LoginPage.login(username, password);
  await getDriver().waitUntil(async () => (await getDriver().getUrl()).includes("dashboard.html"), {
    timeout: 8000,
    timeoutMsg: `Tidak redirect ke dashboard.html setelah login sebagai ${username}`,
  });
}

// Cakupan: setara TC-QRIS-004 (QR expired ditolak), TC-QRIS-009 (Merchant ID
// mismatch ditolak) dari 03-Test-Case, plus QR dinamis/statis normal &
// validasi limit, terhadap persona nasabah_normal di SigmaPay Bank Demo
// (di persona ini SEMUA guard aktif — kontras dengan skenario bug di
// 04-bug-regression.spec.js).
describe("QRIS Payment — SigmaPay Bank Demo", function () {
  before(async function () {
    await startSession();
  });

  after(async function () {
    await endSession();
  });

  beforeEach(async function () {
    await resetAppState();
    await loginAs("nasabah_normal", "Sigma123!");
    await QrisPage.open();
  });

  it("bayar QR dinamis valid (QRIS001) sukses, saldo terpotong sesuai nominal QR", async function () {
    await QrisPage.pilihQr("QRIS001"); // Kedai Kopi Nusantara, dinamis Rp 25.000
    await QrisPage.bayar({ pin: "123456" }); // nominal sudah terisi otomatis, tidak perlu diisi ulang

    await QrisPage.qrisResultSuccess.waitForDisplayed({ timeout: 3000 });
    const text = await QrisPage.qrisResultSuccess.getText();
    expect(text).to.include(`Saldo baru: ${formatRupiah(5000000 - 25000)}`);
  });

  it("QR kedaluwarsa (QRIS003) ditolak sebelum tahap pembayaran — setara TC-QRIS-004", async function () {
    await QrisPage.pilihQr("QRIS003");

    await QrisPage.qrExpiredError.waitForDisplayed({ timeout: 3000 });
    expect(await QrisPage.qrExpiredError.getText()).to.include("kedaluwarsa");
    // isDisplayed() resolves false untuk elemen yang hidden/tidak ada di DOM,
    // tidak perlu try/catch — pay-form disembunyikan lewat blockedBox guard.
    expect(await QrisPage.paySection.$('[data-testid="pay-form"]').isDisplayed()).to.be.false;
  });

  it("QR dengan Merchant ID tidak cocok (QRIS004) ditolak — setara TC-QRIS-009", async function () {
    await QrisPage.pilihQr("QRIS004");

    await QrisPage.qrMismatchError.waitForDisplayed({ timeout: 3000 });
    expect(await QrisPage.qrMismatchError.getText()).to.include("tidak sesuai data terdaftar");
  });

  it("nominal QR statis melebihi limit Rp 10.000.000 per transaksi ditolak", async function () {
    await QrisPage.pilihQr("QRIS002"); // Toko Sembako Makmur, statis, nominal manual
    await QrisPage.bayar({ nominal: 15000000, pin: "123456" });

    await QrisPage.qrisNominalError.waitForDisplayed({ timeout: 3000 });
    expect(await QrisPage.qrisNominalError.getText()).to.include("Melebihi limit QRIS");
  });
});
