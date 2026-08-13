const { expect } = require("chai");
const { startSession, endSession, resetAppState, getDriver, BASE_URL } = require("../helpers/driver");
const { formatRupiah } = require("../helpers/format");
const LoginPage = require("../pageobjects/LoginPage");
const DashboardPage = require("../pageobjects/DashboardPage");

// Cakupan: skenario login dasar (positive/negative/locked/slow) mengikuti
// daftar akun uji di "SigmaPay Bank Demo/README.md".
describe("Login — SigmaPay Bank Demo", function () {
  before(async function () {
    await startSession();
  });

  after(async function () {
    await endSession();
  });

  beforeEach(async function () {
    await resetAppState();
  });

  it("login sukses dengan akun normal, redirect ke Beranda dengan saldo & no. rekening benar", async function () {
    await LoginPage.login("nasabah_normal", "Sigma123!");

    await getDriver().waitUntil(async () => (await getDriver().getUrl()).includes("dashboard.html"), {
      timeout: 5000,
      timeoutMsg: "Tidak redirect ke dashboard.html setelah login normal",
    });

    expect(await DashboardPage.saldoValue.getText()).to.equal(formatRupiah(5000000));
    expect(await DashboardPage.accountNo.getText()).to.equal("8802 1111 2222");
  });

  it("login gagal dengan password salah — tetap di halaman login dan tampilkan pesan error", async function () {
    await LoginPage.login("nasabah_normal", "PasswordSalah!");

    await LoginPage.loginError.waitForDisplayed({ timeout: 3000 });
    expect(await LoginPage.loginError.getText()).to.equal("Username atau password salah.");
    expect(await getDriver().getUrl()).to.equal(`${BASE_URL}/index.html`);
  });

  it("akun terkunci (nasabah_terkunci) selalu ditolak walau password benar", async function () {
    await LoginPage.login("nasabah_terkunci", "Sigma123!");

    await LoginPage.loginError.waitForDisplayed({ timeout: 3000 });
    expect(await LoginPage.loginError.getText()).to.include("Akun terkunci");
  });

  it("akun lambat (nasabah_lambat) menampilkan loading-spinner sebelum akhirnya redirect", async function () {
    await LoginPage.login("nasabah_lambat", "Sigma123!");

    // Persona ini punya delay buatan ~3 detik (lihat USERS.nasabah_lambat.slow
    // di assets/app.js) — spinner harus tampil selama proses berlangsung.
    await LoginPage.loadingSpinner.waitForDisplayed({ timeout: 1000 });

    await getDriver().waitUntil(async () => (await getDriver().getUrl()).includes("dashboard.html"), {
      timeout: 6000,
      timeoutMsg: "Tidak redirect ke dashboard.html setelah delay akun lambat selesai",
    });
  });
});
