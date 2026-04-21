@echo off
set MSBUILD_PATH="C:\Program Files\Microsoft Visual Studio\18\Community\MSBuild\Current\Bin\MSBuild.exe"

echo ========================================
echo COMPILANDO CLIENTE DEBUG (OpenGL x64)
echo ========================================
cd /d "%~dp0client\vc17"
%MSBUILD_PATH% otclient.sln /p:Configuration=Debug /p:Platform=x64 /m
if %ERRORLEVEL% neq 0 (
    echo [ERRO] Falha ao compilar o cliente debug.
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo ========================================
echo CLIENTE DEBUG COMPILADO COM SUCESSO!
echo O executavel esta em: client\
echo traceDebug logs serao visiveis (sem NDEBUG)
echo ========================================
pause
