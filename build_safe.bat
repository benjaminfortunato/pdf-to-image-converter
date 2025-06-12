@echo off
echo PDF to Image Converter - Antivirus-Safe Build
echo =============================================

echo.
echo IMPORTANT: Before building, please:
echo 1. Add this folder to your antivirus exclusions
echo 2. Temporarily disable real-time protection (if possible)
echo 3. Press any key when ready...
pause

echo.
echo Cleaning previous builds thoroughly...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist __pycache__ rmdir /s /q __pycache__

echo.
echo Installing dependencies...
pip install -r requirements.txt

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
echo (This may trigger antivirus warnings - please allow)
pyinstaller PDF-to-Image-Converter-with-Poppler.spec

if %ERRORLEVEL% NEQ 0 (
    echo Build failed! This might be due to antivirus interference.
    echo Please check your antivirus logs and add exclusions.
    pause
    exit /b 1
)

echo.
if exist dist\PDF-to-Image-Converter.exe (
    echo ✓ Build completed successfully!
    echo ✓ Self-contained executable: dist\PDF-to-Image-Converter.exe
    echo.
    echo Testing the executable...
    echo If this hangs, your antivirus may be scanning it.
    
    timeout /t 2 /nobreak >nul
    .\dist\PDF-to-Image-Converter.exe --help >nul 2>&1
    
    if %ERRORLEVEL% EQU 0 (
        echo ✓ Executable test passed!
    ) else (
        echo ⚠ Executable test failed - may need antivirus exclusion
    )
    
    echo.
    echo File information:
    dir dist\PDF-to-Image-Converter.exe
    echo.
    echo Remember to add 'dist\PDF-to-Image-Converter.exe' to antivirus exclusions
    echo if you plan to distribute this executable.
) else (
    echo ✗ Build failed - executable not found!
    echo Check for antivirus interference in build process.
)

echo.
pause
