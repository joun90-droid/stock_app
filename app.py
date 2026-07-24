# -*- coding: utf-8 -*-
"""
=============================================================================
전영재 전용 주식종목 찾기 (app.py) - 52개 대표 종목 데이터베이스
Naver Finance Undervalued Stock Scraper & Web Server API for Jeon Young-jae
=============================================================================
"""

import sys
import os
import json
import time
import threading
import urllib.request
import urllib.parse
from http.server import HTTPServer, SimpleHTTPRequestHandler
import requests
from bs4 import BeautifulSoup

if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# ---------------------------------------------------------------------------
# Full 52 Stocks Database (KOSPI, KOSDAQ, NYSE, NASDAQ)
# ---------------------------------------------------------------------------
STOCKS_DATABASE = [
    {
        "id": "kr_105560",
        "market": "KR",
        "marketName": "KOSPI",
        "code": "105560",
        "symbol": "105560",
        "name": "KB금융",
        "englishName": "KB Financial Group",
        "sector": "금융/은행",
        "price": 176300,
        "changeRate": 0.69,
        "per": 5.8,
        "pbr": 0.48,
        "roe": 10.9,
        "dividendYield": 6.1,
        "bps": 171600,
        "eps": 14200,
        "marketCap": "33조 2,000억원",
        "fairValue": 236400,
        "upsidePotential": 34.1,
        "valueScore": 99,
        "tag": "DIV",
        "tagName": "💰 전영재 배당 1픽 (6.1%)",
        "naverUrl": "https://m.stock.naver.com/domestic/stock/105560/total",
        "description": "전영재 배당수익 최상위 픽! PBR 0.48배의 심각한 저평가 구간. 분기 배당 실시 및 총주주환원율 40% 목표 설정으로 한국 밸류업 프로그램 최대 수혜주.",
        "pros": [
            "PBR 0.48배 청산가치 미달",
            "배당수익률 6.1% 분기배당",
            "자사주 매입/소각 확대"
        ],
        "risks": [
            "금리 인하 시 NIM 압박",
            "부동산 PF 리스크"
        ],
        "naverPcUrl": "https://finance.naver.com/item/main.naver?code=105560"
    },
    {
        "id": "kr_005380",
        "market": "KR",
        "marketName": "KOSPI",
        "code": "005380",
        "symbol": "005380",
        "name": "현대차",
        "englishName": "Hyundai Motor",
        "sector": "자동차/제조",
        "price": 432000,
        "changeRate": 3.35,
        "per": 5.2,
        "pbr": 0.62,
        "roe": 14.2,
        "dividendYield": 5.2,
        "bps": 396000,
        "eps": 47200,
        "marketCap": "52조 4,000억원",
        "fairValue": 564300,
        "upsidePotential": 30.6,
        "valueScore": 98,
        "tag": "PBR",
        "tagName": "💎 전영재 1픽 초저PBR (0.62배)",
        "naverUrl": "https://m.stock.naver.com/domestic/stock/005380/total",
        "description": "전영재 강력 추천 1위! PBR 0.6배 수준의 극단적 저평가 상태이며, 높은 ROE(14%+)와 주주환원 자사주 소각/고배당(5%+) 정책으로 밸류체인 재평가 진행 중.",
        "pros": [
            "PBR 0.62배 자산가치 극저평가",
            "배당수익률 5.2% 고배당",
            "하이브리드 & 전기차 경쟁력 1위"
        ],
        "risks": [
            "글로벌 자동차 경기 변동성",
            "환율 변동 위험"
        ],
        "naverPcUrl": "https://finance.naver.com/item/main.naver?code=005380"
    },
    {
        "id": "kr_086790",
        "market": "KR",
        "marketName": "KOSPI",
        "code": "086790",
        "symbol": "086790",
        "name": "하나금융지주",
        "englishName": "Hana Financial",
        "sector": "금융/은행",
        "price": 130500,
        "changeRate": -0.84,
        "per": 4.8,
        "pbr": 0.41,
        "roe": 10.5,
        "dividendYield": 6.4,
        "bps": 154100,
        "eps": 13160,
        "marketCap": "18조 2,000억원",
        "fairValue": 177700,
        "upsidePotential": 36.2,
        "valueScore": 98,
        "tag": "DIV",
        "tagName": "💰 배당 6.4% 초저PBR",
        "naverUrl": "https://m.stock.naver.com/domestic/stock/086790/total",
        "description": "PBR 0.41배, PER 4.8배로 국내 은행주 중 극단적 저평가. 배당수익률 6.4%에 분기배당 시행으로 안정적 현금흐름 제공.",
        "pros": [
            "PBR 0.41배 청산가치 극저평가",
            "배당수익률 6.4% 분기배당",
            "자사주 소각 추진"
        ],
        "risks": [
            "환율 변동성 부담",
            "대손 비용 증가"
        ],
        "naverPcUrl": "https://finance.naver.com/item/main.naver?code=086790"
    },
    {
        "id": "us_GOOGL",
        "market": "US",
        "marketName": "NASDAQ",
        "code": "GOOGL",
        "symbol": "GOOGL.O",
        "name": "알파벳 (구글)",
        "englishName": "Alphabet (Google)",
        "sector": "빅테크/인터넷",
        "price": 318.3,
        "changeRate": -6.96,
        "per": 21.5,
        "pbr": 5.8,
        "roe": 28.5,
        "dividendYield": 0.4,
        "bps": 31.46,
        "eps": 8.48,
        "marketCap": "2조 2,600억 달러",
        "fairValue": 429.71,
        "upsidePotential": 35.0,
        "valueScore": 98,
        "tag": "ROE",
        "tagName": "🚀 전영재 미국 1픽 빅테크 저평가",
        "naverUrl": "https://m.stock.naver.com/worldstock/stock/GOOGL.O/total",
        "description": "전영재 추천 미국 빅테크 1위! M7 대형주 중 가장 저평가된 거인. 검색 독점력과 클라우드 고성장, 자체 AI 칩(TPU) 및 제미나이 AI 생태계 구축.",
        "pros": [
            "M7 대형주 중 최저 PER(21배)",
            "검색 & 유튜브 캐시카우 현금흐름",
            "클라우드 30%+ 고성장"
        ],
        "risks": [
            "반독점 소송 이슈",
            "AI 검색 전환기 비용 증가"
        ],
        "naverPcUrl": "https://finance.naver.com/world/sitemain.naver?symbol=GOOGL.O"
    },
    {
        "id": "us_PYPL",
        "market": "US",
        "marketName": "NASDAQ",
        "code": "PYPL",
        "symbol": "PYPL.O",
        "name": "페이팔",
        "englishName": "PayPal Holdings",
        "sector": "핀테크/결제",
        "price": 55.07,
        "changeRate": -0.79,
        "per": 14.5,
        "pbr": 2.1,
        "roe": 18.2,
        "dividendYield": 0.0,
        "bps": 30.57,
        "eps": 4.42,
        "marketCap": "660억 달러",
        "fairValue": 98.0,
        "upsidePotential": 78.0,
        "valueScore": 98,
        "tag": "PER",
        "tagName": "📉 전영재 1픽 FCF 부자 PER 14배",
        "naverUrl": "https://m.stock.naver.com/worldstock/stock/PYPL.O/total",
        "description": "전영재 강추 핀테크 저평가 1위! 연간 50억 달러 이상 잉여현금흐름(FCF) 창출. PER 14.5배 및 대규모 자사주 소각 진행.",
        "pros": [
            "PER 14.5배 및 FCF 50억 달러 창출",
            "시총 7~8% 수준 자사주 소각",
            "Fastlane 간편결제 신제품 도입"
        ],
        "risks": [
            "애플페이 등 결제 경쟁",
            "마진율 압박"
        ],
        "naverPcUrl": "https://finance.naver.com/world/sitemain.naver?symbol=PYPL.O"
    },
    {
        "id": "us_EXPE",
        "market": "US",
        "marketName": "NASDAQ",
        "code": "EXPE",
        "symbol": "EXPE.O",
        "name": "익스피디아 그룹",
        "englishName": "Expedia Group",
        "sector": "여행 테크",
        "price": 258.99,
        "changeRate": -0.8,
        "per": 11.4,
        "pbr": 4.8,
        "roe": 40.0,
        "dividendYield": 0.0,
        "bps": 27.5,
        "eps": 11.57,
        "marketCap": "172억 달러",
        "fairValue": 349.64,
        "upsidePotential": 35.0,
        "valueScore": 98,
        "tag": "PER",
        "tagName": "📉 전영재 1픽 초저PER 11.4배 여행테크",
        "naverUrl": "https://m.stock.naver.com/worldstock/stock/EXPE.O/total",
        "description": "전영재 1픽 저평가! Expedia, Hotels.com, Vrbo 플랫폼 보유. PER 11.4배로 여행 테크 중 최고 가치 매력.",
        "pros": [
            "PER 11.4배 극단적 저평가",
            "Hotels.com & One Key 리워드 통합",
            "ROE 40% 및 대규모 자사주 소각"
        ],
        "risks": [
            "구글/부킹닷컴과 경쟁",
            "여행 경기 침체"
        ],
        "naverPcUrl": "https://finance.naver.com/world/sitemain.naver?symbol=EXPE.O"
    },
    {
        "id": "kr_000270",
        "market": "KR",
        "marketName": "KOSPI",
        "code": "000270",
        "symbol": "000270",
        "name": "기아",
        "englishName": "Kia Corporation",
        "sector": "자동차/제조",
        "price": 149800,
        "changeRate": 2.04,
        "per": 4.1,
        "pbr": 0.76,
        "roe": 21.4,
        "dividendYield": 5.8,
        "bps": 155500,
        "eps": 28820,
        "marketCap": "47조 8,000억원",
        "fairValue": 175000,
        "upsidePotential": 16.8,
        "valueScore": 97,
        "tag": "ROE",
        "tagName": "💎 고ROE 21.4% 1위",
        "naverUrl": "https://m.stock.naver.com/domestic/stock/000270/total",
        "description": "ROE 21.4%의 압도적 수익성을 자랑하는 완성차 기업. PER 4.1배 수준으로 세계 주요 완성차 중 최저 수준.",
        "pros": [
            "ROE 21.4% 글로벌 완성차 1위급",
            "PER 4.1배 극저평가",
            "RV/SUV 고수익 차종 비중 70%+"
        ],
        "risks": [
            "글로벌 관세 장벽 리스크",
            "전기차 수요 둔화"
        ],
        "naverPcUrl": "https://finance.naver.com/item/main.naver?code=000270"
    },
    {
        "id": "kr_017670",
        "market": "KR",
        "marketName": "KOSPI",
        "code": "017670",
        "symbol": "017670",
        "name": "SK텔레콤",
        "englishName": "SK Telecom",
        "sector": "통신",
        "price": 99500,
        "changeRate": 5.74,
        "per": 9.2,
        "pbr": 0.85,
        "roe": 9.8,
        "dividendYield": 6.8,
        "bps": 64400,
        "eps": 5950,
        "marketCap": "11조 8,000억원",
        "fairValue": 127000,
        "upsidePotential": 27.6,
        "valueScore": 97,
        "tag": "DIV",
        "tagName": "💰 고배당 6.8% 방어주",
        "naverUrl": "https://m.stock.naver.com/domestic/stock/017670/total",
        "description": "국내 1위 이동통신 사업자. 배당수익률 6.8%에 달하는 대표 현금흐름 방어주. AI 데이터센터 및 에이닷 AI 서비스 확장.",
        "pros": [
            "배당수익률 6.8% 초고배당",
            "경기 방어적 안정적 현금흐름",
            "AI 데이터센터 신성장동력"
        ],
        "risks": [
            "통신 요금 인하 압박",
            "5G 가입자 성장 둔화"
        ],
        "naverPcUrl": "https://finance.naver.com/item/main.naver?code=017670"
    },
    {
        "id": "us_BRKB",
        "market": "US",
        "marketName": "NYSE",
        "code": "BRK.B",
        "symbol": "BRKb.N",
        "name": "버크셔 해서웨이",
        "englishName": "Berkshire Hathaway",
        "sector": "금융/지주사",
        "price": 487.09,
        "changeRate": -0.47,
        "per": 18.2,
        "pbr": 1.45,
        "roe": 14.8,
        "dividendYield": 0.0,
        "bps": 307.45,
        "eps": 24.5,
        "marketCap": "9,650억 달러",
        "fairValue": 530.0,
        "upsidePotential": 8.8,
        "valueScore": 97,
        "tag": "PBR",
        "tagName": "🛡️ 워런 버핏가치주",
        "naverUrl": "https://m.stock.naver.com/worldstock/stock/BRKb.N/total",
        "description": "워런 버핏이 이끄는 세계 최대 복합 가치투자 기업. 철도, 보험, 에너지 및 역대 최대 현금(1,800억 달러+) 보유로 경기 하락기 최고의 방어주.",
        "pros": [
            "1,800억 달러 압도적 현금성 자산",
            "버크셔 독점 포트폴리오 안전성",
            "자사주 매입을 통한 가치 제고"
        ],
        "risks": [
            "워런 버핏 승계 이슈",
            "거대 규모에 따른 성장 속도"
        ],
        "naverPcUrl": "https://finance.naver.com/world/sitemain.naver?symbol=BRKb.N"
    },
    {
        "id": "us_QCOM",
        "market": "US",
        "marketName": "NASDAQ",
        "code": "QCOM",
        "symbol": "QCOM.O",
        "name": "퀄컴",
        "englishName": "Qualcomm",
        "sector": "통신/온디바이스AI",
        "price": 172.92,
        "changeRate": -1.54,
        "per": 15.2,
        "pbr": 6.8,
        "roe": 31.0,
        "dividendYield": 2.0,
        "bps": 25.76,
        "eps": 11.52,
        "marketCap": "1,950억 달러",
        "fairValue": 235.0,
        "upsidePotential": 35.9,
        "valueScore": 97,
        "tag": "PER",
        "tagName": "📉 전영재 픽 PER 15배 저평가",
        "naverUrl": "https://m.stock.naver.com/worldstock/stock/QCOM.O/total",
        "description": "스냅드래곤 X 엘리트 PC 칩 및 온디바이스 AI 스마트폰 칩 선도. PER 15.2배로 반도체 대형주 중 극저평가.",
        "pros": [
            "PER 15.2배 저평가 반도체",
            "스냅드래곤 AI PC 시장 확장",
            "전장(Auto) 반도체 수주 잔고 급증"
        ],
        "risks": [
            "애플 자체 모뎀 칩 개발",
            "스마트폰 교체 주기 변수"
        ],
        "naverPcUrl": "https://finance.naver.com/world/sitemain.naver?symbol=QCOM.O"
    },
    {
        "id": "us_MU",
        "market": "US",
        "marketName": "NASDAQ",
        "code": "MU",
        "symbol": "MU.O",
        "name": "마이크론 테크놀로지",
        "englishName": "Micron Technology",
        "sector": "메모리/HBM",
        "price": 988.49,
        "changeRate": 3.02,
        "per": 14.2,
        "pbr": 2.1,
        "roe": 18.5,
        "dividendYield": 0.4,
        "bps": 53.57,
        "eps": 7.92,
        "marketCap": "1,245억 달러",
        "fairValue": 1334.46,
        "upsidePotential": 35.0,
        "valueScore": 97,
        "tag": "PBR",
        "tagName": "💎 PBR 2.1배 HBM3E 고성장",
        "naverUrl": "https://m.stock.naver.com/worldstock/stock/MU.O/total",
        "description": "엔비디아 HBM3E 8단/12단 주요 공급업체로 선정. PBR 2.1배로 메모리 턴어라운드 전영재 저평가 핵심 매수 종목.",
        "pros": [
            "엔비디아 HBM3E 공급 본궤도",
            "PBR 2.1배 자산저평가",
            "DRAM/NAND 가격 상승 사이클"
        ],
        "risks": [
            "메모리 가격 사이클 변동성",
            "삼성전자/SK하이닉스와 경쟁"
        ],
        "naverPcUrl": "https://finance.naver.com/world/sitemain.naver?symbol=MU.O"
    },
    {
        "id": "us_CMCSA",
        "market": "US",
        "marketName": "NASDAQ",
        "code": "CMCSA",
        "symbol": "CMCSA.O",
        "name": "컴캐스트",
        "englishName": "Comcast Corporation",
        "sector": "미디어/통신",
        "price": 23.42,
        "changeRate": -0.43,
        "per": 10.2,
        "pbr": 1.2,
        "roe": 16.5,
        "dividendYield": 3.2,
        "bps": 32.08,
        "eps": 3.77,
        "marketCap": "1,510억 달러",
        "fairValue": 54.0,
        "upsidePotential": 130.6,
        "valueScore": 97,
        "tag": "PER",
        "tagName": "📉 PER 10배 극단적 저평가",
        "naverUrl": "https://m.stock.naver.com/worldstock/stock/CMCSA.O/total",
        "description": "유니버설 스튜디오, 피콕 OTT, 초고속 인터넷 인프라 보유. PER 10.2배로 주가 청산 수준의 초저평가 전영재 픽.",
        "pros": [
            "PER 10.2배 극단적 저평가",
            "유니버설 테마파크 & 영화 IP",
            "배당 3.2% 및 자사주 매입"
        ],
        "risks": [
            "케이블 TV 코드커팅 이탈",
            "OTT 피콕 적자"
        ],
        "naverPcUrl": "https://finance.naver.com/world/sitemain.naver?symbol=CMCSA.O"
    },
    {
        "id": "us_ABNB",
        "market": "US",
        "marketName": "NASDAQ",
        "code": "ABNB",
        "symbol": "ABNB.O",
        "name": "에어비앤비",
        "englishName": "Airbnb Inc.",
        "sector": "숙박 플랫폼",
        "price": 137.71,
        "changeRate": -1.67,
        "per": 18.5,
        "pbr": 8.4,
        "roe": 41.0,
        "dividendYield": 0.0,
        "bps": 17.61,
        "eps": 8.0,
        "marketCap": "930억 달러",
        "fairValue": 198.0,
        "upsidePotential": 43.8,
        "valueScore": 97,
        "tag": "PER",
        "tagName": "📉 전영재 픽 PER 18배 마진 35%",
        "naverUrl": "https://m.stock.naver.com/worldstock/stock/ABNB.O/total",
        "description": "세계 1위 공유 숙박 네트워크. FCF 마진 35%+ 및 PER 18.5배로 현금흐름 대비 주가 극저평가 전영재 픽.",
        "pros": [
            "PER 18.5배 현금 흐름 우수",
            "FCF 마진 35% 이상",
            "장기 숙박 및 체험 상품 확대"
        ],
        "risks": [
            "각국 도시 단기 숙박 규제",
            "여행 수요 변동"
        ],
        "naverPcUrl": "https://finance.naver.com/world/sitemain.naver?symbol=ABNB.O"
    },
    {
        "id": "us_LULU",
        "market": "US",
        "marketName": "NASDAQ",
        "code": "LULU",
        "symbol": "LULU.O",
        "name": "룰루레몬 아틀레티카",
        "englishName": "Lululemon Athletica",
        "sector": "프리미엄 의류",
        "price": 111.45,
        "changeRate": -1.69,
        "per": 20.2,
        "pbr": 8.2,
        "roe": 42.0,
        "dividendYield": 0.0,
        "bps": 35.97,
        "eps": 14.6,
        "marketCap": "362억 달러",
        "fairValue": 420.0,
        "upsidePotential": 276.9,
        "valueScore": 97,
        "tag": "PER",
        "tagName": "📉 전영재 픽 PER 20배 바닥권 매수",
        "naverUrl": "https://m.stock.naver.com/worldstock/stock/LULU.O/total",
        "description": "프리미엄 애슬레저 1위 브랜드. 고성장세 대비 주가 40% 조정으로 PER 20.2배 역사적 저평가 전영재 픽.",
        "pros": [
            "PER 20.2배 역사적 바닥 수준",
            "ROE 42% 브랜드 프리미엄",
            "중국 및 글로벌 매장 고성장"
        ],
        "risks": [
            "북미 의류 소비 둔화 우려",
            "경쟁 브랜드 저가화"
        ],
        "naverPcUrl": "https://finance.naver.com/world/sitemain.naver?symbol=LULU.O"
    },
    {
        "id": "kr_000660",
        "market": "KR",
        "marketName": "KOSPI",
        "code": "000660",
        "symbol": "000660",
        "name": "SK하이닉스",
        "englishName": "SK Hynix",
        "sector": "반도체/HBM",
        "price": 1919000,
        "changeRate": 4.86,
        "per": 10.8,
        "pbr": 1.85,
        "roe": 18.5,
        "dividendYield": 1.2,
        "bps": 121300,
        "eps": 20780,
        "marketCap": "163조 4,000억원",
        "fairValue": 2470500,
        "upsidePotential": 28.7,
        "valueScore": 96,
        "tag": "ROE",
        "tagName": "🚀 HBM 독점 주도",
        "naverUrl": "https://m.stock.naver.com/domestic/stock/000660/total",
        "description": "엔비디아 HBM3E 독점 공급망 형성. 글로벌 AI 반도체 메모리 리더로서 주가 밸류에이션 리레이팅 지속 진행 중.",
        "pros": [
            "HBM 시장 1위 독점력",
            "영업이익률 40%+ 육박",
            "AI 서버 메모리 폭발적 수요"
        ],
        "risks": [
            "사이클 반도체 변동성",
            "경쟁사 HBM 진입 리스크"
        ],
        "naverPcUrl": "https://finance.naver.com/item/main.naver?code=000660"
    },
    {
        "id": "kr_002380",
        "market": "KR",
        "marketName": "KOSPI",
        "code": "002380",
        "symbol": "002380",
        "name": "KCC",
        "englishName": "KCC",
        "sector": "건자재/화학",
        "price": 440500,
        "changeRate": 5.01,
        "per": 5.9,
        "pbr": 0.38,
        "roe": 7.2,
        "dividendYield": 3.8,
        "bps": 748000,
        "eps": 48200,
        "marketCap": "2조 5,000억원",
        "fairValue": 480000,
        "upsidePotential": 9.0,
        "valueScore": 96,
        "tag": "PBR",
        "tagName": "💎 PBR 0.38배 초저평가",
        "naverUrl": "https://m.stock.naver.com/domestic/stock/002380/total",
        "description": "삼성물산 지분 9.1% 등 보유 주식자산가치만 약 3조원 돌파. 현재 시가총액이 보유 주식가치보다 작아서 PBR 0.38배 수준.",
        "pros": [
            "보유 지분가치가 시가총액 상회",
            "PBR 0.38배 자산 극저평가",
            "실리콘 업황 턴어라운드"
        ],
        "risks": [
            "건설 경기 둔화",
            "차입금 이자 부담"
        ],
        "naverPcUrl": "https://finance.naver.com/item/main.naver?code=002380"
    },
    {
        "id": "us_MSFT",
        "market": "US",
        "marketName": "NASDAQ",
        "code": "MSFT",
        "symbol": "MSFT.O",
        "name": "마이크로소프트",
        "englishName": "Microsoft",
        "sector": "클라우드/AI",
        "price": 388.94,
        "changeRate": -0.36,
        "per": 34.5,
        "pbr": 12.5,
        "roe": 38.5,
        "dividendYield": 0.7,
        "bps": 35.91,
        "eps": 13.01,
        "marketCap": "3조 3,300억 달러",
        "fairValue": 540.0,
        "upsidePotential": 38.8,
        "valueScore": 96,
        "tag": "ROE",
        "tagName": "🚀 오픈AI & 클라우드 독점",
        "naverUrl": "https://m.stock.naver.com/worldstock/stock/MSFT.O/total",
        "description": "생성형 AI 시대 최고 리더. 오픈AI 대주주 및 오피스 365 Copilot 구독 모델과 애저(Azure) 클라우드 폭발 성장.",
        "pros": [
            "오픈AI 파트너십 독점적 위치",
            "오피스 Copilot 구독 매출 추가",
            "애저 클라우드 30%+ 고성장"
        ],
        "risks": [
            "AI 인프라 CAPEX 부담",
            "클라우드 경쟁 심화"
        ],
        "naverPcUrl": "https://finance.naver.com/world/sitemain.naver?symbol=MSFT.O"
    },
    {
        "id": "us_AVGO",
        "market": "US",
        "marketName": "NASDAQ",
        "code": "AVGO",
        "symbol": "AVGO.O",
        "name": "브로드컴",
        "englishName": "Broadcom Inc.",
        "sector": "반도체/네트워크",
        "price": 394.91,
        "changeRate": -0.48,
        "per": 28.4,
        "pbr": 11.2,
        "roe": 32.4,
        "dividendYield": 1.4,
        "bps": 14.53,
        "eps": 5.73,
        "marketCap": "7,620억 달러",
        "fairValue": 533.13,
        "upsidePotential": 35.0,
        "valueScore": 96,
        "tag": "ROE",
        "tagName": "🚀 맞춤형 ASIC AI 칩 1위",
        "naverUrl": "https://m.stock.naver.com/worldstock/stock/AVGO.O/total",
        "description": "구글, 메타 맞춤형 AI 반도체(ASIC) 설계 독점 및 VM웨어 인수를 통한 기업용 클라우드 소프트웨어 통합.",
        "pros": [
            "맞춤형 AI ASIC 칩 시장 독점력",
            "VM웨어 구독 매출 시너지",
            "지속적인 배당 증액"
        ],
        "risks": [
            "VM웨어 기업 고객 이탈",
            "부채 비율 관리"
        ],
        "naverPcUrl": "https://finance.naver.com/world/sitemain.naver?symbol=AVGO.O"
    },
    {
        "id": "us_AMAT",
        "market": "US",
        "marketName": "NASDAQ",
        "code": "AMAT",
        "symbol": "AMAT.O",
        "name": "어플라이드 머티리얼즈",
        "englishName": "Applied Materials",
        "sector": "반도체 장비",
        "price": 562.96,
        "changeRate": 1.63,
        "per": 18.5,
        "pbr": 7.4,
        "roe": 35.2,
        "dividendYield": 0.8,
        "bps": 29.09,
        "eps": 11.63,
        "marketCap": "1,780억 달러",
        "fairValue": 760.0,
        "upsidePotential": 35.0,
        "valueScore": 96,
        "tag": "PER",
        "tagName": "📉 반도체 장비 1위 PER 18배",
        "naverUrl": "https://m.stock.naver.com/worldstock/stock/AMAT.O/total",
        "description": "세계 1위 반도체 종합 증착/재료 장비 기업. HBM 및 초미세 파운드리 공정 필수 장비 공급으로 전영재 추천 가치주.",
        "pros": [
            "세계 1위 반도체 장비 포트폴리오",
            "PER 18.5배 안정적 밸류에이션",
            "ROE 35.2% 고수익성"
        ],
        "risks": [
            "중국 수출 제한 규제",
            "반도체 설비투자(CAPEX) 주기"
        ],
        "naverPcUrl": "https://finance.naver.com/world/sitemain.naver?symbol=AMAT.O"
    },
    {
        "id": "us_LRCX",
        "market": "US",
        "marketName": "NASDAQ",
        "code": "LRCX",
        "symbol": "LRCX.O",
        "name": "램리서치",
        "englishName": "Lam Research",
        "sector": "반도체 식각장비",
        "price": 320.73,
        "changeRate": 0.45,
        "per": 20.1,
        "pbr": 11.8,
        "roe": 52.0,
        "dividendYield": 1.0,
        "bps": 80.67,
        "eps": 47.36,
        "marketCap": "1,240억 달러",
        "fairValue": 1280.0,
        "upsidePotential": 299.1,
        "valueScore": 96,
        "tag": "ROE",
        "tagName": "💎 ROE 52% HBM 식각 1위",
        "naverUrl": "https://m.stock.naver.com/worldstock/stock/LRCX.O/total",
        "description": "메모리 낸드(NAND) 및 HBM 고단 적층용 플라즈마 식각 장비 세계 1위. ROE 52%의 강력한 이익 창출력.",
        "pros": [
            "HBM & 3D NAND 식각 독점력",
            "ROE 52% 극상위 수익성",
            "메모리 업황 턴어라운드 수혜"
        ],
        "risks": [
            "메모리 제조사 투자 시점 변수",
            "대중국 수출 규제"
        ],
        "naverPcUrl": "https://finance.naver.com/world/sitemain.naver?symbol=LRCX.O"
    },
    {
        "id": "us_GILD",
        "market": "US",
        "marketName": "NASDAQ",
        "code": "GILD",
        "symbol": "GILD.O",
        "name": "길리어드 사이언스",
        "englishName": "Gilead Sciences",
        "sector": "바이오/제약",
        "price": 128.47,
        "changeRate": -1.44,
        "per": 11.8,
        "pbr": 3.4,
        "roe": 28.5,
        "dividendYield": 4.2,
        "bps": 21.29,
        "eps": 6.13,
        "marketCap": "902억 달러",
        "fairValue": 173.43,
        "upsidePotential": 35.0,
        "valueScore": 96,
        "tag": "DIV",
        "tagName": "💰 고배당 4.2% 저PER 바이오",
        "naverUrl": "https://m.stock.naver.com/worldstock/stock/GILD.O/total",
        "description": "HIV 치료제 시장 80% 독점 및 항암 신약(트로델비) 파이프라인 고성장. 배당 4.2%와 PER 11.8배 전영재 가치 바이오주.",
        "pros": [
            "배당수익률 4.2% 고배당",
            "PER 11.8배 저평가",
            "HIV 장기 지속형 신약 독점"
        ],
        "risks": [
            "항암제 임상3상 결과 변수",
            "특허 만료 일정"
        ],
        "naverPcUrl": "https://finance.naver.com/world/sitemain.naver?symbol=GILD.O"
    },
    {
        "id": "us_NXPI",
        "market": "US",
        "marketName": "NASDAQ",
        "code": "NXPI",
        "symbol": "NXPI.O",
        "name": "NXP 반도체",
        "englishName": "NXP Semiconductors",
        "sector": "차량용 반도체",
        "price": 277.48,
        "changeRate": -0.48,
        "per": 15.8,
        "pbr": 6.2,
        "roe": 38.0,
        "dividendYield": 1.5,
        "bps": 42.74,
        "eps": 16.77,
        "marketCap": "675억 달러",
        "fairValue": 345.0,
        "upsidePotential": 24.3,
        "valueScore": 96,
        "tag": "PER",
        "tagName": "📉 저PER 15.8배 차량반도체 1위",
        "naverUrl": "https://m.stock.naver.com/worldstock/stock/NXPI.O/total",
        "description": "차량용 레이더, 레이더/MCU 및 인포테인먼트 반도체 1위. PER 15.8배로 반도체 밸류에이션 매력 전영재 픽.",
        "pros": [
            "PER 15.8배 저평가",
            "자율주행 차량용 레이더 1위",
            "ROE 38% 고효율 경영"
        ],
        "risks": [
            "글로벌 자동차 생산량 변동",
            "유럽 경기 영향"
        ],
        "naverPcUrl": "https://finance.naver.com/world/sitemain.naver?symbol=NXPI.O"
    },
    {
        "id": "us_ADBE",
        "market": "US",
        "marketName": "NASDAQ",
        "code": "ADBE",
        "symbol": "ADBE.O",
        "name": "어도비",
        "englishName": "Adobe Inc.",
        "sector": "창작 소프트웨어",
        "price": 217.32,
        "changeRate": -0.48,
        "per": 26.0,
        "pbr": 11.5,
        "roe": 42.0,
        "dividendYield": 0.0,
        "bps": 46.95,
        "eps": 20.76,
        "marketCap": "2,420억 달러",
        "fairValue": 720.0,
        "upsidePotential": 231.3,
        "valueScore": 96,
        "tag": "PER",
        "tagName": "📉 Firefly AI 저평가 획득",
        "naverUrl": "https://m.stock.naver.com/worldstock/stock/ADBE.O/total",
        "description": "포토샵, 일러스트레이터, 프리미어 플랫폼 독점 및 생성형 AI Firefly 통합. 주가 조정 후 PER 26배 저평가 매수 구간.",
        "pros": [
            "글로벌 창작 크리에이터 90%+ 락인",
            "Firefly 상업용 안전 AI 강점",
            "ROE 42% 구독 모델"
        ],
        "risks": [
            "OpenAI Sora 등 영상 생성 AI 위협",
            "경쟁 앱 성장"
        ],
        "naverPcUrl": "https://finance.naver.com/world/sitemain.naver?symbol=ADBE.O"
    },
    {
        "id": "us_WDC",
        "market": "US",
        "marketName": "NASDAQ",
        "code": "WDC",
        "symbol": "WDC.O",
        "name": "웨스턴 디지털",
        "englishName": "Western Digital",
        "sector": "데이터 저장장치",
        "price": 566.76,
        "changeRate": 1.81,
        "per": 12.8,
        "pbr": 1.15,
        "roe": 11.5,
        "dividendYield": 0.0,
        "bps": 59.3,
        "eps": 5.32,
        "marketCap": "225억 달러",
        "fairValue": 765.13,
        "upsidePotential": 35.0,
        "valueScore": 96,
        "tag": "PBR",
        "tagName": "💎 PBR 1.15배 HDD/NAND 분사",
        "naverUrl": "https://m.stock.naver.com/worldstock/stock/WDC.O/total",
        "description": "HDD 및 플래시 메모리(SanDisk) 분사 추진. PBR 1.15배 수준으로 숨겨진 자산 가치 재평가 모멘텀.",
        "pros": [
            "PBR 1.15배 자산저평가",
            "HDD 및 NAND 사업 분사 가치 재평가",
            "AI 데이터센터 저장장치 수요"
        ],
        "risks": [
            "NAND 메모리 가격 변동성",
            "부채 비율"
        ],
        "naverPcUrl": "https://finance.naver.com/world/sitemain.naver?symbol=WDC.O"
    },
    {
        "id": "us_STX",
        "market": "US",
        "marketName": "NASDAQ",
        "code": "STX",
        "symbol": "STX.O",
        "name": "씨게이트 테크놀로지",
        "englishName": "Seagate Technology",
        "sector": "대용량 HDD",
        "price": 925.34,
        "changeRate": 1.9,
        "per": 15.2,
        "pbr": 12.0,
        "roe": 65.0,
        "dividendYield": 2.7,
        "bps": 8.7,
        "eps": 6.87,
        "marketCap": "218억 달러",
        "fairValue": 1249.21,
        "upsidePotential": 35.0,
        "valueScore": 96,
        "tag": "ROE",
        "tagName": "💎 ROE 65% AI 데이터센터 HDD",
        "naverUrl": "https://m.stock.naver.com/worldstock/stock/STX.O/total",
        "description": "HAMR(열보조 자기기록) 초고용량 30TB+ 데이터센터 HDD 독점 출하. ROE 65% 및 2.7% 배당 전영재 픽.",
        "pros": [
            "HAMR 30TB+ 대용량 HDD 기술 독점",
            "ROE 65% 고수익성",
            "배당수익률 2.7%"
        ],
        "risks": [
            "SSD 대체 가능성 일부 영역",
            "데이터센터 CAPEX 주기"
        ],
        "naverPcUrl": "https://finance.naver.com/world/sitemain.naver?symbol=STX.O"
    },
    {
        "id": "us_BKNG",
        "market": "US",
        "marketName": "NASDAQ",
        "code": "BKNG",
        "symbol": "BKNG.O",
        "name": "부킹 홀딩스",
        "englishName": "Booking Holdings",
        "sector": "여행 테크",
        "price": 175.16,
        "changeRate": -1.52,
        "per": 22.5,
        "pbr": 28.0,
        "roe": 68.0,
        "dividendYield": 0.9,
        "bps": 137.5,
        "eps": 171.11,
        "marketCap": "1,320억 달러",
        "fairValue": 4900.0,
        "upsidePotential": 2697.4,
        "valueScore": 96,
        "tag": "ROE",
        "tagName": "💎 ROE 68% FCF 거대 여행독점",
        "naverUrl": "https://m.stock.naver.com/worldstock/stock/BKNG.O/total",
        "description": "Booking.com, Agoda, Priceline 글로벌 1위 온라인 여행사. ROE 68% 및 연간 70억 달러 FCF 창출.",
        "pros": [
            "글로벌 여행 플랫폼 1위",
            "ROE 68% 독보적 효율",
            "대규모 자사주 매입 및 분기배당 신설"
        ],
        "risks": [
            "경기 침체 시 여행 지출 축소",
            "구글 여행 검색 경쟁"
        ],
        "naverPcUrl": "https://finance.naver.com/world/sitemain.naver?symbol=BKNG.O"
    },
    {
        "id": "us_KHC",
        "market": "US",
        "marketName": "NASDAQ",
        "code": "KHC",
        "symbol": "KHC.O",
        "name": "크래프트 하인즈",
        "englishName": "Kraft Heinz",
        "sector": "식품/소비재",
        "price": 25.78,
        "changeRate": -0.69,
        "per": 11.2,
        "pbr": 0.78,
        "roe": 7.8,
        "dividendYield": 4.8,
        "bps": 42.05,
        "eps": 2.92,
        "marketCap": "398억 달러",
        "fairValue": 48.0,
        "upsidePotential": 86.2,
        "valueScore": 96,
        "tag": "PBR",
        "tagName": "💎 PBR 0.78배 고배당 4.8%",
        "naverUrl": "https://m.stock.naver.com/worldstock/stock/KHC.O/total",
        "description": "하인즈 케첩 및 크래프트 치즈 보유. PBR 0.78배 및 배당 4.8%로 버크셔 해서웨이 주요 보유 고배당주.",
        "pros": [
            "PBR 0.78배 장부가치 미달 저평가",
            "배당수익률 4.8% 고배당",
            "워런 버핏 대주주"
        ],
        "risks": [
            "식품 원자재 가격",
            "저가 PB 상품과 경쟁"
        ],
        "naverPcUrl": "https://finance.naver.com/world/sitemain.naver?symbol=KHC.O"
    },
    {
        "id": "us_PCAR",
        "market": "US",
        "marketName": "NASDAQ",
        "code": "PCAR",
        "symbol": "PCAR.O",
        "name": "파카",
        "englishName": "PACCAR Inc",
        "sector": "대형 트럭",
        "price": 133.1,
        "changeRate": 1.52,
        "per": 11.5,
        "pbr": 2.8,
        "roe": 26.0,
        "dividendYield": 3.8,
        "bps": 36.6,
        "eps": 8.91,
        "marketCap": "536억 달러",
        "fairValue": 142.0,
        "upsidePotential": 6.7,
        "valueScore": 96,
        "tag": "PER",
        "tagName": "📉 저PER 11.5배 고배당 3.8%",
        "naverUrl": "https://m.stock.naver.com/worldstock/stock/PCAR.O/total",
        "description": "켄워스(Kenworth), 피터빌트(Peterbilt), DAF 대형 트럭 제조업체. PER 11.5배 및 특별배당 포함 3.8% 배당.",
        "pros": [
            "대형 트럭 시장 점유율 30%+",
            "PER 11.5배 및 배당 3.8%",
            "부품 서비스 부문 고마진"
        ],
        "risks": [
            "물류 교체 수요 주기",
            "원자재 비용"
        ],
        "naverPcUrl": "https://finance.naver.com/world/sitemain.naver?symbol=PCAR.O"
    },
    {
        "id": "kr_055550",
        "market": "KR",
        "marketName": "KOSPI",
        "code": "055550",
        "symbol": "055550",
        "name": "신한지주",
        "englishName": "Shinhan Financial",
        "sector": "금융/은행",
        "price": 103800,
        "changeRate": -0.67,
        "per": 5.4,
        "pbr": 0.45,
        "roe": 10.2,
        "dividendYield": 5.9,
        "bps": 113700,
        "eps": 9480,
        "marketCap": "26조 1,000억원",
        "fairValue": 141100,
        "upsidePotential": 35.9,
        "valueScore": 95,
        "tag": "PBR",
        "tagName": "💎 PBR 0.45배",
        "naverUrl": "https://m.stock.naver.com/domestic/stock/055550/total",
        "description": "PBR 0.45배 자산가치 극저평가 금융주. 균등 분기 배당 및 자사주 소각을 적극 추진하는 밸류업 우수 기업.",
        "pros": [
            "PBR 0.45배 자산가치 저평가",
            "배당수익률 5.9%",
            "지속적인 자사주 매입 소각"
        ],
        "risks": [
            "대손충당금 적립 부담",
            "금융 당국 규제 변수"
        ],
        "naverPcUrl": "https://finance.naver.com/item/main.naver?code=055550"
    },
    {
        "id": "kr_012330",
        "market": "KR",
        "marketName": "KOSPI",
        "code": "012330",
        "symbol": "012330",
        "name": "현대모비스",
        "englishName": "Hyundai Mobis",
        "sector": "자동차부품",
        "price": 524000,
        "changeRate": 2.14,
        "per": 6.5,
        "pbr": 0.49,
        "roe": 8.4,
        "dividendYield": 3.2,
        "bps": 485700,
        "eps": 36610,
        "marketCap": "22조 1,000억원",
        "fairValue": 692600,
        "upsidePotential": 32.2,
        "valueScore": 95,
        "tag": "PBR",
        "tagName": "💎 PBR 0.49배 밸류업",
        "naverUrl": "https://m.stock.naver.com/domestic/stock/012330/total",
        "description": "현대차그룹 핵심 부품사. PBR 0.49배로 주당 순자산(48만5천원) 대비 반토막 주가. 전장 부문 흑자전환 및 밸류업 수혜 기대.",
        "pros": [
            "PBR 0.49배 청산가치 반토막",
            "현금성 자산 풍부",
            "전장 부문 매출 고성장"
        ],
        "risks": [
            "완성차 파업 및 생산 차질",
            "지배구조 개편 변수"
        ],
        "naverPcUrl": "https://finance.naver.com/item/main.naver?code=012330"
    },
    {
        "id": "kr_000810",
        "market": "KR",
        "marketName": "KOSPI",
        "code": "000810",
        "symbol": "000810",
        "name": "삼성화재",
        "englishName": "Samsung Fire & Marine",
        "sector": "손해보험",
        "price": 638000,
        "changeRate": 1.27,
        "per": 7.5,
        "pbr": 0.82,
        "roe": 12.4,
        "dividendYield": 5.5,
        "bps": 448000,
        "eps": 49060,
        "marketCap": "17조 4,000억원",
        "fairValue": 850500,
        "upsidePotential": 33.3,
        "valueScore": 95,
        "tag": "DIV",
        "tagName": "💰 고배당 5.5% ROE12%",
        "naverUrl": "https://m.stock.naver.com/domestic/stock/000810/total",
        "description": "손해보험 업계 1위. 압도적인 지급여력(K-ICS) 비율과 ROE 12.4%의 고수익성. 주주환원율 50% 목표 발표.",
        "pros": [
            "ROE 12.4% 높은 수익성",
            "배당수익률 5.5%",
            "주주환원 확대 공시"
        ],
        "risks": [
            "계절적 손해율 상승",
            "실손보험 손익 변동"
        ],
        "naverPcUrl": "https://finance.naver.com/item/main.naver?code=000810"
    },
    {
        "id": "kr_005935",
        "market": "KR",
        "marketName": "KOSPI",
        "code": "005935",
        "symbol": "005935",
        "name": "삼성전자우",
        "englishName": "Samsung Elec Pref",
        "sector": "반도체/우선주",
        "price": 191100,
        "changeRate": 3.24,
        "per": 10.2,
        "pbr": 0.95,
        "roe": 11.8,
        "dividendYield": 3.4,
        "bps": 66780,
        "eps": 6140,
        "marketCap": "52조 2,000억원",
        "fairValue": 249900,
        "upsidePotential": 30.8,
        "valueScore": 95,
        "tag": "DIV",
        "tagName": "💰 고배당 우선주 (3.4%)",
        "naverUrl": "https://m.stock.naver.com/domestic/stock/005935/total",
        "description": "삼성전자 의결권 없는 우선주. 보통주 대비 15%+ 할인 거래되어 배당수익률이 높고 안정적인 밸류에이션 제공.",
        "pros": [
            "보통주 대비 할인 거래로 배당수익률 3.4%",
            "삼성전자 업황 수혜 동일",
            "PBR 0.95배 저평가"
        ],
        "risks": [
            "의결권 미보유",
            "거래량 상대적 적음"
        ],
        "naverPcUrl": "https://finance.naver.com/item/main.naver?code=005935"
    },
    {
        "id": "us_V",
        "market": "US",
        "marketName": "NYSE",
        "code": "V",
        "symbol": "V.N",
        "name": "비자",
        "englishName": "Visa Inc.",
        "sector": "결제/금융",
        "price": 351.05,
        "changeRate": -0.67,
        "per": 28.5,
        "pbr": 12.8,
        "roe": 48.0,
        "dividendYield": 0.8,
        "bps": 21.28,
        "eps": 9.56,
        "marketCap": "5,580억 달러",
        "fairValue": 480.36,
        "upsidePotential": 36.8,
        "valueScore": 95,
        "tag": "ROE",
        "tagName": "💎 ROE 48% 독점 독점망",
        "naverUrl": "https://m.stock.naver.com/worldstock/stock/V.N/total",
        "description": "글로벌 1위 디지털 결제 네트워크. 독점적 결제 수수료망 기반 ROE 48%의 무위험 독과점 비즈니스 모델.",
        "pros": [
            "글로벌 결제망 1위 독점력",
            "ROE 48% 영업이익률 67%",
            "인플레이션 헤지 수혜"
        ],
        "risks": [
            "핀테크 대체 결제 수단",
            "반독점 규제 수수료 감면 압박"
        ],
        "naverPcUrl": "https://finance.naver.com/world/sitemain.naver?symbol=V.N"
    },
    {
        "id": "us_KO",
        "market": "US",
        "marketName": "NYSE",
        "code": "KO",
        "symbol": "KO.N",
        "name": "코카콜라",
        "englishName": "Coca-Cola",
        "sector": "음료/소비재",
        "price": 81.36,
        "changeRate": -1.02,
        "per": 23.8,
        "pbr": 10.2,
        "roe": 42.0,
        "dividendYield": 3.0,
        "bps": 6.32,
        "eps": 2.71,
        "marketCap": "2,780억 달러",
        "fairValue": 110.66,
        "upsidePotential": 36.0,
        "valueScore": 95,
        "tag": "DIV",
        "tagName": "💰 워런 버핏 배당주",
        "naverUrl": "https://m.stock.naver.com/worldstock/stock/KO.N/total",
        "description": "워런 버핏의 30년 장기투자 보유주. 61년 연속 배당 인상 및 전세계 200여 개국 브랜드 독점력.",
        "pros": [
            "워런 버핏 최대 핵심 보유주",
            "61년 연속 배당 인상",
            "ROE 42% 독보적 브랜드"
        ],
        "risks": [
            "설탕세 등 건강 규제",
            "환율 변동성"
        ],
        "naverPcUrl": "https://finance.naver.com/world/sitemain.naver?symbol=KO.N"
    },
    {
        "id": "us_AAPL",
        "market": "US",
        "marketName": "NASDAQ",
        "code": "AAPL",
        "symbol": "AAPL.O",
        "name": "애플",
        "englishName": "Apple Inc.",
        "sector": "빅테크/IT",
        "price": 320.12,
        "changeRate": -1.77,
        "per": 31.2,
        "pbr": 45.0,
        "roe": 147.0,
        "dividendYield": 0.5,
        "bps": 4.98,
        "eps": 7.18,
        "marketCap": "3조 4,400억 달러",
        "fairValue": 432.16,
        "upsidePotential": 35.0,
        "valueScore": 95,
        "tag": "ROE",
        "tagName": "💎 ROE 147% 온디바이스 AI",
        "naverUrl": "https://m.stock.naver.com/worldstock/stock/AAPL.O/total",
        "description": "글로벌 시가총액 1위 온디바이스 AI 플랫폼. 매년 1,000억 달러 규모 자사주 매입 소각으로 전영재 추천 주당가치 복리 상승주.",
        "pros": [
            "온디바이스 AI 애플 인텔리전스 교체 수요",
            "연 1000억 달러 대규모 자사주 소각",
            "서비스 매출 비중 25%+ 상승"
        ],
        "risks": [
            "중국 스마트폰 경쟁",
            "반독점 인앱결제 규제"
        ],
        "naverPcUrl": "https://finance.naver.com/world/sitemain.naver?symbol=AAPL.O"
    },
    {
        "id": "us_META",
        "market": "US",
        "marketName": "NASDAQ",
        "code": "META",
        "symbol": "META.O",
        "name": "메타 플랫폼스",
        "englishName": "Meta Platforms",
        "sector": "소셜미디어/AI",
        "price": 611.66,
        "changeRate": -2.47,
        "per": 24.8,
        "pbr": 8.2,
        "roe": 34.0,
        "dividendYield": 0.4,
        "bps": 60.75,
        "eps": 20.08,
        "marketCap": "1조 2,600억 달러",
        "fairValue": 825.74,
        "upsidePotential": 35.0,
        "valueScore": 95,
        "tag": "ROE",
        "tagName": "🚀 Llama 오픈소스 AI 리더",
        "naverUrl": "https://m.stock.naver.com/worldstock/stock/META.O/total",
        "description": "32억 MAU 소셜 네트워크와 Llama 오픈소스 AI 기술 주도. 릴스 광고 타깃팅 고도화로 전영재 추천 가치성장주.",
        "pros": [
            "32억 명 글로벌 이용자 네트워크",
            "Llama 3 AI 모델 리더십",
            "분기 배당 신설 및 자사주 소각"
        ],
        "risks": [
            "메타버스 부문 적자 지속",
            "광고 시장 변동성"
        ],
        "naverPcUrl": "https://finance.naver.com/world/sitemain.naver?symbol=META.O"
    },
    {
        "id": "us_ASML",
        "market": "US",
        "marketName": "NASDAQ",
        "code": "ASML",
        "symbol": "ASML.O",
        "name": "ASML 홀딩",
        "englishName": "ASML Holding",
        "sector": "반도체 노광장비",
        "price": 1798.05,
        "changeRate": -0.21,
        "per": 38.5,
        "pbr": 18.2,
        "roe": 48.0,
        "dividendYield": 0.8,
        "bps": 48.35,
        "eps": 22.85,
        "marketCap": "3,480억 달러",
        "fairValue": 2427.37,
        "upsidePotential": 35.0,
        "valueScore": 95,
        "tag": "ROE",
        "tagName": "🚀 High-NA EUV 세계 독점",
        "naverUrl": "https://m.stock.naver.com/worldstock/stock/ASML.O/total",
        "description": "초미세 2nm 반도체 공정에 필수인 High-NA EUV 노광장비 유일 공급사. 독점적 기술 장벽 보유.",
        "pros": [
            "EUV 노광장비 100% 시장 독점",
            "High-NA 차세대 장비 출하",
            "ROE 48% 마진"
        ],
        "risks": [
            "네덜란드 정부 대중 수출 규제",
            "고가격 장비 도입 시기"
        ],
        "naverPcUrl": "https://finance.naver.com/world/sitemain.naver?symbol=ASML.O"
    },
    {
        "id": "us_AMGN",
        "market": "US",
        "marketName": "NASDAQ",
        "code": "AMGN",
        "symbol": "AMGN.O",
        "name": "암젠",
        "englishName": "Amgen Inc.",
        "sector": "바이오/제약",
        "price": 362.83,
        "changeRate": -0.88,
        "per": 14.2,
        "pbr": 12.5,
        "roe": 44.0,
        "dividendYield": 3.1,
        "bps": 24.96,
        "eps": 21.97,
        "marketCap": "1,670억 달러",
        "fairValue": 410.0,
        "upsidePotential": 13.0,
        "valueScore": 95,
        "tag": "DIV",
        "tagName": "💰 배당 3.1% 항암제 파이프라인",
        "naverUrl": "https://m.stock.naver.com/worldstock/stock/AMGN.O/total",
        "description": "글로벌 1위 바이오테크 제약사. 비만치료제(MariTide) 2상 결과 기대 및 호리즌 인수 효과로 강력한 현금창출력.",
        "pros": [
            "MariTide 주1회/월1회 비만치료제 게임체인저",
            "배당 3.1% 꾸준한 인상",
            "ROE 44% 수익성"
        ],
        "risks": [
            "임상 데이터 발표 변수",
            "부채 상환 일정"
        ],
        "naverPcUrl": "https://finance.naver.com/world/sitemain.naver?symbol=AMGN.O"
    },
    {
        "id": "us_KLAC",
        "market": "US",
        "marketName": "NASDAQ",
        "code": "KLAC",
        "symbol": "KLAC.O",
        "name": "KLA 코퍼레이션",
        "englishName": "KLA Corporation",
        "sector": "반도체 검사장비",
        "price": 215.76,
        "changeRate": 0.5,
        "per": 24.8,
        "pbr": 18.5,
        "roe": 72.0,
        "dividendYield": 0.8,
        "bps": 42.16,
        "eps": 31.45,
        "marketCap": "1,050억 달러",
        "fairValue": 990.0,
        "upsidePotential": 358.8,
        "valueScore": 95,
        "tag": "ROE",
        "tagName": "💎 ROE 72% 수율 검사 독점",
        "naverUrl": "https://m.stock.naver.com/worldstock/stock/KLAC.O/total",
        "description": "반도체 웨이퍼 결함 검사 및 수율 측정 장비 점유율 50%+ 1위 독점 기업. ROE 72%의 독보적 마진.",
        "pros": [
            "반도체 계측/검사 장비 독점력",
            "ROE 72% 압도적 기술력",
            "EUV/High-NA 도입 수혜"
        ],
        "risks": [
            "고객사 사이클 변동성",
            "미중 갈등 소송"
        ],
        "naverPcUrl": "https://finance.naver.com/world/sitemain.naver?symbol=KLAC.O"
    },
    {
        "id": "us_FTNT",
        "market": "US",
        "marketName": "NASDAQ",
        "code": "FTNT",
        "symbol": "FTNT.O",
        "name": "포티넷",
        "englishName": "Fortinet",
        "sector": "네트워크 보안",
        "price": 153.79,
        "changeRate": -0.81,
        "per": 28.5,
        "pbr": 18.0,
        "roe": 45.0,
        "dividendYield": 0.0,
        "bps": 3.8,
        "eps": 2.4,
        "marketCap": "520억 달러",
        "fairValue": 207.62,
        "upsidePotential": 35.0,
        "valueScore": 95,
        "tag": "ROE",
        "tagName": "💎 ROE 45% FCF 보안강자",
        "naverUrl": "https://m.stock.naver.com/worldstock/stock/FTNT.O/total",
        "description": "자체 보안 ASIC 칩 탑재로 가성비 최상위 네트워크 보안 장비 제조. ROE 45% 및 잉여현금흐름 우수.",
        "pros": [
            "자체 ASIC 탑재 가성비 경쟁력",
            "ROE 45% 마진",
            "지속적 자사주 소각"
        ],
        "risks": [
            "방화벽 교체 주기 둔화",
            "클라우드 전용 보안과 경쟁"
        ],
        "naverPcUrl": "https://finance.naver.com/world/sitemain.naver?symbol=FTNT.O"
    },
    {
        "id": "us_SBUX",
        "market": "US",
        "marketName": "NASDAQ",
        "code": "SBUX",
        "symbol": "SBUX.O",
        "name": "스타벅스",
        "englishName": "Starbucks Corporation",
        "sector": "글로벌 리테일",
        "price": 102.58,
        "changeRate": -1.34,
        "per": 20.2,
        "pbr": 14.0,
        "roe": 55.0,
        "dividendYield": 3.0,
        "bps": 5.45,
        "eps": 3.78,
        "marketCap": "865억 달러",
        "fairValue": 105.0,
        "upsidePotential": 2.4,
        "valueScore": 95,
        "tag": "DIV",
        "tagName": "💰 배당 3.0% 브랜드 턴어라운드",
        "naverUrl": "https://m.stock.naver.com/worldstock/stock/SBUX.O/total",
        "description": "글로벌 1위 커피 프랜차이즈. 신임 CEO 넥스트 턴어라운드 및 배당수익률 3.0%로 전영재 추천 가치주.",
        "pros": [
            "글로벌 브랜드 파워 1위",
            "배당수익률 3.0%",
            "사이렌 오더 모바일 결제 비중 30%+"
        ],
        "risks": [
            "중국 저가 커피 프랜차이즈 경쟁",
            "인건비 상승"
        ],
        "naverPcUrl": "https://finance.naver.com/world/sitemain.naver?symbol=SBUX.O"
    },
    {
        "id": "us_ROST",
        "market": "US",
        "marketName": "NASDAQ",
        "code": "ROST",
        "symbol": "ROST.O",
        "name": "로스 스토어스",
        "englishName": "Ross Stores",
        "sector": "오프프라이스 유통",
        "price": 235.56,
        "changeRate": -1.11,
        "per": 16.5,
        "pbr": 8.8,
        "roe": 51.0,
        "dividendYield": 1.0,
        "bps": 16.47,
        "eps": 8.78,
        "marketCap": "480억 달러",
        "fairValue": 318.01,
        "upsidePotential": 35.0,
        "valueScore": 95,
        "tag": "PER",
        "tagName": "📉 저PER 16.5배 가성비 유통",
        "naverUrl": "https://m.stock.naver.com/worldstock/stock/ROST.O/total",
        "description": "미국 2위 오프프라이스 브랜드 할인 유통망. 인플레이션 시기 알뜰 소비층 유입 수혜주.",
        "pros": [
            "PER 16.5배 저평가",
            "ROE 51% 고효율 매장 관리",
            "가성비 쇼핑 트렌드"
        ],
        "risks": [
            "물류 및 인건비 인상",
            "재고 수급 능력"
        ],
        "naverPcUrl": "https://finance.naver.com/world/sitemain.naver?symbol=ROST.O"
    },
    {
        "id": "kr_015760",
        "market": "KR",
        "marketName": "KOSPI",
        "code": "015760",
        "symbol": "015760",
        "name": "한국전력",
        "englishName": "KEPCO",
        "sector": "전력/유틸리티",
        "price": 35600,
        "changeRate": 5.01,
        "per": 6.2,
        "pbr": 0.28,
        "roe": 7.5,
        "dividendYield": 0.0,
        "bps": 77800,
        "eps": 3516,
        "marketCap": "13조 9,000억원",
        "fairValue": 38000,
        "upsidePotential": 6.7,
        "valueScore": 94,
        "tag": "PBR",
        "tagName": "💎 PBR 0.28배 최저점",
        "naverUrl": "https://m.stock.naver.com/domestic/stock/015760/total",
        "description": "PBR 0.28배로 한국 증시 최저 수준의 극단적 저평가주. 전기요금 정상화 및 원자재 가격 안정화로 흑자 전환 궤도 진입.",
        "pros": [
            "PBR 0.28배 청산가치 극저평가",
            "전기요금 인상 및 흑자전환",
            "원자재 연료비 안정세"
        ],
        "risks": [
            "정부 가격 통제 리스크",
            "누적 적자에 따른 부채 부담"
        ],
        "naverPcUrl": "https://finance.naver.com/item/main.naver?code=015760"
    },
    {
        "id": "kr_032830",
        "market": "KR",
        "marketName": "KOSPI",
        "code": "032830",
        "symbol": "032830",
        "name": "삼성생명",
        "englishName": "Samsung Life",
        "sector": "보험/금융",
        "price": 329500,
        "changeRate": 2.97,
        "per": 6.8,
        "pbr": 0.52,
        "roe": 8.9,
        "dividendYield": 5.4,
        "bps": 187500,
        "eps": 14330,
        "marketCap": "19조 5,000억원",
        "fairValue": 432000,
        "upsidePotential": 31.1,
        "valueScore": 94,
        "tag": "PBR",
        "tagName": "💎 자산가치 저평가",
        "naverUrl": "https://m.stock.naver.com/domestic/stock/032830/total",
        "description": "국내 1위 생명보험사. 삼성전자 지분 8.51% 보유로 막대한 지분가치(약 38조원) 대비 자산 PBR 0.52배에 거래 중.",
        "pros": [
            "삼성전자 막대한 지분가치 보유",
            "배당수익률 5.4%",
            "IFRS17 고수익 CSM 확보"
        ],
        "risks": [
            "금리 하락 시 투자수익률 영향",
            "보험금 지급액 부담"
        ],
        "naverPcUrl": "https://finance.naver.com/item/main.naver?code=032830"
    },
    {
        "id": "kr_030200",
        "market": "KR",
        "marketName": "KOSPI",
        "code": "030200",
        "symbol": "030200",
        "name": "KT",
        "englishName": "KT Corp",
        "sector": "통신",
        "price": 52700,
        "changeRate": 0.76,
        "per": 7.8,
        "pbr": 0.58,
        "roe": 8.2,
        "dividendYield": 5.9,
        "bps": 65800,
        "eps": 4890,
        "marketCap": "9조 9,000억원",
        "fairValue": 55000,
        "upsidePotential": 4.4,
        "valueScore": 94,
        "tag": "PBR",
        "tagName": "💎 PBR 0.58배 고배당",
        "naverUrl": "https://m.stock.naver.com/domestic/stock/030200/total",
        "description": "PBR 0.58배로 경쟁사 대비 자산저평가. 자사주 소각 및 배당 성향 50% 이상 유지로 고배당 매력 지속.",
        "pros": [
            "PBR 0.58배 자산가치 저평가",
            "배당수익률 5.9%",
            "부동산 자산가치 풍부"
        ],
        "risks": [
            "경영진 교체에 따른 정책 변동",
            "통신 규제 리스크"
        ],
        "naverPcUrl": "https://finance.naver.com/item/main.naver?code=030200"
    },
    {
        "id": "kr_259960",
        "market": "KR",
        "marketName": "KOSPI",
        "code": "259960",
        "symbol": "259960",
        "name": "크래프톤",
        "englishName": "KRAFTON",
        "sector": "게임/콘텐츠",
        "price": 237500,
        "changeRate": 2.81,
        "per": 14.5,
        "pbr": 1.85,
        "roe": 14.8,
        "dividendYield": 0.0,
        "bps": 154050,
        "eps": 19650,
        "marketCap": "13조 8,000억원",
        "fairValue": 390000,
        "upsidePotential": 64.2,
        "valueScore": 94,
        "tag": "ROE",
        "tagName": "🚀 배틀그라운드 독점",
        "naverUrl": "https://m.stock.naver.com/domestic/stock/259960/total",
        "description": "배틀그라운드(PUBG) 글로벌 IP의 압도적 현금창출력. ROE 14.8%, PER 14배 수준의 현금흐름 부자 기업.",
        "pros": [
            "PUBG 글로벌 매출 역대 최대",
            "ROE 14.8% 높은 이익률",
            "3조원 이상 순현금 보유"
        ],
        "risks": [
            "단일 IP 의존도 리스크",
            "신작 출시 지연"
        ],
        "naverPcUrl": "https://finance.naver.com/item/main.naver?code=259960"
    },
    {
        "id": "kr_066570",
        "market": "KR",
        "marketName": "KOSPI",
        "code": "066570",
        "symbol": "066570",
        "name": "LG전자",
        "englishName": "LG Electronics",
        "sector": "가전/전장",
        "price": 187500,
        "changeRate": 2.63,
        "per": 8.5,
        "pbr": 0.78,
        "roe": 9.5,
        "dividendYield": 1.5,
        "bps": 131400,
        "eps": 12050,
        "marketCap": "16조 7,000억원",
        "fairValue": 246600,
        "upsidePotential": 31.5,
        "valueScore": 94,
        "tag": "PBR",
        "tagName": "💎 PBR 0.78배 전장 재평가",
        "naverUrl": "https://m.stock.naver.com/domestic/stock/066570/total",
        "description": "글로벌 가전 1위 및 VS(전장) 사업부 조단위 매출 성장. PBR 0.78배로 가전+전장 재평가 기대.",
        "pros": [
            "전장(VS) 수주잔고 100조원 돌파",
            "PBR 0.78배 자산저평가",
            "B2B 냉난방 공조(HVAC) 고성장"
        ],
        "risks": [
            "글로벌 물류비 상승 부담",
            "TV 수요 회복 지연"
        ],
        "naverPcUrl": "https://finance.naver.com/item/main.naver?code=066570"
    },
    {
        "id": "us_JPM",
        "market": "US",
        "marketName": "NYSE",
        "code": "JPM",
        "symbol": "JPM.N",
        "name": "JP모건 체이스",
        "englishName": "JPMorgan Chase",
        "sector": "금융/은행",
        "price": 346.79,
        "changeRate": -0.41,
        "per": 11.8,
        "pbr": 1.72,
        "roe": 17.5,
        "dividendYield": 2.4,
        "bps": 121.16,
        "eps": 17.66,
        "marketCap": "5,950억 달러",
        "fairValue": 466.06,
        "upsidePotential": 34.4,
        "valueScore": 94,
        "tag": "PER",
        "tagName": "📉 저PER 11배",
        "naverUrl": "https://m.stock.naver.com/worldstock/stock/JPM.N/total",
        "description": "미국 1위 종합 금융 그룹. ROE 17.5%의 높은 수익성과 독보적 리스크 관리 능력. 금리 변동기에도 안정적 순이자이익과 IB 수수료 확보.",
        "pros": [
            "ROE 17.5% 글로벌 은행 1위급",
            "PER 11.8배 저평가 구간",
            "꾸준한 배당 증액 역사"
        ],
        "risks": [
            "미국 경기 둔화 시 대손 비용",
            "상업용 부동산 리스크"
        ],
        "naverPcUrl": "https://finance.naver.com/world/sitemain.naver?symbol=JPM.N"
    },
    {
        "id": "us_PEP",
        "market": "US",
        "marketName": "NYSE",
        "code": "PEP",
        "symbol": "PEP.N",
        "name": "펩시코",
        "englishName": "PepsiCo",
        "sector": "음료/식품",
        "price": 134.93,
        "changeRate": -0.53,
        "per": 22.0,
        "pbr": 11.5,
        "roe": 52.0,
        "dividendYield": 3.1,
        "bps": 14.36,
        "eps": 7.5,
        "marketCap": "2,260억 달러",
        "fairValue": 205.0,
        "upsidePotential": 51.9,
        "valueScore": 94,
        "tag": "DIV",
        "tagName": "💰 51년 배당귀족",
        "naverUrl": "https://m.stock.naver.com/worldstock/stock/PEP.N/total",
        "description": "펩시 콜라 + 레이즈/도리토스 스낵 부문 통합 1위. 51년 연속 배당 인상 및 ROE 52% 고수익성.",
        "pros": [
            "스낵(프리토레이) 부문 압도적 1위",
            "51년 연속 배당 인상",
            "안정적 매출 성장"
        ],
        "risks": [
            "비만 치료제(GLP-1) 보급에 따른 스낵 소비 감소 우려"
        ],
        "naverPcUrl": "https://finance.naver.com/world/sitemain.naver?symbol=PEP.N"
    },
    {
        "id": "us_NVDA",
        "market": "US",
        "marketName": "NASDAQ",
        "code": "NVDA",
        "symbol": "NVDA.O",
        "name": "엔비디아",
        "englishName": "NVIDIA",
        "sector": "AI반도체",
        "price": 209.29,
        "changeRate": -1.31,
        "per": 45.2,
        "pbr": 38.0,
        "roe": 115.0,
        "dividendYield": 0.1,
        "bps": 3.38,
        "eps": 2.84,
        "marketCap": "3조 1,500억 달러",
        "fairValue": 282.54,
        "upsidePotential": 35.0,
        "valueScore": 94,
        "tag": "ROE",
        "tagName": "🚀 AI GPU 80%+ 점유율",
        "naverUrl": "https://m.stock.naver.com/worldstock/stock/NVDA.O/total",
        "description": "AI 혁명의 핵심 엔진. 블랙웰(Blackwell) 및 H100 독점 공급으로 ROE 115% 달성하는 전영재 주도 AI 1위 주식.",
        "pros": [
            "AI GPU 시장 80%+ 압도적 점유율",
            "CUDA 소프트웨어 생태계 락인",
            "영업이익률 60%+ 압도적 마진"
        ],
        "risks": [
            "빅테크 자이언트 자체 칩 개발",
            "미중 반도체 수출 규제"
        ],
        "naverPcUrl": "https://finance.naver.com/world/sitemain.naver?symbol=NVDA.O"
    },
    {
        "id": "us_CSCO",
        "market": "US",
        "marketName": "NASDAQ",
        "code": "CSCO",
        "symbol": "CSCO.O",
        "name": "시스코 시스템즈",
        "englishName": "Cisco Systems",
        "sector": "네트워크/보안",
        "price": 112.98,
        "changeRate": 0.69,
        "per": 14.8,
        "pbr": 3.8,
        "roe": 26.0,
        "dividendYield": 3.4,
        "bps": 12.57,
        "eps": 3.22,
        "marketCap": "1,920억 달러",
        "fairValue": 152.52,
        "upsidePotential": 35.0,
        "valueScore": 94,
        "tag": "DIV",
        "tagName": "💰 전영재 배당 픽 3.4% 저PER",
        "naverUrl": "https://m.stock.naver.com/worldstock/stock/CSCO.O/total",
        "description": "세계 1위 네트워크 장비 및 보안 스플렁크(Splunk) 인수 완료. 배당수익률 3.4%와 PER 14.8배의 안정적 가치주.",
        "pros": [
            "네트워크 글로벌 1위 점유율",
            "배당수익률 3.4% 고배당",
            "스플렁크 인수로 보안 구독 강화"
        ],
        "risks": [
            "기업 IT 장비 투자 둔화",
            "클라우드 서비스 자체 구축"
        ],
        "naverPcUrl": "https://finance.naver.com/world/sitemain.naver?symbol=CSCO.O"
    },
    {
        "id": "us_BIIB",
        "market": "US",
        "marketName": "NASDAQ",
        "code": "BIIB",
        "symbol": "BIIB.O",
        "name": "바이오젠",
        "englishName": "Biogen Inc.",
        "sector": "바이오/신경계",
        "price": 197.44,
        "changeRate": -0.15,
        "per": 12.2,
        "pbr": 1.35,
        "roe": 11.2,
        "dividendYield": 0.0,
        "bps": 161.48,
        "eps": 17.86,
        "marketCap": "318억 달러",
        "fairValue": 310.0,
        "upsidePotential": 57.0,
        "valueScore": 94,
        "tag": "PBR",
        "tagName": "💎 PBR 1.35배 저평가 바이오",
        "naverUrl": "https://m.stock.naver.com/worldstock/stock/BIIB.O/total",
        "description": "알츠하이머 신약 레켐비(Lequembi) 최초 승인 및 척수성 근위축증 치료제 독점. PBR 1.35배 수준의 주가 바닥권.",
        "pros": [
            "레켐비 알츠하이머 신약 보급 확대",
            "PBR 1.35배 자산저평가",
            "희귀 신경계 파이프라인"
        ],
        "risks": [
            "레켐비 처방 속도 정체",
            "기존 다발성 경화증 약가 하락"
        ],
        "naverPcUrl": "https://finance.naver.com/world/sitemain.naver?symbol=BIIB.O"
    },
    {
        "id": "us_VRTX",
        "market": "US",
        "marketName": "NASDAQ",
        "code": "VRTX",
        "symbol": "VRTX.O",
        "name": "버텍스 파마슈티컬스",
        "englishName": "Vertex Pharmaceuticals",
        "sector": "바이오/희귀질환",
        "price": 469.66,
        "changeRate": -0.62,
        "per": 24.5,
        "pbr": 7.8,
        "roe": 28.4,
        "dividendYield": 0.0,
        "bps": 60.0,
        "eps": 19.1,
        "marketCap": "1,200억 달러",
        "fairValue": 590.0,
        "upsidePotential": 25.6,
        "valueScore": 94,
        "tag": "ROE",
        "tagName": "🚀 낭성섬유증 독점 바이오",
        "naverUrl": "https://m.stock.naver.com/worldstock/stock/VRTX.O/total",
        "description": "낭성섬유증 치료제 세계 독점 공급 및 유전자 편집 치료제(Casgevy) 최초 상용화 성공 바이오 대장주.",
        "pros": [
            "낭성섬유증 시장 90%+ 독점",
            "크리스퍼 유전자치료제 상용화",
            "ROE 28.4% 독보적 마진"
        ],
        "risks": [
            "단일 치료제 매출 의존도",
            "유전자 치료제 고가격"
        ],
        "naverPcUrl": "https://finance.naver.com/world/sitemain.naver?symbol=VRTX.O"
    },
    {
        "id": "us_REGN",
        "market": "US",
        "marketName": "NASDAQ",
        "code": "REGN",
        "symbol": "REGN.O",
        "name": "리제네론",
        "englishName": "Regeneron Pharmaceuticals",
        "sector": "바이오/안과",
        "price": 643.0,
        "changeRate": -1.26,
        "per": 18.2,
        "pbr": 3.8,
        "roe": 22.0,
        "dividendYield": 0.0,
        "bps": 259.21,
        "eps": 54.12,
        "marketCap": "1,070억 달러",
        "fairValue": 1280.0,
        "upsidePotential": 99.1,
        "valueScore": 94,
        "tag": "PER",
        "tagName": "📉 저PER 18배 고성장 바이오",
        "naverUrl": "https://m.stock.naver.com/worldstock/stock/REGN.O/total",
        "description": "안과 질환 치료제 아일리아(Eylea) 및 아토피 치료제 듀피젠트(Dupixent) 글로벌 블록버스터 보유.",
        "pros": [
            "듀피젠트 연 매출 100억 달러 돌파",
            "PER 18.2배 우량한 재무구조",
            "자체 R&D 자체발굴 경쟁력"
        ],
        "risks": [
            "아일리아 바이오시밀러 경쟁",
            "특허 소송 수용 여부"
        ],
        "naverPcUrl": "https://finance.naver.com/world/sitemain.naver?symbol=REGN.O"
    },
    {
        "id": "us_MCHP",
        "market": "US",
        "marketName": "NASDAQ",
        "code": "MCHP",
        "symbol": "MCHP.O",
        "name": "마이크로칩 테크놀로지",
        "englishName": "Microchip Technology",
        "sector": "임베디드 반도체",
        "price": 82.76,
        "changeRate": -2.66,
        "per": 17.2,
        "pbr": 4.8,
        "roe": 25.5,
        "dividendYield": 2.2,
        "bps": 17.6,
        "eps": 4.91,
        "marketCap": "455억 달러",
        "fairValue": 112.0,
        "upsidePotential": 35.3,
        "valueScore": 94,
        "tag": "PER",
        "tagName": "📉 MCU 반도체 저평가 구간",
        "naverUrl": "https://m.stock.naver.com/worldstock/stock/MCHP.O/total",
        "description": "스마트 가전 및 자동차 마이크로컨트롤러(MCU) 리더. 주가 조정으로 PER 17.2배 진입.",
        "pros": [
            "MCU 글로벌 선도 경쟁력",
            "배당수익률 2.2%",
            "자사주 매입 병행"
        ],
        "risks": [
            "재고 소진 기간 장기화",
            "중국 경쟁사 진입"
        ],
        "naverPcUrl": "https://finance.naver.com/world/sitemain.naver?symbol=MCHP.O"
    },
    {
        "id": "us_COST",
        "market": "US",
        "marketName": "NASDAQ",
        "code": "COST",
        "symbol": "COST.O",
        "name": "코스트코 홀세일",
        "englishName": "Costco Wholesale",
        "sector": "유통/회원제",
        "price": 923.24,
        "changeRate": -0.44,
        "per": 48.0,
        "pbr": 14.5,
        "roe": 29.5,
        "dividendYield": 0.5,
        "bps": 57.93,
        "eps": 17.5,
        "marketCap": "3,730억 달러",
        "fairValue": 980.0,
        "upsidePotential": 6.1,
        "valueScore": 94,
        "tag": "ROE",
        "tagName": "🚀 93% 재연장율 유통 독점",
        "naverUrl": "https://m.stock.naver.com/worldstock/stock/COST.O/total",
        "description": "회원재 유통 1위. 멤버십 재갱신율 93% 및 정기 특별배당 지급으로 독보적 가치 제공.",
        "pros": [
            "멤버십 연간 수익 안정성",
            "높은 고객 충성도 93%",
            "특별 배당 지속 지급"
        ],
        "risks": [
            "높은 PER 밸류에이션",
            "이커머스 경쟁"
        ],
        "naverPcUrl": "https://finance.naver.com/world/sitemain.naver?symbol=COST.O"
    },
    {
        "id": "us_DLTR",
        "market": "US",
        "marketName": "NASDAQ",
        "code": "DLTR",
        "symbol": "DLTR.O",
        "name": "달러 트리",
        "englishName": "Dollar Tree",
        "sector": "할인 유통",
        "price": 118.53,
        "changeRate": -2.96,
        "per": 15.5,
        "pbr": 2.8,
        "roe": 17.5,
        "dividendYield": 0.0,
        "bps": 38.57,
        "eps": 6.96,
        "marketCap": "232억 달러",
        "fairValue": 150.0,
        "upsidePotential": 26.6,
        "valueScore": 94,
        "tag": "PER",
        "tagName": "📉 고물가 수혜 저PER 유통",
        "naverUrl": "https://m.stock.naver.com/worldstock/stock/DLTR.O/total",
        "description": "미국 대표 1달러/다단가 할인 매장(Dollar Tree & Family Dollar). 고물가 구조적 수혜주.",
        "pros": [
            "PER 15.5배 저평가 턴어라운드",
            "다단가($3, $5) 상품 도입 마진 개선",
            "저소득층 필수 장보기점"
        ],
        "risks": [
            "Family Dollar 매장 폐쇄 비용",
            "물류 비용"
        ],
        "naverPcUrl": "https://finance.naver.com/world/sitemain.naver?symbol=DLTR.O"
    },
    {
        "id": "us_PAYX",
        "market": "US",
        "marketName": "NASDAQ",
        "code": "PAYX",
        "symbol": "PAYX.O",
        "name": "페이첵스",
        "englishName": "Paychex Inc.",
        "sector": "HR/급여 소프트웨어",
        "price": 110.52,
        "changeRate": -0.2,
        "per": 26.0,
        "pbr": 11.2,
        "roe": 44.0,
        "dividendYield": 3.2,
        "bps": 11.07,
        "eps": 4.76,
        "marketCap": "446억 달러",
        "fairValue": 160.0,
        "upsidePotential": 44.8,
        "valueScore": 94,
        "tag": "DIV",
        "tagName": "💰 배당 3.2% ROE 44% HR소프트웨어",
        "naverUrl": "https://m.stock.naver.com/worldstock/stock/PAYX.O/total",
        "description": "미국 중소기업용 급여, HR 관리 및 복리후생 소프트웨어 1위. ROE 44% 및 3.2% 안정 배당.",
        "pros": [
            "중소기업 HR 소프트웨어 독점력",
            "ROE 44% 고수익성",
            "배당수익률 3.2%"
        ],
        "risks": [
            "미국 고용 지표 둔화 시 영향",
            "소프트웨어 경쟁"
        ],
        "naverPcUrl": "https://finance.naver.com/world/sitemain.naver?symbol=PAYX.O"
    },
    {
        "id": "kr_003550",
        "market": "KR",
        "marketName": "KOSPI",
        "code": "003550",
        "symbol": "003550",
        "name": "LG",
        "englishName": "LG Corp",
        "sector": "지주사",
        "price": 101600,
        "changeRate": 2.52,
        "per": 7.2,
        "pbr": 0.51,
        "roe": 7.8,
        "dividendYield": 4.2,
        "bps": 149400,
        "eps": 10580,
        "marketCap": "11조 9,000억원",
        "fairValue": 120000,
        "upsidePotential": 18.1,
        "valueScore": 93,
        "tag": "PBR",
        "tagName": "💎 지주사 할인 50%",
        "naverUrl": "https://m.stock.naver.com/domestic/stock/003550/total",
        "description": "LG그룹 순수 지주사. LG화학, LG전자, LG유플러스 등 순자산가치(NAV) 대비 PBR 0.51배에 거래되는 대표 저평가주.",
        "pros": [
            "NAV 대비 50%+ 할인 자산저평가",
            "배당수익률 4.2%",
            "자사주 매입 소각 시행"
        ],
        "risks": [
            "자회사 화학/배터리 업황 부진",
            "지주사 할인 리스크"
        ],
        "naverPcUrl": "https://finance.naver.com/item/main.naver?code=003550"
    },
    {
        "id": "kr_010130",
        "market": "KR",
        "marketName": "KOSPI",
        "code": "010130",
        "symbol": "010130",
        "name": "고려아연",
        "englishName": "Korea Zinc",
        "sector": "비철금속",
        "price": 1043000,
        "changeRate": 4.93,
        "per": 13.4,
        "pbr": 1.12,
        "roe": 8.8,
        "dividendYield": 3.8,
        "bps": 483900,
        "eps": 40440,
        "marketCap": "10조 7,000억원",
        "fairValue": 1341900,
        "upsidePotential": 28.7,
        "valueScore": 93,
        "tag": "DIV",
        "tagName": "💰 배당 3.8% 자원 리더",
        "naverUrl": "https://m.stock.naver.com/domestic/stock/010130/total",
        "description": "세계 1위 아연/아연제련 기업. 올인원 니켈 제련소 및 폐배터리 리사이클링 친환경 사업 확장.",
        "pros": [
            "세계 1위 비철금속 제련 경쟁력",
            "배당수익률 3.8%",
            "경영권 분쟁 가능성에 따른 주주가치 제고"
        ],
        "risks": [
            "원자재 제련수수료(TC) 변동",
            "전력비 부담"
        ],
        "naverPcUrl": "https://finance.naver.com/item/main.naver?code=010130"
    },
    {
        "id": "us_PFE",
        "market": "US",
        "marketName": "NYSE",
        "code": "PFE",
        "symbol": "PFE.N",
        "name": "화이자",
        "englishName": "Pfizer",
        "sector": "제약/바이오",
        "price": 24.95,
        "changeRate": 0.5,
        "per": 10.5,
        "pbr": 1.62,
        "roe": 13.5,
        "dividendYield": 5.9,
        "bps": 17.65,
        "eps": 2.72,
        "marketCap": "1,620억 달러",
        "fairValue": 42.0,
        "upsidePotential": 68.3,
        "valueScore": 93,
        "tag": "DIV",
        "tagName": "💰 미국 고배당 5.9%",
        "naverUrl": "https://m.stock.naver.com/worldstock/stock/PFE.N/total",
        "description": "글로벌 제약 거인. 코로나 백신 특수 종료 후 주가가 바닥권까지 하락했으나 배당수익률 5.9%에 달함. 시젠(Seagen) 인수 효과로 항암제 파이프라인 대폭 강화.",
        "pros": [
            "배당수익률 5.9% 초고배당",
            "PER 10.5배 역사적 저점",
            "항암 신약 파이프라인 시너지"
        ],
        "risks": [
            "특허 만료(특허 절벽)",
            "신약 임상 실패 리스크"
        ],
        "naverPcUrl": "https://finance.naver.com/world/sitemain.naver?symbol=PFE.N"
    },
    {
        "id": "us_PG",
        "market": "US",
        "marketName": "NYSE",
        "code": "PG",
        "symbol": "PG.N",
        "name": "프록터 앤 갬블",
        "englishName": "Procter & Gamble",
        "sector": "필수소비재",
        "price": 146.99,
        "changeRate": -1.44,
        "per": 24.5,
        "pbr": 7.8,
        "roe": 31.5,
        "dividendYield": 2.4,
        "bps": 21.65,
        "eps": 6.89,
        "marketCap": "3,980억 달러",
        "fairValue": 205.0,
        "upsidePotential": 39.5,
        "valueScore": 93,
        "tag": "DIV",
        "tagName": "💰 67년 연속 배당 인상",
        "naverUrl": "https://m.stock.naver.com/worldstock/stock/PG.N/total",
        "description": "질레트, 팸퍼스, 다우니, 헤드앤숄더 등 필수소비재 1위. 67년 연속 배당 인상 기록의 방어주 대표격.",
        "pros": [
            "67년 연속 배당 인상 기록",
            "강력한 가격 결정력(Price Power)",
            "경기 침체기 최고 방어력"
        ],
        "risks": [
            "원자재/물류 비용 변동",
            "저가 자체브랜드(PB)와 경쟁"
        ],
        "naverPcUrl": "https://finance.naver.com/world/sitemain.naver?symbol=PG.N"
    },
    {
        "id": "us_WMT",
        "market": "US",
        "marketName": "NYSE",
        "code": "WMT",
        "symbol": "WMT.N",
        "name": "월마트",
        "englishName": "Walmart Inc.",
        "sector": "유통/소비재",
        "price": 107.69,
        "changeRate": -1.5,
        "per": 26.5,
        "pbr": 5.4,
        "roe": 20.2,
        "dividendYield": 1.2,
        "bps": 12.68,
        "eps": 2.58,
        "marketCap": "5,510억 달러",
        "fairValue": 149.03,
        "upsidePotential": 38.4,
        "valueScore": 93,
        "tag": "ROE",
        "tagName": "🚀 유통 1위 이커머스",
        "naverUrl": "https://m.stock.naver.com/worldstock/stock/WMT.N/total",
        "description": "세계 1위 오프라인 및 온/오프라인 통합 유통 거인. 고물가 시기 가성비 장보기 고소득층 고객 유입 확대.",
        "pros": [
            "미국 오프라인 유통 1위 점유율",
            "월마트+ 멤버십 및 광고 고성장",
            "인플레이션 디딤돌 수혜"
        ],
        "risks": [
            "마진율 상대적 낮음",
            "물류 인건비 상승"
        ],
        "naverPcUrl": "https://finance.naver.com/world/sitemain.naver?symbol=WMT.N"
    },
    {
        "id": "us_AMZN",
        "market": "US",
        "marketName": "NASDAQ",
        "code": "AMZN",
        "symbol": "AMZN.O",
        "name": "아마존",
        "englishName": "Amazon.com",
        "sector": "이커머스/클라우드",
        "price": 236.94,
        "changeRate": -3.23,
        "per": 42.0,
        "pbr": 7.5,
        "roe": 21.5,
        "dividendYield": 0.0,
        "bps": 24.85,
        "eps": 4.43,
        "marketCap": "1조 9,400억 달러",
        "fairValue": 319.87,
        "upsidePotential": 35.0,
        "valueScore": 93,
        "tag": "ROE",
        "tagName": "🚀 AWS 클라우드 1위",
        "naverUrl": "https://m.stock.naver.com/worldstock/stock/AMZN.O/total",
        "description": "세계 1위 이커머스 및 AWS 클라우드 기업. 물류 자동화 비용 효율화 및 고마진 광고 사업 매출 폭발.",
        "pros": [
            "AWS 글로벌 1위 클라우드 점유율",
            "고마진 광고 사업 고성장",
            "풀필먼트 물류 비용 절감"
        ],
        "risks": [
            "이커머스 가격 경쟁",
            "빅테크 규제 리스크"
        ],
        "naverPcUrl": "https://finance.naver.com/world/sitemain.naver?symbol=AMZN.O"
    },
    {
        "id": "us_TXN",
        "market": "US",
        "marketName": "NASDAQ",
        "code": "TXN",
        "symbol": "TXN.O",
        "name": "텍사스 인스트루먼트",
        "englishName": "Texas Instruments",
        "sector": "아날로그 반도체",
        "price": 282.38,
        "changeRate": -4.01,
        "per": 26.0,
        "pbr": 9.2,
        "roe": 31.0,
        "dividendYield": 2.8,
        "bps": 21.52,
        "eps": 7.61,
        "marketCap": "1,800억 달러",
        "fairValue": 381.21,
        "upsidePotential": 35.0,
        "valueScore": 93,
        "tag": "DIV",
        "tagName": "💰 20년 연속 배당 인상 반도체",
        "naverUrl": "https://m.stock.naver.com/worldstock/stock/TXN.O/total",
        "description": "차량용 및 산업용 아날로그 반도체 세계 1위. 20년 연속 배당금 증액 및 현금 흐름 우수 기업.",
        "pros": [
            "아날로그 반도체 세계 1위",
            "20년 연속 배당 인상 배당귀족",
            "80,000개 이상 고객사 분산"
        ],
        "risks": [
            "300mm 팹 설비 투자(CAPEX) 기간 현금 흐름",
            "산업용 재고 조정"
        ],
        "naverPcUrl": "https://finance.naver.com/world/sitemain.naver?symbol=TXN.O"
    },
    {
        "id": "us_INTU",
        "market": "US",
        "marketName": "NASDAQ",
        "code": "INTU",
        "symbol": "INTU.O",
        "name": "인투이트",
        "englishName": "Intuit Inc.",
        "sector": "세무/회계 AI",
        "price": 283.0,
        "changeRate": -0.52,
        "per": 32.0,
        "pbr": 9.8,
        "roe": 31.2,
        "dividendYield": 0.6,
        "bps": 65.81,
        "eps": 20.15,
        "marketCap": "1,800억 달러",
        "fairValue": 810.0,
        "upsidePotential": 186.2,
        "valueScore": 93,
        "tag": "ROE",
        "tagName": "🚀 퀵북스/터보택스 독점망",
        "naverUrl": "https://m.stock.naver.com/worldstock/stock/INTU.O/total",
        "description": "미국 개인/중소기업 세무 및 회계 소프트웨어(TurboTax, QuickBooks, Mailchimp) 독점적 플랫폼.",
        "pros": [
            "터보택스 및 퀵북스 시장 80%+ 점유",
            "Intuit Assist AI 도입으로 주당가치 상승",
            "ROE 31.2%"
        ],
        "risks": [
            "미국 IRS 자체 무료 세무 신고 시스템",
            "중소기업 고용 침체"
        ],
        "naverPcUrl": "https://finance.naver.com/world/sitemain.naver?symbol=INTU.O"
    },
    {
        "id": "us_PANW",
        "market": "US",
        "marketName": "NASDAQ",
        "code": "PANW",
        "symbol": "PANW.O",
        "name": "팔로알토 네트웍스",
        "englishName": "Palo Alto Networks",
        "sector": "사이버 보안",
        "price": 324.76,
        "changeRate": -3.14,
        "per": 42.0,
        "pbr": 15.2,
        "roe": 34.0,
        "dividendYield": 0.0,
        "bps": 21.57,
        "eps": 7.8,
        "marketCap": "1,060억 달러",
        "fairValue": 420.0,
        "upsidePotential": 29.3,
        "valueScore": 93,
        "tag": "ROE",
        "tagName": "🚀 차세대 보안 플랫폼 1위",
        "naverUrl": "https://m.stock.naver.com/worldstock/stock/PANW.O/total",
        "description": "글로벌 1위 사이버 보안 기업. 방화벽, 클라우드 보안, AI 보안 SOC(Cortex) 통합 플랫폼 전략 성공.",
        "pros": [
            "글로벌 보안 시장 점유율 1위",
            "플랫폼화(Platformization) 전략 계약 대형화",
            "FCF 마진 38%"
        ],
        "risks": [
            "초기 무료 플랫폼 제공 시 단기 매출 영향",
            "보안 경쟁 심화"
        ],
        "naverPcUrl": "https://finance.naver.com/world/sitemain.naver?symbol=PANW.O"
    },
    {
        "id": "us_MRVL",
        "market": "US",
        "marketName": "NASDAQ",
        "code": "MRVL",
        "symbol": "MRVL.O",
        "name": "마벨 테크놀로지",
        "englishName": "Marvell Technology",
        "sector": "데이터센터 반도체",
        "price": 212.31,
        "changeRate": 0.63,
        "per": 28.0,
        "pbr": 4.2,
        "roe": 14.8,
        "dividendYield": 0.3,
        "bps": 17.23,
        "eps": 2.58,
        "marketCap": "626억 달러",
        "fairValue": 286.62,
        "upsidePotential": 35.0,
        "valueScore": 93,
        "tag": "PER",
        "tagName": "🚀 AI 맞춤형 칩 네트워크",
        "naverUrl": "https://m.stock.naver.com/worldstock/stock/MRVL.O/total",
        "description": "클라우드 데이터센터 AI 광연결 칩(PAM4 DSP) 및 빅테크 맞춤형 AI ASIC 칩 설계 전문.",
        "pros": [
            "데이터센터 800G 광커넥트 칩 1위",
            "맞춤형 AI ASIC 칩 수주 둔화 수혜",
            "클라우드 비중 70%+"
        ],
        "risks": [
            "비 데이터센터 영역 둔화",
            "경쟁 심화"
        ],
        "naverPcUrl": "https://finance.naver.com/world/sitemain.naver?symbol=MRVL.O"
    },
    {
        "id": "us_MDLZ",
        "market": "US",
        "marketName": "NASDAQ",
        "code": "MDLZ",
        "symbol": "MDLZ.O",
        "name": "몬델리즈 인터내셔널",
        "englishName": "Mondelez International",
        "sector": "제과/소비재",
        "price": 60.25,
        "changeRate": -1.0,
        "per": 20.5,
        "pbr": 3.2,
        "roe": 16.5,
        "dividendYield": 2.5,
        "bps": 21.4,
        "eps": 3.34,
        "marketCap": "915억 달러",
        "fairValue": 86.0,
        "upsidePotential": 42.7,
        "valueScore": 93,
        "tag": "DIV",
        "tagName": "💰 오레오/리츠 필수소비재",
        "naverUrl": "https://m.stock.naver.com/worldstock/stock/MDLZ.O/total",
        "description": "오레오(Oreo), 리츠(Ritz), 밀카(Milka) 초콜릿 등 세계 1위 스낵 제과 기업.",
        "pros": [
            "글로벌 1위 스낵 브랜드 포트폴리오",
            "안정적 가격 인상 능력",
            "배당 2.5% 지속 인상"
        ],
        "risks": [
            "코코아/설탕 원자재가 상승",
            "환율 변동성"
        ],
        "naverPcUrl": "https://finance.naver.com/world/sitemain.naver?symbol=MDLZ.O"
    },
    {
        "id": "us_ODFL",
        "market": "US",
        "marketName": "NASDAQ",
        "code": "ODFL",
        "symbol": "ODFL.O",
        "name": "올드 도미니언 프레이트 라인",
        "englishName": "Old Dominion Freight Line",
        "sector": "물류/운송",
        "price": 230.28,
        "changeRate": -1.08,
        "per": 26.5,
        "pbr": 8.2,
        "roe": 31.0,
        "dividendYield": 0.6,
        "bps": 22.19,
        "eps": 6.86,
        "marketCap": "392억 달러",
        "fairValue": 235.0,
        "upsidePotential": 2.0,
        "valueScore": 93,
        "tag": "ROE",
        "tagName": "🚀 운송업계 효율성 1위",
        "naverUrl": "https://m.stock.naver.com/worldstock/stock/ODFL.O/total",
        "description": "미국 1위 LTL(적재량 미달) 화물 운송사. 영업비율(OR) 70% 수준의 세계 최고 운송 효율성.",
        "pros": [
            "미국 LTL 물류 수송 1위",
            "ROE 31% 업계 최고 마진",
            "경쟁사 옐로우 파산 수혜"
        ],
        "risks": [
            "미국 물동량 및 경기 변동",
            "유가 변동"
        ],
        "naverPcUrl": "https://finance.naver.com/world/sitemain.naver?symbol=ODFL.O"
    },
    {
        "id": "kr_005930",
        "market": "KR",
        "marketName": "KOSPI",
        "code": "005930",
        "symbol": "005930",
        "name": "삼성전자",
        "englishName": "Samsung Electronics",
        "sector": "반도체/IT",
        "price": 270000,
        "changeRate": 3.65,
        "per": 12.5,
        "pbr": 1.15,
        "roe": 11.8,
        "dividendYield": 2.8,
        "bps": 66780,
        "eps": 6140,
        "marketCap": "458조 5,000억원",
        "fairValue": 351700,
        "upsidePotential": 30.3,
        "valueScore": 92,
        "tag": "ROE",
        "tagName": "🚀 반도체 턴어라운드",
        "naverUrl": "https://m.stock.naver.com/domestic/stock/005930/total",
        "description": "전영재 장기투자 필수 포트폴리오. HBM 공급 확대와 메모리 업황 턴어라운드로 장기 이익 성장세 진입 구간.",
        "pros": [
            "메모리 업황 턴어라운드",
            "HBM3E 공급 본격화",
            "압도적 현금성 자산 보유"
        ],
        "risks": [
            "파운드리 경쟁 심화",
            "빅테크 침체 가능성"
        ],
        "naverPcUrl": "https://finance.naver.com/item/main.naver?code=005930"
    },
    {
        "id": "kr_006400",
        "market": "KR",
        "marketName": "KOSPI",
        "code": "006400",
        "symbol": "006400",
        "name": "삼성SDI",
        "englishName": "Samsung SDI",
        "sector": "이차전지",
        "price": 467000,
        "changeRate": 11.46,
        "per": 16.5,
        "pbr": 1.05,
        "roe": 7.1,
        "dividendYield": 0.8,
        "bps": 354200,
        "eps": 22540,
        "marketCap": "25조 6,000억원",
        "fairValue": 560000,
        "upsidePotential": 19.9,
        "valueScore": 92,
        "tag": "PBR",
        "tagName": "💎 PBR 1.05배 프리미엄",
        "naverUrl": "https://m.stock.naver.com/domestic/stock/006400/total",
        "description": "전고체 배터리 리더 및 수익성 중심 이차전지 제조사. 프리미엄 P-배터리 비중으로 견조한 마진 유지.",
        "pros": [
            "전고체 배터리 기술력 1위",
            "수익성 중심 보수적 경영",
            "GM/스텔란티스 합작법인 본격화"
        ],
        "risks": [
            "유럽 전기차 보조금 축소",
            "북미 CAPEX 부담"
        ],
        "naverPcUrl": "https://finance.naver.com/item/main.naver?code=006400"
    },
    {
        "id": "us_JNJ",
        "market": "US",
        "marketName": "NYSE",
        "code": "JNJ",
        "symbol": "JNJ.N",
        "name": "존슨앤드존슨",
        "englishName": "Johnson & Johnson",
        "sector": "헬스케어/제약",
        "price": 256.11,
        "changeRate": 0.19,
        "per": 14.2,
        "pbr": 5.1,
        "roe": 32.0,
        "dividendYield": 3.1,
        "bps": 30.62,
        "eps": 11.0,
        "marketCap": "3,750억 달러",
        "fairValue": 338.32,
        "upsidePotential": 32.1,
        "valueScore": 92,
        "tag": "DIV",
        "tagName": "💰 62년 연속 배당 인상",
        "naverUrl": "https://m.stock.naver.com/worldstock/stock/JNJ.N/total",
        "description": "62년 연속 배당을 인상한 세계 최고의 배당킹(Dividend King) 헬스케어 기업. 제약 및 의료기기 부문 이중 성장.",
        "pros": [
            "62년 연속 배당 인상 배당킹",
            "의료기기 & 바이오제약 포트폴리오",
            "AAA 등급 신용도"
        ],
        "risks": [
            "탈크 파우더 소송 합의금 이슈",
            "약가 인하 법안(IRA)"
        ],
        "naverPcUrl": "https://finance.naver.com/world/sitemain.naver?symbol=JNJ.N"
    },
    {
        "id": "us_BAC",
        "market": "US",
        "marketName": "NYSE",
        "code": "BAC",
        "symbol": "BAC.N",
        "name": "뱅크 오브 아메리카",
        "englishName": "Bank of America",
        "sector": "금융/은행",
        "price": 61.05,
        "changeRate": -0.93,
        "per": 11.5,
        "pbr": 1.15,
        "roe": 10.2,
        "dividendYield": 2.6,
        "bps": 36.34,
        "eps": 3.63,
        "marketCap": "3,260억 달러",
        "fairValue": 82.65,
        "upsidePotential": 35.4,
        "valueScore": 92,
        "tag": "PER",
        "tagName": "📉 저PER 11.5배",
        "naverUrl": "https://m.stock.naver.com/worldstock/stock/BAC.N/total",
        "description": "미국 2위 예금 상업은행. 워런 버핏의 버크셔 해서웨이 주요 보유 종목. 금리 환경에 따른 이자이익 수혜.",
        "pros": [
            "미국 2위 상업은행 탄탄한 예금 기반",
            "PER 11.5배 저평가",
            "워런 버핏 2위 보유주"
        ],
        "risks": [
            "미국 상업용 부동산 대출 손실",
            "예금 금리 상승 비용"
        ],
        "naverPcUrl": "https://finance.naver.com/world/sitemain.naver?symbol=BAC.N"
    },
    {
        "id": "us_CVX",
        "market": "US",
        "marketName": "NYSE",
        "code": "CVX",
        "symbol": "CVX.N",
        "name": "셰브론",
        "englishName": "Chevron Corp",
        "sector": "에너지",
        "price": 196.34,
        "changeRate": 1.74,
        "per": 12.2,
        "pbr": 1.65,
        "roe": 14.2,
        "dividendYield": 4.2,
        "bps": 96.06,
        "eps": 12.99,
        "marketCap": "2,910억 달러",
        "fairValue": 265.06,
        "upsidePotential": 35.0,
        "valueScore": 92,
        "tag": "DIV",
        "tagName": "💰 고배당 4.2%",
        "naverUrl": "https://m.stock.naver.com/worldstock/stock/CVX.N/total",
        "description": "미국 2위 석유 및 천연가스 공룡. 37년 연속 배당 인상 및 버크셔 해서웨이 대량 보유 에너지주.",
        "pros": [
            "37년 연속 배당 인상",
            "배당수익률 4.2%",
            "헤스(Hess) 인수 통한 생산량 증대"
        ],
        "risks": [
            "국제 유가 하락 리스크",
            "기후 변화 규제"
        ],
        "naverPcUrl": "https://finance.naver.com/world/sitemain.naver?symbol=CVX.N"
    },
    {
        "id": "us_AMD",
        "market": "US",
        "marketName": "NASDAQ",
        "code": "AMD",
        "symbol": "AMD.O",
        "name": "AMD",
        "englishName": "Advanced Micro Devices",
        "sector": "AI반도체/CPU",
        "price": 550.52,
        "changeRate": -0.33,
        "per": 32.5,
        "pbr": 3.4,
        "roe": 12.8,
        "dividendYield": 0.0,
        "bps": 45.7,
        "eps": 4.78,
        "marketCap": "2,510억 달러",
        "fairValue": 743.2,
        "upsidePotential": 35.0,
        "valueScore": 92,
        "tag": "PER",
        "tagName": "📉 MI300X AI 칩 턴어라운드",
        "naverUrl": "https://m.stock.naver.com/worldstock/stock/AMD.O/total",
        "description": "MI300X AI 가속기로 엔비디아 독점에 맞서는 유일한 대항마. 라이젠 CPU 및 서버 데이터센터 점유율 지속 확대.",
        "pros": [
            "MI300X AI 가속기 매출 급증",
            "서버용 EPYC CPU 점유율 상승",
            "PBR 3.4배 수준"
        ],
        "risks": [
            "엔비디아 시장 독점력",
            "PC 수요 변동"
        ],
        "naverPcUrl": "https://finance.naver.com/world/sitemain.naver?symbol=AMD.O"
    },
    {
        "id": "us_ADI",
        "market": "US",
        "marketName": "NASDAQ",
        "code": "ADI",
        "symbol": "ADI.O",
        "name": "아날로그 디바이스",
        "englishName": "Analog Devices",
        "sector": "차량/산업 반도체",
        "price": 377.78,
        "changeRate": -2.31,
        "per": 28.0,
        "pbr": 3.2,
        "roe": 12.5,
        "dividendYield": 1.6,
        "bps": 71.25,
        "eps": 8.14,
        "marketCap": "1,130억 달러",
        "fairValue": 510.0,
        "upsidePotential": 35.0,
        "valueScore": 92,
        "tag": "PBR",
        "tagName": "💎 PBR 3.2배 전장 반도체",
        "naverUrl": "https://m.stock.naver.com/worldstock/stock/ADI.O/total",
        "description": "전기차 배터리 관리 시스템(BMS) 및 고정밀 아날로그 신호 처리 칩 글로벌 2위.",
        "pros": [
            "전기차 BMS 시장 독점력",
            "PBR 3.2배 안정적 구조",
            "영업이익률 40%+"
        ],
        "risks": [
            "차량용 반도체 재고 축적 기간",
            "경기 민감도"
        ],
        "naverPcUrl": "https://finance.naver.com/world/sitemain.naver?symbol=ADI.O"
    },
    {
        "id": "us_ISRG",
        "market": "US",
        "marketName": "NASDAQ",
        "code": "ISRG",
        "symbol": "ISRG.O",
        "name": "인투이티브 서지컬",
        "englishName": "Intuitive Surgical",
        "sector": "의료 로봇",
        "price": 331.31,
        "changeRate": -2.75,
        "per": 55.0,
        "pbr": 12.4,
        "roe": 21.0,
        "dividendYield": 0.0,
        "bps": 35.08,
        "eps": 7.9,
        "marketCap": "1,540억 달러",
        "fairValue": 540.0,
        "upsidePotential": 63.0,
        "valueScore": 92,
        "tag": "ROE",
        "tagName": "🚀 다빈치 수술로봇 세계 1위",
        "naverUrl": "https://m.stock.naver.com/worldstock/stock/ISRG.O/total",
        "description": "세계 1위 수술용 로봇 '다빈치(da Vinci 5)' 제조. 수술 소모품 및 서비스 반복 매출 구조 80%.",
        "pros": [
            "다빈치 로봇 수술 독점 생태계",
            "다빈치5 신제품 승인 모멘텀",
            "수술 건수 지속 성장"
        ],
        "risks": [
            "비만치료제(GLP-1) 수술 건수 영향 우려",
            "병원 CAPEX 예산"
        ],
        "naverPcUrl": "https://finance.naver.com/world/sitemain.naver?symbol=ISRG.O"
    },
    {
        "id": "kr_035420",
        "market": "KR",
        "marketName": "KOSPI",
        "code": "035420",
        "symbol": "035420",
        "name": "NAVER",
        "englishName": "NAVER",
        "sector": "플랫폼/인터넷",
        "price": 220000,
        "changeRate": 11.73,
        "per": 18.2,
        "pbr": 1.25,
        "roe": 10.4,
        "dividendYield": 0.8,
        "bps": 142400,
        "eps": 9780,
        "marketCap": "28조 5,000억원",
        "fairValue": 250000,
        "upsidePotential": 13.6,
        "valueScore": 91,
        "tag": "ROE",
        "tagName": "🚀 플랫폼 저점 매수",
        "naverUrl": "https://m.stock.naver.com/domestic/stock/035420/total",
        "description": "국내 1위 포털 플랫폼. 커머스, 웹툰, 핀테크 사업 호조 및 생성형 AI 하이퍼클로바X 도입으로 밸류에이션 하단 매수 기회.",
        "pros": [
            "국내 1위 검색/커머스 플랫폼 독점력",
            "PER 18배 역사적 하단",
            "치지직/웹툰 글로벌 확장"
        ],
        "risks": [
            "C-커머스(알리/테무) 침투 리스크",
            "라인야후 지분 이슈"
        ],
        "naverPcUrl": "https://finance.naver.com/item/main.naver?code=035420"
    },
    {
        "id": "us_XOM",
        "market": "US",
        "marketName": "NYSE",
        "code": "XOM",
        "symbol": "XOM.N",
        "name": "엑손모빌",
        "englishName": "Exxon Mobil",
        "sector": "에너지/석유",
        "price": 156.88,
        "changeRate": 1.58,
        "per": 11.2,
        "pbr": 1.85,
        "roe": 16.2,
        "dividendYield": 3.3,
        "bps": 63.13,
        "eps": 10.42,
        "marketCap": "4,620억 달러",
        "fairValue": 204.81,
        "upsidePotential": 30.6,
        "valueScore": 91,
        "tag": "DIV",
        "tagName": "💰 배당귀족 (3.3%)",
        "naverUrl": "https://m.stock.naver.com/worldstock/stock/XOM.N/total",
        "description": "서방 최대 인프라 석유/가스 기업. 낮은 손익분기점 생산단가($35/배럴 이하)와 41년 연속 배당 인상 기록 보유.",
        "pros": [
            "41년 연속 배당 인상 배당귀족주",
            "낮은 생산 단가 경쟁력",
            "강력한 잉여현금흐름(FCF)"
        ],
        "risks": [
            "유가 등 원자재 가격 변동성",
            "친환경 전환 압박"
        ],
        "naverPcUrl": "https://finance.naver.com/world/sitemain.naver?symbol=XOM.N"
    },
    {
        "id": "us_ZS",
        "market": "US",
        "marketName": "NASDAQ",
        "code": "ZS",
        "symbol": "ZS.O",
        "name": "지스케일러",
        "englishName": "Zscaler Inc.",
        "sector": "클라우드 보안",
        "price": 142.09,
        "changeRate": -0.12,
        "per": 52.0,
        "pbr": 14.5,
        "roe": 24.0,
        "dividendYield": 0.0,
        "bps": 12.75,
        "eps": 3.55,
        "marketCap": "285억 달러",
        "fairValue": 245.0,
        "upsidePotential": 72.4,
        "valueScore": 91,
        "tag": "ROE",
        "tagName": "🚀 제로트러스트 보안 혁신",
        "naverUrl": "https://m.stock.naver.com/worldstock/stock/ZS.O/total",
        "description": "원격 근무 및 클라우드 트래픽 보호 제로 트러스트(Zero Trust) 보안 아키텍처 글로벌 선도.",
        "pros": [
            "제로 트러스트 보안 네트워크 독점력",
            "ARR 20억 달러 돌파",
            "원격 근무 필수 솔루션"
        ],
        "risks": [
            "팔로알토 등 대형 보안사 침범",
            "영업 마케팅 비용"
        ],
        "naverPcUrl": "https://finance.naver.com/world/sitemain.naver?symbol=ZS.O"
    },
    {
        "id": "kr_068270",
        "market": "KR",
        "marketName": "KOSPI",
        "code": "068270",
        "symbol": "068270",
        "name": "셀트리온",
        "englishName": "Celltrion",
        "sector": "제약/바이오",
        "price": 172200,
        "changeRate": 1.23,
        "per": 35.0,
        "pbr": 2.85,
        "roe": 8.5,
        "dividendYield": 0.3,
        "bps": 63850,
        "eps": 5200,
        "marketCap": "39조 8,000억원",
        "fairValue": 240000,
        "upsidePotential": 39.4,
        "valueScore": 90,
        "tag": "ROE",
        "tagName": "🚀 바이오시밀러 글로벌",
        "naverUrl": "https://m.stock.naver.com/domestic/stock/068270/total",
        "description": "세계 최초 항체 바이오시밀러 개발사. 짐펜트라(램시마SC) 미국 출시 및 직판망 구축으로 이익 성장 기대.",
        "pros": [
            "미국 짐펜트라 신약 매출 가시화",
            "통합 셀트리온 시너지",
            "자사주 소각 적극 시행"
        ],
        "risks": [
            "바이오시밀러 가격 경쟁 심화",
            "합병 후 단기 마진 감소"
        ],
        "naverPcUrl": "https://finance.naver.com/item/main.naver?code=068270"
    },
    {
        "id": "us_CRWD",
        "market": "US",
        "marketName": "NASDAQ",
        "code": "CRWD",
        "symbol": "CRWD.O",
        "name": "크라우드스트라이크",
        "englishName": "CrowdStrike Holdings",
        "sector": "클라우드 보안",
        "price": 185.66,
        "changeRate": -1.47,
        "per": 65.0,
        "pbr": 22.0,
        "roe": 28.0,
        "dividendYield": 0.0,
        "bps": 15.68,
        "eps": 5.3,
        "marketCap": "840억 달러",
        "fairValue": 450.0,
        "upsidePotential": 142.4,
        "valueScore": 90,
        "tag": "ROE",
        "tagName": "🚀 엔드포인트 AI 보안 1위",
        "naverUrl": "https://m.stock.naver.com/worldstock/stock/CRWD.O/total",
        "description": "Falcon 클라우드 AI 보안 플랫폼 1위. 시스템 업데이트 일시 장애 이후 과도한 하락으로 저평가 반등 기회.",
        "pros": [
            "엔드포인트 보안 위협 탐지 1위",
            "고객 이탈률 2% 이하 극저",
            "ARR(연간반복매출) 35억달러+"
        ],
        "risks": [
            "업데이트 오류 보상 소송 이슈",
            "고밸류에이션 부담"
        ],
        "naverPcUrl": "https://finance.naver.com/world/sitemain.naver?symbol=CRWD.O"
    },
    {
        "id": "kr_207940",
        "market": "KR",
        "marketName": "KOSPI",
        "code": "207940",
        "symbol": "207940",
        "name": "삼성바이오로직스",
        "englishName": "Samsung Biologics",
        "sector": "바이오/CDMO",
        "price": 1379000,
        "changeRate": 0.51,
        "per": 48.0,
        "pbr": 4.2,
        "roe": 9.8,
        "dividendYield": 0.0,
        "bps": 201190,
        "eps": 17600,
        "marketCap": "60조 1,000억원",
        "fairValue": 1852200,
        "upsidePotential": 34.3,
        "valueScore": 89,
        "tag": "ROE",
        "tagName": "🚀 바이오 CDMO 1위",
        "naverUrl": "https://m.stock.naver.com/domestic/stock/207940/total",
        "description": "세계 최대 바이오의약품 수탁생산(CDMO) 기업. 5공장 증설 및 수주 잔고 초과로 장기 고성장 보장.",
        "pros": [
            "세계 최대 생산 능력(Capacitiy)",
            "글로벌 제약사 대형 장기 계약",
            "미국 생물보안법 수혜"
        ],
        "risks": [
            "높은 밸류에이션 부담",
            "환율 하락 변수"
        ],
        "naverPcUrl": "https://finance.naver.com/item/main.naver?code=207940"
    },
    {
        "id": "kr_091990",
        "market": "KR",
        "marketName": "KOSDAQ",
        "code": "091990",
        "symbol": "091990",
        "name": "셀트리온제약",
        "englishName": "Celltrion Pharm",
        "sector": "코스닥/제약",
        "price": 92000,
        "changeRate": 0.55,
        "per": 28.0,
        "pbr": 2.1,
        "roe": 7.9,
        "dividendYield": 0.0,
        "bps": 43800,
        "eps": 3280,
        "marketCap": "3조 8,500억원",
        "fairValue": 130000,
        "upsidePotential": 41.3,
        "valueScore": 89,
        "tag": "ROE",
        "tagName": "🚀 코스닥 바이오 1위",
        "naverUrl": "https://m.stock.naver.com/domestic/stock/091990/total",
        "description": "코스닥 대표 제약사. 셀트리온 그룹 바이오시밀러 국내 독점 유통 및 케미컬 의약품 고성장.",
        "pros": [
            "셀트리온 바이오시밀러 유통망",
            "코스닥 150 대표 지수주",
            "케미컬 신약 개발 진행"
        ],
        "risks": [
            "셀트리온 3사 합병 일정 변수",
            "약가 인하 리스크"
        ],
        "naverPcUrl": "https://finance.naver.com/item/main.naver?code=091990"
    },
    {
        "id": "kr_005490",
        "market": "KR",
        "marketName": "KOSPI",
        "code": "005490",
        "symbol": "005490",
        "name": "POSCO홀딩스",
        "englishName": "POSCO Holdings",
        "sector": "철강/소재",
        "price": 323500,
        "changeRate": 6.77,
        "per": 14.8,
        "pbr": 0.55,
        "roe": 4.8,
        "dividendYield": 2.6,
        "bps": 694000,
        "eps": 25800,
        "marketCap": "32조 3,000억원",
        "fairValue": 550000,
        "upsidePotential": 70.0,
        "valueScore": 88,
        "tag": "PBR",
        "tagName": "💎 PBR 0.55배",
        "naverUrl": "https://m.stock.naver.com/domestic/stock/005490/total",
        "description": "철강업계 세계 최고 경쟁력 보유 및 리튬/양극재 친환경 미래소재 풀밸류체인 구축. PBR 0.55배로 역사적 저점 매수 구간.",
        "pros": [
            "PBR 0.55배 자산저평가",
            "아르헨티나 리튬염호 본격 양산",
            "철강 업황 바닥 통과"
        ],
        "risks": [
            "중국 철강 과잉 공급",
            "이차전지 소재 가격 변동"
        ],
        "naverPcUrl": "https://finance.naver.com/item/main.naver?code=005490"
    },
    {
        "id": "kr_036570",
        "market": "KR",
        "marketName": "KOSPI",
        "code": "036570",
        "symbol": "036570",
        "name": "엔씨소프트",
        "englishName": "NCSOFT",
        "sector": "게임/콘텐츠",
        "price": 225000,
        "changeRate": 3.21,
        "per": 16.8,
        "pbr": 0.92,
        "roe": 5.4,
        "dividendYield": 2.1,
        "bps": 211950,
        "eps": 11600,
        "marketCap": "4조 2,800억원",
        "fairValue": 280000,
        "upsidePotential": 24.4,
        "valueScore": 88,
        "tag": "PBR",
        "tagName": "💎 PBR 0.92배 청산가치",
        "naverUrl": "https://m.stock.naver.com/domestic/stock/036570/total",
        "description": "리니지 IP 보유 대표 MMORPG 가치주. 부동산 및 현금 자산 풍부하며 콘솔 신작(TL 등) 체질 개선 중.",
        "pros": [
            "보유 현금 및 판교 사옥 자산가치 2조원+",
            "PBR 0.92배 저평가",
            "글로벌 슈팅/콘솔 장르 다변화"
        ],
        "risks": [
            "리니지 쇄신 성과 지연",
            "신작 모멘텀 부진"
        ],
        "naverPcUrl": "https://finance.naver.com/item/main.naver?code=036570"
    },
    {
        "id": "us_TSLA",
        "market": "US",
        "marketName": "NASDAQ",
        "code": "TSLA",
        "symbol": "TSLA.O",
        "name": "테슬라",
        "englishName": "Tesla",
        "sector": "전기차/자율주행",
        "price": 330.71,
        "changeRate": -11.58,
        "per": 58.0,
        "pbr": 8.8,
        "roe": 15.2,
        "dividendYield": 0.0,
        "bps": 28.67,
        "eps": 4.35,
        "marketCap": "8,020억 달러",
        "fairValue": 446.46,
        "upsidePotential": 35.0,
        "valueScore": 88,
        "tag": "ROE",
        "tagName": "🚀 FSD 자율주행 & 로봇",
        "naverUrl": "https://m.stock.naver.com/worldstock/stock/TSLA.O/total",
        "description": "전기차 1위 및 FSD 자율주행, 로보택시, 옵티머스 휴머노이드 로봇 기술 보유 신개념 인공지능 플랫폼.",
        "pros": [
            "FSD 자율주행 주행데이터 1위",
            "에너지 저장장치(Megapack) 고성장",
            "옵티머스 로봇 생태계"
        ],
        "risks": [
            "전기차 할인 경쟁 마진 압박",
            "CEO 리스크 변수"
        ],
        "naverPcUrl": "https://finance.naver.com/world/sitemain.naver?symbol=TSLA.O"
    },
    {
        "id": "kr_051910",
        "market": "KR",
        "marketName": "KOSPI",
        "code": "051910",
        "symbol": "051910",
        "name": "LG화학",
        "englishName": "LG Chem",
        "sector": "석유화학/배터리",
        "price": 271500,
        "changeRate": 7.74,
        "per": 15.2,
        "pbr": 0.88,
        "roe": 6.2,
        "dividendYield": 1.8,
        "bps": 403400,
        "eps": 23350,
        "marketCap": "25조 1,000억원",
        "fairValue": 520000,
        "upsidePotential": 91.5,
        "valueScore": 87,
        "tag": "PBR",
        "tagName": "💎 PBR 0.88배 바닥권",
        "naverUrl": "https://m.stock.naver.com/domestic/stock/051910/total",
        "description": "국내 1위 종합 화학 및 LG에너지솔루션 대주주. 양극재 전구체 소재 고성장 및 석유화학 구조조정 수혜.",
        "pros": [
            "PBR 0.88배 역사적 바닥 수준",
            "양극재 매출 본격 성장",
            "LG엔솔 지분 81% 보유"
        ],
        "risks": [
            "석유화학 중국 공급 과잉",
            "전기차 케즘(일시적 둔화)"
        ],
        "naverPcUrl": "https://finance.naver.com/item/main.naver?code=051910"
    },
    {
        "id": "kr_035720",
        "market": "KR",
        "marketName": "KOSPI",
        "code": "035720",
        "symbol": "035720",
        "name": "카카오",
        "englishName": "Kakao",
        "sector": "플랫폼/인터넷",
        "price": 37150,
        "changeRate": 4.65,
        "per": 22.0,
        "pbr": 1.4,
        "roe": 6.5,
        "dividendYield": 0.2,
        "bps": 30350,
        "eps": 1930,
        "marketCap": "18조 8,000억원",
        "fairValue": 62000,
        "upsidePotential": 66.9,
        "valueScore": 86,
        "tag": "ROE",
        "tagName": "모바일 인프라",
        "naverUrl": "https://m.stock.naver.com/domestic/stock/035720/total",
        "description": "국내 국민 메신저 카카오톡 기반 모바일 플랫폼. 계열사 쇄신 및 톡비즈 광고/커머스 수익성 개선 추진.",
        "pros": [
            "카카오톡 4800만 MAU 트래픽",
            "광고/선물하기 안정적 매출",
            "경영 쇄신 작업 진행"
        ],
        "risks": [
            "사법 리스크 변수",
            "자회사 주가 부진"
        ],
        "naverPcUrl": "https://finance.naver.com/item/main.naver?code=035720"
    },
    {
        "id": "us_INTC",
        "market": "US",
        "marketName": "NASDAQ",
        "code": "INTC",
        "symbol": "INTC.O",
        "name": "인텔",
        "englishName": "Intel Corporation",
        "sector": "반도체/파운드리",
        "price": 102.47,
        "changeRate": -0.15,
        "per": 18.5,
        "pbr": 1.1,
        "roe": 5.8,
        "dividendYield": 1.6,
        "bps": 31.09,
        "eps": 1.85,
        "marketCap": "1,450억 달러",
        "fairValue": 142.36,
        "upsidePotential": 38.9,
        "valueScore": 86,
        "tag": "PBR",
        "tagName": "💎 PBR 1.1배 턴어라운드",
        "naverUrl": "https://m.stock.naver.com/worldstock/stock/INTC.O/total",
        "description": "미국 정부 반도체 지원법(CHIPS Act) 최대 수혜 파운드리 및 PC/서버 CPU 제조업체.",
        "pros": [
            "미국 정부 보조금 최대 지원",
            "파운드리 18A 공정 로드맵",
            "PBR 1.1배 주가 바닥권"
        ],
        "risks": [
            "파운드리 적자 지속",
            "AI 반도체 주도권 상실 우려"
        ],
        "naverPcUrl": "https://finance.naver.com/world/sitemain.naver?symbol=INTC.O"
    },
    {
        "id": "kr_373220",
        "market": "KR",
        "marketName": "KOSPI",
        "code": "373220",
        "symbol": "373220",
        "name": "LG에너지솔루션",
        "englishName": "LG Energy Solution",
        "sector": "이차전지",
        "price": 348000,
        "changeRate": 8.41,
        "per": 65.0,
        "pbr": 4.1,
        "roe": 6.8,
        "dividendYield": 0.0,
        "bps": 94270,
        "eps": 5940,
        "marketCap": "90조 4,000억원",
        "fairValue": 510000,
        "upsidePotential": 46.6,
        "valueScore": 85,
        "tag": "ROE",
        "tagName": "글로벌 배터리 2위",
        "naverUrl": "https://m.stock.naver.com/domestic/stock/373220/total",
        "description": "글로벌 2위 전기차 배터리 기업. GM, 현대차, 스텔란티스, 폰다 등 세계 최다 합작법인(JV) 보유.",
        "pros": [
            "세계 최다 수주 잔고 보유",
            "미국 IRA AMPC 세액공제 수혜",
            "ESS 신시장 확대"
        ],
        "risks": [
            "단기 밸류에이션 부담",
            "전기차 케즘 고비"
        ],
        "naverPcUrl": "https://finance.naver.com/item/main.naver?code=373220"
    },
    {
        "id": "kr_247540",
        "market": "KR",
        "marketName": "KOSDAQ",
        "code": "247540",
        "symbol": "247540",
        "name": "에코프로비엠",
        "englishName": "EcoPro BM",
        "sector": "코스닥/이차전지",
        "price": 118200,
        "changeRate": 9.95,
        "per": 85.0,
        "pbr": 5.2,
        "roe": 6.2,
        "dividendYield": 0.0,
        "bps": 35000,
        "eps": 2140,
        "marketCap": "17조 8,000억원",
        "fairValue": 250000,
        "upsidePotential": 111.5,
        "valueScore": 82,
        "tag": "ROE",
        "tagName": "코스닥 시총 1위",
        "naverUrl": "https://m.stock.naver.com/domestic/stock/247540/total",
        "description": "코스닥 시가총액 1위 하이엔드 양극재 전문 기업. 삼성SDI, SK온 향 대형 장기 계약 체결.",
        "pros": [
            "하이니켈 양극재 기술력 글로벌 1위",
            "코스닥 1위 대표주",
            "코스피 이전상장 추진 모멘텀"
        ],
        "risks": [
            "리튬/니켈 가격 변동",
            "고밸류에이션 부담"
        ],
        "naverPcUrl": "https://finance.naver.com/item/main.naver?code=247540"
    }
]

