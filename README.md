<div align="center">

<img src="https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
<img src="https://img.shields.io/badge/LinkedIn-Jobs-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white"/>
<img src="https://img.shields.io/badge/No_Login-Required-22C55E?style=for-the-badge"/>
<img src="https://img.shields.io/badge/Output-CSV%20%2F%20Excel-F59E0B?style=for-the-badge"/>

# 🔍 LinkedIn Jobs Scraper

**Scrape LinkedIn job listings — no account needed, auto-resume, duplicate-free.**  
**Scraping lowongan LinkedIn — tanpa akun, lanjut otomatis, bebas duplikat.**

</div>

---

## 🌐 Language / Bahasa

- [🇬🇧 English](#-english)
- [🇮🇩 Bahasa Indonesia](#-bahasa-indonesia)

---

# 🇬🇧 English

## What This Does

This tool scrapes public job listings from LinkedIn (no login required) and saves them as a clean CSV or Excel file. It supports multiple keywords and locations in a single run, automatically moves to the next combination when one is exhausted, and resumes exactly where it left off if interrupted.

## Features

| Feature | Description |
|---|---|
| 🔑 **Multi-keyword** | Search multiple job titles in one run |
| 📍 **Multi-location** | Search multiple cities simultaneously |
| 💾 **Single output file** | All results go into one CSV, auto-deduplicated |
| 🔁 **Auto-resume** | Interrupted? Re-run and it picks up where it stopped |
| 🛡️ **Anti-block** | Random delays, rotating user-agents, smart retry |
| 📊 **Excel formatter** | Convert messy CSV into a clean, formatted Excel table |

## Output Columns

| Column | Description |
|---|---|
| `title` | Job title |
| `company` | Company name |
| `location` | Job location |
| `posted` | Date posted |
| `link` | Direct link to the listing |
| `keyword` | Which keyword found this job |
| `search_location` | Which location was searched |

## Getting Started

### Step 1 — Install Python

Download Python at [python.org](https://python.org) → pick the latest version → **check "Add Python to PATH"** during install.

### Step 2 — Install dependencies

```bash
pip install requests beautifulsoup4 pandas openpyxl
```

### Step 3 — Run the scraper

**Interactive mode** (recommended for beginners):
```bash
python linkedin_scraper.py
```
The script will ask for keyword, location, and target count one by one.

**Command-line mode:**
```bash
python linkedin_scraper.py --keyword "data analyst, designer" --location "Jakarta, Remote" --total 500
```

Leave `--location` empty to search worldwide:
```bash
python linkedin_scraper.py --keyword "data analyst" --total 1000
```

### Step 4 — Convert to Excel (optional)

```bash
python csv_to_excel.py
```

Automatically detects the latest CSV and produces a formatted `.xlsx` with:
- Styled header, alternating row colors, auto-fit column widths
- Clickable links in the Link column
- A **Summary** sheet with top companies and locations

## Notes

> ⚠️ LinkedIn limits public search results to ~400 jobs per keyword + location combination. The scraper handles this automatically — when one combination is exhausted, it moves to the next one and everything goes into the same output file.

- **Duplicates** are removed automatically across all combinations
- If you press `Ctrl+C`, your progress is saved — re-run to continue
- Recommended: run overnight with multiple keywords and cities for best results

---

# 🇮🇩 Bahasa Indonesia

## Apa Ini?

Tool ini mengambil data lowongan kerja publik dari LinkedIn (tanpa perlu login) dan menyimpannya sebagai file CSV atau Excel yang rapi. Mendukung banyak keyword dan lokasi sekaligus dalam satu proses, otomatis lanjut ke kombinasi berikutnya saat satu kombinasi habis, dan bisa dilanjutkan tepat dari posisi terakhir jika tiba-tiba berhenti.

## Fitur

| Fitur | Keterangan |
|---|---|
| 🔑 **Multi-keyword** | Cari beberapa posisi pekerjaan sekaligus |
| 📍 **Multi-lokasi** | Cari di beberapa kota dalam satu proses |
| 💾 **Satu file output** | Semua hasil masuk ke satu CSV, duplikat otomatis dihapus |
| 🔁 **Auto-resume** | Berhenti di tengah? Jalankan ulang, lanjut dari posisi terakhir |
| 🛡️ **Anti-block** | Delay acak, rotasi user-agent, retry otomatis saat terkena limit |
| 📊 **Format Excel** | Konversi CSV berantakan menjadi tabel Excel yang rapi |

## Kolom Output

| Kolom | Keterangan |
|---|---|
| `title` | Judul pekerjaan |
| `company` | Nama perusahaan |
| `location` | Lokasi pekerjaan |
| `posted` | Tanggal diposting |
| `link` | Link langsung ke lowongan |
| `keyword` | Keyword yang menemukan lowongan ini |
| `search_location` | Lokasi yang dicari |

## Cara Menjalankan

### Langkah 1 — Install Python

Download Python di [python.org](https://python.org) → pilih versi terbaru → **centang "Add Python to PATH"** saat instalasi.

### Langkah 2 — Install library

```bash
pip install requests beautifulsoup4 pandas openpyxl
```

### Langkah 3 — Jalankan scraper

**Mode interaktif** (direkomendasikan untuk pemula):
```bash
python linkedin_scraper.py
```
Script akan menanyakan keyword, lokasi, dan jumlah target satu per satu.

**Mode command-line langsung:**
```bash
python linkedin_scraper.py --keyword "data analyst, designer" --location "Jakarta, Bandung, Surabaya, Medan, Remote" --total 500
```

Kosongkan `--location` untuk mencari di semua negara:
```bash
python linkedin_scraper.py --keyword "data analyst" --total 1000
```

### Langkah 4 — Konversi ke Excel (opsional)

```bash
python csv_to_excel.py
```

Otomatis mendeteksi CSV terbaru dan menghasilkan `.xlsx` yang rapi dengan:
- Header berwarna, baris selang-seling, lebar kolom otomatis
- Kolom Link bisa diklik langsung
- Sheet **Ringkasan** berisi top perusahaan dan lokasi terbanyak

## Catatan

> ⚠️ LinkedIn membatasi hasil pencarian publik sekitar ~400 jobs per kombinasi keyword + lokasi. Scraper ini menanganinya secara otomatis — saat satu kombinasi habis, langsung lanjut ke kombinasi berikutnya dan semuanya masuk ke file output yang sama.

- **Duplikat** dihapus otomatis dari semua kombinasi
- Tekan `Ctrl+C` kapan saja — progress tersimpan, jalankan ulang untuk lanjut
- Disarankan: jalankan malam hari dengan banyak keyword dan kota untuk hasil terbaik

---

<div align="center">

Made with ☕ — feel free to fork, star, and contribute.

</div>
