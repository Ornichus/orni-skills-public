@echo off
REM web-pdf-compile — standalone installer (Windows)
REM Usage : double-click install.bat or run from cmd

cd /d "%~dp0"

echo === web-pdf-compile installer ===
echo.

where node >nul 2>nul
if %errorlevel% neq 0 (
    echo ERROR: Node.js is not installed. Install from https://nodejs.org ^(^>=18^).
    pause
    exit /b 1
)

for /f "tokens=*" %%v in ('node --version') do set NODE_VER=%%v
echo Node version : %NODE_VER% OK
echo.

set CHROME_PATH=C:\Program Files\Google\Chrome\Application\chrome.exe
if exist "%CHROME_PATH%" (
    echo Chrome found : %CHROME_PATH%
) else (
    set CHROME_PATH=C:\Program Files ^(x86^)\Google\Chrome\Application\chrome.exe
    if exist "%CHROME_PATH%" (
        echo Chrome found : %CHROME_PATH%
    ) else (
        echo WARNING: Google Chrome not found in standard locations.
        echo          Install Chrome from https://www.google.com/chrome/
        echo          OR set "chrome_path" in your sources.json
    )
)
echo.

echo Installing npm dependencies ^(~150 MB^)...
call npm install
if %errorlevel% neq 0 (
    echo.
    echo ERROR: npm install failed.
    pause
    exit /b 1
)

echo.
echo === Install complete ===
echo.
echo Next steps :
echo   npm run probe -- https://your-site.com/article    ^(find selectors^)
echo   npm run capture -- examples/smoke-test.json       ^(smoke test^)
echo   npm run compile -- examples/smoke-test.json       ^(generate PDF^)
echo.
echo PDF lands at output\^<config_name^>\COMPILATION.pdf
echo.
pause
