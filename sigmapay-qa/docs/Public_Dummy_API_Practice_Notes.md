# API Testing Notes — Latihan di Public Dummy API (restful-booker & Swagger Petstore)

> **Catatan kejujuran (penting, dibaca sebelum pakai file ini di interview):** Berbeda dengan [Postman_API_Test_Notes.md](Postman_API_Test_Notes.md) yang mendokumentasikan API **fiktif** SigmaPay (`api-qa.sigmapay.dummy`) sebagai simulasi, file ini mendokumentasikan latihan terhadap API **publik sungguhan** yang memang disediakan untuk latihan QA (restful-booker, Swagger Petstore). Endpoint dan response di bawah ini nyata dan bisa langsung kamu coba sendiri di Postman. Yang **tidak boleh** diklaim: ini bukan pengalaman "testing sistem banking production" — ini latihan skill Postman/API testing di API publik, lalu polanya diterapkan ke studi kasus SigmaPay. Bedakan jelas kalau ditanya interviewer, mengikuti prinsip yang sama seperti di [STLC_Tools_Mapping.md](../00-SDLC-STLC-Overview/STLC_Tools_Mapping.md).

## 0. Kenapa restful-booker Dipilih Jadi Latihan Utama

Dari beberapa dummy API yang ada, **restful-booker** paling relevan untuk portfolio banking karena polanya sama dengan API transaksi finansial: **auth berbasis token → operasi CRUD yang butuh otorisasi**. Alurnya (`POST /auth` untuk dapat token → pakai token untuk create/update/delete) mirip pola `POST /auth/login` → `POST /transfer` di [Postman_API_Test_Notes.md](Postman_API_Test_Notes.md). Swagger Petstore dipakai sebagai latihan tambahan karena scope resource-nya lebih luas (pet/store/user) dan pakai skema auth berbeda (API key header).

---

## 1. restful-booker — Struktur Collection

```
Public API Practice — restful-booker
├── Auth
│   └── POST /auth                    → generate token (username/password)
├── Booking
│   ├── GET  /booking                 → list booking id (bisa filter firstname/lastname/checkin/checkout)
│   ├── GET  /booking/{id}            → detail booking
│   ├── POST /booking                 → create booking (tidak perlu auth)
│   ├── PUT  /booking/{id}            → full update (butuh token)
│   ├── PATCH /booking/{id}           → partial update (butuh token)
│   └── DELETE /booking/{id}          → delete booking (butuh token)
└── Environment Variables
    ├── base_url = https://restful-booker.herokuapp.com
    ├── token     = {{auto-set dari response /auth}}
    └── booking_id = {{auto-set dari response create booking}}
```

## 2. Contoh Request/Response — POST /auth

**Request**
```http
POST {{base_url}}/auth
Content-Type: application/json

{
  "username": "admin",
  "password": "password123"
}
```

**Response — Sukses (200)**
```json
{
  "token": "abc123def456"
}
```

**Test Script**
```javascript
pm.test("Status code 200 saat kredensial valid", function () {
    pm.response.to.have.status(200);
});

pm.test("Response mengandung token", function () {
    const body = pm.response.json();
    pm.expect(body).to.have.property("token");
});

if (pm.response.code === 200) {
    pm.environment.set("token", pm.response.json().token);
}
```

## 3. Contoh Request/Response — POST /booking (Create)

**Request**
```http
POST {{base_url}}/booking
Content-Type: application/json

{
  "firstname": "Adrian",
  "lastname": "Nindit",
  "totalprice": 150,
  "depositpaid": true,
  "bookingdates": {
    "checkin": "2026-08-20",
    "checkout": "2026-08-25"
  },
  "additionalneeds": "Breakfast"
}
```

**Response — Sukses (200)**
```json
{
  "bookingid": 1,
  "booking": {
    "firstname": "Adrian",
    "lastname": "Nindit",
    "totalprice": 150,
    "depositpaid": true,
    "bookingdates": {
      "checkin": "2026-08-20",
      "checkout": "2026-08-25"
    },
    "additionalneeds": "Breakfast"
  }
}
```

**Test Script**
```javascript
pm.test("Status code 200 untuk create booking valid", function () {
    pm.response.to.have.status(200);
});

pm.test("Response memiliki bookingid", function () {
    const body = pm.response.json();
    pm.expect(body).to.have.property("bookingid");
});

pm.test("Data booking di response sesuai request", function () {
    const req = JSON.parse(pm.request.body.raw);
    const body = pm.response.json();
    pm.expect(body.booking.firstname).to.eql(req.firstname);
    pm.expect(body.booking.totalprice).to.eql(req.totalprice);
});

pm.environment.set("booking_id", pm.response.json().bookingid);
```

## 4. Skenario Negative Testing — restful-booker

