# WIG-Stocks-Real-Value-Analyzer

## Overview
A Python script for analyzing Polish stock market (WIG) assets by recalculating their historical values against hard currencies (USD) and commodities (Gold). It fetches local stock data and applies conversion rates to account for local currency fluctuations.

## Tech Stack
* **Language:** Python 3
* **Data Processing:** Pandas
* **Integrations:** Yahoo Finance API (`yfinance`), NBP API (National Bank of Poland)
* **Visualization:** Matplotlib

## Technical Implementation
* **API Pagination:** Implements an automated date-based loop to handle the strict 365-day per-request limit of the NBP API.
* **Time Series Alignment:** Uses Pandas outer joins and forward-filling (`ffill()`) to handle missing weekend and holiday data points across different market calendars.
* **Data Export:** Exports the merged and cleaned historical datasets into structured `.json` files.

<img width="1686" height="1021" alt="image" src="https://github.com/user-attachments/assets/72f4337b-0d9d-462e-a377-0f482176d01a" />

## How to run
1. Clone the repo and install dependencies:
```bash
git clone https://github.com/Wodoroscik/WIG-Stocks-Real-Value-Analyzer.git
cd WIG-Stocks-Real-Value-Analyzer 
pip install -r requirements.txt
```
2. Run the script:
```bash
python3 scraper.py
```
