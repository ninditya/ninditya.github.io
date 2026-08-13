#!/usr/bin/env python3
"""
Medika Nusantara - Synthetic Workforce Data Generator
=====================================================
Rakamin Workforce Intelligence Platform - Case Study Deliverable 3

Menghasilkan:
  1. dataset_a_messy.csv       - union naif dari 3 sistem yang masih bisa diakses
  2. dataset_b_clean.csv       - hasil data contextualization layer (1 baris = 1 orang)
  3. ground_truth.csv          - kebenaran yang ditanam generator (untuk mengukur pipeline)
  4. resolution_audit.csv      - jejak audit identity resolution
  5. role_taxonomy.json        - taxonomy peran + skill requirement
  6. comparison_metrics.json   - angka pembanding A vs B untuk dokumen & prototype

PRINSIP DESAIN UTAMA
--------------------
Kekosongan data di sini SENGAJA dibuat TIDAK acak (bukan MCAR). Fill rate skill
ditentukan oleh tingkat adopsi HRIS per cabang, sementara skill sebenarnya
(ground truth) diambil dari distribusi yang sama untuk semua cabang.

Konsekuensinya bisa dibuktikan secara numerik, bukan sekadar diargumenkan:
analisis naif di atas Dataset A akan menempatkan cabang ber-adopsi-HRIS-rendah
di puncak daftar "tim paling bermasalah", padahal kondisi riil mereka setara
cabang lain. Model yang dilatih di atas data ini mempelajari higienitas
pencatatan, bukan realitas tenaga kerja.

Jalankan: python generate_medika_data.py [output_dir]
Deterministik, seed = 20260807.
"""

import csv
import json
import random
import sys
from datetime import date, timedelta
from difflib import SequenceMatcher
from pathlib import Path

SEED = 20260807
random.seed(SEED)

N_PERSONS = 200
TODAY = date(2026, 8, 7)

# ---------------------------------------------------------------------------
# ASUMSI YANG DICATAT (dikutip di dokumen, Ground Rule: cite your assumptions)
# ---------------------------------------------------------------------------
ASSUMPTIONS = {
    "A1_sample_scope": (
        "200 record adalah sampel terstratifikasi dari 15.000 karyawan, diambil "
        "dari 12 cabang yang mewakili 90 cabang. Rasio kekosongan dan variasi "
        "title dipertahankan sesuai proporsi populasi."
    ),
    "A2_ats_coverage": (
        "Workable diasumsikan diadopsi tahun 2023. Karyawan dengan tanggal masuk "
        "sebelum 2023 tidak punya record ATS. Coverage ATS efektif ~30 persen "
        "populasi aktif. Ini alasan ATS diposisikan sebagai enrichment, bukan "
        "sumber matching utama."
    ),
    "A3_payroll_absent": (
        "Oracle Payroll tidak tersedia (diblok Legal per Day 30). Kolom payroll_id "
        "sengaja diikutsertakan dalam skema dan dibiarkan kosong untuk menunjukkan "
        "secara eksplisit apa yang hilang: roster otoritatif dan arbiter deduplikasi."
    ),
    "A4_pre_2022_performance": (
        "Rating performa sebelum 2022 dinyatakan tidak reliable oleh klien. "
        "Digenerate dengan nilai di luar rentang skala yang berlaku agar alasan "
        "pembuangannya bisa dibuktikan, bukan diasumsikan."
    ),
    "A5_rating_scales": (
        "Skala rating berbeda antar cabang (1-5 numerik, 1-4 numerik, A-D huruf). "
        "Ini menjadikan perbandingan performa lintas cabang tidak valid tanpa "
        "harmonisasi, dan harmonisasi tersebut berada di luar scope 90 hari."
    ),
    "A6_transfer_as_termination": (
        "Sebagian mutasi antar cabang tercatat di HRIS sebagai terminasi lalu "
        "rehire dengan employee ID baru. Ini mengkontaminasi label attrition dan "
        "merupakan alasan utama attrition prediction ditunda ke Fase 2."
    ),
    "A7_skill_missingness_mechanism": (
        "Kekosongan skill berkorelasi dengan adopsi HRIS per cabang, bukan acak. "
        "Skill sebenarnya diambil dari distribusi identik untuk semua cabang."
    ),
}

# ---------------------------------------------------------------------------
# CABANG: tingkat adopsi HRIS menentukan fill rate, bukan kualitas SDM-nya
# ---------------------------------------------------------------------------
BRANCHES = [
    # (nama, region, tier adopsi, skala rating yang dipakai)
    ("Jakarta Pusat",  "Jabodetabek",  "high", "1-5"),
    ("Bekasi",         "Jabodetabek",  "high", "1-5"),
    ("Bandung",        "Jawa Barat",   "high", "1-5"),
    ("Surabaya",       "Jawa Timur",   "mid",  "1-5"),
    ("Semarang",       "Jawa Tengah",  "mid",  "1-4"),
    ("Yogyakarta",     "DIY",          "mid",  "1-4"),
    ("Medan",          "Sumatera",     "mid",  "1-5"),
    ("Palembang",      "Sumatera",     "low",  "A-D"),
    ("Makassar",       "Sulawesi",     "low",  "A-D"),
    ("Balikpapan",     "Kalimantan",   "low",  "1-4"),
    ("Denpasar",       "Bali Nusra",   "mid",  "1-5"),
    ("Manado",         "Sulawesi",     "low",  "A-D"),
]

# Fill rate skill di HRIS berdasarkan tier adopsi. Rata-rata tertimbang ~0.55,
# menghasilkan kekosongan sekitar 45 persen (spesifikasi case: 40 persen lebih).
ADOPTION_FILL_RATE = {"high": 0.85, "mid": 0.55, "low": 0.15}

# ---------------------------------------------------------------------------
# SKILL & TAXONOMY PERAN (domain: distribusi farmasi / alat kesehatan)
# ---------------------------------------------------------------------------
SKILLS = [
    "CDOB Compliance",          # Cara Distribusi Obat yang Baik
    "Cold Chain Handling",
    "Inventory Management",
    "SAP Navigation",
    "Distributor Negotiation",
    "Medical Product Knowledge",
    "Route Planning",
    "Advanced Excel",
    "Customer Relationship Management",
    "Regulatory Documentation",
    "Warehouse Safety",
    "Data Entry Accuracy",
    "Team Leadership",
    "Demand Forecasting",
]

