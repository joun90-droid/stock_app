@echo off
chcp 65001 > nul
title 전영재 전용 주식종목 찾기 - Cloudflare 실시간 서버 실행기

echo =================================================================
echo [ 전영재 전용 주식종목 찾기 - Cloudflare 터널 서버 실행 중 ]
echo =================================================================
echo.

cd /d "%~dp0"

echo 1. Python 실시간 시세 서버 실행 중 (포트 8080)...
start /b python app.py 8080

timeout /t 2 > nul

echo 2. Cloudflare 고성능 보안 인터넷 터널 생성 중...
start /b .\cloudflared.exe tunnel --url http://127.0.0.1:8080

timeout /t 3 > nul

echo 3. 웹 브라우저에서 자동 열기...
start http://localhost:8080

echo.
echo =================================================================
echo 초고속 Cloudflare 서버가 성공적으로 실행되었습니다!
echo 카카오톡 공유 링크를 이용해 스마트폰에서 연결해 보세요.
echo =================================================================
echo.
pause
