# -*- coding: utf-8 -*-
import json
import re
import os

from app import STOCKS_DATABASE as existing_db

# 50 NASDAQ Stocks customized for 전영재
nasdaq_stocks = [
    {
        "id": "us_GOOGL", "market": "US", "marketName": "NASDAQ", "code": "GOOGL", "symbol": "GOOGL.O",
        "name": "알파벳 (구글)", "englishName": "Alphabet (Google)", "sector": "빅테크/인터넷",
        "price": 182.50, "changeRate": 1.65, "per": 21.5, "pbr": 5.8, "roe": 28.5, "dividendYield": 0.4,
        "bps": 31.46, "eps": 8.48, "marketCap": "2조 2,600억 달러", "fairValue": 240.00, "upsidePotential": 31.5,
        "valueScore": 98, "tag": "ROE", "tagName": "🚀 전영재 미국 1픽 빅테크 저평가",
        "naverUrl": "https://finance.naver.com/world/sitemain.naver?symbol=GOOGL.O",
        "description": "전영재 추천 미국 빅테크 1위! M7 대형주 중 가장 저평가된 거인. 검색 독점력과 클라우드 고성장, 자체 AI 칩(TPU) 및 제미나이 AI 생태계 구축.",
        "pros": ["M7 대형주 중 최저 PER(21배)", "검색 & 유튜브 캐시카우 현금흐름", "클라우드 30%+ 고성장"],
        "risks": ["반독점 소송 이슈", "AI 검색 전환기 비용 증가"]
    },
    {
        "id": "us_AAPL", "market": "US", "marketName": "NASDAQ", "code": "AAPL", "symbol": "AAPL.O",
        "name": "애플", "englishName": "Apple Inc.", "sector": "빅테크/IT",
        "price": 224.20, "changeRate": 1.20, "per": 31.2, "pbr": 45.0, "roe": 147.0, "dividendYield": 0.5,
        "bps": 4.98, "eps": 7.18, "marketCap": "3조 4,400억 달러", "fairValue": 270.00, "upsidePotential": 20.4,
        "valueScore": 95, "tag": "ROE", "tagName": "💎 ROE 147% 온디바이스 AI",
        "naverUrl": "https://finance.naver.com/world/sitemain.naver?symbol=AAPL.O",
        "description": "글로벌 시가총액 1위 온디바이스 AI 플랫폼. 매년 1,000억 달러 규모 자사주 매입 소각으로 전영재 추천 주당가치 복리 상승주.",
        "pros": ["온디바이스 AI 애플 인텔리전스 교체 수요", "연 1000억 달러 대규모 자사주 소각", "서비스 매출 비중 25%+ 상승"],
        "risks": ["중국 스마트폰 경쟁", "반독점 인앱결제 규제"]
    },
    {
        "id": "us_MSFT", "market": "US", "marketName": "NASDAQ", "code": "MSFT", "symbol": "MSFT.O",
        "name": "마이크로소프트", "englishName": "Microsoft", "sector": "클라우드/AI",
        "price": 448.90, "changeRate": 1.42, "per": 34.5, "pbr": 12.5, "roe": 38.5, "dividendYield": 0.7,
        "bps": 35.91, "eps": 13.01, "marketCap": "3조 3,300억 달러", "fairValue": 540.00, "upsidePotential": 20.3,
        "valueScore": 96, "tag": "ROE", "tagName": "🚀 오픈AI & 클라우드 독점",
        "naverUrl": "https://finance.naver.com/world/sitemain.naver?symbol=MSFT.O",
        "description": "생성형 AI 시대 최고 리더. 오픈AI 대주주 및 오피스 365 Copilot 구독 모델과 애저(Azure) 클라우드 폭발 성장.",
        "pros": ["오픈AI 파트너십 독점적 위치", "오피스 Copilot 구독 매출 추가", "애저 클라우드 30%+ 고성장"],
        "risks": ["AI 인프라 CAPEX 부담", "클라우드 경쟁 심화"]
    },
    {
        "id": "us_NVDA", "market": "US", "marketName": "NASDAQ", "code": "NVDA", "symbol": "NVDA.O",
        "name": "엔비디아", "englishName": "NVIDIA", "sector": "AI반도체",
        "price": 128.50, "changeRate": 3.85, "per": 45.2, "pbr": 38.0, "roe": 115.0, "dividendYield": 0.1,
        "bps": 3.38, "eps": 2.84, "marketCap": "3조 1,500억 달러", "fairValue": 165.00, "upsidePotential": 28.4,
        "valueScore": 94, "tag": "ROE", "tagName": "🚀 AI GPU 80%+ 점유율",
        "naverUrl": "https://finance.naver.com/world/sitemain.naver?symbol=NVDA.O",
        "description": "AI 혁명의 핵심 엔진. 블랙웰(Blackwell) 및 H100 독점 공급으로 ROE 115% 달성하는 전영재 주도 AI 1위 주식.",
        "pros": ["AI GPU 시장 80%+ 압도적 점유율", "CUDA 소프트웨어 생태계 락인", "영업이익률 60%+ 압도적 마진"],
        "risks": ["빅테크 자이언트 자체 칩 개발", "미중 반도체 수출 규제"]
    },
    {
        "id": "us_META", "market": "US", "marketName": "NASDAQ", "code": "META", "symbol": "META.O",
        "name": "메타 플랫폼스", "englishName": "Meta Platforms", "sector": "소셜미디어/AI",
        "price": 498.20, "changeRate": 2.10, "per": 24.8, "pbr": 8.2, "roe": 34.0, "dividendYield": 0.4,
        "bps": 60.75, "eps": 20.08, "marketCap": "1조 2,600억 달러", "fairValue": 610.00, "upsidePotential": 22.4,
        "valueScore": 95, "tag": "ROE", "tagName": "🚀 Llama 오픈소스 AI 리더",
        "naverUrl": "https://finance.naver.com/world/sitemain.naver?symbol=META.O",
        "description": "32억 MAU 소셜 네트워크와 Llama 오픈소스 AI 기술 주도. 릴스 광고 타깃팅 고도화로 전영재 추천 가치성장주.",
        "pros": ["32억 명 글로벌 이용자 네트워크", "Llama 3 AI 모델 리더십", "분기 배당 신설 및 자사주 소각"],
        "risks": ["메타버스 부문 적자 지속", "광고 시장 변동성"]
    },
    {
        "id": "us_AMZN", "market": "US", "marketName": "NASDAQ", "code": "AMZN", "symbol": "AMZN.O",
        "name": "아마존", "englishName": "Amazon.com", "sector": "이커머스/클라우드",
        "price": 186.40, "changeRate": 1.25, "per": 42.0, "pbr": 7.5, "roe": 21.5, "dividendYield": 0.0,
        "bps": 24.85, "eps": 4.43, "marketCap": "1조 9,400억 달러", "fairValue": 235.00, "upsidePotential": 26.1,
        "valueScore": 93, "tag": "ROE", "tagName": "🚀 AWS 클라우드 1위",
        "naverUrl": "https://finance.naver.com/world/sitemain.naver?symbol=AMZN.O",
        "description": "세계 1위 이커머스 및 AWS 클라우드 기업. 물류 자동화 비용 효율화 및 고마진 광고 사업 매출 폭발.",
        "pros": ["AWS 글로벌 1위 클라우드 점유율", "고마진 광고 사업 고성장", "풀필먼트 물류 비용 절감"],
        "risks": ["이커머스 가격 경쟁", "빅테크 규제 리스크"]
    },
    {
        "id": "us_TSLA", "market": "US", "marketName": "NASDAQ", "code": "TSLA", "symbol": "TSLA.O",
        "name": "테슬라", "englishName": "Tesla", "sector": "전기차/자율주행",
        "price": 252.30, "changeRate": 4.50, "per": 58.0, "pbr": 8.8, "roe": 15.2, "dividendYield": 0.0,
        "bps": 28.67, "eps": 4.35, "marketCap": "8,020억 달러", "fairValue": 330.00, "upsidePotential": 30.8,
        "valueScore": 88, "tag": "ROE", "tagName": "🚀 FSD 자율주행 & 로봇",
        "naverUrl": "https://finance.naver.com/world/sitemain.naver?symbol=TSLA.O",
        "description": "전기차 1위 및 FSD 자율주행, 로보택시, 옵티머스 휴머노이드 로봇 기술 보유 신개념 인공지능 플랫폼.",
        "pros": ["FSD 자율주행 주행데이터 1위", "에너지 저장장치(Megapack) 고성장", "옵티머스 로봇 생태계"],
        "risks": ["전기차 할인 경쟁 마진 압박", "CEO 리스크 변수"]
    },
    {
        "id": "us_AMD", "market": "US", "marketName": "NASDAQ", "code": "AMD", "symbol": "AMD.O",
        "name": "AMD", "englishName": "Advanced Micro Devices", "sector": "AI반도체/CPU",
        "price": 155.40, "changeRate": 2.10, "per": 32.5, "pbr": 3.4, "roe": 12.8, "dividendYield": 0.0,
        "bps": 45.70, "eps": 4.78, "marketCap": "2,510억 달러", "fairValue": 210.00, "upsidePotential": 35.1,
        "valueScore": 92, "tag": "PER", "tagName": "📉 MI300X AI 칩 턴어라운드",
        "naverUrl": "https://finance.naver.com/world/sitemain.naver?symbol=AMD.O",
        "description": "MI300X AI 가속기로 엔비디아 독점에 맞서는 유일한 대항마. 라이젠 CPU 및 서버 데이터센터 점유율 지속 확대.",
        "pros": ["MI300X AI 가속기 매출 급증", "서버용 EPYC CPU 점유율 상승", "PBR 3.4배 수준"],
        "risks": ["엔비디아 시장 독점력", "PC 수요 변동"]
    },
    {
        "id": "us_QCOM", "market": "US", "marketName": "NASDAQ", "code": "QCOM", "symbol": "QCOM.O",
        "name": "퀄컴", "englishName": "Qualcomm", "sector": "통신/온디바이스AI",
        "price": 175.20, "changeRate": 1.85, "per": 15.2, "pbr": 6.8, "roe": 31.0, "dividendYield": 2.0,
        "bps": 25.76, "eps": 11.52, "marketCap": "1,950억 달러", "fairValue": 235.00, "upsidePotential": 34.1,
        "valueScore": 97, "tag": "PER", "tagName": "📉 전영재 픽 PER 15배 저평가",
        "naverUrl": "https://finance.naver.com/world/sitemain.naver?symbol=QCOM.O",
        "description": "스냅드래곤 X 엘리트 PC 칩 및 온디바이스 AI 스마트폰 칩 선도. PER 15.2배로 반도체 대형주 중 극저평가.",
        "pros": ["PER 15.2배 저평가 반도체", "스냅드래곤 AI PC 시장 확장", "전장(Auto) 반도체 수주 잔고 급증"],
        "risks": ["애플 자체 모뎀 칩 개발", "스마트폰 교체 주기 변수"]
    },
    {
        "id": "us_AVGO", "market": "US", "marketName": "NASDAQ", "code": "AVGO", "symbol": "AVGO.O",
        "name": "브로드컴", "englishName": "Broadcom Inc.", "sector": "반도체/네트워크",
        "price": 162.80, "changeRate": 2.40, "per": 28.4, "pbr": 11.2, "roe": 32.4, "dividendYield": 1.4,
        "bps": 14.53, "eps": 5.73, "marketCap": "7,620억 달러", "fairValue": 210.00, "upsidePotential": 29.0,
        "valueScore": 96, "tag": "ROE", "tagName": "🚀 맞춤형 ASIC AI 칩 1위",
        "naverUrl": "https://finance.naver.com/world/sitemain.naver?symbol=AVGO.O",
        "description": "구글, 메타 맞춤형 AI 반도체(ASIC) 설계 독점 및 VM웨어 인수를 통한 기업용 클라우드 소프트웨어 통합.",
        "pros": ["맞춤형 AI ASIC 칩 시장 독점력", "VM웨어 구독 매출 시너지", "지속적인 배당 증액"],
        "risks": ["VM웨어 기업 고객 이탈", "부채 비율 관리"]
    },
    {
        "id": "us_AMAT", "market": "US", "marketName": "NASDAQ", "code": "AMAT", "symbol": "AMAT.O",
        "name": "어플라이드 머티리얼즈", "englishName": "Applied Materials", "sector": "반도체 장비",
        "price": 215.30, "changeRate": 1.50, "per": 18.5, "pbr": 7.4, "roe": 35.2, "dividendYield": 0.8,
        "bps": 29.09, "eps": 11.63, "marketCap": "1,780억 달러", "fairValue": 285.00, "upsidePotential": 32.4,
        "valueScore": 96, "tag": "PER", "tagName": "📉 반도체 장비 1위 PER 18배",
        "naverUrl": "https://finance.naver.com/world/sitemain.naver?symbol=AMAT.O",
        "description": "세계 1위 반도체 종합 증착/재료 장비 기업. HBM 및 초미세 파운드리 공정 필수 장비 공급으로 전영재 추천 가치주.",
        "pros": ["세계 1위 반도체 장비 포트폴리오", "PER 18.5배 안정적 밸류에이션", "ROE 35.2% 고수익성"],
        "risks": ["중국 수출 제한 규제", "반도체 설비투자(CAPEX) 주기"]
    },
    {
        "id": "us_LRCX", "market": "US", "marketName": "NASDAQ", "code": "LRCX", "symbol": "LRCX.O",
        "name": "램리서치", "englishName": "Lam Research", "sector": "반도체 식각장비",
        "price": 952.00, "changeRate": 1.90, "per": 20.1, "pbr": 11.8, "roe": 52.0, "dividendYield": 1.0,
        "bps": 80.67, "eps": 47.36, "marketCap": "1,240억 달러", "fairValue": 1280.00, "upsidePotential": 34.5,
        "valueScore": 96, "tag": "ROE", "tagName": "💎 ROE 52% HBM 식각 1위",
        "naverUrl": "https://finance.naver.com/world/sitemain.naver?symbol=LRCX.O",
        "description": "메모리 낸드(NAND) 및 HBM 고단 적층용 플라즈마 식각 장비 세계 1위. ROE 52%의 강력한 이익 창출력.",
        "pros": ["HBM & 3D NAND 식각 독점력", "ROE 52% 극상위 수익성", "메모리 업황 턴어라운드 수혜"],
        "risks": ["메모리 제조사 투자 시점 변수", "대중국 수출 규제"]
    },
    {
        "id": "us_MU", "market": "US", "marketName": "NASDAQ", "code": "MU", "symbol": "MU.O",
        "name": "마이크론 테크놀로지", "englishName": "Micron Technology", "sector": "메모리/HBM",
        "price": 112.50, "changeRate": 3.10, "per": 14.2, "pbr": 2.1, "roe": 18.5, "dividendYield": 0.4,
        "bps": 53.57, "eps": 7.92, "marketCap": "1,245억 달러", "fairValue": 165.00, "upsidePotential": 46.7,
        "valueScore": 97, "tag": "PBR", "tagName": "💎 PBR 2.1배 HBM3E 고성장",
        "naverUrl": "https://finance.naver.com/world/sitemain.naver?symbol=MU.O",
        "description": "엔비디아 HBM3E 8단/12단 주요 공급업체로 선정. PBR 2.1배로 메모리 턴어라운드 전영재 저평가 핵심 매수 종목.",
        "pros": ["엔비디아 HBM3E 공급 본궤도", "PBR 2.1배 자산저평가", "DRAM/NAND 가격 상승 사이클"],
        "risks": ["메모리 가격 사이클 변동성", "삼성전자/SK하이닉스와 경쟁"]
    },
    {
        "id": "us_ASML", "market": "US", "marketName": "NASDAQ", "code": "ASML", "symbol": "ASML.O",
        "name": "ASML 홀딩", "englishName": "ASML Holding", "sector": "반도체 노광장비",
        "price": 880.00, "changeRate": 1.10, "per": 38.5, "pbr": 18.2, "roe": 48.0, "dividendYield": 0.8,
        "bps": 48.35, "eps": 22.85, "marketCap": "3,480억 달러", "fairValue": 1150.00, "upsidePotential": 30.7,
        "valueScore": 95, "tag": "ROE", "tagName": "🚀 High-NA EUV 세계 독점",
        "naverUrl": "https://finance.naver.com/world/sitemain.naver?symbol=ASML.O",
        "description": "초미세 2nm 반도체 공정에 필수인 High-NA EUV 노광장비 유일 공급사. 독점적 기술 장벽 보유.",
        "pros": ["EUV 노광장비 100% 시장 독점", "High-NA 차세대 장비 출하", "ROE 48% 마진"],
        "risks": ["네덜란드 정부 대중 수출 규제", "고가격 장비 도입 시기"]
    },
    {
        "id": "us_CSCO", "market": "US", "marketName": "NASDAQ", "code": "CSCO", "symbol": "CSCO.O",
        "name": "시스코 시스템즈", "englishName": "Cisco Systems", "sector": "네트워크/보안",
        "price": 47.80, "changeRate": 0.40, "per": 14.8, "pbr": 3.8, "roe": 26.0, "dividendYield": 3.4,
        "bps": 12.57, "eps": 3.22, "marketCap": "1,920억 달러", "fairValue": 62.00, "upsidePotential": 29.7,
        "valueScore": 94, "tag": "DIV", "tagName": "💰 전영재 배당 픽 3.4% 저PER",
        "naverUrl": "https://finance.naver.com/world/sitemain.naver?symbol=CSCO.O",
        "description": "세계 1위 네트워크 장비 및 보안 스플렁크(Splunk) 인수 완료. 배당수익률 3.4%와 PER 14.8배의 안정적 가치주.",
        "pros": ["네트워크 글로벌 1위 점유율", "배당수익률 3.4% 고배당", "스플렁크 인수로 보안 구독 강화"],
        "risks": ["기업 IT 장비 투자 둔화", "클라우드 서비스 자체 구축"]
    },
    {
        "id": "us_CMCSA", "market": "US", "marketName": "NASDAQ", "code": "CMCSA", "symbol": "CMCSA.O",
        "name": "컴캐스트", "englishName": "Comcast Corporation", "sector": "미디어/통신",
        "price": 38.50, "changeRate": -0.20, "per": 10.2, "pbr": 1.2, "roe": 16.5, "dividendYield": 3.2,
        "bps": 32.08, "eps": 3.77, "marketCap": "1,510억 달러", "fairValue": 54.00, "upsidePotential": 40.3,
        "valueScore": 97, "tag": "PER", "tagName": "📉 PER 10배 극단적 저평가",
        "naverUrl": "https://finance.naver.com/world/sitemain.naver?symbol=CMCSA.O",
        "description": "유니버설 스튜디오, 피콕 OTT, 초고속 인터넷 인프라 보유. PER 10.2배로 주가 청산 수준의 초저평가 전영재 픽.",
        "pros": ["PER 10.2배 극단적 저평가", "유니버설 테마파크 & 영화 IP", "배당 3.2% 및 자사주 매입"],
        "risks": ["케이블 TV 코드커팅 이탈", "OTT 피콕 적자"]
    },
    {
        "id": "us_PYPL", "market": "US", "marketName": "NASDAQ", "code": "PYPL", "symbol": "PYPL.O",
        "name": "페이팔", "englishName": "PayPal Holdings", "sector": "핀테크/결제",
        "price": 64.20, "changeRate": 1.15, "per": 14.5, "pbr": 2.1, "roe": 18.2, "dividendYield": 0.0,
        "bps": 30.57, "eps": 4.42, "marketCap": "660억 달러", "fairValue": 98.00, "upsidePotential": 52.6,
        "valueScore": 98, "tag": "PER", "tagName": "📉 전영재 1픽 FCF 부자 PER 14배",
        "naverUrl": "https://finance.naver.com/world/sitemain.naver?symbol=PYPL.O",
        "description": "전영재 강추 핀테크 저평가 1위! 연간 50억 달러 이상 잉여현금흐름(FCF) 창출. PER 14.5배 및 대규모 자사주 소각 진행.",
        "pros": ["PER 14.5배 및 FCF 50억 달러 창출", "시총 7~8% 수준 자사주 소각", "Fastlane 간편결제 신제품 도입"],
        "risks": ["애플페이 등 결제 경쟁", "마진율 압박"]
    },
    {
        "id": "us_GILD", "market": "US", "marketName": "NASDAQ", "code": "GILD", "symbol": "GILD.O",
        "name": "길리어드 사이언스", "englishName": "Gilead Sciences", "sector": "바이오/제약",
        "price": 72.40, "changeRate": 0.60, "per": 11.8, "pbr": 3.4, "roe": 28.5, "dividendYield": 4.2,
        "bps": 21.29, "eps": 6.13, "marketCap": "902억 달러", "fairValue": 105.00, "upsidePotential": 45.0,
        "valueScore": 96, "tag": "DIV", "tagName": "💰 고배당 4.2% 저PER 바이오",
        "naverUrl": "https://finance.naver.com/world/sitemain.naver?symbol=GILD.O",
        "description": "HIV 치료제 시장 80% 독점 및 항암 신약(트로델비) 파이프라인 고성장. 배당 4.2%와 PER 11.8배 전영재 가치 바이오주.",
        "pros": ["배당수익률 4.2% 고배당", "PER 11.8배 저평가", "HIV 장기 지속형 신약 독점"],
        "risks": ["항암제 임상3상 결과 변수", "특허 만료 일정"]
    },
    {
        "id": "us_BIIB", "market": "US", "marketName": "NASDAQ", "code": "BIIB", "symbol": "BIIB.O",
        "name": "바이오젠", "englishName": "Biogen Inc.", "sector": "바이오/신경계",
        "price": 218.00, "changeRate": -0.40, "per": 12.2, "pbr": 1.35, "roe": 11.2, "dividendYield": 0.0,
        "bps": 161.48, "eps": 17.86, "marketCap": "318억 달러", "fairValue": 310.00, "upsidePotential": 42.2,
        "valueScore": 94, "tag": "PBR", "tagName": "💎 PBR 1.35배 저평가 바이오",
        "naverUrl": "https://finance.naver.com/world/sitemain.naver?symbol=BIIB.O",
        "description": "알츠하이머 신약 레켐비(Lequembi) 최초 승인 및 척수성 근위축증 치료제 독점. PBR 1.35배 수준의 주가 바닥권.",
        "pros": ["레켐비 알츠하이머 신약 보급 확대", "PBR 1.35배 자산저평가", "희귀 신경계 파이프라인"],
        "risks": ["레켐비 처방 속도 정체", "기존 다발성 경화증 약가 하락"]
    },
    {
        "id": "us_AMGN", "market": "US", "marketName": "NASDAQ", "code": "AMGN", "symbol": "AMGN.O",
        "name": "암젠", "englishName": "Amgen Inc.", "sector": "바이오/제약",
        "price": 312.00, "changeRate": 0.80, "per": 14.2, "pbr": 12.5, "roe": 44.0, "dividendYield": 3.1,
        "bps": 24.96, "eps": 21.97, "marketCap": "1,670억 달러", "fairValue": 410.00, "upsidePotential": 31.4,
        "valueScore": 95, "tag": "DIV", "tagName": "💰 배당 3.1% 항암제 파이프라인",
        "naverUrl": "https://finance.naver.com/world/sitemain.naver?symbol=AMGN.O",
        "description": "글로벌 1위 바이오테크 제약사. 비만치료제(MariTide) 2상 결과 기대 및 호리즌 인수 효과로 강력한 현금창출력.",
        "pros": ["MariTide 주1회/월1회 비만치료제 게임체인저", "배당 3.1% 꾸준한 인상", "ROE 44% 수익성"],
        "risks": ["임상 데이터 발표 변수", "부채 상환 일정"]
    },
    {
        "id": "us_VRTX", "market": "US", "marketName": "NASDAQ", "code": "VRTX", "symbol": "VRTX.O",
        "name": "버텍스 파마슈티컬스", "englishName": "Vertex Pharmaceuticals", "sector": "바이오/희귀질환",
        "price": 468.00, "changeRate": 1.30, "per": 24.5, "pbr": 7.8, "roe": 28.4, "dividendYield": 0.0,
        "bps": 60.00, "eps": 19.10, "marketCap": "1,200억 달러", "fairValue": 590.00, "upsidePotential": 26.1,
        "valueScore": 94, "tag": "ROE", "tagName": "🚀 낭성섬유증 독점 바이오",
        "naverUrl": "https://finance.naver.com/world/sitemain.naver?symbol=VRTX.O",
        "description": "낭성섬유증 치료제 세계 독점 공급 및 유전자 편집 치료제(Casgevy) 최초 상용화 성공 바이오 대장주.",
        "pros": ["낭성섬유증 시장 90%+ 독점", "크리스퍼 유전자치료제 상용화", "ROE 28.4% 독보적 마진"],
        "risks": ["단일 치료제 매출 의존도", "유전자 치료제 고가격"]
    },
    {
        "id": "us_REGN", "market": "US", "marketName": "NASDAQ", "code": "REGN", "symbol": "REGN.O",
        "name": "리제네론", "englishName": "Regeneron Pharmaceuticals", "sector": "바이오/안과",
        "price": 985.00, "changeRate": 0.90, "per": 18.2, "pbr": 3.8, "roe": 22.0, "dividendYield": 0.0,
        "bps": 259.21, "eps": 54.12, "marketCap": "1,070억 달러", "fairValue": 1280.00, "upsidePotential": 29.9,
        "valueScore": 94, "tag": "PER", "tagName": "📉 저PER 18배 고성장 바이오",
        "naverUrl": "https://finance.naver.com/world/sitemain.naver?symbol=REGN.O",
        "description": "안과 질환 치료제 아일리아(Eylea) 및 아토피 치료제 듀피젠트(Dupixent) 글로벌 블록버스터 보유.",
        "pros": ["듀피젠트 연 매출 100억 달러 돌파", "PER 18.2배 우량한 재무구조", "자체 R&D 자체발굴 경쟁력"],
        "risks": ["아일리아 바이오시밀러 경쟁", "특허 소송 수용 여부"]
    },
    {
        "id": "us_KLAC", "market": "US", "marketName": "NASDAQ", "code": "KLAC", "symbol": "KLAC.O",
        "name": "KLA 코퍼레이션", "englishName": "KLA Corporation", "sector": "반도체 검사장비",
        "price": 780.00, "changeRate": 1.70, "per": 24.8, "pbr": 18.5, "roe": 72.0, "dividendYield": 0.8,
        "bps": 42.16, "eps": 31.45, "marketCap": "1,050억 달러", "fairValue": 990.00, "upsidePotential": 26.9,
        "valueScore": 95, "tag": "ROE", "tagName": "💎 ROE 72% 수율 검사 독점",
        "naverUrl": "https://finance.naver.com/world/sitemain.naver?symbol=KLAC.O",
        "description": "반도체 웨이퍼 결함 검사 및 수율 측정 장비 점유율 50%+ 1위 독점 기업. ROE 72%의 독보적 마진.",
        "pros": ["반도체 계측/검사 장비 독점력", "ROE 72% 압도적 기술력", "EUV/High-NA 도입 수혜"],
        "risks": ["고객사 사이클 변동성", "미중 갈등 소송"]
    },
    {
        "id": "us_TXN", "market": "US", "marketName": "NASDAQ", "code": "TXN", "symbol": "TXN.O",
        "name": "텍사스 인스트루먼트", "englishName": "Texas Instruments", "sector": "아날로그 반도체",
        "price": 198.00, "changeRate": 0.50, "per": 26.0, "pbr": 9.2, "roe": 31.0, "dividendYield": 2.8,
        "bps": 21.52, "eps": 7.61, "marketCap": "1,800억 달러", "fairValue": 250.00, "upsidePotential": 26.3,
        "valueScore": 93, "tag": "DIV", "tagName": "💰 20년 연속 배당 인상 반도체",
        "naverUrl": "https://finance.naver.com/world/sitemain.naver?symbol=TXN.O",
        "description": "차량용 및 산업용 아날로그 반도체 세계 1위. 20년 연속 배당금 증액 및 현금 흐름 우수 기업.",
        "pros": ["아날로그 반도체 세계 1위", "20년 연속 배당 인상 배당귀족", "80,000개 이상 고객사 분산"],
        "risks": ["300mm 팹 설비 투자(CAPEX) 기간 현금 흐름", "산업용 재고 조정"]
    },
    {
        "id": "us_ADI", "market": "US", "marketName": "NASDAQ", "code": "ADI", "symbol": "ADI.O",
        "name": "아날로그 디바이스", "englishName": "Analog Devices", "sector": "차량/산업 반도체",
        "price": 228.00, "changeRate": 0.80, "per": 28.0, "pbr": 3.2, "roe": 12.5, "dividendYield": 1.6,
        "bps": 71.25, "eps": 8.14, "marketCap": "1,130억 달러", "fairValue": 285.00, "upsidePotential": 25.0,
        "valueScore": 92, "tag": "PBR", "tagName": "💎 PBR 3.2배 전장 반도체",
        "naverUrl": "https://finance.naver.com/world/sitemain.naver?symbol=ADI.O",
        "description": "전기차 배터리 관리 시스템(BMS) 및 고정밀 아날로그 신호 처리 칩 글로벌 2위.",
        "pros": ["전기차 BMS 시장 독점력", "PBR 3.2배 안정적 구조", "영업이익률 40%+"],
        "risks": ["차량용 반도체 재고 축적 기간", "경기 민감도"]
    },
    {
        "id": "us_NXPI", "market": "US", "marketName": "NASDAQ", "code": "NXPI", "symbol": "NXPI.O",
        "name": "NXP 반도체", "englishName": "NXP Semiconductors", "sector": "차량용 반도체",
        "price": 265.00, "changeRate": 1.20, "per": 15.8, "pbr": 6.2, "roe": 38.0, "dividendYield": 1.5,
        "bps": 42.74, "eps": 16.77, "marketCap": "675억 달러", "fairValue": 345.00, "upsidePotential": 30.2,
        "valueScore": 96, "tag": "PER", "tagName": "📉 저PER 15.8배 차량반도체 1위",
        "naverUrl": "https://finance.naver.com/world/sitemain.naver?symbol=NXPI.O",
        "description": "차량용 레이더, 레이더/MCU 및 인포테인먼트 반도체 1위. PER 15.8배로 반도체 밸류에이션 매력 전영재 픽.",
        "pros": ["PER 15.8배 저평가", "자율주행 차량용 레이더 1위", "ROE 38% 고효율 경영"],
        "risks": ["글로벌 자동차 생산량 변동", "유럽 경기 영향"]
    },
    {
        "id": "us_MCHP", "market": "US", "marketName": "NASDAQ", "code": "MCHP", "symbol": "MCHP.O",
        "name": "마이크로칩 테크놀로지", "englishName": "Microchip Technology", "sector": "임베디드 반도체",
        "price": 84.50, "changeRate": 0.30, "per": 17.2, "pbr": 4.8, "roe": 25.5, "dividendYield": 2.2,
        "bps": 17.60, "eps": 4.91, "marketCap": "455억 달러", "fairValue": 112.00, "upsidePotential": 32.5,
        "valueScore": 94, "tag": "PER", "tagName": "📉 MCU 반도체 저평가 구간",
        "naverUrl": "https://finance.naver.com/world/sitemain.naver?symbol=MCHP.O",
        "description": "스마트 가전 및 자동차 마이크로컨트롤러(MCU) 리더. 주가 조정으로 PER 17.2배 진입.",
        "pros": ["MCU 글로벌 선도 경쟁력", "배당수익률 2.2%", "자사주 매입 병행"],
        "risks": ["재고 소진 기간 장기화", "중국 경쟁사 진입"]
    },
    {
        "id": "us_INTU", "market": "US", "marketName": "NASDAQ", "code": "INTU", "symbol": "INTU.O",
        "name": "인투이트", "englishName": "Intuit Inc.", "sector": "세무/회계 AI",
        "price": 645.00, "changeRate": 1.40, "per": 32.0, "pbr": 9.8, "roe": 31.2, "dividendYield": 0.6,
        "bps": 65.81, "eps": 20.15, "marketCap": "1,800억 달러", "fairValue": 810.00, "upsidePotential": 25.6,
        "valueScore": 93, "tag": "ROE", "tagName": "🚀 퀵북스/터보택스 독점망",
        "naverUrl": "https://finance.naver.com/world/sitemain.naver?symbol=INTU.O",
        "description": "미국 개인/중소기업 세무 및 회계 소프트웨어(TurboTax, QuickBooks, Mailchimp) 독점적 플랫폼.",
        "pros": ["터보택스 및 퀵북스 시장 80%+ 점유", "Intuit Assist AI 도입으로 주당가치 상승", "ROE 31.2%"],
        "risks": ["미국 IRS 자체 무료 세무 신고 시스템", "중소기업 고용 침체"]
    },
    {
        "id": "us_ADBE", "market": "US", "marketName": "NASDAQ", "code": "ADBE", "symbol": "ADBE.O",
        "name": "어도비", "englishName": "Adobe Inc.", "sector": "창작 소프트웨어",
        "price": 540.00, "changeRate": 2.20, "per": 26.0, "pbr": 11.5, "roe": 42.0, "dividendYield": 0.0,
        "bps": 46.95, "eps": 20.76, "marketCap": "2,420억 달러", "fairValue": 720.00, "upsidePotential": 33.3,
        "valueScore": 96, "tag": "PER", "tagName": "📉 Firefly AI 저평가 획득",
        "naverUrl": "https://finance.naver.com/world/sitemain.naver?symbol=ADBE.O",
        "description": "포토샵, 일러스트레이터, 프리미어 플랫폼 독점 및 생성형 AI Firefly 통합. 주가 조정 후 PER 26배 저평가 매수 구간.",
        "pros": ["글로벌 창작 크리에이터 90%+ 락인", "Firefly 상업용 안전 AI 강점", "ROE 42% 구독 모델"],
        "risks": ["OpenAI Sora 등 영상 생성 AI 위협", "경쟁 앱 성장"]
    },
    {
        "id": "us_PANW", "market": "US", "marketName": "NASDAQ", "code": "PANW", "symbol": "PANW.O",
        "name": "팔로알토 네트웍스", "englishName": "Palo Alto Networks", "sector": "사이버 보안",
        "price": 328.00, "changeRate": 1.80, "per": 42.0, "pbr": 15.2, "roe": 34.0, "dividendYield": 0.0,
        "bps": 21.57, "eps": 7.80, "marketCap": "1,060억 달러", "fairValue": 420.00, "upsidePotential": 28.0,
        "valueScore": 93, "tag": "ROE", "tagName": "🚀 차세대 보안 플랫폼 1위",
        "naverUrl": "https://finance.naver.com/world/sitemain.naver?symbol=PANW.O",
        "description": "글로벌 1위 사이버 보안 기업. 방화벽, 클라우드 보안, AI 보안 SOC(Cortex) 통합 플랫폼 전략 성공.",
        "pros": ["글로벌 보안 시장 점유율 1위", "플랫폼화(Platformization) 전략 계약 대형화", "FCF 마진 38%"],
        "risks": ["초기 무료 플랫폼 제공 시 단기 매출 영향", "보안 경쟁 심화"]
    },
    {
        "id": "us_CRWD", "market": "US", "marketName": "NASDAQ", "code": "CRWD", "symbol": "CRWD.O",
        "name": "크라우드스트라이크", "englishName": "CrowdStrike Holdings", "sector": "클라우드 보안",
        "price": 345.00, "changeRate": 2.50, "per": 65.0, "pbr": 22.0, "roe": 28.0, "dividendYield": 0.0,
        "bps": 15.68, "eps": 5.30, "marketCap": "840억 달러", "fairValue": 450.00, "upsidePotential": 30.4,
        "valueScore": 90, "tag": "ROE", "tagName": "🚀 엔드포인트 AI 보안 1위",
        "naverUrl": "https://finance.naver.com/world/sitemain.naver?symbol=CRWD.O",
        "description": "Falcon 클라우드 AI 보안 플랫폼 1위. 시스템 업데이트 일시 장애 이후 과도한 하락으로 저평가 반등 기회.",
        "pros": ["엔드포인트 보안 위협 탐지 1위", "고객 이탈률 2% 이하 극저", "ARR(연간반복매출) 35억달러+"],
        "risks": ["업데이트 오류 보상 소송 이슈", "고밸류에이션 부담"]
    },
    {
        "id": "us_FTNT", "market": "US", "marketName": "NASDAQ", "code": "FTNT", "symbol": "FTNT.O",
        "name": "포티넷", "englishName": "Fortinet", "sector": "네트워크 보안",
        "price": 68.50, "changeRate": 1.10, "per": 28.5, "pbr": 18.0, "roe": 45.0, "dividendYield": 0.0,
        "bps": 3.80, "eps": 2.40, "marketCap": "520억 달러", "fairValue": 92.00, "upsidePotential": 34.3,
        "valueScore": 95, "tag": "ROE", "tagName": "💎 ROE 45% FCF 보안강자",
        "naverUrl": "https://finance.naver.com/world/sitemain.naver?symbol=FTNT.O",
        "description": "자체 보안 ASIC 칩 탑재로 가성비 최상위 네트워크 보안 장비 제조. ROE 45% 및 잉여현금흐름 우수.",
        "pros": ["자체 ASIC 탑재 가성비 경쟁력", "ROE 45% 마진", "지속적 자사주 소각"],
        "risks": ["방화벽 교체 주기 둔화", "클라우드 전용 보안과 경쟁"]
    },
    {
        "id": "us_ZS", "market": "US", "marketName": "NASDAQ", "code": "ZS", "symbol": "ZS.O",
        "name": "지스케일러", "englishName": "Zscaler Inc.", "sector": "클라우드 보안",
        "price": 185.00, "changeRate": 1.90, "per": 52.0, "pbr": 14.5, "roe": 24.0, "dividendYield": 0.0,
        "bps": 12.75, "eps": 3.55, "marketCap": "285억 달러", "fairValue": 245.00, "upsidePotential": 32.4,
        "valueScore": 91, "tag": "ROE", "tagName": "🚀 제로트러스트 보안 혁신",
        "naverUrl": "https://finance.naver.com/world/sitemain.naver?symbol=ZS.O",
        "description": "원격 근무 및 클라우드 트래픽 보호 제로 트러스트(Zero Trust) 보안 아키텍처 글로벌 선도.",
        "pros": ["제로 트러스트 보안 네트워크 독점력", "ARR 20억 달러 돌파", "원격 근무 필수 솔루션"],
        "risks": ["팔로알토 등 대형 보안사 침범", "영업 마케팅 비용"]
    },
    {
        "id": "us_WDC", "market": "US", "marketName": "NASDAQ", "code": "WDC", "symbol": "WDC.O",
        "name": "웨스턴 디지털", "englishName": "Western Digital", "sector": "데이터 저장장치",
        "price": 68.20, "changeRate": 2.80, "per": 12.8, "pbr": 1.15, "roe": 11.5, "dividendYield": 0.0,
        "bps": 59.30, "eps": 5.32, "marketCap": "225억 달러", "fairValue": 98.00, "upsidePotential": 43.7,
        "valueScore": 96, "tag": "PBR", "tagName": "💎 PBR 1.15배 HDD/NAND 분사",
        "naverUrl": "https://finance.naver.com/world/sitemain.naver?symbol=WDC.O",
        "description": "HDD 및 플래시 메모리(SanDisk) 분사 추진. PBR 1.15배 수준으로 숨겨진 자산 가치 재평가 모멘텀.",
        "pros": ["PBR 1.15배 자산저평가", "HDD 및 NAND 사업 분사 가치 재평가", "AI 데이터센터 저장장치 수요"],
        "risks": ["NAND 메모리 가격 변동성", "부채 비율"]
    },
    {
        "id": "us_STX", "market": "US", "marketName": "NASDAQ", "code": "STX", "symbol": "STX.O",
        "name": "씨게이트 테크놀로지", "englishName": "Seagate Technology", "sector": "대용량 HDD",
        "price": 104.50, "changeRate": 2.10, "per": 15.2, "pbr": 12.0, "roe": 65.0, "dividendYield": 2.7,
        "bps": 8.70, "eps": 6.87, "marketCap": "218억 달러", "fairValue": 145.00, "upsidePotential": 38.8,
        "valueScore": 96, "tag": "ROE", "tagName": "💎 ROE 65% AI 데이터센터 HDD",
        "naverUrl": "https://finance.naver.com/world/sitemain.naver?symbol=STX.O",
        "description": "HAMR(열보조 자기기록) 초고용량 30TB+ 데이터센터 HDD 독점 출하. ROE 65% 및 2.7% 배당 전영재 픽.",
        "pros": ["HAMR 30TB+ 대용량 HDD 기술 독점", "ROE 65% 고수익성", "배당수익률 2.7%"],
        "risks": ["SSD 대체 가능성 일부 영역", "데이터센터 CAPEX 주기"]
    },
    {
        "id": "us_MRVL", "market": "US", "marketName": "NASDAQ", "code": "MRVL", "symbol": "MRVL.O",
        "name": "마벨 테크놀로지", "englishName": "Marvell Technology", "sector": "데이터센터 반도체",
        "price": 72.40, "changeRate": 2.00, "per": 28.0, "pbr": 4.2, "roe": 14.8, "dividendYield": 0.3,
        "bps": 17.23, "eps": 2.58, "marketCap": "626억 달러", "fairValue": 98.00, "upsidePotential": 35.4,
        "valueScore": 93, "tag": "PER", "tagName": "🚀 AI 맞춤형 칩 네트워크",
        "naverUrl": "https://finance.naver.com/world/sitemain.naver?symbol=MRVL.O",
        "description": "클라우드 데이터센터 AI 광연결 칩(PAM4 DSP) 및 빅테크 맞춤형 AI ASIC 칩 설계 전문.",
        "pros": ["데이터센터 800G 광커넥트 칩 1위", "맞춤형 AI ASIC 칩 수주 둔화 수혜", "클라우드 비중 70%+"],
        "risks": ["비 데이터센터 영역 둔화", "경쟁 심화"]
    },
    {
        "id": "us_ISRG", "market": "US", "marketName": "NASDAQ", "code": "ISRG", "symbol": "ISRG.O",
        "name": "인투이티브 서지컬", "englishName": "Intuitive Surgical", "sector": "의료 로봇",
        "price": 435.00, "changeRate": 1.20, "per": 55.0, "pbr": 12.4, "roe": 21.0, "dividendYield": 0.0,
        "bps": 35.08, "eps": 7.90, "marketCap": "1,540억 달러", "fairValue": 540.00, "upsidePotential": 24.1,
        "valueScore": 92, "tag": "ROE", "tagName": "🚀 다빈치 수술로봇 세계 1위",
        "naverUrl": "https://finance.naver.com/world/sitemain.naver?symbol=ISRG.O",
        "description": "세계 1위 수술용 로봇 '다빈치(da Vinci 5)' 제조. 수술 소모품 및 서비스 반복 매출 구조 80%.",
        "pros": ["다빈치 로봇 수술 독점 생태계", "다빈치5 신제품 승인 모멘텀", "수술 건수 지속 성장"],
        "risks": ["비만치료제(GLP-1) 수술 건수 영향 우려", "병원 CAPEX 예산"]
    },
    {
        "id": "us_BKNG", "market": "US", "marketName": "NASDAQ", "code": "BKNG", "symbol": "BKNG.O",
        "name": "부킹 홀딩스", "englishName": "Booking Holdings", "sector": "여행 테크",
        "price": 3850.00, "changeRate": 1.50, "per": 22.5, "pbr": 28.0, "roe": 68.0, "dividendYield": 0.9,
        "bps": 137.50, "eps": 171.11, "marketCap": "1,320억 달러", "fairValue": 4900.00, "upsidePotential": 27.3,
        "valueScore": 96, "tag": "ROE", "tagName": "💎 ROE 68% FCF 거대 여행독점",
        "naverUrl": "https://finance.naver.com/world/sitemain.naver?symbol=BKNG.O",
        "description": "Booking.com, Agoda, Priceline 글로벌 1위 온라인 여행사. ROE 68% 및 연간 70억 달러 FCF 창출.",
        "pros": ["글로벌 여행 플랫폼 1위", "ROE 68% 독보적 효율", "대규모 자사주 매입 및 분기배당 신설"],
        "risks": ["경기 침체 시 여행 지출 축소", "구글 여행 검색 경쟁"]
    },
    {
        "id": "us_ABNB", "market": "US", "marketName": "NASDAQ", "code": "ABNB", "symbol": "ABNB.O",
        "name": "에어비앤비", "englishName": "Airbnb Inc.", "sector": "숙박 플랫폼",
        "price": 148.00, "changeRate": 1.40, "per": 18.5, "pbr": 8.4, "roe": 41.0, "dividendYield": 0.0,
        "bps": 17.61, "eps": 8.00, "marketCap": "930억 달러", "fairValue": 198.00, "upsidePotential": 33.8,
        "valueScore": 97, "tag": "PER", "tagName": "📉 전영재 픽 PER 18배 마진 35%",
        "naverUrl": "https://finance.naver.com/world/sitemain.naver?symbol=ABNB.O",
        "description": "세계 1위 공유 숙박 네트워크. FCF 마진 35%+ 및 PER 18.5배로 현금흐름 대비 주가 극저평가 전영재 픽.",
        "pros": ["PER 18.5배 현금 흐름 우수", "FCF 마진 35% 이상", "장기 숙박 및 체험 상품 확대"],
        "risks": ["각국 도시 단기 숙박 규제", "여행 수요 변동"]
    },
    {
        "id": "us_SBUX", "market": "US", "marketName": "NASDAQ", "code": "SBUX", "symbol": "SBUX.O",
        "name": "스타벅스", "englishName": "Starbucks Corporation", "sector": "글로벌 리테일",
        "price": 76.40, "changeRate": 0.80, "per": 20.2, "pbr": 14.0, "roe": 55.0, "dividendYield": 3.0,
        "bps": 5.45, "eps": 3.78, "marketCap": "865억 달러", "fairValue": 105.00, "upsidePotential": 37.4,
        "valueScore": 95, "tag": "DIV", "tagName": "💰 배당 3.0% 브랜드 턴어라운드",
        "naverUrl": "https://finance.naver.com/world/sitemain.naver?symbol=SBUX.O",
        "description": "글로벌 1위 커피 프랜차이즈. 신임 CEO 넥스트 턴어라운드 및 배당수익률 3.0%로 전영재 추천 가치주.",
        "pros": ["글로벌 브랜드 파워 1위", "배당수익률 3.0%", "사이렌 오더 모바일 결제 비중 30%+"],
        "risks": ["중국 저가 커피 프랜차이즈 경쟁", "인건비 상승"]
    },
    {
        "id": "us_KHC", "market": "US", "marketName": "NASDAQ", "code": "KHC", "symbol": "KHC.O",
        "name": "크래프트 하인즈", "englishName": "Kraft Heinz", "sector": "식품/소비재",
        "price": 32.80, "changeRate": 0.10, "per": 11.2, "pbr": 0.78, "roe": 7.8, "dividendYield": 4.8,
        "bps": 42.05, "eps": 2.92, "marketCap": "398억 달러", "fairValue": 48.00, "upsidePotential": 46.3,
        "valueScore": 96, "tag": "PBR", "tagName": "💎 PBR 0.78배 고배당 4.8%",
        "naverUrl": "https://finance.naver.com/world/sitemain.naver?symbol=KHC.O",
        "description": "하인즈 케첩 및 크래프트 치즈 보유. PBR 0.78배 및 배당 4.8%로 버크셔 해서웨이 주요 보유 고배당주.",
        "pros": ["PBR 0.78배 장부가치 미달 저평가", "배당수익률 4.8% 고배당", "워런 버핏 대주주"],
        "risks": ["식품 원자재 가격", "저가 PB 상품과 경쟁"]
    },
    {
        "id": "us_MDLZ", "market": "US", "marketName": "NASDAQ", "code": "MDLZ", "symbol": "MDLZ.O",
        "name": "몬델리즈 인터내셔널", "englishName": "Mondelez International", "sector": "제과/소비재",
        "price": 68.50, "changeRate": 0.30, "per": 20.5, "pbr": 3.2, "roe": 16.5, "dividendYield": 2.5,
        "bps": 21.40, "eps": 3.34, "marketCap": "915억 달러", "fairValue": 86.00, "upsidePotential": 25.5,
        "valueScore": 93, "tag": "DIV", "tagName": "💰 오레오/리츠 필수소비재",
        "naverUrl": "https://finance.naver.com/world/sitemain.naver?symbol=MDLZ.O",
        "description": "오레오(Oreo), 리츠(Ritz), 밀카(Milka) 초콜릿 등 세계 1위 스낵 제과 기업.",
        "pros": ["글로벌 1위 스낵 브랜드 포트폴리오", "안정적 가격 인상 능력", "배당 2.5% 지속 인상"],
        "risks": ["코코아/설탕 원자재가 상승", "환율 변동성"]
    },
    {
        "id": "us_COST", "market": "US", "marketName": "NASDAQ", "code": "COST", "symbol": "COST.O",
        "name": "코스트코 홀세일", "englishName": "Costco Wholesale", "sector": "유통/회원제",
        "price": 840.00, "changeRate": 1.10, "per": 48.0, "pbr": 14.5, "roe": 29.5, "dividendYield": 0.5,
        "bps": 57.93, "eps": 17.50, "marketCap": "3,730억 달러", "fairValue": 980.00, "upsidePotential": 16.7,
        "valueScore": 94, "tag": "ROE", "tagName": "🚀 93% 재연장율 유통 독점",
        "naverUrl": "https://finance.naver.com/world/sitemain.naver?symbol=COST.O",
        "description": "회원재 유통 1위. 멤버십 재갱신율 93% 및 정기 특별배당 지급으로 독보적 가치 제공.",
        "pros": ["멤버십 연간 수익 안정성", "높은 고객 충성도 93%", "특별 배당 지속 지급"],
        "risks": ["높은 PER 밸류에이션", "이커머스 경쟁"]
    },
    {
        "id": "us_LULU", "market": "US", "marketName": "NASDAQ", "code": "LULU", "symbol": "LULU.O",
        "name": "룰루레몬 아틀레티카", "englishName": "Lululemon Athletica", "sector": "프리미엄 의류",
        "price": 295.00, "changeRate": 1.60, "per": 20.2, "pbr": 8.2, "roe": 42.0, "dividendYield": 0.0,
        "bps": 35.97, "eps": 14.60, "marketCap": "362억 달러", "fairValue": 420.00, "upsidePotential": 42.4,
        "valueScore": 97, "tag": "PER", "tagName": "📉 전영재 픽 PER 20배 바닥권 매수",
        "naverUrl": "https://finance.naver.com/world/sitemain.naver?symbol=LULU.O",
        "description": "프리미엄 애슬레저 1위 브랜드. 고성장세 대비 주가 40% 조정으로 PER 20.2배 역사적 저평가 전영재 픽.",
        "pros": ["PER 20.2배 역사적 바닥 수준", "ROE 42% 브랜드 프리미엄", "중국 및 글로벌 매장 고성장"],
        "risks": ["북미 의류 소비 둔화 우려", "경쟁 브랜드 저가화"]
    },
    {
        "id": "us_ROST", "market": "US", "marketName": "NASDAQ", "code": "ROST", "symbol": "ROST.O",
        "name": "로스 스토어스", "englishName": "Ross Stores", "sector": "오프프라이스 유통",
        "price": 145.00, "changeRate": 0.70, "per": 16.5, "pbr": 8.8, "roe": 51.0, "dividendYield": 1.0,
        "bps": 16.47, "eps": 8.78, "marketCap": "480억 달러", "fairValue": 192.00, "upsidePotential": 32.4,
        "valueScore": 95, "tag": "PER", "tagName": "📉 저PER 16.5배 가성비 유통",
        "naverUrl": "https://finance.naver.com/world/sitemain.naver?symbol=ROST.O",
        "description": "미국 2위 오프프라이스 브랜드 할인 유통망. 인플레이션 시기 알뜰 소비층 유입 수혜주.",
        "pros": ["PER 16.5배 저평가", "ROE 51% 고효율 매장 관리", "가성비 쇼핑 트렌드"],
        "risks": ["물류 및 인건비 인상", "재고 수급 능력"]
    },
    {
        "id": "us_DLTR", "market": "US", "marketName": "NASDAQ", "code": "DLTR", "symbol": "DLTR.O",
        "name": "달러 트리", "englishName": "Dollar Tree", "sector": "할인 유통",
        "price": 108.00, "changeRate": 0.40, "per": 15.5, "pbr": 2.8, "roe": 17.5, "dividendYield": 0.0,
        "bps": 38.57, "eps": 6.96, "marketCap": "232억 달러", "fairValue": 150.00, "upsidePotential": 38.9,
        "valueScore": 94, "tag": "PER", "tagName": "📉 고물가 수혜 저PER 유통",
        "naverUrl": "https://finance.naver.com/world/sitemain.naver?symbol=DLTR.O",
        "description": "미국 대표 1달러/다단가 할인 매장(Dollar Tree & Family Dollar). 고물가 구조적 수혜주.",
        "pros": ["PER 15.5배 저평가 턴어라운드", "다단가($3, $5) 상품 도입 마진 개선", "저소득층 필수 장보기점"],
        "risks": ["Family Dollar 매장 폐쇄 비용", "물류 비용"]
    },
    {
        "id": "us_ODFL", "market": "US", "marketName": "NASDAQ", "code": "ODFL", "symbol": "ODFL.O",
        "name": "올드 도미니언 프레이트 라인", "englishName": "Old Dominion Freight Line", "sector": "물류/운송",
        "price": 182.00, "changeRate": 1.10, "per": 26.5, "pbr": 8.2, "roe": 31.0, "dividendYield": 0.6,
        "bps": 22.19, "eps": 6.86, "marketCap": "392억 달러", "fairValue": 235.00, "upsidePotential": 29.1,
        "valueScore": 93, "tag": "ROE", "tagName": "🚀 운송업계 효율성 1위",
        "naverUrl": "https://finance.naver.com/world/sitemain.naver?symbol=ODFL.O",
        "description": "미국 1위 LTL(적재량 미달) 화물 운송사. 영업비율(OR) 70% 수준의 세계 최고 운송 효율성.",
        "pros": ["미국 LTL 물류 수송 1위", "ROE 31% 업계 최고 마진", "경쟁사 옐로우 파산 수혜"],
        "risks": ["미국 물동량 및 경기 변동", "유가 변동"]
    },
    {
        "id": "us_PCAR", "market": "US", "marketName": "NASDAQ", "code": "PCAR", "symbol": "PCAR.O",
        "name": "파카", "englishName": "PACCAR Inc", "sector": "대형 트럭",
        "price": 102.50, "changeRate": 0.90, "per": 11.5, "pbr": 2.8, "roe": 26.0, "dividendYield": 3.8,
        "bps": 36.60, "eps": 8.91, "marketCap": "536억 달러", "fairValue": 142.00, "upsidePotential": 38.5,
        "valueScore": 96, "tag": "PER", "tagName": "📉 저PER 11.5배 고배당 3.8%",
        "naverUrl": "https://finance.naver.com/world/sitemain.naver?symbol=PCAR.O",
        "description": "켄워스(Kenworth), 피터빌트(Peterbilt), DAF 대형 트럭 제조업체. PER 11.5배 및 특별배당 포함 3.8% 배당.",
        "pros": ["대형 트럭 시장 점유율 30%+", "PER 11.5배 및 배당 3.8%", "부품 서비스 부문 고마진"],
        "risks": ["물류 교체 수요 주기", "원자재 비용"]
    },
    {
        "id": "us_PAYX", "market": "US", "marketName": "NASDAQ", "code": "PAYX", "symbol": "PAYX.O",
        "name": "페이첵스", "englishName": "Paychex Inc.", "sector": "HR/급여 소프트웨어",
        "price": 124.00, "changeRate": 0.40, "per": 26.0, "pbr": 11.2, "roe": 44.0, "dividendYield": 3.2,
        "bps": 11.07, "eps": 4.76, "marketCap": "446억 달러", "fairValue": 160.00, "upsidePotential": 29.0,
        "valueScore": 94, "tag": "DIV", "tagName": "💰 배당 3.2% ROE 44% HR소프트웨어",
        "naverUrl": "https://finance.naver.com/world/sitemain.naver?symbol=PAYX.O",
        "description": "미국 중소기업용 급여, HR 관리 및 복리후생 소프트웨어 1위. ROE 44% 및 3.2% 안정 배당.",
        "pros": ["중소기업 HR 소프트웨어 독점력", "ROE 44% 고수익성", "배당수익률 3.2%"],
        "risks": ["미국 고용 지표 둔화 시 영향", "소프트웨어 경쟁"]
    },
    {
        "id": "us_EXPE", "market": "US", "marketName": "NASDAQ", "code": "EXPE", "symbol": "EXPE.O",
        "name": "익스피디아 그룹", "englishName": "Expedia Group", "sector": "여행 테크",
        "price": 132.00, "changeRate": 1.20, "per": 11.4, "pbr": 4.8, "roe": 40.0, "dividendYield": 0.0,
        "bps": 27.50, "eps": 11.57, "marketCap": "172억 달러", "fairValue": 195.00, "upsidePotential": 47.7,
        "valueScore": 98, "tag": "PER", "tagName": "📉 전영재 1픽 초저PER 11.4배 여행테크",
        "naverUrl": "https://finance.naver.com/world/sitemain.naver?symbol=EXPE.O",
        "description": "전영재 1픽 저평가! Expedia, Hotels.com, Vrbo 플랫폼 보유. PER 11.4배로 여행 테크 중 최고 가치 매력.",
        "pros": ["PER 11.4배 극단적 저평가", "Hotels.com & One Key 리워드 통합", "ROE 40% 및 대규모 자사주 소각"],
        "risks": ["구글/부킹닷컴과 경쟁", "여행 경기 침체"]
    }
]

