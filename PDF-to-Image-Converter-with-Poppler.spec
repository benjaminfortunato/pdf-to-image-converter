# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for PDF to Image Converter with bundled Poppler
"""
import os
from pathlib import Path

# Get the poppler path
poppler_path = Path("poppler")
poppler_binaries = []
poppler_data = []

# Find poppler binaries if they exist
if poppler_path.exists():
    print(f"Including Poppler from: {poppler_path}")
    
    for root, dirs, files in os.walk(poppler_path):
        for file in files:
            src = os.path.join(root, file)
            rel_path = os.path.relpath(src, poppler_path)
            
            # Include all files in poppler directory
            if file.endswith(('.exe', '.dll')):
                # Binaries go to poppler/bin or appropriate subdirectory
                poppler_binaries.append((src, f'poppler/{os.path.dirname(rel_path)}'))
            else:
                # Data files (configs, etc.)
                poppler_data.append((src, f'poppler/{os.path.dirname(rel_path)}'))
else:
    print("Warning: Poppler not found - building without bundled Poppler")

a = Analysis(
    ['pdf_to_image_gui.py'],
    pathex=[],
    binaries=poppler_binaries,
    datas=[('requirements.txt', '.')] + poppler_data,
    hiddenimports=['FreeSimpleGUI', 'pdf2image', 'PIL', 'PyPDF2'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='PDF-to-Image-Converter',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,  # Disable UPX to avoid antivirus issues
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='pdf_to_image.ico',  # Add custom icon
)