ROLE_TAXONOMY = {
    "SALES_JR": {
        "canonical_title": "Sales Representative",
        "family": "Commercial",
        "level": 1,
        "required_skills": ["Medical Product Knowledge", "Customer Relationship Management",
                            "Route Planning", "Data Entry Accuracy"],
        "variants": ["Sales Rep", "Sales 1", "Sales Junior", "Jr. Sales", "Sales Executive",
                     "Medical Representative", "Salesman", "Staff Sales"],
    },
    "SALES_SR": {
        "canonical_title": "Senior Sales Representative",
        "family": "Commercial",
        "level": 2,
        "required_skills": ["Medical Product Knowledge", "Customer Relationship Management",
                            "Distributor Negotiation", "Demand Forecasting", "Advanced Excel"],
        "variants": ["Senior Sales", "Sales 2", "Sales Senior", "SR. SALES", "Senior Sales Exec",
                     "Sr Medical Rep", "Sales Executive Senior"],
    },
    "SALES_MGR": {
        "canonical_title": "Branch Sales Manager",
        "family": "Commercial",
        "level": 4,
        "required_skills": ["Team Leadership", "Demand Forecasting", "Distributor Negotiation",
                            "Advanced Excel", "Customer Relationship Management"],
        "variants": ["Sales Manager", "Kepala Sales", "Branch Sales Head", "Manager Penjualan",
                     "Sales Mgr", "Koordinator Sales"],
    },
    "WHS_STAFF": {
        "canonical_title": "Warehouse Staff",
        "family": "Supply Chain",
        "level": 1,
        "required_skills": ["Warehouse Safety", "Inventory Management", "Cold Chain Handling",
                            "Data Entry Accuracy"],
        "variants": ["Staff Gudang", "Warehouse Operator", "Gudang", "WH Staff",
                     "Petugas Gudang", "Warehouse Admin"],
    },
    "WHS_SPV": {
        "canonical_title": "Warehouse Supervisor",
        "family": "Supply Chain",
        "level": 3,
        "required_skills": ["Warehouse Safety", "Inventory Management", "Cold Chain Handling",
                            "Team Leadership", "CDOB Compliance"],
        "variants": ["Spv Gudang", "Supervisor Warehouse", "WH Supervisor", "Kepala Gudang",
                     "Warehouse Spv", "Koordinator Gudang"],
    },
    "LOG_COORD": {
        "canonical_title": "Logistics Coordinator",
        "family": "Supply Chain",
        "level": 2,
        "required_skills": ["Route Planning", "Cold Chain Handling", "Inventory Management",
                            "SAP Navigation"],
        "variants": ["Koordinator Logistik", "Logistic Coord", "Logistics Staff",
                     "Staff Logistik", "Distribution Coordinator"],
    },
    "PHARM_SPEC": {
        "canonical_title": "Product Specialist (Pharma)",
        "family": "Technical",
        "level": 2,
        "required_skills": ["Medical Product Knowledge", "CDOB Compliance",
                            "Regulatory Documentation", "Cold Chain Handling"],
        "variants": ["Product Specialist", "Spesialis Produk", "Apoteker Pendamping",
                     "Pharmacy Assistant", "Asisten Apoteker", "Product Spec"],
    },
    "QA_REG": {
        "canonical_title": "Regulatory & QA Officer",
        "family": "Technical",
        "level": 3,
        "required_skills": ["CDOB Compliance", "Regulatory Documentation",
                            "Medical Product Knowledge", "Data Entry Accuracy"],
        "variants": ["QA Officer", "Regulatory Officer", "Staff QA", "QA/RA",
                     "Petugas Regulasi", "Quality Assurance"],
    },
    "FIN_ADMIN": {
        "canonical_title": "Finance & Admin Staff",
        "family": "Corporate",
        "level": 1,
        "required_skills": ["Advanced Excel", "Data Entry Accuracy", "SAP Navigation"],
        "variants": ["Staff Finance", "Admin Keuangan", "Finance Admin", "Staff Adm & Keu",
                     "Accounting Staff", "Admin"],
    },
    "IT_SUPPORT": {
        "canonical_title": "IT Support Officer",
        "family": "Corporate",
        "level": 2,
        "required_skills": ["SAP Navigation", "Data Entry Accuracy", "Advanced Excel"],
        "variants": ["IT Support", "Helpdesk", "Staff IT", "IT Officer", "Teknisi IT"],
    },
}

ROLE_WEIGHTS = {
    "SALES_JR": 0.20, "SALES_SR": 0.15, "SALES_MGR": 0.06,
    "WHS_STAFF": 0.17, "WHS_SPV": 0.06, "LOG_COORD": 0.09,
    "PHARM_SPEC": 0.10, "QA_REG": 0.06, "FIN_ADMIN": 0.07, "IT_SUPPORT": 0.04,
}

# Kursus LMS -> skill. Sumber "evidenced": bukti perilaku, bukan klaim.
LMS_COURSES = {
    "Pelatihan CDOB Dasar": "CDOB Compliance",
    "CDOB Lanjutan & Audit Internal": "CDOB Compliance",
    "Cold Chain & Penanganan Produk Termolabil": "Cold Chain Handling",
    "Manajemen Inventori Gudang": "Inventory Management",
    "SAP SuccessFactors untuk Staff": "SAP Navigation",
    "SAP Modul Logistik": "SAP Navigation",
    "Teknik Negosiasi Distributor": "Distributor Negotiation",
    "Product Knowledge Alkes 2024": "Medical Product Knowledge",
    "Product Knowledge Farmasi 2025": "Medical Product Knowledge",
    "Optimasi Rute Distribusi": "Route Planning",
    "Excel untuk Analisis Penjualan": "Advanced Excel",
    "Dasar CRM & Retensi Pelanggan": "Customer Relationship Management",
    "Dokumentasi Regulasi BPOM": "Regulatory Documentation",
    "K3 Gudang & Penanganan B3": "Warehouse Safety",
    "Akurasi Input Data Operasional": "Data Entry Accuracy",
    "Kepemimpinan Tim Cabang": "Team Leadership",
    "Forecasting Permintaan Dasar": "Demand Forecasting",
}
# Kategori LMS memang berantakan (issue: poor skill taxonomy)
LMS_CATEGORIES = ["Umum", "umum", "Training", "Compliance", "", "Lain-lain", "TRAINING", None]

# ---------------------------------------------------------------------------
# NAMA (Indonesia) + varian ejaan untuk memaksa probabilistic matching
# ---------------------------------------------------------------------------
FIRST_M = ["Ahmad", "Muhammad", "Budi", "Agus", "Rizky", "Dwi", "Bayu", "Fajar", "Hendra",
           "Irfan", "Yusuf", "Andi", "Dedi", "Eko", "Galih", "Hasan", "Imam", "Joko",
           "Krisna", "Lukman", "Nanda", "Oktavianus", "Prasetyo", "Rahmat", "Surya",
           "Teguh", "Wahyu", "Yoga", "Zainal", "Bagus"]
FIRST_F = ["Siti", "Dewi", "Ayu", "Rina", "Fitri", "Nur", "Indah", "Lestari", "Maya",
           "Nadia", "Putri", "Ratna", "Sari", "Tika", "Wulan", "Yuni", "Anisa", "Citra",
           "Dinda", "Erika", "Gita", "Hana", "Intan", "Jihan", "Kartika", "Laras",
           "Mega", "Novi", "Oktavia", "Rahma"]
LAST = ["Wijaya", "Santoso", "Pratama", "Nugroho", "Setiawan", "Kurniawan", "Hidayat",
        "Saputra", "Ramadhan", "Firmansyah", "Halim", "Sanjaya", "Wibowo", "Permana",
        "Maulana", "Anggraini", "Puspita", "Handayani", "Kusuma", "Rahayu", "Safitri",
        "Utami", "Lestari", "Mardiana", "Yulianti", "Simanjuntak", "Situmorang",
        "Hutapea", "Panjaitan", "Tanujaya"]

