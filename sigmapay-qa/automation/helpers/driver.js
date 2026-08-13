const { remote } = require("webdriverio");
const connection = require("../config/capabilities");

// Gotcha yang sering kejebak pemula: dari dalam Android emulator, "localhost"
// menunjuk ke emulator itu sendiri, BUKAN mesin host. Harus pakai 10.0.2.2.
// iOS Simulator sebaliknya berbagi network stack dengan host, jadi 127.0.0.1
// langsung berfungsi. Override manual via APP_BASE_URL kalau setup berbeda
// (mis. real device di jaringan yang sama, atau port lain).
const DEFAULT_BASE_URL = {
  android: "http://10.0.2.2:8080",
  ios: "http://127.0.0.1:8080",
};

const BASE_URL =
  process.env.APP_BASE_URL || DEFAULT_BASE_URL[connection.platform] || "http://localhost:8080";

let driver;

async function startSession() {
  driver = await remote({ ...connection, baseUrl: BASE_URL });
  return driver;
}

async function endSession() {
  if (driver) {
    await driver.deleteSession();
    driver = undefined;
  }
}

function getDriver() {
  if (!driver) {
    throw new Error("Driver belum diinisialisasi — panggil startSession() dulu di hook before().");
  }
  return driver;
}

// SigmaPay Bank Demo menyimpan state di sessionStorage (lihat assets/app.js).
// Reload halaman saja TIDAK membersihkannya (sessionStorage bertahan selama
// tab/context yang sama) — harus dibersihkan eksplisit supaya tiap test
// mulai dari kondisi bersih (saldo & mutasi awal), idempotent antar test.
async function resetAppState() {
  await getDriver().url("/index.html");
  await getDriver().execute(() => {
    window.sessionStorage.clear();
  });
}

module.exports = { startSession, endSession, getDriver, resetAppState, BASE_URL };
