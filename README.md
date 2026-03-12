# WIG-Stocks-Real-Value-Analyzer
A Python data pipeline designed to analyze Polish stock market (WIG) assets by stripping away local currency inflation. It fetches historical stock data and recalculates asset values against hard currencies (USD) and commodities (Gold). 

## Tech Stack
* **Python 3**
* **Pandas** (Data manipulation, merging, forward-filling time series data)
* **APIs:** Yahoo Finance (`yfinance`), NBP API (National Bank of Poland)
* **Matplotlib** (Data visualization)

## Engineering Highlights
* **API Pagination Handling:** The National Bank of Poland API strictly limits historical queries to 365 days. The script implements an automated date-chunking loop to bypass this and fetch decades of data seamlessly.
* **Time Series Alignment:** Uses Pandas outer joins and `ffill()` (forward-fill) to elegantly handle market desynchronization (e.g., matching weekend gold prices with Friday stock closes).
* **Data Export:** Automatically dumps cleaned historical datasets into structured `.json` files for further downstream processing.

<img width="1536" height="941" alt="image" src="https://github.com/user-attachments/assets/364823fb-b7e4-44bc-af47-3fae6300c340" />

## How to run
1. Clone the repo and install dependencies:
```bash
pip install -r requirements.txt
```
2. Run the script:
```bash
python scraper.py
```
