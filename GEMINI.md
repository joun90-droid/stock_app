# GEMINI.md - 프로젝트 UI/UX 디자인 및 레이아웃 개발 지침

## 📐 핵심 UI/UX 레이아웃 지침
> **"모든 UI 작업 시 PC 웹 화면은 넓은 카드형 레이아웃, 모바일 접속 시에는 1열 자동 조정 반응형 레이아웃을 기본으로 적용할 것"**

### 🖥️ PC 웹 화면 (Desktop View)
- PC 화면 해상도에서는 넓은 다컬럼 카드형 대시보드 레이아웃 (`max-width: 1400px`, `grid-template-columns: repeat(auto-fill, minmax(350px, 1fr))`)을 적용합니다.
- 모든 종목 카드의 타이틀, 실시간 현재가, S-RIM 적정주가, PBR/PER/ROE 지표 박스 및 하단 버튼군이 픽셀 단위 일직선(Pixel-Perfect Alignment)으로 단정하게 정렬되어야 합니다.

### 📱 모바일 화면 (Mobile Responsive View - max-width: 768px)
- 모바일 디바이스 접속 시 1열 자동 조정 반응형 레이아웃 (`grid-template-columns: 1fr`)을 기본으로 적용합니다.
- 모바일 스티키 헤더는 뒤쪽 주식 종목 카드를 가리지 않도록 슬림형 레일 및 가로 스크롤 버튼 레일 구조를 유지합니다.
- 모바일 하단에는 고정 탭 바 (`Mobile Bottom Navigation Bar`)를 제공합니다.

### 🟢 실시간 데이터 & 네이버 증권 연동
- 네이버 증권 🇰🇷국내(`finance.naver.com`) 및 🇺🇸미국 해외증권(`api.stock.naver.com`) 시세 스크레이핑 엔진을 통해 15초 주기 실시간 자동 동기화를 유지합니다.
