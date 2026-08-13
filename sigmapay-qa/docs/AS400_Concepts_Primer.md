# AS400 / IBM i — Core Banking Layer SigmaPay + Panduan CV/Interview

Melengkapi [Test Plan §Arsitektur](../01-Test-Plan/Test_Plan_MobileBanking.md) dan [STLC Tools Mapping](../00-SDLC-STLC-Overview/STLC_Tools_Mapping.md) dengan konteks **core banking backend**: banyak bank di Indonesia (BCA, Mandiri, BRI, BNI, dst.) menjalankan sistem inti (ledger, rekening, batch EOD) di atas **IBM i (dulu disebut AS/400)** dengan database **DB2 for i**. Loker QA Banking sering mensyaratkan familiaritas dengan platform ini, jadi folder ini menambahkan lapisan itu ke studi kasus SigmaPay.

> **Kejujuran dulu, sebelum apa pun:** semua isi folder ini adalah **hasil belajar mandiri untuk kebutuhan portfolio**, disusun dari dokumentasi publik AS400/IBM i dan pengetahuan umum core banking — **bukan pengalaman hands-on di lingkungan AS400 production sungguhan**. Jangan pernah klaim ini sebagai pengalaman kerja nyata. Prinsip yang sama dengan [STLC_Tools_Mapping.md §5](../00-SDLC-STLC-Overview/STLC_Tools_Mapping.md#5-template-jawaban-interview-versi-jujur-berbasis-project-ini) berlaku persis di sini.

## 1. Kenapa AS400 masuk ke arsitektur SigmaPay

Narasi arsitektur SigmaPay (lihat update di [Test Plan](../01-Test-Plan/Test_Plan_MobileBanking.md)):

```
[Mobile App Android/iOS] ──► [API/Middleware Layer] ──► [Core Banking: IBM i / AS400 + DB2 for i]
     (channel, UI)              (REST API, lihat            (ledger, rekening, batch EOD,
                                  06-API-Testing)              interest accrual, reconciliation)
```

- **Mobile app & API** (sudah dibangun di `06-API-Testing`) adalah *channel layer* — apa yang dites lewat UI/Postman selama ini.
- **Core banking di AS400** adalah *system of record* — tempat saldo & ledger sebenarnya disimpan, dan tempat **batch job semalam (EOD)** berjalan: akrual bunga, rekonsiliasi transaksi harian, generate laporan mutasi.
- QA di lingkungan ini tidak cukup hanya cek UI — perlu memvalidasi **hasil batch di sisi AS400** cocok dengan yang ditampilkan di aplikasi. Ini pembeda level 3-5 tahun pengalaman yang sering ditanyakan interviewer banking.

## 2. Konsep Dasar AS400/IBM i untuk QA (Istilah Penting)

| Istilah | Penjelasan Singkat | Analogi/Konteks QA |
|---|---|---|
| **IBM i** | Nama modern sistem operasi AS/400 (istilah "AS400" masih dipakai luas di industri perbankan Indonesia) | Platform tempat core banking SigmaPay berjalan |
| **5250 Emulator / IBM ACS** (Access Client Solutions) | Terminal emulator untuk akses "green screen" ke AS400 — cara tradisional operator/QA berinteraksi dengan sistem | Setara "connect ke server lewat SSH" di dunia Linux/Unix |
| **Library (LIB)** | Wadah objek (file, program, tabel) — mirip schema/database di dunia relasional modern | Contoh: `SIGMAPRD` (library production simulasi), `SIGMAQA` (library QA) |
| **Job** | Satuan eksekusi program di AS400 — bisa **interactive** (user login langsung) atau **batch** (dijadwalkan, tanpa interaksi user) | Batch job EOD SigmaPay = `SGPEOD01` |
| **Job Queue (JOBQ)** | Antrian tempat batch job menunggu giliran dieksekusi subsystem | Dicek QA saat curiga batch job "menggantung" / delay |
| **Subsystem** | Lingkungan runtime yang mengatur job (mis. `QBATCH` untuk batch, `QINTER` untuk interactive) | Konteks environment saat troubleshooting job stuck |
| **Spool File / Output Queue (OUTQ)** | Output cetak/laporan dari job (mis. laporan EOD) yang bisa direview tanpa dicetak fisik | QA review laporan rekonsiliasi EOD dari sini |
| **Job Log** | Riwayat pesan (informational, warning, error) selama job berjalan — kode pesan diawali `CPF`/`MCH` | QA cek di sini untuk root cause saat batch gagal |
| **STRSQL / Run SQL Scripts (ACS)** | Tool untuk menjalankan query SQL langsung ke DB2 for i, setara `psql`/DBeaver di dunia PostgreSQL | Dipakai untuk [DB2_for_i_Validation_Queries.sql](DB2_for_i_Validation_Queries.sql) |
| **DB2 for i** | Database relasional bawaan IBM i tempat tabel core banking (`ACCOUNTS`, `LEDGER`, `BATCH_CTL`) disimpan | Setara PostgreSQL di [07-SQL-Validation](../07-SQL-Validation/SQL_Queries_Validation.sql), tapi versi legacy/production |
| **CL (Control Language)** | Bahasa scripting native AS400 untuk menjalankan/mengatur job, program, dan command sistem | Program yang memicu job `SGPEOD01` ditulis dalam CL |
| **PTF (Program Temporary Fix)** | Setara "patch"/hotfix di dunia AS400 — di-apply ke OS atau aplikasi core banking | Setelah PTF di-apply, QA wajib regression test (lihat [Job Monitoring Checklist](AS400_Job_Monitoring_Checklist.md)) |

## 3. Tugas QA yang Realistis di Lingkungan AS400 Perbankan

Berdasarkan pola umum QA manual tester banking yang bersinggungan dengan core banking legacy:

1. **Verifikasi hasil batch job EOD** — cek job selesai tanpa *abnormal end*, cek job log bersih dari pesan error, cek spool file laporan tersedia dan datanya benar → lihat [AS400_Job_Monitoring_Checklist.md](AS400_Job_Monitoring_Checklist.md).
2. **Validasi data langsung di DB2 for i** — pakai STRSQL untuk cek saldo/ledger akhir hari cocok dengan yang tampil di aplikasi mobile, tidak cuma percaya UI → lihat [DB2_for_i_Validation_Queries.sql](DB2_for_i_Validation_Queries.sql).
3. **Cek konsistensi interface channel ↔ core banking** — jumlah transaksi yang dikirim dari API/middleware harus sama dengan yang diterima & diproses di AS400 (file interface/queue).
4. **Regression test setelah PTF/patch** — core banking legacy biasanya jarang di-deploy, tapi setiap PTF tetap wajib smoke + regression test karena risikonya tinggi (semua channel bergantung pada sistem ini).
5. **Uji skenario batch/cut-off time** — transaksi yang masuk mendekati/melewati jam cut-off (mis. 23:00) harus diproses di batch hari yang benar, bukan tertukar H vs H+1.
6. **Uji idempotency batch (tidak boleh double-run)** — lihat [BUG-SGP-008](../05-Bug-Report/Bug_Report_Sample.md) sebagai contoh konkret bug kelas ini.

Semua poin di atas dituangkan jadi test case konkret di [AS400_Batch_Test_Cases.csv](AS400_Batch_Test_Cases.csv).

## 4. Status Kejujuran (mengikuti pola STLC_Tools_Mapping.md)

| Skill/Konsep AS400 | Status di Project Ini |
|---|---|
| Terminologi & konsep dasar IBM i/DB2 for i (tabel di atas) | Dipelajari mandiri untuk kebutuhan portfolio — **konsep**, bukan hands-on |
| Test case verifikasi batch job EOD | ✅ Dibuat nyata (tertulis): [AS400_Batch_Test_Cases.csv](AS400_Batch_Test_Cases.csv) — belum pernah dieksekusi di AS400 sungguhan |
| Query validasi gaya DB2 for i | ✅ Dibuat nyata (tertulis, gaya sintaks DB2 for i): [DB2_for_i_Validation_Queries.sql](DB2_for_i_Validation_Queries.sql) — belum pernah dijalankan lewat STRSQL/ACS sungguhan |
| Checklist monitoring job (WRKACTJOB/WRKJOBQ/WRKOUTQ) | ✅ Dibuat nyata (tertulis): [AS400_Job_Monitoring_Checklist.md](AS400_Job_Monitoring_Checklist.md) — command AS400 dikutip dari dokumentasi publik IBM, belum pernah dijalankan langsung |
| Operasional 5250 emulator/IBM ACS sungguhan | Belum pernah — sebatas paham fungsinya dari dokumentasi |

## 5. Template Jawaban Interview (Versi Jujur)

Kalau ditanya *"Ada pengalaman dengan AS400/core banking?"*:

> "Saya belum pernah kerja langsung di lingkungan AS400 production, tapi karena tahu banyak bank di Indonesia masih pakai IBM i untuk core banking, saya sengaja pelajari mandiri konsepnya — job, batch processing, DB2 for i, spool file — dan terapkan ke project portfolio saya sendiri: saya tulis test case untuk verifikasi batch job EOD, query validasi data ala DB2 for i, dan checklist monitoring job. Jadi saya paham *apa* yang perlu dicek dan *kenapa* pentingnya (misalnya risiko double-posting kalau batch di-rerun tanpa validasi), dan saya siap onboarding cepat begitu dikasih akses ke sistem sungguhan."

Kalimat ini jujur (tidak mengklaim pengalaman production) tapi tetap menunjukkan inisiatif dan pemahaman konkret — sama seperti pola template di [STLC_Tools_Mapping.md](../00-SDLC-STLC-Overview/STLC_Tools_Mapping.md#5-template-jawaban-interview-versi-jujur-berbasis-project-ini).

**Prinsip yang tetap dipegang:** kalau interviewer menggali lebih dalam ("pernah pegang terminal AS400 langsung?"), jawab jujur "belum, ini hasil belajar mandiri lewat project portfolio" — bukan mengarang pengalaman.