NAME_NOISE = [
    ("Muhammad", "Muhamad"), ("Muhammad", "M."), ("Muhammad", "Moh."),
    ("Ahmad", "Achmad"), ("Rizky", "Rizki"), ("Rizky", "Risky"),
    ("Fitri", "Fitry"), ("Dewi", "Dewie"), ("Nur", "Nuur"),
    ("Setiawan", "Setiyawan"), ("Nugroho", "Nugraha"), ("Prasetyo", "Prasetya"),
    ("Anisa", "Annisa"), ("Kurniawan", "Kurnianwan"), ("Hidayat", "Hidayah"),
]


def normalize_name(name):
    """Normalisasi ringan untuk matching: lowercase, hapus gelar, rapikan spasi."""
    if not name:
        return ""
    n = name.lower().strip().replace(",", " ")
    for t in [" s.farm", " apt.", "apt. ", " s.e.", " s.kom", " a.md", "drs. ", "dr. "]:
        n = n.replace(t, " ")
    return " ".join(n.split())


def name_key(name):
    """
    Token-sorted key. Menetralkan pembalikan urutan ('Wijaya, Ahmad Budi')
    dan spasi ganda. Inisial dipertahankan agar 'A. Wijaya' tetap punya
    kemiripan tinggi dengan 'Ahmad Wijaya' lewat SequenceMatcher.
    """
    return " ".join(sorted(normalize_name(name).split()))


def name_similarity(a, b):
    """Ambil skor terbaik antara urutan asli dan urutan tersortir."""
    a1, b1 = normalize_name(a), normalize_name(b)
    a2, b2 = name_key(a), name_key(b)
    return max(SequenceMatcher(None, a1, b1).ratio(),
               SequenceMatcher(None, a2, b2).ratio())


def apply_name_noise(name):
    """Terapkan varian ejaan supaya deduplikasi tidak bisa hanya string-equality."""
    for src, dst in NAME_NOISE:
        if src in name and random.random() < 0.75:
            return name.replace(src, dst)
    parts = name.split()
    r = random.random()
    if r < 0.20 and len(parts) >= 2:                 # singkat nama depan
        return f"{parts[0][0]}. {' '.join(parts[1:])}"
    if r < 0.35 and len(parts) >= 2:                 # balik urutan
        return f"{parts[-1]}, {' '.join(parts[:-1])}"
    if r < 0.45:                                     # kapital semua
        return name.upper()
    if r < 0.55:                                     # spasi ganda
        return name.replace(" ", "  ")
    return name


def title_noise(title):
    """Noise pengetikan pada job title: kapitalisasi, spasi, titik."""
    r = random.random()
    if r < 0.12:
        return title.upper()
    if r < 0.22:
        return title.lower()
    if r < 0.30:
        return f" {title} "
    if r < 0.36:
        return title.replace(" ", "  ")
    return title


def rand_date(start, end):
    delta = (end - start).days
    return start + timedelta(days=random.randint(0, max(delta, 1)))


# ===========================================================================
# TAHAP 1 - GROUND TRUTH: 200 manusia nyata. Tidak pernah dilihat pipeline.
# ===========================================================================
def build_ground_truth():
    persons = []
    role_codes = list(ROLE_WEIGHTS.keys())
    role_probs = [ROLE_WEIGHTS[r] for r in role_codes]

    for i in range(1, N_PERSONS + 1):
        pid = f"MN-P-{i:04d}"
        branch, region, adoption, scale = random.choices(
            BRANCHES, weights=[1.4 if b[2] == "high" else 1.0 for b in BRANCHES]
        )[0]
        role = random.choices(role_codes, weights=role_probs)[0]

        gender = random.choice(["M", "F"])
        first = random.choice(FIRST_M if gender == "M" else FIRST_F)
        last = random.choice(LAST)
        mid = random.choice(FIRST_M + FIRST_F) if random.random() < 0.25 else ""
        full_name = " ".join(x for x in [first, mid, last] if x)

        # Tanggal masuk. Level lebih tinggi cenderung lebih lama bekerja.
        lvl = ROLE_TAXONOMY[role]["level"]
        earliest = TODAY - timedelta(days=365 * (4 + lvl * 2))
        hire = rand_date(earliest, TODAY - timedelta(days=120))
        dob = rand_date(date(1975, 1, 1), date(2002, 12, 31))

        # SKILL SEBENARNYA. Distribusi identik untuk semua cabang.
        # Cabang adopsi rendah TIDAK dibuat lebih tidak kompeten.
        req = ROLE_TAXONOMY[role]["required_skills"]
        true_skills = [s for s in req if random.random() < 0.68]
        for s in SKILLS:
            if s not in req and random.random() < 0.10:
                true_skills.append(s)

        persons.append({
            "person_id": pid,
            "full_name": full_name,
            "gender": gender,
            "dob": dob.isoformat(),
            "branch": branch,
            "region": region,
            "hris_adoption_tier": adoption,
            "rating_scale": scale,
            "true_role_code": role,
            "true_canonical_title": ROLE_TAXONOMY[role]["canonical_title"],
            "true_hire_date": hire.isoformat(),
            "true_skills": sorted(set(true_skills)),
            "email": f"{normalize_name(full_name).replace(' ', '.')}@medikanusantara.co.id",
        })
    return persons


