/* SigmaPay Bank Demo — shared app logic (no framework, no build step)
   Test-target app for QA automation practice, in the spirit of saucedemo.com. */

const PIN_VALID = "123456";
const QRIS_LIMIT_PER_TRX = 10000000;

/* ---------- Test user directory (documented in README.md) ---------- */
const USERS = {
  nasabah_normal: {
    password: "Sigma123!", name: "Rangga Wibisono", accountNo: "8802 1111 2222",
    balance: 5000000, locked: false, slow: false, bug: null,
  },
  nasabah_terkunci: {
    password: "Sigma123!", name: "Akun Terkunci", accountNo: "8802 3333 4444",
    balance: 0, locked: true, slow: false, bug: null,
  },
  nasabah_saldo_kosong: {
    password: "Sigma123!", name: "Melati Suryani", accountNo: "8802 5555 6666",
    balance: 0, locked: false, slow: false, bug: null,
  },
  nasabah_lambat: {
    password: "Sigma123!", name: "Bram Setiawan", accountNo: "8802 4567 8901",
    balance: 2500000, locked: false, slow: true, bug: null,
  },
  nasabah_dobel_transaksi: {
    password: "Sigma123!", name: "Yusuf Hakim", accountNo: "8802 7777 8888",
    balance: 3000000, locked: false, slow: false, bug: "double_debit",
  },
  nasabah_status_ambigu: {
    password: "Sigma123!", name: "Farah Amelia", accountNo: "8802 9999 0000",
    balance: 2000000, locked: false, slow: false, bug: "status_ambigu",
  },
  nasabah_interbank_macet: {
    password: "Sigma123!", name: "Galih Purnomo", accountNo: "8802 6543 2109",
    balance: 3500000, locked: false, slow: false, bug: "interbank_macet",
  },
  nasabah_qris_kadaluwarsa: {
    password: "Sigma123!", name: "Nadia Kirana", accountNo: "8802 8765 4321",
    balance: 1500000, locked: false, slow: false, bug: "qris_expired",
  },
  nasabah_qris_merchant_salah: {
    password: "Sigma123!", name: "Wulan Ardianti", accountNo: "8802 2468 1357",
    balance: 1800000, locked: false, slow: false, bug: "qris_merchant_mismatch",
  },
  nasabah_nominal_negatif: {
    password: "Sigma123!", name: "Doni Saputra", accountNo: "8802 1234 5678",
    balance: 4000000, locked: false, slow: false, bug: "negative_nominal",
  },
};

/* ---------- Transfer destination directory ---------- */
const RECIPIENTS = {
  "8802 1111 2222": { name: "Rangga Wibisono", status: "active" },
  "8802 5555 6666": { name: "Melati Suryani", status: "active" },
  "8802 7777 8888": { name: "Yusuf Hakim", status: "active" },
  "8802 9999 0000": { name: "Farah Amelia", status: "active" },
  "8802 6543 2109": { name: "Galih Purnomo", status: "active" },
  "8802 0000 0001": { name: "Toko Sinar Jaya", status: "blocked" },
};

/* ---------- QRIS merchant directory (no camera — pick from list) ---------- */
const MERCHANTS = {
  QRIS001: {
    name: "Kedai Kopi Nusantara", type: "dinamis", nominal: 25000,
    expired: false, merchantIdMismatch: false,
  },
  QRIS002: {
    name: "Toko Sembako Makmur", type: "statis", nominal: null,
    expired: false, merchantIdMismatch: false,
  },
  QRIS003: {
    name: "Percetakan Warna Digital (QR kedaluwarsa)", type: "statis", nominal: null,
    expired: true, merchantIdMismatch: false,
  },
  QRIS004: {
    name: "Toko Elektronik Jaya (Merchant ID tidak cocok)", type: "dinamis", nominal: 450000,
    expired: false, merchantIdMismatch: true,
  },
};

/* ---------- Session helpers (sessionStorage = state resets per browser tab/session) ---------- */
const SESSION_KEY = "sigmapay_demo_session";

function getSession() {
  const raw = sessionStorage.getItem(SESSION_KEY);
  return raw ? JSON.parse(raw) : null;
}

function setSession(session) {
  sessionStorage.setItem(SESSION_KEY, JSON.stringify(session));
}

function clearSession() {
  sessionStorage.removeItem(SESSION_KEY);
}

function requireAuth() {
  const session = getSession();
  if (!session) {
    window.location.href = "index.html";
    return null;
  }
  return session;
}

/* ---------- Utilities ---------- */
function formatRupiah(n) {
  return "Rp " + Number(n).toLocaleString("id-ID");
}

function nowLabel() {
  const d = new Date();
  return d.toLocaleString("id-ID", { dateStyle: "medium", timeStyle: "short" });
}

function addMutasi(session, entry) {
  session.mutasi = session.mutasi || [];
  session.mutasi.unshift(entry);
}

/* Artificial delay for the "nasabah_lambat" persona — used to practice
   testing loading states / client-side timeout handling. */
function withDelay(session, fn) {
  const spinner = document.querySelector('[data-testid="loading-spinner"]');
  if (session.slow) {
    if (spinner) spinner.hidden = false;
    setTimeout(() => {
      if (spinner) spinner.hidden = true;
      fn();
    }, 3000);
  } else {
    fn();
  }
}

/* ---------- Shared topbar (rendered into <div id="topbar"></div>) ---------- */
function renderTopbar(activePage) {
  const session = getSession();
  const el = document.getElementById("topbar");
  if (!el || !session) return;

  const links = [
    { href: "dashboard.html", id: "dashboard", label: "Beranda" },
    { href: "transfer.html", id: "transfer", label: "Transfer" },
    { href: "qris.html", id: "qris", label: "QRIS" },
    { href: "mutasi.html", id: "mutasi", label: "Mutasi" },
    { href: "profil.html", id: "profil", label: "Profil" },
  ];

  el.innerHTML = `
    <div class="topbar">
      <div class="topbar-brand">SigmaPay <span>Bank Demo</span></div>
      <nav class="topbar-nav" data-testid="nav-menu">
        ${links
          .map(
            (l) =>
              `<a href="${l.href}" data-testid="nav-${l.id}" class="${l.id === activePage ? "active" : ""}">${l.label}</a>`
          )
          .join("")}
      </nav>
      <div class="topbar-user">
        <span data-testid="topbar-username">${session.name}</span>
        <button type="button" data-testid="btn-logout" onclick="doLogout()">Keluar</button>
      </div>
    </div>`;
}

function doLogout() {
  clearSession();
  window.location.href = "index.html";
}
