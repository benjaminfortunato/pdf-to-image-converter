@echo off
echo PDF to Image Converter - Build Script
echo =====================================

echo.
echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Cleaning previous build...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"

echo.
echo Building executable with PyInstaller...
pyinstaller PDF-to-Image-Converter.spec

if %ERRORLEVEL% NEQ 0 (
    echo Build failed!
    pause
    exit /b 1
)

echo.
echo Build complete! Check the 'dist' folder for the executable.
echo.
pause
