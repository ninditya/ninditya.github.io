// Replika persis fungsi formatRupiah() di SigmaPay Bank Demo/assets/app.js,
// supaya assertion di test bisa hitung nilai yang diharapkan (mis. saldo
// setelah transfer) tanpa hardcode string yang gampang typo.
function formatRupiah(n) {
  return "Rp " + Number(n).toLocaleString("id-ID");
}

module.exports = { formatRupiah };
