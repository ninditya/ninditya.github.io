const BasePage = require("./BasePage");

class TransferPage extends BasePage {
  get selectJenisTransfer() { return this.testid("select-jenis-transfer"); }
  get inputRekeningTujuan() { return this.testid("input-rekening-tujuan"); }
  get btnCekRekening() { return this.testid("btn-cek-rekening"); }
  get inquiryResult() { return this.testid("inquiry-result"); }
  get inputNominal() { return this.testid("input-nominal"); }
  get nominalError() { return this.testid("nominal-error"); }
  get btnLanjutTransfer() { return this.testid("btn-lanjut-transfer"); }

  get inputPin() { return this.testid("input-pin"); }
  get pinError() { return this.testid("pin-error"); }
  get btnKirimTransfer() { return this.testid("btn-kirim-transfer"); }
  get btnBatalTransfer() { return this.testid("btn-batal-transfer"); }

  get transferResultSuccess() { return this.testid("transfer-result-success"); }
  get transferResultError() { return this.testid("transfer-result-error"); }
  get transferResultPending() { return this.testid("transfer-result-pending"); }

  async open() {
    await this.driver.url("/transfer.html");
  }

  async pilihJenis(jenis) {
    await this.selectJenisTransfer.selectByAttribute("value", jenis);
  }

  async cekRekening(norek) {
    await this.inputRekeningTujuan.setValue(norek);
    await this.btnCekRekening.click();
  }

  async isiNominal(nominal) {
    await this.inputNominal.setValue(String(nominal));
  }

  async lanjut() {
    await this.btnLanjutTransfer.click();
  }

  async kirim(pin) {
    await this.inputPin.setValue(pin);
    await this.btnKirimTransfer.click();
  }

  // Alur lengkap positive path: cek rekening -> isi nominal -> lanjut -> PIN -> kirim
  async transfer({ jenis = "intrabank", norek, nominal, pin }) {
    if (jenis !== "intrabank") await this.pilihJenis(jenis);
    await this.cekRekening(norek);
    await this.isiNominal(nominal);
    await this.lanjut();
    await this.kirim(pin);
  }
}

module.exports = new TransferPage();
