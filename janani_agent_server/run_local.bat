@echo off
echo.
echo ==========================================
echo  Janani Setu - Strands Agent Server Setup
echo ==========================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH.
    echo Please install Python 3.10+ from https://python.org
    pause
    exit /b 1
)

:: Check for .env file
if not exist .env (
    echo [SETUP] .env file not found. Creating from template...
    copy .env.example .env
    echo.
    echo *** IMPORTANT: Open .env and fill in your AWS credentials before continuing ***
    echo     AWS_ACCESS_KEY_ID=your_access_key
    echo     AWS_SECRET_ACCESS_KEY=your_secret_key
    echo.
    echo How to get AWS credentials:
    echo  1. Go to https://console.aws.amazon.com
    echo  2. Navigate to IAM > Users > Your User > Security credentials
    echo  3. Create Access Key (choose 'Application running outside AWS')
    echo  4. Copy the keys into .env
    echo.
    echo Also enable Bedrock model access:
    echo  1. Go to https://console.aws.amazon.com/bedrock
    echo  2. Click 'Model access' in left sidebar
    echo  3. Enable 'Claude 3.5 Sonnet v2' under Anthropic
    echo.
    pause
)

:: Create virtual environment if not exists
if not exist venv (
    echo [SETUP] Creating Python virtual environment...
    python -m venv venv
)

:: Activate and install deps
echo [SETUP] Installing dependencies...
call venv\Scripts\activate.bat
pip install -r requirements.txt --quiet

echo.
echo [INFO] Getting your local IP address...
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /R "IPv4"') do (
    set LOCAL_IP=%%a
    goto :found
)
:found
set LOCAL_IP=%LOCAL_IP: =%
echo.
echo ==========================================
echo  SERVER READY TO START
echo ==========================================
echo.
echo  Your local IP: %LOCAL_IP%
echo.
echo  In maa-app/.env, set:
echo  EXPO_PUBLIC_STRANDS_AGENT_URL=http://%LOCAL_IP%:8000
echo.
echo  Starting Janani Agent Server...
echo ==========================================
echo.

python main.py
pause
