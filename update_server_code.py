# -*- coding: utf-8 -*-
import sys
import os
import json
import urllib.request
import urllib.parse
import threading
import time
import requests
from bs4 import BeautifulSoup
from http.server import HTTPServer, SimpleHTTPRequestHandler
import concurrent.futures

from app import STOCKS_DATABASE

def get_yahoo_ticker(stock):
    code = stock['code']
    market = stock['market']
    market_name = stock.get('marketName', '')

    if market == 'KR':
        if market_name == 'KOSDAQ':
            return f"{code}.KQ"
        return f"{code}.KS"
    else:
        return code.replace('.B', '-B').replace('.', '-')

def fetch_single_live(stock):
    ticker = get_yahoo_ticker(stock)
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    try:
        r = requests.get(url, headers=headers, timeout=5)
        if r.status_code == 200:
            result = r.json()['chart']['result'][0]
            meta = result['meta']
            price = meta['regularMarketPrice']
            prev_close = meta.get('previousClose', meta.get('chartPreviousClose', price))
            
            change_rate = round(((price - prev_close) / prev_close) * 100, 2) if prev_close else 0.0

            stock['price'] = int(price) if stock['market'] == 'KR' else round(float(price), 2)
            stock['changeRate'] = change_rate
            
            # Recalculate upside
            curr_price = stock['price']
            fair_val = stock['fairValue']
            if curr_price > 0:
                if fair_val <= curr_price:
                    fair_val = round(curr_price * 1.35, 2 if stock['market'] == 'US' else -2)
                    stock['fairValue'] = int(fair_val) if stock['market'] == 'KR' else float(fair_val)
                stock['upsidePotential'] = round(((fair_val - curr_price) / curr_price) * 100, 1)
    except Exception as e:
        pass
    return stock

def refresh_all_stocks_live():
    global STOCKS_DATABASE
    with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:
        updated = list(executor.map(fetch_single_live, STOCKS_DATABASE))
    STOCKS_DATABASE = updated
    print(f"[{time.strftime('%H:%M:%S')}] 🔴 Refreshed live prices for {len(STOCKS_DATABASE)} stocks.")

def live_updater_loop():
    while True:
        try:
            refresh_all_stocks_live()
        except Exception as e:
            print("Live update loop error:", e)
        time.sleep(30) # Refresh every 30 seconds

# HTTP Handler
class StockAppRequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        
        if parsed_path.path == '/api/stocks':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(STOCKS_DATABASE, ensure_ascii=False).encode('utf-8'))
            return
            
        if parsed_path.path == '/api/refresh-live':
            refresh_all_stocks_live()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"success": True, "count": len(STOCKS_DATABASE), "data": STOCKS_DATABASE}, ensure_ascii=False).encode('utf-8'))
            return

        return super().do_GET()

def run_server(port=8080):
    # Start live price updater thread
    updater_thread = threading.Thread(target=live_updater_loop, daemon=True)
    updater_thread.start()

    server_address = ('0.0.0.0', port)
    httpd = HTTPServer(server_address, StockAppRequestHandler)
    print(f"=================================================================")
    print(f"전영재 전용 실시간 주식 큐레이션 서버 (93개 실시간 시세 동기화) 실행 중!")
    print(f"로컬 접속: http://localhost:{port}")
    print(f"=================================================================")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n서버를 종료합니다.")
        httpd.server_close()

if __name__ == '__main__':
    port = 8080
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        port = int(sys.argv[1])
    run_server(port)
