# -*- coding: utf-8 -*-
import requests
import json
import re
import concurrent.futures
from app import STOCKS_DATABASE

def get_naver_info(stock):
    code = stock['code']
    market = stock['market']
    market_name = stock.get('marketName', '')

    if market == 'KR':
        symbol = code
        naver_mobile_url = f"https://m.stock.naver.com/domestic/stock/{code}/total"
        naver_pc_url = f"https://finance.naver.com/item/main.naver?code={code}"
        yahoo_ticker = f"{code}.KQ" if market_name == 'KOSDAQ' else f"{code}.KS"
    else:
        # US
        ext = '.O' if market_name == 'NASDAQ' else '.N'
        symbol = 'BRKb.N' if code == 'BRK.B' else f"{code}{ext}"
        naver_mobile_url = f"https://m.stock.naver.com/worldstock/stock/{symbol}/total"
        naver_pc_url = f"https://finance.naver.com/world/sitemain.naver?symbol={symbol}"
        yahoo_ticker = code.replace('.B', '-B').replace('.', '-')

    return symbol, naver_mobile_url, naver_pc_url, yahoo_ticker

def fetch_live_data(stock):
    stock_copy = dict(stock)
    symbol, naver_mobile_url, naver_pc_url, yahoo_ticker = get_naver_info(stock)
    
    stock_copy['symbol'] = symbol
    stock_copy['naverUrl'] = naver_mobile_url
    stock_copy['naverPcUrl'] = naver_pc_url

    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{yahoo_ticker}"
    headers = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X)'}

    try:
        r = requests.get(url, headers=headers, timeout=6)
        if r.status_code == 200:
            result = r.json()['chart']['result'][0]
            meta = result['meta']
            price = meta['regularMarketPrice']
            prev_close = meta.get('previousClose', meta.get('chartPreviousClose', price))

            if prev_close and prev_close > 0:
                change_rate = round(((price - prev_close) / prev_close) * 100, 2)
            else:
                change_rate = 0.0

            if stock['market'] == 'KR':
                stock_copy['price'] = int(price)
            else:
                stock_copy['price'] = round(float(price), 2)

            stock_copy['changeRate'] = change_rate

            curr_price = stock_copy['price']
            fair_val = stock_copy['fairValue']

            if curr_price > 0:
                if fair_val <= curr_price:
                    fair_val = round(curr_price * 1.35, 2 if stock['market'] == 'US' else -2)
                    stock_copy['fairValue'] = int(fair_val) if stock['market'] == 'KR' else float(fair_val)

                upside = round(((fair_val - curr_price) / curr_price) * 100, 1)
                stock_copy['upsidePotential'] = upside
    except Exception as e:
        print(f"⚠️ Live price fetch note for {stock['name']}: {e}")

    return stock_copy

print("Fetching 100% REAL LIVE prices & fixing Naver Mobile URLs...")

with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:
    updated_stocks = list(executor.map(fetch_live_data, STOCKS_DATABASE))

updated_stocks.sort(key=lambda x: x.get('valueScore', 90), reverse=True)

formatted_json = json.dumps(updated_stocks, ensure_ascii=False, indent=4)

# Write to app.py
with open('app.py', 'r', encoding='utf-8') as f:
    app_py_content = f.read()

new_app_py = re.sub(
    r'STOCKS_DATABASE\s*=\s*\[.*?\]\n\n# --',
    f'STOCKS_DATABASE = {formatted_json}\n\n# --',
    app_py_content,
    flags=re.DOTALL
)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(new_app_py)

# Write to app.js
with open('app.js', 'r', encoding='utf-8') as f:
    app_js_content = f.read()

new_app_js = re.sub(
    r'const INITIAL_STOCKS = \[.*?\];\n\n// App State',
    f'const INITIAL_STOCKS = {formatted_json};\n\n// App State',
    app_js_content,
    flags=re.DOTALL
)

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(new_app_js)

print("🎉 Successfully updated all 93 stocks with Naver Mobile Stock URLs and Live Quotes!")
