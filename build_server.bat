@echo off
set MSBUILD_PATH="C:\Program Files\Microsoft Visual Studio\18\Community\MSBuild\Current\Bin\MSBuild.exe"

echo ========================================
echo COMPILANDO SERVIDOR (Release x64)
echo ========================================
cd /d "%~dp0server\vc17"
%MSBUILD_PATH% theforgottenserver.sln /p:Configuration=Release /p:Platform=x64 /m
if %ERRORLEVEL% neq 0 (
    echo [ERRO] Falha ao compilar o servidor.
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo ========================================
echo COPIANDO DLLs para o diretorio do servidor
echo ========================================
xcopy /Y "%~dp0server\vcpkg_installed\x64-windows\x64-windows\bin\*.dll" "%~dp0server\"
if %ERRORLEVEL% neq 0 (
    echo [ERRO] Falha ao copiar DLLs.
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo ========================================
echo SERVIDOR COMPILADO COM SUCESSO!
echo ========================================
pause
