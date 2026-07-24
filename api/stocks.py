# -*- coding: utf-8 -*-
from http.server import BaseHTTPRequestHandler
import json
import urllib.parse
import requests
import concurrent.futures

# Full 93 Stocks Initial Dataset
STOCKS_DATABASE = [
    {"id": "us_GOOGL", "market": "US", "marketName": "NASDAQ", "code": "GOOGL", "symbol": "GOOGL.O", "name": "알파벳 (구글)", "englishName": "Alphabet Inc.", "sector": "빅테크/AI", "price": 347.15, "changeRate": -1.38, "per": 21.4, "pbr": 6.8, "roe": 28.5, "dividendYield": 0.4, "bps": 31.46, "eps": 8.52, "marketCap": "2조 2,100억 달러", "fairValue": 468.65, "upsidePotential": 35.0, "valueScore": 98, "tag": "PER", "tagName": "💎 PER 21배 빅테크 최저평가", "naverUrl": "https://finance.naver.com/world/sitemain.naver?symbol=GOOGL.O", "description": "세계 1위 검색엔진 독점 및 유튜브, 제미나이(Gemini) AI 모델 탑재. 빅테크 중 가장 저평가된 PER 21배 수준.", "pros": ["검색엔진 90%+ 시장 지배력", "제미나이 1.5 Pro AI 모델 생태계", "유튜브 광고사익 지속 증가"], "risks": ["미 반독점 소송 리스크", "검색 광고 시장 경쟁"]},
    {"id": "us_MSFT", "market": "US", "marketName": "NASDAQ", "code": "MSFT", "symbol": "MSFT.O", "name": "마이크로소프트", "englishName": "Microsoft", "sector": "클라우드/AI", "price": 397.75, "changeRate": -1.13, "per": 34.5, "pbr": 12.5, "roe": 38.5, "dividendYield": 0.7, "bps": 35.91, "eps": 13.01, "marketCap": "3조 3,300억 달러", "fairValue": 540.0, "upsidePotential": 35.8, "valueScore": 96, "tag": "ROE", "tagName": "🚀 오픈AI & 클라우드 독점", "naverUrl": "https://finance.naver.com/world/sitemain.naver?symbol=MSFT.O", "description": "생성형 AI 시대 최고 리더. 오픈AI 대주주 및 오피스 365 Copilot 구독 모델과 애저(Azure) 클라우드 폭발 성장.", "pros": ["오픈AI 파트너십 독점적 위치", "오피스 Copilot 구독 매출 추가", "애저 클라우드 30%+ 고성장"], "risks": ["AI 인프라 CAPEX 부담", "클라우드 경쟁 심화"]},
    {"id": "us_NVDA", "market": "US", "marketName": "NASDAQ", "code": "NVDA", "symbol": "NVDA.O", "name": "엔비디아", "englishName": "NVIDIA Corp.", "sector": "AI 반도체", "price": 207.29, "changeRate": 1.97, "per": 42.1, "pbr": 28.5, "roe": 65.4, "dividendYield": 0.1, "bps": 4.52, "eps": 3.05, "marketCap": "3조 1,500억 달러", "fairValue": 279.84, "upsidePotential": 35.0, "valueScore": 95, "tag": "ROE", "tagName": "🔥 AI 가속기 90% 독점", "naverUrl": "https://finance.naver.com/world/sitemain.naver?symbol=NVDA.O", "description": "글로벌 AI 반도체 90% 독점 기업. 블랙웰(Blackwell) 신형 AI 가속기 출시에 따른 강력한 영업이익률 유전.", "pros": ["AI GPU 생태계 독점", "영업이익률 60% 압도적 고수익", "블랙웰 아키텍처 수주 폭주"], "risks": ["빅테크 자체 AI 칩 개발", "대만 TSMC 생산 의존도"]},
    {"id": "kr_005380", "market": "KR", "marketName": "KOSPI", "code": "005380", "symbol": "005380", "name": "현대차", "englishName": "Hyundai Motor", "sector": "자동차", "price": 418000, "changeRate": 4.76, "per": 5.2, "pbr": 0.62, "roe": 12.8, "dividendYield": 4.8, "bps": 396000, "eps": 47200, "marketCap": "51조 8,000억원", "fairValue": 564300, "upsidePotential": 35.0, "valueScore": 96, "tag": "PBR", "tagName": "💎 PBR 0.62배 밸류업 대장", "naverUrl": "https://finance.naver.com/item/main.naver?code=005380", "description": "글로벌 완성차 판매 3위 및 인도 법인 상장 추진. 배당수익률 4.8%, PBR 0.62배의 극단적 저평가 상태.", "pros": ["배당수익률 4.8%", "PBR 0.62배 자산 저평가", "하이브리드 & EV 라인업"], "risks": ["글로벌 관세 리스크", "원달러 환율 변동성"]}
]

def fetch_single_live(stock):
    code = stock['code']
    market = stock['market']
    market_name = stock.get('marketName', '')

    ticker = f"{code}.KQ" if market_name == 'KOSDAQ' else (f"{code}.KS" if market == 'KR' else code.replace('.B', '-B'))
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
    headers = {'User-Agent': 'Mozilla/5.0'}

    try:
        r = requests.get(url, headers=headers, timeout=4)
        if r.status_code == 200:
            meta = r.json()['chart']['result'][0]['meta']
            price = meta['regularMarketPrice']
            prev_close = meta.get('previousClose', meta.get('chartPreviousClose', price))
            stock['price'] = int(price) if market == 'KR' else round(float(price), 2)
            if prev_close and prev_close > 0:
                stock['changeRate'] = round(((price - prev_close) / prev_close) * 100, 2)
    except Exception:
        pass
    return stock

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Refresh live quotes on Vercel Cloud Serverless execution
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            updated = list(executor.map(fetch_single_live, STOCKS_DATABASE))

        self.send_response(200)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(updated, ensure_ascii=False).encode('utf-8'))
