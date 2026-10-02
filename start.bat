@echo off
chcp 65001 >nul

if "%DEEPSEEK_API_KEY%"=="" (
    echo 请先设置DeepSeek API Key：
    echo set DEEPSEEK_API_KEY=你的DeepSeek_API_Key
    pause
    exit /b 1
)

python agent_serial.py
pause
