# API Testing Notes — Postman (Transfer & QRIS)

Dokumentasi ini merepresentasikan struktur **Postman Collection** yang dipakai untuk menguji API di balik UI. Ini bagian yang membedakan kandidat "hanya bisa klik UI" dengan kandidat berpengalaman 3-5 tahun yang diminta di loker.

## 1. Struktur Collection

```
SigmaPay QA Collection
├── Auth
│   └── POST /auth/login          → generate token untuk request selanjutnya
├── Transfer
│   ├── POST /transfer/inquiry    → cek nama pemilik rekening tujuan
│   ├── POST /transfer            → eksekusi transfer
│   └── GET  /transaction/status  → cek status transaksi by transactionId
├── QRIS
│   ├── POST /qris/decode         → decode isi QR (merchant id, nominal, expiry)
│   └── POST /qris/pay            → eksekusi pembayaran QRIS
└── Environment Variables
    ├── base_url = https://api-qa.sigmapay.dummy
    ├── token     = {{auto-set dari response login}}
    └── device_id = QA-DEVICE-001
```

## 2. Contoh Request/Response — POST /transfer

**Request**
```http
POST {{base_url}}/v1/transfer
Authorization: Bearer {{token}}
Content-Type: application/json

{
  "sourceAccount": "1010101010",
  "destinationAccount": "2020202020",
  "destinationBankCode": "SGMA",
  "amount": 500000,
  "note": "Bayar patungan",
  "idempotencyKey": "TRX-QA-0001"
}
```

**Response — Sukses (200)**
```json
{
  "status": "SUCCESS",
  "transactionId": "TRX20260803000123",
  "amount": 500000,
  "adminFee": 0,
  "timestamp": "2026-08-03T10:15:00+07:00"
}
```

**Response — Saldo Tidak Cukup (400)**
```json
{
  "status": "FAILED",
  "errorCode": "INSUFFICIENT_BALANCE",
  "message": "Saldo tidak mencukupi untuk melakukan transaksi ini"
}
```

## 3. Test Script (Postman "Tests" tab) — Contoh Assertion

```javascript
// Dijalankan otomatis setelah request POST /transfer terkirim

pm.test("Status code harus 200 untuk transfer valid", function () {
    pm.response.to.have.status(200);
});

pm.test("Response memiliki transactionId", function () {
    const body = pm.response.json();
    pm.expect(body).to.have.property("transactionId");
    pm.expect(body.transactionId).to.match(/^TRX/);
});

pm.test("Amount pada response sesuai request", function () {
    const req = JSON.parse(pm.request.body.raw);
    const body = pm.response.json();
    pm.expect(body.amount).to.eql(req.amount);
});

pm.test("Response time di bawah 3 detik (sanity check)", function () {
    pm.expect(pm.response.responseTime).to.be.below(3000);
});

// Simpan transactionId ke environment variable untuk dipakai di request GET /transaction/status
if (pm.response.code === 200) {
    pm.environment.set("last_transaction_id", pm.response.json().transactionId);
}
```

## 4. Skenario Negative Testing di Level API (Sering Terlewat kalau Hanya Test via UI)

| Skenario | Cara Uji di Postman | Expected |
|---|---|---|
| Token expired/invalid | Ganti header `Authorization` dengan token acak/expired | HTTP 401 Unauthorized |
| Field wajib tidak dikirim (`amount` dihapus dari body) | Hapus field dari JSON body | HTTP 400 dengan pesan validasi jelas, bukan 500 |
| Tipe data salah (`amount` dikirim sebagai string `"lima ratus ribu"`) | Ubah tipe data di body | HTTP 400, bukan crash/500 |
| Idempotency key sama dikirim 2x (simulasi double submit dari UI) | Kirim request `POST /transfer` 2x dengan `idempotencyKey` sama | Request kedua ditolak/mengembalikan response transaksi pertama, **bukan** transaksi baru — ini validasi otomatis untuk BUG-SGP-001 |
| SQL Injection payload di field `note` | `"note": "' OR '1'='1"` | Tidak menyebabkan error 500 / data corruption; input di-treat sebagai string biasa |
| Request tanpa `Content-Type: application/json` | Hapus header | HTTP 400/415, bukan crash |
| Test endpoint `GET /transaction/status` dengan `transactionId` milik user lain (IDOR check) | Ganti `transactionId` ke milik user lain menggunakan token user A | HTTP 403 Forbidden — user A tidak boleh bisa lihat transaksi user B |

## 5. Contoh Test Script — POST /qris/pay (Validasi Expiry, terkait BUG-SGP-004)

```javascript
pm.test("QR expired harus ditolak backend, bukan hanya di UI", function () {
    pm.response.to.have.status(400);
    const body = pm.response.json();
    pm.expect(body.errorCode).to.eql("QR_EXPIRED");
});
```
> Test script ini dibuat khusus setelah menemukan BUG-SGP-004 di UI, untuk memastikan **root cause**-nya ada di backend (bukan cuma validasi client yang bisa dilewati).

## 6. Kenapa API Testing Penting di Konteks Banking

- Lebih cepat dieksekusi & di-otomasi dibanding UI testing (baik untuk regression suite ke depannya).
- Bisa menguji skenario yang **tidak bisa** direproduksi lewat UI (misal: request tanpa field wajib, header token diubah manual, IDOR).
- Memisahkan **bug UI** (misal tombol tidak disable) dari **bug backend** (misal validasi expiry tidak ada) — penting untuk laporan defect yang akurat ke developer.
