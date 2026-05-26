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
        return BeautifulSoup(r.text, "lxml") if r.status_code == 200 else None
    except:
        return None

# 1. Get all category URLs
homepage = fetch(BASE_URL)
categories = [
    (urljoin(BASE_URL, a["href"]), a.get_text(strip=True))
    for a in homepage.select("ul.nav.nav-list ul li a")
]
print(f"Found {len(categories)} categories")

# 2. Crawl every category and collect all book URLs
book_queue = []  # list of (book_url, category_name)

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

# 3. Scrape each detail page and write to CSV
with open("books_raw.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["title", "price", "rating", "availability", "category", "product_page_url"])
    writer.writeheader()

    for i, (book_url, cat_name) in enumerate(book_queue):
        soup = fetch(book_url)
        if not soup:
            continue

        title    = soup.select_one("h1").get_text(strip=True)
        price    = soup.select_one("p.price_color").get_text(strip=True)
        rating   = soup.select_one("p.star-rating")["class"][1]
        avail    = soup.select_one("p.instock.availability").get_text(strip=True)

        writer.writerow({
            "title":            title,
            "price":            price,
            "rating":           rating,
            "availability":     avail,
            "category":         cat_name,
            "product_page_url": book_url,
        })

        if i % 50 == 0:
            print(f"  {i}/{len(book_queue)} done...")

        time.sleep(0.5)

print("Done. books_raw.csv written")