# Linkedin-Jobs-Scraper-
Alat untuk menemukan 19 juta lapangan pekerjaan yang dijanjikan

Cara Menjalankan
Langkah 1 — Install Python
Kalau belum punya Python, download di python.org → pilih versi terbaru → centang "Add Python to PATH" saat install.

Langkah 2 — Install library
Buka CMD (Windows) atau Terminal (Mac/Linux), ketik:
bashpip install requests beautifulsoup4 pandas

Langkah 4 — Jalankan
masih di terminal ketik:
bashpython python linkedin_scraper.py (atau drag and drop file linkedin_scraper.py)  --keyword "data analyst, designer" --location "Jakarta, Bandung, Surabaya, Medan, Remote"

Langkah 5 - Selesai
jika proses sudah selesai file csv akan dihasilkan dengan kolom title,	company,	location,	posted,	 dan link,

note: 
keyword dan location bisa diganti atau di tambahkan sesuai dengan keinginan
jika dihapus akan otomatis mencari tanpa keyword atau dengan lokasi disemua negara

maksimal pencarian per keyword atau session hanya 398 jobs, setelah itu kan di lanjut ke session selanjutnya atau berhenti,
dalam satu proses data yang sama akan otomatis dihapus

