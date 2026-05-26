# Python Web Scraping & Data Pipeline — Take-Home Assessment

**Position:** Junior Data Scientist  
**Estimated Time:** 3–4 hours  
**Submission:** A GitHub repository or `.zip` file containing your code, outputs, and a brief write-up.

---

## Overview

You will build an end-to-end data pipeline that **scrapes**, **cleans**, and **analyzes** publicly available data. The goal is to assess your ability to work with real-world, messy web data and turn it into actionable insights.

You may use any Python libraries you wish (common choices include `requests`, `beautifulsoup4`, `pandas`, `matplotlib`, `seaborn`). Please include a `requirements.txt` file.

> **Important:** This test evaluates your process and reasoning as much as your code. Clean, well-commented code with clear explanations is valued over flashy but opaque solutions.

---

## The Task

### Scenario

A fictional consulting firm wants to understand trends in the global book market. They've asked you to collect data from a **practice scraping website**, clean it up, and produce a short analytical report.

### Target Website

Use the following website, which is specifically designed for scraping practice:

> **[https://books.toscrape.com](https://books.toscrape.com)**

This site lists ~1,000 books across 50 categories with titles, prices, ratings, and availability info.

---

## Part 1 — Web Scraping (40 points)

Write a Python script (`scraper.py`) that extracts the following fields for **every book** on the site (all pages, all categories):

| Field | Description |
|---|---|
| `title` | Full title of the book |
| `price` | Price in GBP (£), as a numeric value |
| `rating` | Star rating (1–5), as an integer |
| `availability` | Number of copies in stock (as an integer) |
| `category` | The genre/category the book belongs to |
| `product_page_url` | The full URL to the book's detail page |

### Requirements

1. **Pagination:** The site has multiple pages per category and overall. Your scraper must handle pagination correctly and collect all books — not just the first page.
2. **Detail Pages:** Some of the required fields (e.g., exact stock count) are only available on each book's individual product page. Your scraper should visit these pages when necessary.
3. **Robustness:** Include basic error handling (e.g., failed requests, missing elements). Use polite scraping practices — add a short delay between requests.
4. **Output:** Save the final scraped data as a CSV file called `books_raw.csv`.

### Evaluation Criteria

- Completeness — are all ~1,000 books captured?
- Correctness — are fields extracted and typed properly?
- Code quality — is the scraper well-structured, readable, and documented?
- Error handling — does it fail gracefully?

---

## Part 2 — Data Cleaning (25 points)

Write a script or notebook (`cleaning.py` or `cleaning.ipynb`) that loads `books_raw.csv` and performs the following:

1. **Type Enforcement**
   - Ensure `price` is a float.
   - Ensure `rating` is an integer (1–5).
   - Ensure `availability` is an integer.

2. **Missing / Malformed Data**
   - Identify and report any rows with missing or clearly malformed values.
   - Decide how to handle them (drop, impute, flag) and **justify your choice** in a comment or markdown cell.

3. **Duplicates**
   - Check for and remove any duplicate entries. Explain how you identified duplicates.

4. **Derived Columns**
   - Create a `price_category` column:
     - `"budget"` if price < £15
     - `"mid-range"` if £15 ≤ price < £35
     - `"premium"` if price ≥ £35
   - Create a `high_rated` boolean column: `True` if rating ≥ 4.

5. **Output:** Save the cleaned dataset as `books_cleaned.csv`.

### Evaluation Criteria

- Thoroughness of data quality checks.
- Soundness of cleaning decisions and justifications.
- Clean, reproducible code.

---

## Part 3 — Exploratory Analysis & Visualization (25 points)

Create a notebook (`analysis.ipynb`) or script that answers the following questions using the cleaned data. **Each answer must include at least one supporting visualization.**

### Questions

1. **Price Distribution:** What does the overall price distribution look like? Are there notable outliers?

2. **Ratings by Category:** Which categories have the highest and lowest average ratings? Show the top 10 and bottom 10.

3. **Price vs. Rating:** Is there a relationship between a book's price and its rating? Create an appropriate chart and comment on any pattern (or lack thereof).

4. **Category Size & Availability:** Which categories have the most books? Among the largest categories, which ones have the lowest average stock availability?

5. **Insight of Your Choice:** Present one additional finding that you think is interesting or commercially relevant. Explain why.

### Evaluation Criteria

- Appropriate chart types for each question.
- Visual clarity (labels, titles, legibility).
- Quality of written interpretation — do you tell a story with the data?
- Creativity and depth of the self-chosen insight (Question 5).

---

## Part 4 — Short Written Responses (10 points)

Answer the following in a file called `responses.md` (a few sentences each is fine):

1. **Ethics & Legality:** Before scraping a real website, what steps would you take to determine whether it's permissible? Name at least three things you'd check.

2. **Scaling Up:** If this dataset had 100,000 books across thousands of pages, what changes would you make to your scraper to improve performance and reliability?

3. **Data Storage:** If this pipeline needed to run daily and store historical data, what storage solution would you recommend and why?

4. **Pipeline Orchestration:** Briefly describe how you would automate this entire pipeline (scrape → clean → analyze → report) to run on a schedule in a production environment. What tools or frameworks might you use?

---

## Submission Checklist

Please ensure your submission includes:

- [ ] `scraper.py` — the scraping script
- [ ] `books_raw.csv` — raw scraped output
- [ ] `cleaning.py` or `cleaning.ipynb` — the cleaning script/notebook
- [ ] `books_cleaned.csv` — cleaned dataset
- [ ] `analysis.ipynb` — analysis notebook with visualizations
- [ ] `responses.md` — written responses
- [ ] `requirements.txt` — Python dependencies
- [ ] `README.md` — brief instructions on how to run your code

---

## Grading Rubric

| Section | Points | Weight |
|---|---|---|
| Part 1 — Web Scraping | 40 | 40% |
| Part 2 — Data Cleaning | 25 | 25% |
| Part 3 — Analysis & Visualization | 25 | 25% |
| Part 4 — Written Responses | 10 | 10% |
| **Total** | **100** | **100%** |

### Bonus (up to +5 points)

Bonus points may be awarded for:

- Using logging instead of print statements in the scraper.
- Writing unit tests for any part of the pipeline.
- Containerizing the project (e.g., a `Dockerfile`).
- Particularly elegant or well-documented code.

---

## Notes for the Candidate

- **No trick questions.** This test is designed to see how you work, not to trip you up.
- **Commit often.** If submitting via GitHub, meaningful commit messages help us understand your process.
- **Ask questions.** If something is genuinely unclear, reach out — we'd rather clarify than have you guess.
- **Have fun with it.** We chose a books dataset for a reason — it's more interesting than dummy data.

Good luck! 📚
