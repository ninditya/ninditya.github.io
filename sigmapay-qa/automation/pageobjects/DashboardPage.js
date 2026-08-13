const BasePage = require("./BasePage");

class DashboardPage extends BasePage {
  get saldoValue() { return this.testid("saldo-value"); }
  get accountNo() { return this.testid("account-no"); }
  get navTransfer() { return this.testid("nav-transfer"); }
  get navQris() { return this.testid("nav-qris"); }
  get navMutasi() { return this.testid("nav-mutasi"); }
  get navProfil() { return this.testid("nav-profil"); }
  get btnLogout() { return this.testid("btn-logout"); }
  get recentMutasi() { return this.testid("recent-mutasi"); }
}

module.exports = new DashboardPage();
