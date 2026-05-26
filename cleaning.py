"""
cleaning.py
===========
Loads books_raw.csv, cleans and validates all fields, adds derived columns,
and saves the result to books_cleaned.csv.

Cleaning steps:
    1. Type enforcement  — price (float), rating (Int64), availability (Int64)
    2. Missing/malformed — identify, report, and handle invalid rows
    3. Duplicates        — detect and remove based on product_page_url
    4. Derived columns   — price_category, high_rated

Usage:
    python cleaning.py
"""

import pandas as pd

INPUT_FILE  = "books_raw.csv"
OUTPUT_FILE = "books_cleaned.csv"

# ---------------------------------------------------------------------------
# Load
# ---------------------------------------------------------------------------

df = pd.read_csv(INPUT_FILE)
print(f"Loaded {len(df)} rows from {INPUT_FILE}")
print(f"\nRaw dtypes:\n{df.dtypes}")

# ---------------------------------------------------------------------------
# Step 1: Type Enforcement
# ---------------------------------------------------------------------------
# pd.to_numeric(errors="coerce") converts unparseable values to NaN
# instead of crashing — we catch and report those NaNs in Step 2.
#
# Int64 (capital I) is pandas' nullable integer type. Regular int64
# cannot hold NaN — it upcasts to float64. Int64 avoids that.

df["price"]        = pd.to_numeric(df["price"],        errors="coerce")         # float64
df["rating"]       = pd.to_numeric(df["rating"],        errors="coerce")         # Int64 after cleaning
df["availability"] = pd.to_numeric(df["availability"], errors="coerce")         # Int64 after cleaning

print(f"\n--- Step 1: Types after enforcement ---")
print(df.dtypes)

# ---------------------------------------------------------------------------
# Step 2: Missing and Malformed Data
# ---------------------------------------------------------------------------

print("\n--- Step 2: Data Quality Checks ---")

# --- 2a. Null check ---
print("\nNull values per column:")
print(df.isnull().sum())

# --- 2b. Malformed price ---
# Price should be a positive number. Zero or negative means something
# went wrong during scraping or type casting.
malformed_price = df[df["price"].notnull() & (df["price"] <= 0)]
print(f"\nMalformed price (≤ 0): {len(malformed_price)} rows")
if len(malformed_price) > 0:
    print(malformed_price[["title", "price"]])

# --- 2c. Malformed rating ---
# Rating must be an integer between 1 and 5.
# Anything outside this range is not a valid star rating.
malformed_rating = df[df["rating"].notnull() & ~df["rating"].between(1, 5)]
print(f"\nMalformed rating (outside 1–5): {len(malformed_rating)} rows")
if len(malformed_rating) > 0:
    print(malformed_rating[["title", "rating"]])

# --- 2d. Malformed availability ---
# Stock count should be zero or positive. Negative values are nonsensical.
malformed_avail = df[df["availability"].notnull() & (df["availability"] < 0)]
print(f"\nMalformed availability (< 0): {len(malformed_avail)} rows")
if len(malformed_avail) > 0:
    print(malformed_avail[["title", "availability"]])

# --- 2e. Empty string title ---
# A title that is an empty string would pass a null check but is still
# unusable — catches scraper edge cases where the tag existed but was empty.
malformed_title = df[df["title"].str.strip() == ""]
print(f"\nEmpty title: {len(malformed_title)} rows")

# ---------------------------------------------------------------------------
# Handling decisions
# ---------------------------------------------------------------------------
#
# | Issue                  | Action      | Justification                        |
# |------------------------|-------------|--------------------------------------|
# | Missing title          | Drop        | Unidentifiable record                |
# | Missing/malformed price| Drop        | Core analysis field — cannot impute  |
# | Missing/malformed rating| Drop       | Core analysis field — cannot impute  |
# | Missing availability   | Impute → 0  | Likely out of stock, not truly unknown|
# | Negative availability  | Impute → 0  | Nonsensical value, treat as no stock |
#
# We do not impute price or rating because these are factual fields —
# inventing values would corrupt the analysis. With ~1000 books, dropping
# a small number of bad rows does not affect the dataset meaningfully.

# Impute missing/negative availability with 0
df["availability"] = df["availability"].fillna(0)
df.loc[df["availability"] < 0, "availability"] = 0

# Drop rows with missing or malformed price
before = len(df)
df = df[df["price"].notnull() & (df["price"] > 0)]
print(f"\nDropped {before - len(df)} rows with missing or malformed price.")

# Drop rows with missing or out-of-range rating
before = len(df)
df = df[df["rating"].notnull() & df["rating"].between(1, 5)]
print(f"Dropped {before - len(df)} rows with missing or malformed rating.")

# Drop rows with missing or empty title
before = len(df)
df = df[df["title"].notnull() & (df["title"].str.strip() != "")]
print(f"Dropped {before - len(df)} rows with missing or empty title.")

print(f"\nRows remaining after cleaning: {len(df)}")

# Safe to cast to Int64 now that NaNs are resolved
df["rating"]       = df["rating"].astype("Int64")
df["availability"] = df["availability"].astype("Int64")

print(f"\nDtypes after casting:\n{df.dtypes}")

# ---------------------------------------------------------------------------
# Step 3: Duplicates
# ---------------------------------------------------------------------------
# product_page_url is the natural unique key — each book has exactly one
# URL on the site. Duplicates arise when a book appears under multiple
# categories and gets scraped more than once.
# We keep the first occurrence and drop the rest.

before = len(df)
dupes = df.duplicated(subset=["product_page_url"], keep=False).sum()
print(f"\n--- Step 3: Duplicates ---")
print(f"Duplicate rows detected: {dupes}")

df = df.drop_duplicates(subset=["product_page_url"], keep="first")
print(f"Removed {before - len(df)} duplicate rows.")
print(f"Remaining: {len(df)} rows.")

# ---------------------------------------------------------------------------
# Step 4: Derived Columns
# ---------------------------------------------------------------------------

# price_category — three pricing tiers based on price:
#   budget:    £0 ≤ price < £15 
#   mid-range: £15 ≤ price < £35
#   premium:   £35 ≤ price < ∞
df["price_category"] = pd.cut(
    df["price"],
    bins=[0, 15, 35, float("inf")],
    labels=["budget", "mid-range", "premium"],
    right=False
)

# high_rated — True if rating is 4 or 5, False otherwise
df["high_rated"] = df["rating"].isin([4, 5])

print(f"\n--- Step 4: Derived Columns ---")
print("\nprice_category distribution:")
print(df["price_category"].value_counts())
print(f"\nHigh rated books (rating ≥ 4): {df['high_rated'].sum()} / {len(df)}")

# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

df.to_csv(OUTPUT_FILE, index=False)

print(f"\n{'=' * 40}")
print(f"  Input rows     : {pd.read_csv(INPUT_FILE).shape[0]}")
print(f"  Output rows    : {len(df)}")
print(f"  Columns        : {list(df.columns)}")
print(f"  Price range    : £{df['price'].min():.2f} – £{df['price'].max():.2f}")
print(f"  Rating range   : {df['rating'].min()} – {df['rating'].max()}")
print(f"  Avg price      : £{df['price'].mean():.2f}")
print(f"  Output file    : {OUTPUT_FILE}")
print(f"{'=' * 40}")