# ===========================================================================
# TAHAP 2 - DATASET A: apa yang benar-benar keluar dari 3 sistem
# ===========================================================================
def build_messy(persons):
    rows = []
    audit_seed = {}     # person_id -> daftar record mentah miliknya
    injected = {
        "hris_records": 0, "ats_records": 0, "lms_records": 0,
        "skill_blank": 0, "ghost_transfer_pairs": 0, "conflicting_hire_date": 0,
        "unreliable_perf_rows": 0, "title_variants_used": set(),
    }

    for p in persons:
        pid = p["person_id"]
        audit_seed[pid] = []
        role = p["true_role_code"]
        tax = ROLE_TAXONOMY[role]
        adoption = p["hris_adoption_tier"]
        fill = ADOPTION_FILL_RATE[adoption]
        hire = date.fromisoformat(p["true_hire_date"])

        # ---------------- HRIS (SAP SuccessFactors) ----------------
        emp_id = f"EMP-{random.randint(1000, 9999)}"
        raw_title = title_noise(random.choice(tax["variants"]))
        injected["title_variants_used"].add(raw_title.strip().lower())

        # MEKANISME KEKOSONGAN: bergantung adopsi cabang, bukan acak
        if random.random() < fill:
            declared = [s for s in p["true_skills"] if random.random() < 0.80]
            skill_field = "; ".join(declared) if declared else ""
        else:
            skill_field = ""
        if not skill_field:
            injected["skill_blank"] += 1

        hris_hire = hire

        rows.append({
            "source_system": "HRIS_SuccessFactors",
            "source_record_id": emp_id,
            "employee_name": apply_name_noise(p["full_name"]),
            "date_of_birth": p["dob"] if random.random() < 0.88 else "",
            # Email korporat: peran kantor hampir selalu punya, peran lapangan
            # (gudang, sales keliling) sering tidak. Ini realitas distribusi
            # farmasi, dan menjadi penentu utama sebaran antrean review.
            "email": p["email"] if random.random() < (
                0.93 if tax["family"] == "Corporate" or tax["level"] >= 3 else 0.48
            ) else "",
            "national_id_nik": (f"32{random.randint(10**14, 10**15 - 1)}"
                                if random.random() < 0.34 else ""),
            "branch": p["branch"] if random.random() < 0.90 else p["branch"].upper(),
            "raw_job_title": raw_title,
            "department": tax["family"],
            "hire_date": hris_hire.isoformat(),
            "employment_status": "Active",
            "skills_raw": skill_field,
            "last_performance_rating": "",
            "performance_years_available": "",
            "rating_scale_used": "",
            "lms_course": "",
            "lms_category": "",
            "lms_completion_date": "",
            "payroll_id": "",   # Oracle diblok Legal. Sengaja kosong.
            "record_notes": "",
        })
        audit_seed[pid].append(("HRIS_SuccessFactors", emp_id))
        injected["hris_records"] += 1

        # ---- Performa: sebagian punya 3 tahun, sebagian 1, sebagian nihil ----
        n_years = random.choices([0, 1, 2, 3], weights=[0.28, 0.24, 0.22, 0.26])[0]
        scale = p["rating_scale"]
        for k in range(n_years):
            year = 2025 - k
            unreliable = year < 2022
            if scale == "1-5":
                val = str(random.randint(7, 9) if unreliable else random.randint(2, 5))
            elif scale == "1-4":
                val = str(random.randint(6, 8) if unreliable else random.randint(1, 4))
            else:
                val = random.choice(["X", "Z"]) if unreliable else random.choice(
                    ["A", "B", "B", "C", "D"])
            if unreliable:
                injected["unreliable_perf_rows"] += 1
            rows.append({
                "source_system": "HRIS_SuccessFactors",
                "source_record_id": emp_id,
                "employee_name": apply_name_noise(p["full_name"]),
                "date_of_birth": "", "email": "", "national_id_nik": "",
                "branch": p["branch"], "raw_job_title": raw_title,
                "department": tax["family"], "hire_date": "",
                "employment_status": "Active", "skills_raw": "",
                "last_performance_rating": val,
                "performance_years_available": str(year),
                "rating_scale_used": scale,
                "lms_course": "", "lms_category": "", "lms_completion_date": "",
                "payroll_id": "",
                "record_notes": "performance_history",
            })

        # ---- Mutasi tercatat sebagai terminasi + rehire (kontaminasi label) ----
        if random.random() < 0.045:
            old_id = f"EMP-{random.randint(1000, 9999)}"
            old_branch = random.choice([b[0] for b in BRANCHES if b[0] != p["branch"]])
            rows.append({
                "source_system": "HRIS_SuccessFactors",
                "source_record_id": old_id,
                "employee_name": apply_name_noise(p["full_name"]),
                "date_of_birth": p["dob"], "email": "", "national_id_nik": "",
                "branch": old_branch,
                "raw_job_title": title_noise(random.choice(tax["variants"])),
                "department": tax["family"],
                "hire_date": (hire - timedelta(days=random.randint(400, 1200))).isoformat(),
                "employment_status": "Terminated",
                "skills_raw": "", "last_performance_rating": "",
                "performance_years_available": "", "rating_scale_used": "",
                "lms_course": "", "lms_category": "", "lms_completion_date": "",
                "payroll_id": "",
                "record_notes": "status_terminated_prior_branch",
            })
            audit_seed[pid].append(("HRIS_SuccessFactors", old_id))
            injected["ghost_transfer_pairs"] += 1

        # ---------------- ATS (Workable) : hanya hire >= 2023 ----------------
        if hire >= date(2023, 1, 1) and random.random() < 0.86:
            cand_id = f"candidate_{random.randint(100, 999)}"
            # Konflik tanggal: ATS mencatat tanggal offer, bukan tanggal masuk
            ats_date = hire - timedelta(days=random.randint(7, 75))
            if ats_date != hire:
                injected["conflicting_hire_date"] += 1
            rows.append({
                "source_system": "ATS_Workable",
                "source_record_id": cand_id,
                "employee_name": apply_name_noise(p["full_name"]),
                "date_of_birth": p["dob"] if random.random() < 0.55 else "",
                "email": p["email"] if random.random() < 0.93 else "",
                "national_id_nik": "",
                "branch": p["branch"],
                "raw_job_title": title_noise(random.choice(tax["variants"])),
                "department": "",
                "hire_date": ats_date.isoformat(),
                "employment_status": "Hired",
                "skills_raw": "; ".join(
                    random.sample(p["true_skills"], min(len(p["true_skills"]), 3))
                ) if p["true_skills"] and random.random() < 0.62 else "",
                "last_performance_rating": "", "performance_years_available": "",
                "rating_scale_used": "", "lms_course": "", "lms_category": "",
                "lms_completion_date": "", "payroll_id": "",
                "record_notes": "ats_offer_date_not_hire_date",
            })
            audit_seed[pid].append(("ATS_Workable", cand_id))
            injected["ats_records"] += 1

        # ---------------- LMS (Moodle) ----------------
        n_courses = random.choices([0, 1, 2, 3], weights=[0.34, 0.30, 0.22, 0.14])[0]
        if n_courses:
            moodle_id = f"moodle_{random.randint(10000, 99999)}"
            relevant = [c for c, s in LMS_COURSES.items() if s in p["true_skills"]]
            pool = relevant if relevant else list(LMS_COURSES.keys())
            for course in random.sample(pool, min(n_courses, len(pool))):
                rows.append({
                    "source_system": "LMS_Moodle",
                    "source_record_id": moodle_id,
                    "employee_name": apply_name_noise(p["full_name"]),
                    "date_of_birth": "",
                    "email": p["email"] if random.random() < 0.81 else "",
                    "national_id_nik": "", "branch": "",
                    "raw_job_title": "", "department": "", "hire_date": "",
                    "employment_status": "", "skills_raw": "",
                    "last_performance_rating": "", "performance_years_available": "",
                    "rating_scale_used": "",
                    "lms_course": course,
                    "lms_category": str(random.choice(LMS_CATEGORIES) or ""),
                    "lms_completion_date": rand_date(
                        max(hire, date(2023, 1, 1)), TODAY).isoformat(),
                    "payroll_id": "",
                    "record_notes": "",
                })
                injected["lms_records"] += 1
            audit_seed[pid].append(("LMS_Moodle", moodle_id))

    random.shuffle(rows)
    injected["title_variants_used"] = len(injected["title_variants_used"])
    return rows, audit_seed, injected


# ===========================================================================
# TAHAP 3 - CONTEXTUALIZATION LAYER: Dataset A -> Dataset B
# ===========================================================================
VARIANT_LOOKUP = {}
for code, tax in ROLE_TAXONOMY.items():
    VARIANT_LOOKUP[tax["canonical_title"].lower()] = code
    for v in tax["variants"]:
        VARIANT_LOOKUP[v.lower()] = code


