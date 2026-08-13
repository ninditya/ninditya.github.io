const { expect } = require("chai");
const { startSession, endSession, resetAppState, getDriver } = require("../helpers/driver");
const LoginPage = require("../pageobjects/LoginPage");
const TransferPage = require("../pageobjects/TransferPage");
const QrisPage = require("../pageobjects/QrisPage");
const MutasiPage = require("../pageobjects/MutasiPage");

// PENTING: berbeda dari 3 spec sebelumnya, file ini SENGAJA menguji persona
// "bug" yang perilakunya cacat by design (lihat daftar lengkap di
// "SigmaPay Bank Demo/README.md" & assets/app.js). Assertion di bawah
// mengonfirmasi BUG tersebut memang terjadi — ini pola "regression test
// yang mendokumentasikan defect" (setara BUG-SGP-001..006 di
// 05-Bug-Report/Bug_Report_Sample.md), bukan test yang salah tulis.
// Kalau develover memperbaiki persona ini, test ini seharusnya mulai GAGAL
// dan perlu ditulis ulang jadi assertion "seharusnya benar".
describe("Bug Regression — persona cacat di SigmaPay Bank Demo", function () {
  before(async function () {
    await startSession();
  });

  after(async function () {
    await endSession();
  });

  beforeEach(async function () {
    await resetAppState();
  });

  async function loginAs(username, password) {
    await LoginPage.login(username, password);
    await getDriver().waitUntil(async () => (await getDriver().getUrl()).includes("dashboard.html"), {
      timeout: 8000,
      timeoutMsg: `Tidak redirect ke dashboard.html setelah login sebagai ${username}`,
    });
  }

  it("nasabah_dobel_transaksi: tombol Kirim tidak ter-disable, double-click cepat = dobel debit", async function () {
    await loginAs("nasabah_dobel_transaksi", "Sigma123!");
    await TransferPage.open();

    await TransferPage.cekRekening("8802 5555 6666"); // Melati Suryani
    await TransferPage.isiNominal(200000);
    await TransferPage.lanjut();
    await TransferPage.inputPin.setValue("123456");

    // Dua klik cepat berturut-turut TANPA menunggu request pertama selesai —
    // mereproduksi kondisi race yang jadi akar masalah BUG-SGP-001.
    await TransferPage.btnKirimTransfer.click();
    await TransferPage.btnKirimTransfer.click();

    // processTransfer() dijadwalkan via setTimeout 400ms (persona ini tidak
    // "lambat") — beri jeda lebih supaya kedua alur async selesai.
    await getDriver().pause(1500);

    await MutasiPage.open();
    expect(await MutasiPage.mutasiItem(0).isExisting()).to.be.true;
    expect(await MutasiPage.mutasiItem(1).isExisting()).to.be.true; // seharusnya cuma 1 entri kalau tidak ada bug
  });

  it("nasabah_status_ambigu: UI klaim 'Transfer Gagal' padahal Mutasi mencatat status Berhasil", async function () {
    await loginAs("nasabah_status_ambigu", "Sigma123!");
    await TransferPage.open();

    await TransferPage.transfer({ norek: "8802 5555 6666", nominal: 150000, pin: "123456" });

    await TransferPage.transferResultError.waitForDisplayed({ timeout: 3000 });
    expect(await TransferPage.transferResultError.getText()).to.include("Transfer Gagal");

    await MutasiPage.open();
    expect(await MutasiPage.mutasiStatus(0).getText()).to.equal("Berhasil");
  });

  it("nasabah_interbank_macet: transfer BI-FAST macet di status Diproses tanpa reversal", async function () {
    await loginAs("nasabah_interbank_macet", "Sigma123!");
    await TransferPage.open();

    await TransferPage.transfer({
      jenis: "interbank",
      norek: "8802 5555 6666",
      nominal: 300000,
      pin: "123456",
    });

    await TransferPage.transferResultPending.waitForDisplayed({ timeout: 3000 });

    await MutasiPage.open();
    expect(await MutasiPage.mutasiStatus(0).getText()).to.equal("Diproses");
  });

  it("nasabah_qris_kadaluwarsa: QR expired (QRIS003) tetap bisa dibayar — guard normal ter-bypass", async function () {
    await loginAs("nasabah_qris_kadaluwarsa", "Sigma123!");
    await QrisPage.open();

    await QrisPage.pilihQr("QRIS003");
    // Untuk persona normal, ini akan diblokir (lihat 03-qris.spec.js).
    // Untuk persona ini, pay-form seharusnya TETAP tampil.
    expect(await QrisPage.paySection.$('[data-testid="pay-form"]').isDisplayed()).to.be.true;

    await QrisPage.bayar({ nominal: 50000, pin: "123456" });
    await QrisPage.qrisResultSuccess.waitForDisplayed({ timeout: 3000 });
  });

  it("nasabah_qris_merchant_salah: QR Merchant ID mismatch (QRIS004) tetap diproses tanpa peringatan", async function () {
    await loginAs("nasabah_qris_merchant_salah", "Sigma123!");
    await QrisPage.open();

    await QrisPage.pilihQr("QRIS004");
    expect(await QrisPage.paySection.$('[data-testid="pay-form"]').isDisplayed()).to.be.true;

    await QrisPage.bayar({ pin: "123456" }); // QRIS004 dinamis, nominal sudah terisi
    await QrisPage.qrisResultSuccess.waitForDisplayed({ timeout: 3000 });
  });

  it("nasabah_nominal_negatif: field nominal menerima input negatif tanpa validasi", async function () {
    await loginAs("nasabah_nominal_negatif", "Sigma123!");
    await TransferPage.open();

    await TransferPage.cekRekening("8802 5555 6666");
    await TransferPage.isiNominal(-100000);

    // Pada persona normal, ini akan memicu nominal-error dan tombol Lanjut
    // tetap disabled (lihat 02-transfer.spec.js). Di sini validasi ter-bypass.
    expect(await TransferPage.nominalError.isDisplayed()).to.be.false;
    expect(await TransferPage.btnLanjutTransfer.isEnabled()).to.be.true;
  });
});
