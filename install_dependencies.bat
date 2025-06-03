@echo off
echo PDF to Image Converter - Installation Script
echo ==========================================

echo.
echo Installing dependencies...
pip install pdf2image Pillow PyPDF2 pyinstaller

echo.
echo Installing PySimpleGUI from private server...
python -m pip install --extra-index-url https://PySimpleGUI.net/install PySimpleGUI

echo.
echo Installation complete!
echo.
echo To run the GUI application: python pdf_to_image_gui.py
echo To run the command-line version: python pdf_to_image.py [pdf_file]
echo.
pause