def normalize_title(raw):
    """
    Tier 1 - exact match ke kamus varian, confidence 0.97
    Tier 2 - fuzzy match di atas ambang 0.82, confidence proporsional
    Tier 3 - tidak terpetakan, masuk antrean review
    """
    if not raw or not raw.strip():
        return None, 0.0, "unmapped"
    key = " ".join(raw.lower().split())
    if key in VARIANT_LOOKUP:
        return VARIANT_LOOKUP[key], 0.97, "exact"
    best, best_score = None, 0.0
    for variant, code in VARIANT_LOOKUP.items():
        sc = SequenceMatcher(None, key, variant).ratio()
        if sc > best_score:
            best, best_score = code, sc
    if best_score >= 0.82:
        return best, round(0.55 + 0.40 * (best_score - 0.82) / 0.18, 3), "fuzzy"
    return None, round(best_score, 3), "unmapped"


def resolve_identities(messy_rows):
    """
    Cascade identity resolution.
      Tier 1  NIK atau email korporat        -> confidence 1.00
      Tier 2  nama ternormalisasi + DOB      -> confidence 0.92
      Tier 3  fuzzy nama, blocking per cabang-> confidence 0.60-0.85
      Tier 4  tidak terselesaikan            -> antrean review manusia
    Catatan: tanpa Oracle Payroll tidak ada roster otoritatif. HRIS dipromosikan
    jadi system of record secara default, dan itu adalah asumsi berisiko.
    """
    clusters = []          # {keys, records, tiers}
    by_nik, by_email = {}, {}

    def new_cluster(row):
        c = {"records": [row], "niks": set(), "emails": set(),
             "names": [row["employee_name"]], "dobs": set(), "branches": set(),
             "tiers": []}
        clusters.append(c)
        return c

    def attach(c, row, tier):
        c["records"].append(row)
        c["names"].append(row["employee_name"])
        c["tiers"].append(tier)

    def index(c, row):
        if row["national_id_nik"]:
            c["niks"].add(row["national_id_nik"])
            by_nik[row["national_id_nik"]] = c
        if row["email"]:
            c["emails"].add(row["email"].lower())
            by_email[row["email"].lower()] = c
        if row["date_of_birth"]:
            c["dobs"].add(row["date_of_birth"])
        if row["branch"]:
            c["branches"].add(row["branch"].strip().lower())

    for row in messy_rows:
        target, tier = None, None

        if row["national_id_nik"] and row["national_id_nik"] in by_nik:
            target, tier = by_nik[row["national_id_nik"]], "T1_nik"
        elif row["email"] and row["email"].lower() in by_email:
            target, tier = by_email[row["email"].lower()], "T1_email"
        else:
            best, best_sc, best_same_branch = None, 0.0, False
            row_branch = row["branch"].strip().lower()
            for c in clusters:
                same_branch = (not row_branch) or (not c["branches"]) or \
                              (row_branch in c["branches"])
                for cand in c["names"]:
                    sc = name_similarity(row["employee_name"], cand)
                    if sc > best_sc:
                        best, best_sc, best_same_branch = c, sc, same_branch
            if best is not None:
                if best_sc >= 0.92 and row["date_of_birth"] and row["date_of_birth"] in best["dobs"]:
                    # DOB cocok mengalahkan blocking cabang: ini justru pola mutasi
                    target, tier = best, "T2_name_dob"
                elif best_same_branch and best_sc >= 0.965:
                    # nama nyaris identik di cabang sama: cukup untuk auto-merge
                    target, tier = best, "T3a_fuzzy_high"
                elif best_same_branch and best_sc >= 0.86:
                    target, tier = best, "T3b_fuzzy_mid"
                elif (not best_same_branch) and best_sc >= 0.97:
                    # beda cabang, nama nyaris identik: kandidat mutasi, wajib review
                    target, tier = best, "T3b_fuzzy_mid"

        if target is None:
            c = new_cluster(row)
            c["tiers"].append("T4_seed")
            index(c, row)
        else:
            attach(target, row, tier)
            index(target, row)

    return clusters


TIER_CONFIDENCE = {
    "T1_nik": 1.00,          # identifier unik nasional
    "T1_email": 0.98,        # email korporat
    "T2_name_dob": 0.92,     # deterministik komposit
    "T3a_fuzzy_high": 0.88,  # probabilistik ambang tinggi, boleh auto-merge
    "T3b_fuzzy_mid": 0.70,   # probabilistik ambang menengah, wajib review
    "T4_single_hris": 0.85,  # hanya ada di HRIS, tidak ambigu tapi tak terkorroborasi
    "T4_orphan": 0.45,       # hanya ada di ATS/LMS, tanpa jangkar HRIS
    "T4_seed": 0.50,
}


