const { expect } = require("chai");
const { startSession, endSession, resetAppState, getDriver } = require("../helpers/driver");
const { formatRupiah } = require("../helpers/format");
const LoginPage = require("../pageobjects/LoginPage");
const TransferPage = require("../pageobjects/TransferPage");

async function loginAs(username, password) {
  await LoginPage.login(username, password);
  await getDriver().waitUntil(async () => (await getDriver().getUrl()).includes("dashboard.html"), {
    timeout: 8000,
    timeoutMsg: `Tidak redirect ke dashboard.html setelah login sebagai ${username}`,
  });
}

// Cakupan: setara TC-TRF-001 (transfer intrabank sukses), TC-TRF-014
// (transfer ke rekening sendiri → "Pindah Buku"), dan skenario negative
// (saldo tidak cukup, rekening diblokir, rekening tidak ditemukan) dari
// 03-Test-Case/Test_Case_Transfer_QRIS.csv, diimplementasikan terhadap
// SigmaPay Bank Demo (bukan reproduksi identik — lihat README demo).
describe("Transfer Dana — SigmaPay Bank Demo", function () {
  before(async function () {
    await startSession();
  });

  after(async function () {
    await endSession();
  });

  beforeEach(async function () {
    await resetAppState();
  });

  it("transfer intrabank sukses — saldo terpotong sesuai nominal (tanpa biaya admin)", async function () {
    await loginAs("nasabah_normal", "Sigma123!");
    await TransferPage.open();

    await TransferPage.transfer({
      jenis: "intrabank",
      norek: "8802 5555 6666", // Melati Suryani
      nominal: 500000,
      pin: "123456",
    });

    await TransferPage.transferResultSuccess.waitForDisplayed({ timeout: 3000 });
    const text = await TransferPage.transferResultSuccess.getText();
    expect(text).to.include(`Saldo baru: ${formatRupiah(5000000 - 500000)}`);
  });

  it("transfer ditolak saat saldo tidak mencukupi (nasabah_saldo_kosong)", async function () {
    await loginAs("nasabah_saldo_kosong", "Sigma123!");
    await TransferPage.open();

    await TransferPage.cekRekening("8802 1111 2222"); // Rangga Wibisono, akun valid
    await TransferPage.isiNominal(100000);

    await TransferPage.nominalError.waitForDisplayed({ timeout: 3000 });
    expect(await TransferPage.nominalError.getText()).to.equal("Saldo tidak mencukupi.");
    expect(await TransferPage.btnLanjutTransfer.isEnabled()).to.be.false;
  });

  it("transfer ke rekening sendiri ditolak, arahkan ke menu Pindah Buku", async function () {
    await loginAs("nasabah_normal", "Sigma123!");
    await TransferPage.open();

    await TransferPage.cekRekening("8802 1111 2222"); // no. rekening nasabah_normal sendiri

    const errorBox = TransferPage.testid("inquiry-error");
    await errorBox.waitForDisplayed({ timeout: 3000 });
    expect(await errorBox.getText()).to.include("Gunakan menu Pindah Buku");
  });

  it("transfer ke rekening yang diblokir ditolak", async function () {
    await loginAs("nasabah_normal", "Sigma123!");
    await TransferPage.open();

    await TransferPage.cekRekening("8802 0000 0001"); // Toko Sinar Jaya, status diblokir

    const errorBox = TransferPage.testid("inquiry-error");
    await errorBox.waitForDisplayed({ timeout: 3000 });
    expect(await errorBox.getText()).to.include("status diblokir");
  });

  it("transfer ke rekening yang tidak terdaftar menampilkan 'Rekening tidak ditemukan'", async function () {
    await loginAs("nasabah_normal", "Sigma123!");
    await TransferPage.open();

    await TransferPage.cekRekening("8802 0000 9999"); // tidak ada di RECIPIENTS

    const errorBox = TransferPage.testid("inquiry-error");
    await errorBox.waitForDisplayed({ timeout: 3000 });
    expect(await errorBox.getText()).to.equal("Rekening tidak ditemukan.");
  });
});
