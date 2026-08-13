const BasePage = require("./BasePage");

class QrisPage extends BasePage {
  get qrPicker() { return this.testid("qr-picker"); }
  get paySection() { return this.testid("pay-section"); }
  get qrBlockedMsg() { return this.testid("qr-blocked-msg"); }
  get qrExpiredError() { return this.testid("qr-expired-error"); }
  get qrMismatchError() { return this.testid("qr-mismatch-error"); }

  get inputQrisNominal() { return this.testid("input-qris-nominal"); }
  get qrisNominalError() { return this.testid("qris-nominal-error"); }
  get inputQrisPin() { return this.testid("input-qris-pin"); }
  get qrisPinError() { return this.testid("qris-pin-error"); }
  get btnBayarQris() { return this.testid("btn-bayar-qris"); }
  get btnBatalQris() { return this.testid("btn-batal-qris"); }

  get qrisResultSuccess() { return this.testid("qris-result-success"); }

  async open() {
    await this.driver.url("/qris.html");
  }

  qrItem(code) {
    return this.testid(`qr-item-${code}`);
  }

  async pilihQr(code) {
    await this.qrItem(code).click();
  }

  async bayar({ nominal, pin }) {
    if (nominal !== undefined) {
      await this.inputQrisNominal.setValue(String(nominal));
    }
    await this.inputQrisPin.setValue(pin);
    await this.btnBayarQris.click();
  }
}

module.exports = new QrisPage();