def build_clean(clusters):
    """
    Bangun Dataset B. Aturan skill inference (dikutip di dokumen):
      declared  1.00  - tertulis di HRIS
      evidenced 0.90  - ada completion LMS yang memetakan ke skill tsb
      inferred  0.55  - skill wajib peran, HANYA jika sudah ada >=1 sinyal lain
      unknown   0.00  - tidak ada sinyal apa pun. Tidak diimputasi. Tetap lubang.

    Aturan "inferred hanya jika ada sinyal lain" bersifat konservatif dan disengaja.
    Mengimputasi orang tanpa sinyal apa pun akan membuat cabang ber-adopsi rendah
    terlihat normal, sehingga menyembunyikan masalah tepat di tempat masalahnya ada.
    """
    out, audit = [], []
    for idx, c in enumerate(clusters, start=1):
        recs = c["records"]
        person_key = f"MN-R-{idx:04d}"

        hris = [r for r in recs if r["source_system"] == "HRIS_SuccessFactors"]
        ats = [r for r in recs if r["source_system"] == "ATS_Workable"]
        lms = [r for r in recs if r["source_system"] == "LMS_Moodle"]
        master = next((r for r in hris if r["record_notes"] != "performance_history"), None) \
            or (ats[0] if ats else recs[0])

        # --- identitas ---
        merge_tiers = [t for t in c["tiers"]
                       if t in TIER_CONFIDENCE and t != "T4_seed"]
        if merge_tiers:
            best_tier = max(merge_tiers, key=lambda t: TIER_CONFIDENCE[t])
        elif hris:
            # tidak ada penggabungan, tapi ada jangkar HRIS: tidak ambigu
            best_tier = "T4_single_hris"
        else:
            # hanya muncul di ATS atau LMS, tanpa jangkar HRIS
            best_tier = "T4_orphan"
        # Merge probabilistik menurunkan confidence seluruh cluster, bukan sebagian.
        if "T3b_fuzzy_mid" in merge_tiers:
            best_tier = "T3b_fuzzy_mid"
        id_conf = TIER_CONFIDENCE[best_tier]

        # --- peran ---
        titles = [r["raw_job_title"] for r in recs if r["raw_job_title"].strip()]
        role_code, role_conf, role_method = (None, 0.0, "unmapped")
        for t in titles:
            rc, cf, m = normalize_title(t)
            if cf > role_conf:
                role_code, role_conf, role_method = rc, cf, m

        # --- skill: declared / evidenced / inferred / unknown ---
        declared = set()
        for r in recs:
            if r["skills_raw"]:
                declared |= {s.strip() for s in r["skills_raw"].split(";") if s.strip()}
        evidenced = {LMS_COURSES[r["lms_course"]] for r in lms
                     if r["lms_course"] in LMS_COURSES}
        evidenced -= declared

        req = ROLE_TAXONOMY[role_code]["required_skills"] if role_code else []
        has_signal = bool(declared or evidenced)
        inferred = set(req) - declared - evidenced if has_signal else set()
        unknown = set(req) - declared - evidenced - inferred

        # --- konflik tanggal masuk ---
        hire_dates = {r["hire_date"] for r in recs if r["hire_date"]}
        hris_dates = {r["hire_date"] for r in hris if r["hire_date"]}
        # Selisih HRIS vs ATS bukan konflik: ATS mencatat tanggal offer, HRIS
        # mencatat tanggal masuk. Pipeline tahu bedanya, jadi tidak dieskalasi.
        # Yang dieskalasi hanya konflik di dalam satu sistem yang sama.
        conflict = len(hris_dates) > 1
        hire_final = min(hire_dates) if hire_dates else ""
        if hris:
            hd = [r["hire_date"] for r in hris if r["hire_date"]]
            if hd:
                hire_final = max(hd)   # HRIS menang untuk atribut employment

        # --- performa: buang pra-2022, skala tidak dibandingkan lintas cabang ---
        perf = [r for r in recs if r["record_notes"] == "performance_history"
                and r["performance_years_available"]
                and int(r["performance_years_available"]) >= 2022]
        perf_years = len(perf)

        # --- skor kualitas data ---
        completeness = len(declared | evidenced) / len(req) if req else 0.0
        dq = round(0.40 * id_conf + 0.30 * role_conf + 0.30 * min(completeness, 1.0), 3)

        # --- flag review ---
        # Review di-trigger hanya oleh kondisi yang benar-benar butuh mata manusia.
        # Record HRIS tunggal tanpa korroborasi BUKAN alasan review: itu kondisi
        # normal bagi 70 persen populasi yang masuk sebelum ATS diadopsi.
        reasons = []
        if best_tier in ("T3b_fuzzy_mid", "T4_orphan"):
            reasons.append("identity_probabilistic_or_orphan")
        if role_conf < 0.80:
            reasons.append("title_unmapped_or_fuzzy")
        if unknown:
            reasons.append("skill_no_signal")
        if conflict:
            reasons.append("hire_date_conflict_within_hris")
        if any(r["employment_status"] == "Terminated" for r in recs) and \
           any(r["employment_status"] == "Active" for r in recs):
            reasons.append("status_conflict_possible_transfer")

        out.append({
            "person_id": person_key,
            "resolved_name": max(c["names"], key=len).strip(),
            "branch": master["branch"].strip().title() if master["branch"] else "",
            "canonical_role_code": role_code or "",
            "canonical_title": ROLE_TAXONOMY[role_code]["canonical_title"] if role_code else "",
            "role_family": ROLE_TAXONOMY[role_code]["family"] if role_code else "",
            "role_confidence": role_conf,
            "role_match_method": role_method,
            "source_titles_seen": " | ".join(sorted({t.strip() for t in titles})),
            "source_systems": ",".join(sorted({r["source_system"] for r in recs})),
            "source_record_ids": ",".join(sorted({r["source_record_id"] for r in recs})),
            "identity_tier": best_tier,
            "identity_confidence": id_conf,
            "hire_date_final": hire_final,
            "hire_date_conflict": "Y" if conflict else "N",
            "skills_declared": "; ".join(sorted(declared)),
            "skills_evidenced": "; ".join(sorted(evidenced)),
            "skills_inferred": "; ".join(sorted(inferred)),
            "skills_unknown": "; ".join(sorted(unknown)),
            "required_skill_count": len(req),
            "required_skill_covered": len((declared | evidenced) & set(req)),
            "performance_years_usable": perf_years,
            "data_quality_score": dq,
            "review_flag": "Y" if reasons else "N",
            "review_reason": ";".join(reasons),
            "payroll_linked": "N",
        })

        audit.append({
            "person_id": person_key,
            "resolved_name": max(c["names"], key=len).strip(),
            "n_source_records": len(recs),
            "identity_tier": best_tier,
            "identity_confidence": id_conf,
            "name_variants_observed": " | ".join(sorted({n.strip() for n in c["names"]})),
            "source_record_ids": ",".join(sorted({r["source_record_id"] for r in recs})),
            # Ambang harus sama persis dengan pemicu review_flag di Dataset B.
            # Dua artefak dalam satu paket submission tidak boleh berbeda aturan.
            "action": ("queued_for_human_review"
                       if best_tier in ("T3b_fuzzy_mid", "T4_orphan")
                       else "auto_merged"),
        })
    return out, audit


# ===========================================================================
# TAHAP 4 - PERBANDINGAN: analisis naif di A vs analisis di B
# ===========================================================================
def naive_analysis_on_A(messy_rows):
    """
    Analis naif yang realistis, bukan strawman. Yang dia lakukan:
      - lowercase + trim job title (sudah lebih baik dari rata-rata)
      - group by (cabang, raw title)
      - anggap skill kosong = skill tidak dimiliki
      - tidak melakukan deduplikasi lintas sistem
    """
    groups = {}
    for r in messy_rows:
        if r["record_notes"] == "performance_history" or not r["raw_job_title"].strip():
            continue
        key = (r["branch"].strip().title(), " ".join(r["raw_job_title"].lower().split()))
        g = groups.setdefault(key, {"headcount": 0, "skill_tokens": 0})
        g["headcount"] += 1
        g["skill_tokens"] += len([s for s in r["skills_raw"].split(";") if s.strip()])
    ranked = []
    for (branch, title), g in groups.items():
        if g["headcount"] < 2:
            continue
        avg = g["skill_tokens"] / g["headcount"]
        ranked.append({"branch": branch, "group": title, "headcount": g["headcount"],
                       "avg_skills_recorded": round(avg, 2),
                       "gap_score": round(1 - min(avg / 4.0, 1.0), 3)})
    ranked.sort(key=lambda x: (-x["gap_score"], -x["headcount"]))
    return ranked, len(groups)


