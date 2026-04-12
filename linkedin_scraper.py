"""
=======================================================
  LinkedIn Jobs Scraper - Lengkap & Aman
  1 Proses → 1 CSV | Auto-lanjut antar keyword/lokasi
=======================================================
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time, random, os, sys, json, argparse
from datetime import datetime


USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Safari/605.1.15",
]

DELAY_MIN   = 2.0
DELAY_MAX   = 5.0
MAX_RETRIES = 5
SESSION_FILE = "scraper_session.json"


# ══════════════════════════════════════════════════════
#  SESSION — track 1 file CSV + kombinasi mana sudah selesai
# ══════════════════════════════════════════════════════
def load_session():
    """Baca session yang tersimpan jika ada."""
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE, "r") as f:
            return json.load(f)
    return None

def save_session(session):
    with open(SESSION_FILE, "w") as f:
        json.dump(session, f, indent=2)

def delete_session():
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)

def combo_key(keyword, location):
    """ID unik per kombinasi keyword+lokasi."""
    return f"{keyword}||{location or 'worldwide'}"


# ══════════════════════════════════════════════════════
#  INPUT INTERAKTIF
# ══════════════════════════════════════════════════════
def tanya_input():
    print("\n" + "="*54)
    print("  LinkedIn Jobs Scraper  |  Tanpa Login & Aman")
    print("="*54)

    # Cek apakah ada session tersimpan
    session = load_session()
    if session:
        done = len(session.get("done_combos", []))
        total_combo = session.get("total_combos", "?")
        csv_file = session.get("csv_file", "?")
        print(f"\n⚡ Session lama ditemukan!")
        print(f"   File CSV : {csv_file}")
        print(f"   Progress : {done}/{total_combo} kombinasi selesai")
        lanjut = input("   Lanjutkan session ini? (Enter = ya / n = mulai baru) → ").strip().lower()
        if lanjut != "n":
            return session["keywords"], session["locations"], session["total_per_combo"], session

    print("\n📌 KEYWORD")
    print("   Satu  : data analyst")
    print("   Banyak: data analyst, data scientist, python developer")
    raw_kw = input("   → ").strip() or "data analyst"
    keywords = [k.strip() for k in raw_kw.split(",") if k.strip()]

    print("\n📍 LOKASI")
    print("   Satu  : Jakarta")
    print("   Banyak: Jakarta, Bandung, Remote")
    print("   Kosong: Enter saja = semua negara")
    raw_loc = input("   → ").strip()
    locations = [l.strip() for l in raw_loc.split(",") if l.strip()] if raw_loc else [""]

    print("\n🎯 JUMLAH DATA per kombinasi")
    print("   Contoh: 500 | 1000 | 5000")
    raw_total = input("   → ").strip()
    try:
        total = max(1, int(raw_total))
    except ValueError:
        total = 1000
        print(f"   (Pakai default: {total})")

    n_combo = len(keywords) * len(locations)
    est     = (total * n_combo * 3.5) / 3600

    print("\n" + "-"*54)
    print(f"   Keyword   : {', '.join(keywords)}")
    print(f"   Lokasi    : {', '.join(l or 'worldwide' for l in locations)}")
    print(f"   Target    : {total:,} per kombinasi")
    print(f"   Kombinasi : {n_combo}")
    print(f"   Est. waktu: ~{est:.1f} jam")
    print("-"*54)

    if input("\n▶️  Mulai? (Enter = ya / n = batal) → ").strip().lower() == "n":
        sys.exit(0)

    return keywords, locations, total, None   # None = tidak ada session lama


# ══════════════════════════════════════════════════════
#  CHECKPOINT per kombinasi (untuk resume di tengah-tengah)
# ══════════════════════════════════════════════════════
def ckpt_path(keyword, location):
    sk = keyword.replace(" ", "_").replace("/", "-")
    sl = (location or "worldwide").replace(" ", "_").replace("/", "-")
    return f"ckpt_{sk}_{sl}.csv"

def load_ckpt(keyword, location):
    p = ckpt_path(keyword, location)
    if os.path.exists(p):
        df = pd.read_csv(p, dtype=str).fillna("")
        print(f"  🔁 Checkpoint ada: {len(df)} data tersimpan, lanjut...")
        return df.to_dict("records")
    return []

def save_ckpt(jobs, keyword, location):
    pd.DataFrame(jobs).to_csv(ckpt_path(keyword, location), index=False, encoding="utf-8-sig")

def delete_ckpt(keyword, location):
    p = ckpt_path(keyword, location)
    if os.path.exists(p): os.remove(p)


# ══════════════════════════════════════════════════════
#  HTTP
# ══════════════════════════════════════════════════════
def get_headers():
    return {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Referer": "https://www.linkedin.com/jobs/search/",
    }

def safe_request(url, params):
    waits = [30, 60, 120, 300, 600]
    for attempt in range(MAX_RETRIES):
        try:
            r = requests.get(url, headers=get_headers(), params=params, timeout=15)
            if r.status_code == 200:
                return r
            if r.status_code in [429, 403, 999]:
                w = waits[min(attempt, len(waits)-1)]
                print(f"  ⏳ Limit ({r.status_code}), tunggu {w}s...")
                time.sleep(w)
            else:
                print(f"  ❌ Status {r.status_code}, skip.")
                return None
        except requests.exceptions.Timeout:
            print(f"  ⏱️  Timeout ({attempt+1}/{MAX_RETRIES})...")
            time.sleep(10)
        except requests.exceptions.ConnectionError:
            print(f"  🔌 Koneksi error ({attempt+1}/{MAX_RETRIES})...")
            time.sleep(15)
        except Exception as e:
            print(f"  ⚠️  {e}")
            time.sleep(10)
    return None

def human_delay(page_num):
    if page_num > 0 and page_num % 10 == 0:
        w = random.uniform(15, 30)
        print(f"  😴 Istirahat {w:.0f}s...")
        time.sleep(w); return
    if random.random() < 0.1:
        w = random.uniform(8, 15)
        print(f"  ☕ Jeda {w:.0f}s...")
        time.sleep(w); return
    time.sleep(random.uniform(DELAY_MIN, DELAY_MAX))


# ══════════════════════════════════════════════════════
#  PARSE HTML
# ══════════════════════════════════════════════════════
def parse_jobs(html, keyword, location):
    soup = BeautifulSoup(html, "html.parser")
    out  = []
    for card in soup.find_all("li"):
        title    = card.find("h3", class_="base-search-card__title")
        company  = card.find("h4", class_="base-search-card__subtitle")
        loc_tag  = card.find("span", class_="job-search-card__location")
        date_tag = card.find("time")
        link_tag = card.find("a", class_="base-card__full-link")
        if not title: continue
        out.append({
            "title":           title.text.strip(),
            "company":         company.text.strip() if company else "",
            "location":        loc_tag.text.strip() if loc_tag else "",
            "posted":          date_tag["datetime"] if date_tag and date_tag.has_attr("datetime") else "",
            "link":            link_tag["href"].split("?")[0] if link_tag and link_tag.has_attr("href") else "",
            "keyword":         keyword,
            "search_location": location or "worldwide",
        })
    return out


# ══════════════════════════════════════════════════════
#  SCRAPING SATU KOMBINASI
# ══════════════════════════════════════════════════════
def scrape_one(keyword, location, total):
    BASE = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"
    jobs = load_ckpt(keyword, location)
    start_from      = (len(jobs) // 25) * 25
    consecutive_empty = 0
    page_count        = 0

    for start in range(start_from, total, 25):
        res = safe_request(BASE, {"keywords": keyword, "location": location,
                                  "start": start, "position": 1, "pageNum": 0})
        if res is None:
            consecutive_empty += 1
            if consecutive_empty >= 3:
                print("  ⛔ Terlalu banyak gagal, lanjut ke kombinasi berikutnya.")
                break
            continue

        new = parse_jobs(res.text, keyword, location)
        if not new:
            consecutive_empty += 1
            if consecutive_empty >= 5:
                print("  ✅ Data habis untuk kombinasi ini, lanjut ke berikutnya.")
                break
        else:
            consecutive_empty = 0
            jobs.extend(new)
            save_ckpt(jobs, keyword, location)
            print(f"  ✅ hal {start//25+1:>4} | +{len(new):>2} | subtotal: {len(jobs):>5}")

        page_count += 1
        human_delay(page_count)
        if len(jobs) >= total:
            print(f"  🎉 Target {total:,} tercapai!")
            break

    delete_ckpt(keyword, location)
    return jobs


# ══════════════════════════════════════════════════════
#  APPEND KE CSV UTAMA  (1 file untuk semua kombinasi)
# ══════════════════════════════════════════════════════
def append_to_csv(new_jobs, csv_file):
    """Tambahkan jobs baru ke CSV utama, hapus duplikat."""
    if not new_jobs:
        return

    new_df = pd.DataFrame(new_jobs)

    if os.path.exists(csv_file):
        existing = pd.read_csv(csv_file, dtype=str).fillna("")
        combined = pd.concat([existing, new_df], ignore_index=True)
    else:
        combined = new_df

    before = len(combined)
    combined.drop_duplicates(subset=["link"], inplace=True)
    combined.reset_index(drop=True, inplace=True)
    removed = before - len(combined)

    combined.to_csv(csv_file, index=False, encoding="utf-8-sig")
    print(f"  💾 Disimpan ke {csv_file} | total: {len(combined):,} baris"
          + (f" ({removed} duplikat dihapus)" if removed else ""))
    return len(combined)


# ══════════════════════════════════════════════════════
#  SCRAPING SEMUA KOMBINASI
# ══════════════════════════════════════════════════════
def scrape_all(keywords, locations, total_per_combo, existing_session=None):
    # Buat semua kombinasi
    combos = [(kw, loc) for kw in keywords for loc in locations]
    n      = len(combos)

    # Inisialisasi atau lanjutkan session
    if existing_session:
        session  = existing_session
        csv_file = session["csv_file"]
        done     = set(session.get("done_combos", []))
        print(f"\n▶️  Melanjutkan session | CSV: {csv_file}")
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        csv_file  = f"linkedin_jobs_{timestamp}.csv"
        done      = set()
        session   = {
            "csv_file":        csv_file,
            "keywords":        keywords,
            "locations":       locations,
            "total_per_combo": total_per_combo,
            "total_combos":    n,
            "done_combos":     [],
            "started_at":      datetime.now().isoformat(),
        }
        save_session(session)
        print(f"\n🆕 Session baru | CSV: {csv_file}")

    # Jalankan tiap kombinasi
    for idx, (kw, loc) in enumerate(combos, 1):
        key = combo_key(kw, loc)
        if key in done:
            print(f"\n⏭️  Skip [{idx}/{n}] '{kw}' @ '{loc or 'worldwide'}' (sudah selesai)")
            continue

        print(f"\n{'='*54}")
        print(f"  [{idx}/{n}] Keyword: '{kw}' | Lokasi: '{loc or 'Semua negara'}'")
        print(f"{'='*54}")

        jobs = scrape_one(kw, loc, total_per_combo)
        total_in_csv = append_to_csv(jobs, csv_file)

        # Tandai kombinasi ini selesai
        done.add(key)
        session["done_combos"] = list(done)
        save_session(session)

        sisa = n - len(done)
        if sisa > 0:
            print(f"\n  ➡️  {sisa} kombinasi lagi tersisa...")

    # Selesai semua
    print(f"\n{'='*54}")
    print(f"✅ SEMUA KOMBINASI SELESAI")
    print(f"{'='*54}")

    if os.path.exists(csv_file):
        final_df = pd.read_csv(csv_file)
        print(f"📁 File    : {csv_file}")
        print(f"📊 Total   : {len(final_df):,} jobs unik")
        print(f"🔑 Keyword : {final_df['keyword'].unique().tolist()}")
        print(f"\n🏢 Top 5 perusahaan:")
        for co, ct in final_df['company'].value_counts().head(5).items():
            print(f"   {co}: {ct}")

    delete_session()
    print(f"\n✅ Session file dihapus. Jalankan ulang untuk sesi baru.")


# ══════════════════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════════════════
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--keyword",  type=str)
    parser.add_argument("--location", type=str)
    parser.add_argument("--total",    type=int)
    args = parser.parse_args()

    if args.keyword:
        # Mode argumen langsung — selalu cek session lama dulu
        session = load_session()
        if session:
            print(f"⚡ Session lama ditemukan ({session['csv_file']})")
            lanjut = input("   Lanjutkan? (Enter = ya / n = mulai baru) → ").strip().lower()
            if lanjut == "n":
                delete_session()
                session = None
        if session:
            keywords  = session["keywords"]
            locations = session["locations"]
            total     = session["total_per_combo"]
        else:
            keywords  = [k.strip() for k in args.keyword.split(",")]
            locations = [l.strip() for l in args.location.split(",")] if args.location else [""]
            total     = args.total or 1000
            session   = None
    else:
        keywords, locations, total, session = tanya_input()

    try:
        scrape_all(keywords, locations, total, existing_session=session)
    except KeyboardInterrupt:
        print("\n\n⚠️  Dihentikan manual.")
        print("▶️  Jalankan script lagi — akan lanjut dari kombinasi terakhir.")
        print(f"📁 Data yang sudah terkumpul aman di session file.")