# ---------------------------------------------------------------------------
# Live Price Updater Engine
# ---------------------------------------------------------------------------
import concurrent.futures

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
            
            curr_price = stock['price']
            fair_val = stock['fairValue']
            if curr_price > 0:
                if fair_val <= curr_price:
                    fair_val = round(curr_price * 1.35, 2 if stock['market'] == 'US' else -2)
                    stock['fairValue'] = int(fair_val) if stock['market'] == 'KR' else float(fair_val)
                stock['upsidePotential'] = round(((fair_val - curr_price) / curr_price) * 100, 1)
    except Exception:
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
        time.sleep(30)

# ---------------------------------------------------------------------------
# Naver Scraper Function
# ---------------------------------------------------------------------------
def scrape_naver_kr_stock(code):
    url = f"https://finance.naver.com/item/main.naver?code={code}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    try:
        res = requests.get(url, headers=headers, timeout=5)
        res.encoding = 'euc-kr'
        soup = BeautifulSoup(res.text, 'html.parser')
        
        name_elem = soup.select_one('.wrap_company h2 a')
        price_elem = soup.select_one('.no_today .blind')
        name = name_elem.text.strip() if name_elem else ""
        price_str = price_elem.text.replace(',', '').strip() if price_elem else "0"
        price = int(price_str) if price_str.isdigit() else 0
        
        per_elem = soup.select_one('#_per')
        pbr_elem = soup.select_one('#_pbr')
        dvr_elem = soup.select_one('#_dvr')
        
        per = float(per_elem.text.replace(',', '')) if per_elem and per_elem.text != 'N/A' else 0.0
        pbr = float(pbr_elem.text.replace(',', '')) if pbr_elem and pbr_elem.text != 'N/A' else 0.0
        dvr = float(dvr_elem.text.replace(',', '')) if dvr_elem and dvr_elem.text != 'N/A' else 0.0
        
        return {
            "scraped": True,
            "code": code,
            "name": name,
            "price": price,
            "per": per,
            "pbr": pbr,
            "dividendYield": dvr
        }
    except Exception as e:
        return {"scraped": False, "error": str(e)}

# ---------------------------------------------------------------------------
# HTTP Handler
# ---------------------------------------------------------------------------
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
            
        if parsed_path.path == '/api/scrape-kr':
            query = urllib.parse.parse_qs(parsed_path.query)
            code = query.get('code', ['005380'])[0]
            result = scrape_naver_kr_stock(code)
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(result, ensure_ascii=False).encode('utf-8'))
            return

        return super().do_GET()

def run_server(port=8080):
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
