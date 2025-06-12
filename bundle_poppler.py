"""
Download and prepare Poppler for bundling with PyInstaller
"""
import os
import zipfile
import urllib.request
from pathlib import Path

def download_and_extract_poppler():
    """Download and extract Poppler for Windows bundling"""
    print("Downloading Poppler for Windows...")
    
    # Create poppler directory
    poppler_dir = Path("poppler")
    if poppler_dir.exists():
        print("Poppler directory already exists, skipping download...")
        return check_poppler_binaries()
    
    poppler_dir.mkdir(exist_ok=True)
    
    # Download Poppler (using a stable release)
    poppler_url = "https://github.com/oschwartz10612/poppler-windows/releases/download/v23.01.0-0/Release-23.01.0-0.zip"
    zip_path = "poppler.zip"
    
    try:
        print("Downloading from GitHub...")
        urllib.request.urlretrieve(poppler_url, zip_path)
        print("Downloaded Poppler successfully")
        
        # Extract the zip file
        print("Extracting Poppler...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(poppler_dir)
        
        print(f"Extracted Poppler to {poppler_dir}")
        
        # Clean up zip file
        os.remove(zip_path)
        
        return check_poppler_binaries()
            
    except Exception as e:
        print(f"Error downloading Poppler: {e}")
        return False

def check_poppler_binaries():
    """Check if Poppler binaries are available"""
    poppler_dir = Path("poppler")
    
    # Find the actual poppler path (it's usually in a subfolder)
    for item in poppler_dir.iterdir():
        if item.is_dir() and "poppler" in item.name.lower():
            bin_path = item / "Library" / "bin"
            if bin_path.exists():
                print(f"✓ Poppler binaries found at: {bin_path}")
                
                # List key executables
                executables = ["pdftoppm.exe", "pdftocairo.exe"]
                found_exes = []
                for exe in executables:
                    exe_path = bin_path / exe
                    if exe_path.exists():
                        found_exes.append(exe)
                
                if found_exes:
                    print(f"✓ Found executables: {', '.join(found_exes)}")
                    return True
                else:
                    print("✗ No Poppler executables found")
                    return False
    
    print("✗ Could not locate Poppler binaries")
    return False

if __name__ == "__main__":
    success = download_and_extract_poppler()
    if success:
        print("✓ Poppler ready for bundling!")
    else:
        print("✗ Failed to prepare Poppler")
        exit(1)
