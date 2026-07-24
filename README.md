# 📈 stock_app - Undervalued Stock Screener & Real-Time Price Analytics

stock_app은 네이버 증권 🇰🇷국내 저평가 주식 및 🇺🇸미국 나스닥/NYSE 대표 저평가 주식 93개 종목을 실시간으로 추적하고 S-RIM(사경인 적정주가) 공식 기반으로 가치를 산정하는 모바일 최적화 웹 애플리케이션입니다.

## ✨ 주요 기능
- **실시간 주가 동기화**: Yahoo Finance 및 네이버 증권 모바일 연동 실시간 주가 갱신
- **S-RIM 적정주가 계산기**: ROE, BPS 기반 적정주가 및 상승여력(%) 자동 산출
- **모바일 퍼스트 UI**: 스마트폰 해상도(360px~430px) 및 다크 모드에 최적화된 고대비 인터페이스
- **카카오톡 공유 & 홈 화면 앱 추가**: PWA & OpenGraph 카드 지원

## 🚀 실행 방법
`ash
python app.py 8080
`
브라우저에서 http://localhost:8080 으로 접속할 수 있습니다.

## ☁️ Vercel 배포 방법
1. GitHub 저장소(stock_app) 생성 후 푸시
2. Vercel(https://vercel.com)에 로그인 후 해당 저장소 Import
3. 365일 24시간 클라우드 서버 배포 완료!
