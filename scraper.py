# ------------------------------------------------------
# A simple scraper for books.toscrape.com
# ------------------------------------------------------
import csv
import re
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "https://books.toscrape.com/"

session = requests.Session()
session.headers.update({"User-Agent": "Mozilla/5.0"})

def fetch(url):
    try:
        r = session.get(url, timeout=10)
        r.encoding = "utf-8"   # Fixes the python issue
        return BeautifulSoup(r.text, "lxml") if r.status_code == 200 else None
    except:
        return None

# ------------------------------------------------------
# Data cleaning functions
# ------------------------------------------------------
def clean_price(raw):
    # "£51.77" → 51.77
    try:
        return float(raw.replace("£", "").strip())
    except:
        return None

def clean_rating(raw):
    # "Three" → 3
    RATING_MAP = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5} # Maps word-based rating to integer
    return RATING_MAP.get(raw, None)

def clean_availability(raw):
    # "In stock (22 available)" → 22
    match = re.search(r"\d+", raw)
    return int(match.group()) if match else None

# ------------------------------------------------------
#  Scraping logic
# ------------------------------------------------------

# 1. Get first 1 category URLs
homepage = fetch(BASE_URL)
categories = [
    (urljoin(BASE_URL, a["href"]), a.get_text(strip=True))
    for a in homepage.select("ul.nav.nav-list ul li a")
][:1]
print(f"Found {len(categories)} categories")

# 2. Collect all book URLs
book_queue = []

for cat_url, cat_name in categories:
    page_url = cat_url
    while page_url:
        soup = fetch(page_url)
        if not soup:
            break
        for card in soup.select("article.product_pod"):
            book_url = urljoin(page_url, card.select_one("h3 a")["href"])
            book_queue.append((book_url, cat_name))
        next_btn = soup.select_one("li.next a")
        page_url = urljoin(page_url, next_btn["href"]) if next_btn else None
        time.sleep(0.5)

print(f"Found {len(book_queue)} books")

# 3. Scrape detail pages and write to CSV
with open("books_raw_1.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["title", "price", "rating", "availability", "category", "product_page_url"])
    writer.writeheader()

    for i, (book_url, cat_name) in enumerate(book_queue):
        soup = fetch(book_url)
        if not soup:
            continue

        writer.writerow({
            "title":            soup.select_one("h1").get_text(strip=True),
            "price":            clean_price(soup.select_one("p.price_color").get_text(strip=True)),
            "rating":           clean_rating(soup.select_one("p.star-rating")["class"][1]),
            "availability":     clean_availability(soup.select_one("p.instock.availability").get_text(strip=True)),
            "category":         cat_name,
            "product_page_url": book_url,
        })

        if i % 50 == 0:
            print(f"  {i}/{len(book_queue)} done...")

        time.sleep(0.5)

print("Done — books_raw_1.csv written")