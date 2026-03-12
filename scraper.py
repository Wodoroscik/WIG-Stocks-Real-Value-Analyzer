import pandas as pd
import yfinance as yf
import requests
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import warnings

# Suppress specific yfinance/pandas warnings for cleaner terminal output
warnings.filterwarnings("ignore", category=FutureWarning)

TICKERS = {
    "MOBRUK": "MBR.WA",
    "MWTRADE": "MWT.WA",
    "IZOLACJA": "IZO.WA",
    "AGROTON": "AGT.WA"
}
CODES = ["MBR", "MWT", "IZO", "AGT"]

def fetch_nbp_data(table, code, start_date, end_date):
    """
    Fetches historical data from NBP API. 
    Handles the 365-day per request limit automatically.
    """
    code = code.upper()
    url_base = "http://api.nbp.pl/api/"
    data_list = []
    
    current_start = start_date
    while current_start < end_date:
        current_end = current_start + timedelta(days=365)
        if current_end > end_date:
            current_end = end_date
            
        s_str = current_start.strftime('%Y-%m-%d')
        e_str = current_end.strftime('%Y-%m-%d')
        
        if table == 'cenyzlota':
            url = f"{url_base}cenyzlota/{s_str}/{e_str}/?format=json"
        else:
            url = f"{url_base}exchangerates/rates/{table}/{code}/{s_str}/{e_str}/?format=json"
            
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                if table == 'cenyzlota':
                    for entry in data:
                        data_list.append({'Date': entry['data'], 'Gold_PLN': entry['cena']})
                else:
                    for entry in data['rates']:
                        data_list.append({'Date': entry['effectiveDate'], f'{code}_PLN': entry['mid']})
            else:
                print(f"Warning: Failed to fetch NBP data ({table}/{code}) for {s_str} to {e_str}")
        except Exception as e:
            print(f"NBP API Connection Error: {e}")

        current_start = current_end + timedelta(days=1)

    df = pd.DataFrame(data_list)
    if not df.empty:
        df['Date'] = pd.to_datetime(df['Date'])
        df.set_index('Date', inplace=True)
    return df

def main():
    end_date = datetime.now()
    start_date = datetime(2016, 1, 1)
    start_str = start_date.strftime('%Y-%m-%d')
    end_str = end_date.strftime('%Y-%m-%d')

    print("Fetching reference data from NBP (USD & Gold)...")
    df_usd = fetch_nbp_data('a', 'USD', start_date, end_date)
    df_gold = fetch_nbp_data('cenyzlota', '', start_date, end_date)

    # Merge NBP data and forward-fill missing weekend/holiday rates
    ref_df = df_usd.join(df_gold, how='outer').ffill()

    plt.style.use('seaborn-v0_8')
    fig, axes = plt.subplots(4, 2, figsize=(15, 20))
    plt.subplots_adjust(hspace=0.4)

    print("Fetching stock data from Yahoo Finance...")
    for idx, (name, ticker) in enumerate(TICKERS.items()):
        code_short = CODES[idx]
        
        stock_data = yf.download(ticker, start=start_str, end=end_str, progress=False)
        
        if stock_data.empty:
            print(f"Error: No data for {ticker}. Skipping.")
            continue

        # Handle multi-index columns in recent yfinance versions
        if isinstance(stock_data.columns, pd.MultiIndex):
            stock_data.columns = stock_data.columns.get_level_values(0)
            
        # Export raw data to JSON
        stock_data[['Close']].to_json(f"{code_short}.json", orient='index', date_format='iso')
        
        # Merge stock data with NBP reference data
        merged = stock_data[['Close']].join(ref_df, how='inner')
        merged.dropna(inplace=True)
        
        # Calculate real value
        merged['Close_USD'] = merged['Close'] / merged['USD_PLN']
        merged['Close_Gold'] = merged['Close'] / merged['Gold_PLN']
        
        # Plotting USD
        
        ax_usd = axes[idx, 0]
        ax_usd.plot(merged.index, merged['Close_USD'], color='green', label=f'{code_short} (USD)')
        ax_usd.set_title(f"{name} - Price in USD")
        ax_usd.set_ylabel("Price (USD)")
        ax_usd.grid(True)
        ax_usd.legend()

        # Plotting Gold
        ax_gold = axes[idx, 1]
        ax_gold.plot(merged.index, merged['Close_Gold'], color='gold', label=f'{code_short} (Gold)')
        ax_gold.set_title(f"{name} - Price in Gold")
        ax_gold.set_ylabel("Price (Grams of Gold)")
        ax_gold.grid(True)
        ax_gold.legend()

    print(f"JSON files successfully exported: {', '.join([c + '.json' for c in CODES])}")
    output_filename = "market_analysis_charts.png"
    plt.savefig(output_filename, dpi=600)
    print(f"Visualizations saved to: {output_filename}")

if __name__ == "__main__":
    main()
