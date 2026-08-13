const { getDriver } = require("../helpers/driver");

class BasePage {
  get driver() {
    return getDriver();
  }

  testid(id) {
    return this.driver.$(`[data-testid="${id}"]`);
  }
}

module.exports = BasePage;
