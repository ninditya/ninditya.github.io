const BasePage = require("./BasePage");

class MutasiPage extends BasePage {
  get mutasiList() { return this.testid("mutasi-list"); }
  get mutasiEmpty() { return this.testid("mutasi-empty"); }

  async open() {
    await this.driver.url("/mutasi.html");
  }

  mutasiItem(index) {
    return this.testid(`mutasi-item-${index}`);
  }

  mutasiStatus(index) {
    return this.testid(`mutasi-status-${index}`);
  }

  mutasiAmount(index) {
    return this.testid(`mutasi-amount-${index}`);
  }
}

module.exports = new MutasiPage();