def informed_analysis_on_B(clean_rows):
    """
    Group by (cabang, peran kanonik). Skill unknown DIKELUARKAN dari denominator.
    Tim dengan sinyal tidak memadai tidak diberi peringkat, dipindah ke bucket
    'butuh data' dengan CTA berbeda. Ini perilaku produk, bukan sekadar analitik.
    """
    groups = {}
    for r in clean_rows:
        if not r["canonical_role_code"]:
            continue
        key = (r["branch"], r["canonical_role_code"])
        g = groups.setdefault(key, {"members": 0, "covered": 0, "required": 0, "no_signal": 0})
        g["members"] += 1
        g["required"] += r["required_skill_count"]
        g["covered"] += r["required_skill_covered"]
        if not r["skills_declared"] and not r["skills_evidenced"]:
            g["no_signal"] += 1

    ranked, needs_data = [], []
    for (branch, role), g in groups.items():
        if g["members"] < 2:
            continue
        signal_ratio = 1 - g["no_signal"] / g["members"]
        coverage = g["covered"] / g["required"] if g["required"] else 0.0
        item = {"branch": branch, "group": role,
                "canonical_title": ROLE_TAXONOMY[role]["canonical_title"],
                "headcount": g["members"],
                "signal_ratio": round(signal_ratio, 3),
                "skill_coverage": round(coverage, 3),
                "gap_score": round(1 - coverage, 3)}
        (ranked if signal_ratio >= 0.5 else needs_data).append(item)

    ranked.sort(key=lambda x: (-x["gap_score"], -x["headcount"]))
    needs_data.sort(key=lambda x: -x["headcount"])
    return ranked, needs_data


def individual_comparison(messy_rows, clean_rows, top_k=30):
    """
    Pertanyaan eksplisit case: siapa yang salah di-flag, siapa yang terlewat.
    Naif di A  : skor kebutuhan reskilling = sedikitnya skill tercatat.
    Terinformasi di B : gap terhadap skill wajib peran kanonik, orang tanpa
                        sinyal apa pun DIKELUARKAN dari peringkat, bukan diberi
                        skor rendah palsu.
    """
    # Daftar, bukan dict. Employee ID di HRIS ternyata tidak unik: ada tabrakan
    # antar orang berbeda. Meng-index dengan ID akan diam-diam membuang salah
    # satunya, dan kehilangan orang tanpa sadar adalah persis kegagalan yang
    # sedang kita ukur.
    a_scores = []
    for r in messy_rows:
        if r["source_system"] != "HRIS_SuccessFactors" or r["record_notes"]:
            continue
        n = len([s for s in r["skills_raw"].split(";") if s.strip()])
        a_scores.append({
            "record_id": r["source_record_id"],
            "name": r["employee_name"].strip(),
            "branch": r["branch"].strip().title(),
            "skills_recorded": n,
            "naive_need_score": round(1 - min(n / 4.0, 1.0), 3),
        })
    # 111 orang terikat di skor tertinggi karena nol skill tercatat. Sistem naif
    # tidak punya dasar untuk membedakan mereka. Tie-break memakai record id
    # supaya deterministik dan identik dengan prototype, bukan supaya adil.
    a_top = sorted(a_scores,
                   key=lambda x: (-x["naive_need_score"], x["record_id"]))[:top_k]

    b_pool = [r for r in clean_rows
              if r["canonical_role_code"] and r["required_skill_count"]
              and (r["skills_declared"] or r["skills_evidenced"])]
    for r in b_pool:
        r["_gap"] = round(1 - r["required_skill_covered"] / r["required_skill_count"], 3)
    b_top = sorted(b_pool, key=lambda x: (-x["_gap"], x["person_id"]))[:top_k]

    # Petakan lewat source_record_ids supaya kedua daftar bisa dibandingkan.
    b_ids = set()
    b_index = {}
    for r in b_top:
        for rid in r["source_record_ids"].split(","):
            b_ids.add(rid)
            b_index[rid] = r

    a_ids = {x["record_id"] for x in a_top}
    false_alarms = [x for x in a_top if x["record_id"] not in b_ids]
    missed = [{"person_id": r["person_id"], "name": r["resolved_name"],
               "branch": r["branch"], "canonical_title": r["canonical_title"],
               "gap": r["_gap"],
               "skill_coverage": f'{r["required_skill_covered"]}/{r["required_skill_count"]}'}
              for r in b_top
              if not any(rid in a_ids for rid in r["source_record_ids"].split(","))]

    for r in b_pool:
        r.pop("_gap", None)

    return {
        "top_k": top_k,
        "hris_id_collisions": len(a_scores) - len({v["record_id"] for v in a_scores}),
        "tied_at_max_naive_score": sum(
            1 for v in a_scores if v["naive_need_score"] >= 1.0),
        "agreement_count": top_k - len(false_alarms),
        "agreement_rate": round((top_k - len(false_alarms)) / top_k, 3),
        "false_alarm_count": len(false_alarms),
        "missed_count": len(missed),
        "false_alarms_sample": false_alarms[:8],
        "missed_sample": missed[:8],
        "interpretation": (
            "Orang yang muncul di daftar A tapi hilang di daftar B umumnya bukan "
            "orang dengan gap skill, melainkan orang yang record HRIS-nya tidak "
            "diisi. Intervensi reskilling yang diarahkan ke mereka membakar "
            "anggaran pelatihan pada masalah pencatatan."
        ),
    }


def adoption_tier_comparison(messy_rows, clean_rows):
    """
    Metrik headline utama. Tahan terhadap noise sampling top-N.
    Skill sebenarnya digenerate dari distribusi identik di semua tier adopsi,
    jadi setiap perbedaan antar tier pada Dataset A adalah artefak pencatatan.
    """
    tier_of = {b[0]: b[2] for b in BRANCHES}
    a_tier, b_tier = {}, {}

    for r in messy_rows:
        if r["source_system"] != "HRIS_SuccessFactors" or r["record_notes"]:
            continue
        t = tier_of.get(r["branch"].strip().title())
        if not t:
            continue
        n = len([s for s in r["skills_raw"].split(";") if s.strip()])
        d = a_tier.setdefault(t, {"n": 0, "gap": 0.0})
        d["n"] += 1
        d["gap"] += 1 - min(n / 4.0, 1.0)

    for r in clean_rows:
        t = tier_of.get(r["branch"])
        if not t or not r["required_skill_count"]:
            continue
        if not (r["skills_declared"] or r["skills_evidenced"]):
            continue   # tanpa sinyal, tidak diberi peringkat
        d = b_tier.setdefault(t, {"n": 0, "gap": 0.0})
        d["n"] += 1
        d["gap"] += 1 - r["required_skill_covered"] / r["required_skill_count"]

    def mean(d):
        return {k: round(v["gap"] / v["n"], 3) for k, v in d.items() if v["n"]}

    a_m, b_m = mean(a_tier), mean(b_tier)
    a_spread = round(max(a_m.values()) - min(a_m.values()), 3) if a_m else 0
    b_spread = round(max(b_m.values()) - min(b_m.values()), 3) if b_m else 0
    return {
        "mean_gap_score_dataset_a_by_adoption_tier": a_m,
        "mean_gap_score_dataset_b_by_adoption_tier": b_m,
        "spread_dataset_a": a_spread,
        "spread_dataset_b": b_spread,
        "spread_reduction": round(a_spread - b_spread, 3),
        "claim": (
            "Skill sebenarnya digenerate dari distribusi identik untuk semua tier "
            "adopsi HRIS. Karena itu seluruh rentang antar tier pada Dataset A "
            "adalah artefak pencatatan, bukan realitas tenaga kerja."
        ),
    }


