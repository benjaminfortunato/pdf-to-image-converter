@echo off
echo PDF to Image Converter - Build with Bundled Poppler
echo ====================================================

echo.
echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Cleaning previous builds...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

echo.
echo Downloading and preparing Poppler...
python bundle_poppler.py

if %ERRORLEVEL% NEQ 0 (
    echo Failed to prepare Poppler!
    pause
    exit /b 1
)

echo.
echo Building executable with bundled Poppler...
pyinstaller PDF-to-Image-Converter-with-Poppler.spec

if %ERRORLEVEL% NEQ 0 (
    echo Build failed!
    pause
    exit /b 1
)

echo.
if exist dist\PDF-to-Image-Converter.exe (
    echo ✓ Build completed successfully!
    echo ✓ Self-contained executable: dist\PDF-to-Image-Converter.exe
    echo.
    echo File information:
    dir dist\PDF-to-Image-Converter.exe
    echo.
    echo This executable includes all dependencies and requires no external software!
) else (
    echo ✗ Build failed - executable not found!
)

echo.
pause
