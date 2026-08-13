// Connection + capabilities untuk sesi Appium.
// Target testing: Mobile Web (Chrome di Android emulator, atau Safari di iOS
// simulator) — bukan native app, karena SigmaPay Bank Demo adalah web app
// statis. Ini pola resmi Appium untuk "mobile web testing": tidak perlu
// APK/IPA, cukup arahkan browserName ke Chrome/Safari.
//
// Pilih platform lewat env var: MOBILE_PLATFORM=android (default) | ios

const platform = (process.env.MOBILE_PLATFORM || "android").toLowerCase();

const androidChrome = {
  hostname: process.env.APPIUM_HOST || "127.0.0.1",
  port: Number(process.env.APPIUM_PORT) || 4723,
  path: "/",
  logLevel: "warn",
  capabilities: {
    platformName: "Android",
    "appium:automationName": "UiAutomator2",
    "appium:deviceName": process.env.DEVICE_NAME || "Android Emulator",
    "appium:platformVersion": process.env.PLATFORM_VERSION || "13.0",
    browserName: "Chrome",
  },
};

const iosSafari = {
  hostname: process.env.APPIUM_HOST || "127.0.0.1",
  port: Number(process.env.APPIUM_PORT) || 4723,
  path: "/",
  logLevel: "warn",
  capabilities: {
    platformName: "iOS",
    "appium:automationName": "XCUITest",
    "appium:deviceName": process.env.DEVICE_NAME || "iPhone 15",
    "appium:platformVersion": process.env.PLATFORM_VERSION || "17.0",
    browserName: "Safari",
  },
};

module.exports = platform === "ios" ? iosSafari : androidChrome;
module.exports.platform = platform;
