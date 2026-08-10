# API Testing — Tidak Berlaku untuk Project Ini

Folder ini tetap dibuat (mengikuti penomoran lengkap tahapan STLC) supaya nomor `06` tidak
hilang begitu saja dan pembaca tidak bertanya-tanya "kenapa loncat dari 05 ke 07" — isinya justru
penjelasan **kenapa tahap ini sengaja dilewati**, bukan dipaksakan isi yang tidak nyata.

## Alasan

SauceDemo (https://www.saucedemo.com/) adalah aplikasi **client-side murni** untuk demo/latihan
QA. Seluruh data produk, hasil login, dan proses checkout di-mock di sisi browser — tidak ada
endpoint REST/GraphQL publik yang bisa diamati lewat DevTools Network tab maupun diuji langsung
lewat Postman/Swagger.

Ini sudah dicatat sejak awal sebagai Out of Scope di
[Test Plan §4](../01-Test-Plan/Test_Plan_SauceDemo.md#4-out-of-scope-testing).

## Kalau Suatu Saat Dibutuhkan

Kalau target ujinya berganti ke aplikasi yang memang punya API (mis. e-commerce dengan backend
sungguhan), tahap ini akan berisi:

- Dokumentasi endpoint yang diuji (base URL, method, auth)
- Collection Postman/Newman atau test API terprogram
- Skenario positive/negative per endpoint (status code, response schema, error handling)

Lihat pembahasan konsep tools API testing (Postman/Swagger) yang tetap relevan untuk dipahami
meski tidak dipraktikkan di sini, di
[STLC_Tools_Mapping.md](../00-SDLC-STLC-Overview/STLC_Tools_Mapping.md).
