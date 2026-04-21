@echo off

call "%~dp0build_server.bat"
if %ERRORLEVEL% neq 0 exit /b %ERRORLEVEL%

call "%~dp0build_client.bat"
if %ERRORLEVEL% neq 0 exit /b %ERRORLEVEL%