def build_comparison(messy_rows, clean_rows, persons, injected):
    a_rank, a_groups = naive_analysis_on_A(messy_rows)
    b_rank, b_needs = informed_analysis_on_B(clean_rows)

    adoption_of = {b[0]: b[2] for b in BRANCHES}
    a_top10 = a_rank[:10]
    b_top10 = b_rank[:10]
    a_low_share = sum(1 for x in a_top10 if adoption_of.get(x["branch"]) == "low") / max(len(a_top10), 1)
    b_low_share = sum(1 for x in b_top10 if adoption_of.get(x["branch"]) == "low") / max(len(b_top10), 1)

    a_branches = {x["branch"] for x in a_top10}
    b_branches = {x["branch"] for x in b_top10}

    total_persons = len(clean_rows)
    flagged = sum(1 for r in clean_rows if r["review_flag"] == "Y")
    auto = total_persons - flagged
    unmapped = sum(1 for r in clean_rows if not r["canonical_role_code"])
    no_signal = sum(1 for r in clean_rows
                    if not r["skills_declared"] and not r["skills_evidenced"])

    # akurasi identity resolution diukur terhadap ground truth
    ideal = len(persons)
    over_split = total_persons - ideal

    skill_rows = [r for r in messy_rows if r["record_notes"] == ""
                  and r["source_system"] == "HRIS_SuccessFactors"
                  and r["raw_job_title"].strip()]
    blank_rate = sum(1 for r in skill_rows if not r["skills_raw"]) / max(len(skill_rows), 1)

    return {
        "generated_at": TODAY.isoformat(),
        "seed": SEED,
        "dataset_a": {
            "total_rows": len(messy_rows),
            "represents_persons": ideal,
            "distinct_raw_job_titles": injected["title_variants_used"],
            "hris_skill_blank_rate": round(blank_rate, 3),
            "naive_groups_formed": a_groups,
            "conflicting_hire_dates": injected["conflicting_hire_date"],
            "transfer_recorded_as_termination": injected["ghost_transfer_pairs"],
            "unreliable_pre_2022_perf_rows": injected["unreliable_perf_rows"],
        },
        "dataset_b": {
            "resolved_persons": total_persons,
            "ground_truth_persons": ideal,
            "over_split_records": over_split,
            "canonical_roles": len(ROLE_TAXONOMY),
            "auto_approved": auto,
            "flagged_for_review": flagged,
            "flag_rate": round(flagged / max(total_persons, 1), 3),
            "titles_unmapped": unmapped,
            "persons_with_no_skill_signal": no_signal,
        },
        "headline_finding": {
            "claim": (
                "Analisis naif di atas Dataset A mengarahkan intervensi ke cabang "
                "dengan pencatatan HRIS terburuk, bukan ke cabang dengan gap skill "
                "sesungguhnya."
            ),
            "share_of_top10_from_low_adoption_branches_dataset_a": round(a_low_share, 3),
            "share_of_top10_from_low_adoption_branches_dataset_b": round(b_low_share, 3),
            "branches_in_top10_A_only": sorted(a_branches - b_branches),
            "branches_in_top10_B_only": sorted(b_branches - a_branches),
            "top10_branch_overlap": len(a_branches & b_branches),
            "implication": (
                "Model attrition yang dilatih di atas Dataset A akan mempelajari "
                "higienitas pencatatan cabang, bukan risiko tenaga kerja. Inilah "
                "penjelasan mekanistik untuk skenario Day 75: 82 persen akurasi "
                "dengan hasil yang terasa salah bagi manajer HR."
            ),
        },
        "adoption_tier_effect": adoption_tier_comparison(messy_rows, clean_rows),
        "individual_level_comparison": individual_comparison(messy_rows, clean_rows),
        "team_ranking_dataset_a_top10": a_top10,
        "team_ranking_dataset_b_top10": b_top10,
        "dataset_b_needs_data_bucket": b_needs[:10],
        "assumptions": ASSUMPTIONS,
    }


# ===========================================================================
def write_csv(path, rows):
    if not rows:
        return
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


def main():
    out = Path(sys.argv[1] if len(sys.argv) > 1 else "/mnt/user-data/outputs")
    out.mkdir(parents=True, exist_ok=True)

    persons = build_ground_truth()
    messy, _, injected = build_messy(persons)
    clusters = resolve_identities(messy)
    clean, audit = build_clean(clusters)
    metrics = build_comparison(messy, clean, persons, injected)

    gt = [{**p, "true_skills": "; ".join(p["true_skills"])} for p in persons]

    write_csv(out / "dataset_a_messy.csv", messy)
    write_csv(out / "dataset_b_clean.csv", clean)
    write_csv(out / "ground_truth.csv", gt)
    write_csv(out / "resolution_audit.csv", audit)

    with open(out / "role_taxonomy.json", "w", encoding="utf-8") as f:
        json.dump({"version": "0.1", "skills": SKILLS, "roles": ROLE_TAXONOMY},
                  f, indent=2, ensure_ascii=False)
    with open(out / "comparison_metrics.json", "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2, ensure_ascii=False)

    # JSON mirror untuk dikonsumsi prototype tanpa parser CSV
    with open(out / "dataset_a_messy.json", "w", encoding="utf-8") as f:
        json.dump(messy, f, indent=1, ensure_ascii=False)
    with open(out / "dataset_b_clean.json", "w", encoding="utf-8") as f:
        json.dump(clean, f, indent=1, ensure_ascii=False)

    h = metrics["headline_finding"]
    print(f"Dataset A rows        : {metrics['dataset_a']['total_rows']}")
    print(f"Distinct raw titles   : {metrics['dataset_a']['distinct_raw_job_titles']}")
    print(f"HRIS skill blank rate : {metrics['dataset_a']['hris_skill_blank_rate']}")
    print(f"Naive groups formed   : {metrics['dataset_a']['naive_groups_formed']}")
    print(f"Resolved persons      : {metrics['dataset_b']['resolved_persons']} "
          f"(ground truth {metrics['dataset_b']['ground_truth_persons']})")
    print(f"Flag rate             : {metrics['dataset_b']['flag_rate']}")
    print(f"Top10 low-adoption A  : {h['share_of_top10_from_low_adoption_branches_dataset_a']}")
    print(f"Top10 low-adoption B  : {h['share_of_top10_from_low_adoption_branches_dataset_b']}")
    print(f"Top10 branch overlap  : {h['top10_branch_overlap']}")
    at = metrics["adoption_tier_effect"]
    print(f"\nMean gap by tier   A  : {at['mean_gap_score_dataset_a_by_adoption_tier']}")
    print(f"Mean gap by tier   B  : {at['mean_gap_score_dataset_b_by_adoption_tier']}")
    print(f"Spread A -> B         : {at['spread_dataset_a']} -> {at['spread_dataset_b']}")
    ic = metrics["individual_level_comparison"]
    print(f"\nTop-30 agreement      : {ic['agreement_count']}/30 ({ic['agreement_rate']})")
    print(f"False alarms          : {ic['false_alarm_count']}")
    print(f"Missed entirely       : {ic['missed_count']}")


if __name__ == "__main__":
    main()
