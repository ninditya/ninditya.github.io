const BasePage = require("./BasePage");

class ProfilPage extends BasePage {
  get profilNama() { return this.testid("profil-nama"); }
  get profilUsername() { return this.testid("profil-username"); }
  get profilRekening() { return this.testid("profil-rekening"); }
  get btnResetDemo() { return this.testid("btn-reset-demo"); }
  get btnLogoutProfil() { return this.testid("btn-logout-profil"); }

  async open() {
    await this.driver.url("/profil.html");
  }
}

module.exports = new ProfilPage();
