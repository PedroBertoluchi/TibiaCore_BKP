@echo off
set MSBUILD_PATH="C:\Program Files\Microsoft Visual Studio\18\Community\MSBuild\Current\Bin\MSBuild.exe"

echo ========================================
echo COMPILANDO CLIENTE (OpenGL x64)
echo ========================================
cd /d "%~dp0client\vc17"
%MSBUILD_PATH% otclient.sln /p:Configuration=OpenGL /p:Platform=x64 /m
if %ERRORLEVEL% neq 0 (
    echo [ERRO] Falha ao compilar o cliente.
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo ========================================
echo CLIENTE COMPILADO COM SUCESSO!
echo ========================================
pause