# Combine existing non-NASDAQ and new NASDAQ stocks
nasdaq_ids = {s['id'] for s in nasdaq_stocks}
merged_db = [s for s in existing_db if s['id'] not in nasdaq_ids]
merged_db.extend(nasdaq_stocks)

print(f"Total merged database size: {len(merged_db)}")

# Update app.py
app_py_path = 'app.py'
with open(app_py_path, 'r', encoding='utf-8') as f:
    app_py_content = f.read()

formatted_json = json.dumps(merged_db, ensure_ascii=False, indent=4)
new_app_py = re.sub(
    r'STOCKS_DATABASE\s*=\s*\[.*?\]\n\n# --',
    f'STOCKS_DATABASE = {formatted_json}\n\n# --',
    app_py_content,
    flags=re.DOTALL
)

with open(app_py_path, 'w', encoding='utf-8') as f:
    f.write(new_app_py)
print("Updated app.py successfully!")

# Update app.js
app_js_path = 'app.js'
with open(app_js_path, 'r', encoding='utf-8') as f:
    app_js_content = f.read()

new_app_js = re.sub(
    r'const INITIAL_STOCKS = \[.*?\];\n\n// App State',
    f'const INITIAL_STOCKS = {formatted_json};\n\n// App State',
    app_js_content,
    flags=re.DOTALL
)
# Clean up any syntax comments in app.js
new_app_js = re.sub(r'^\s*#.*$', '// Comment cleaned up', new_app_js, flags=re.MULTILINE)

with open(app_js_path, 'w', encoding='utf-8') as f:
    f.write(new_app_js)
print("Updated app.js successfully!")
