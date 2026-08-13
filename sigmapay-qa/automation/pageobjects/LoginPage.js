const BasePage = require("./BasePage");

class LoginPage extends BasePage {
  get inputUsername() { return this.testid("input-username"); }
  get inputPassword() { return this.testid("input-password"); }
  get btnLogin() { return this.testid("btn-login"); }
  get loginError() { return this.testid("login-error"); }
  get loadingSpinner() { return this.testid("loading-spinner"); }

  async open() {
    await this.driver.url("/index.html");
  }

  async login(username, password) {
    await this.inputUsername.setValue(username);
    await this.inputPassword.setValue(password);
    await this.btnLogin.click();
  }
}

module.exports = new LoginPage();