| Skenario | Cara Uji di Postman | Expected |
|---|---|---|
| Update booking tanpa token | Kirim `PUT /booking/{id}` tanpa header `Cookie: token=...` | HTTP 403 Forbidden |
| Update booking dengan token invalid/expired | Ganti header token dengan string acak | HTTP 403 Forbidden |
| Create booking tanpa field wajib (`firstname` dihapus) | Hapus field dari JSON body | HTTP 400/500 — dicatat sebagai **temuan kualitas API**, bukan bug SigmaPay (bandingkan dengan SigmaPay yang diharapkan selalu 400 dengan pesan jelas, lihat §4 di Postman_API_Test_Notes.md) |
| `checkin` > `checkout` (tanggal terbalik) | Tukar posisi tanggal di `bookingdates` | Dicek apakah API benar-benar validasi logika tanggal atau tetap 200 (banyak dummy API tidak validasi ini — jadi bahan diskusi "kenapa validasi business rule penting di API production") |
| Delete booking yang sudah dihapus (double delete) | `DELETE /booking/{id}` 2x berturut-turut | Request kedua harus mengembalikan 404/405, bukan 200 lagi |
| GET booking dengan id yang tidak ada | `GET /booking/999999` | HTTP 404 Not Found |

> Insight untuk interview: dummy API publik seperti ini sering **tidak** memvalidasi semua business rule (contoh: `checkin > checkout` kadang tetap diterima). Ini justru bahan bagus untuk menjelaskan ke interviewer *kenapa* validasi business rule di level API itu penting — kamu bisa bandingkan dengan bagaimana SigmaPay (di studi kasus utama) sengaja didesain untuk menolak input semacam itu.

## 5. Swagger Petstore — Ringkasan Latihan Tambahan

Base URL: `https://petstore.swagger.io/v2`

| Endpoint | Fungsi | Fokus Uji |
|---|---|---|
| `POST /pet` | Tambah pet baru | Validasi field required (`name`, `photoUrls`), response schema |
| `GET /pet/{petId}` | Cari pet by ID | Positive case (id valid) vs negative case (id tidak ada → 404) |
| `PUT /pet` | Update pet | Update dengan id tidak ada → expected 404, tapi Petstore sering balas 200 — bahan diskusi soal *API contract yang tidak konsisten* |
| `DELETE /pet/{petId}` | Hapus pet | Butuh header `api_key`; uji tanpa header untuk lihat perilaku auth |
| `GET /pet/findByStatus?status=available` | Filter by status | Uji dengan value valid (`available`, `pending`, `sold`) vs invalid (`xxx`) |
| `POST /store/order` | Buat order | Validasi `quantity` negatif/nol, `shipDate` format salah |
| `POST /user/login` | Login user | Uji username/password kosong, cek response header `X-Rate-Limit`/`X-Expires-After` |

Petstore dipakai lebih ringkas dibanding restful-booker karena tujuannya melengkapi eksposur ke **auth via API key** dan **file upload (`POST /pet/{petId}/uploadImage`)** — dua pola yang tidak ada di restful-booker maupun studi kasus SigmaPay.

---

## 6. Pemetaan ke Fase STLC

| Fase STLC | Aktivitas dengan API Publik Ini |
|---|---|
| **Requirement Analysis** | Reverse-analysis dari dokumentasi Swagger resmi (bukan user story bisnis) — identifikasi endpoint & expected behavior dari spec |
| **Test Planning** | Scope: endpoint auth + CRUD booking (restful-booker), CRUD pet + auth API key (Petstore). Strategy: functional + negative + auth flow |
| **Test Case Design** | Test case per endpoint, mengikuti format yang sama seperti [Test_Case_Transfer_QRIS.csv](../03-Test-Case/Test_Case_Transfer_QRIS.csv) |
| **Test Environment Setup** | Tidak perlu setup server (langsung API publik hidup) — cukup buat Postman environment (`base_url`, `token`) |
| **Test Execution** | Jalankan request, assertion `pm.test(...)`, capture response sebagai evidence, catat Pass/Fail/Finding |
| **Test Cycle Closure** | Rangkum coverage endpoint + temuan inkonsistensi API (contoh di §4 dan §5 di atas) sebagai lessons learned untuk diterapkan ke desain test case SigmaPay |

## 7. Template Jawaban Interview (Versi Jujur)

> "Selain simulasi API SigmaPay, saya juga latihan langsung di public dummy API seperti restful-booker dan Swagger Petstore untuk mempertajam skill Postman assertion dan negative testing terhadap API yang benar-benar live — termasuk pola auth berbasis token yang mirip alur login banking. Dari situ saya juga belajar bahwa tidak semua API publik memvalidasi business rule dengan ketat, yang jadi bahan refleksi soal pentingnya validasi di level backend, bukan hanya di UI."

Kalimat ini aman karena eksplisit membedakan **latihan di API publik** vs **studi kasus simulasi SigmaPay** vs **pengalaman production sungguhan** (yang tidak diklaim di titik manapun).
