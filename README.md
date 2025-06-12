# PDF to Image Converter

A Python tool that converts multipage PDF files to high-quality images (JPG/PNG) with customizable resolution and output settings. Available as both a command-line script and a user-friendly GUI application.

## ✨ Latest Updates

- **🎨 Custom Icon**: Professional PDF-themed icon for Windows integration
- **📦 Self-Contained Builds**: Embedded Poppler binaries - no external dependencies required
- **🛡️ Antivirus Compatible**: Build process optimized for ESET and other antivirus software
- **💻 GUI v2.0**: Enhanced interface with bundled dependency detection

## Two Ways to Use

### 🖥️ GUI Application (Recommended for Non-Technical Users)
- **User-friendly interface** with file browsers and forms
- **No command-line knowledge required**
- **Real-time progress tracking** with detailed logging
- **Built-in validation** and error handling
- **Distributable as standalone .exe** file

Run the GUI: `python pdf_to_image_gui.py`

### ⌨️ Command-Line Script (For Advanced Users)
- **Powerful command-line interface** for automation
- **Batch processing capabilities**
- **Scriptable for automated workflows**
- **Integration with other tools and scripts**

Run the CLI: `python pdf_to_image.py document.pdf`

## Features

- Convert multipage PDFs to JPG or PNG images
- Specify output resolution in DPI
- Control output directory
- Option to overwrite existing files
- Page-specific DPI calculation based on page size
- Simple command-line interface

## Installation

1. Clone this repository or download the files.
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

This will install:
- pdf2image: For PDF to image conversion
- Pillow: For image processing  
- PyPDF2: For PDF analysis
- FreeSimpleGUI: For the graphical user interface (no registration required)

### Installing Poppler (Required)

The pdf2image library requires poppler to be installed as an external dependency:

**Windows:**
1. Download the latest poppler release from [here](https://github.com/oschwartz10612/poppler-windows/releases/)
2. Extract the ZIP file to a folder (e.g., `C:\Program Files\poppler`)
3. Add the `bin` folder to your PATH environment variable:
   - Go to Control Panel > System > Advanced System Settings > Environment Variables
   - Edit the PATH variable and add the path to the bin folder (e.g., `C:\Program Files\poppler\bin`)
   - Restart your terminal/command prompt for changes to take effect

**macOS:**
```bash
brew install poppler
```

**Linux:**
```bash
sudo apt-get install poppler-utils
```

## Usage

Basic usage:

```bash
python pdf_to_image.py path/to/your/document.pdf
```

This will convert the PDF to JPG images at 150 DPI and save them in the same directory as the PDF.

### Testing with a Sample PDF

If you don't have a PDF file for testing, you can create a simple one using a tool like Microsoft Word or Google Docs, or download a sample PDF from the web. 

For VS Code users, you can run the "Run PDF to Image Converter (Sample)" task if you have a file named `sample.pdf` in your project directory.

### Advanced Options

```bash
python pdf_to_image.py path/to/your/document.pdf --output-dir path/to/output --dpi 300 --format png --overwrite
```

Parameters:
- `pdf_path` (required): Path to the PDF file
- `--output-dir`: Output directory for images (default: same as PDF)
- `--dpi`: Output image DPI (default: 150)
- `--format`: Output image format, 'jpg' or 'png' (default: 'jpg')
- `--overwrite`: Overwrite existing files if they already exist

## GUI Application Usage

### Running the GUI
```bash
python pdf_to_image_gui.py
```

### GUI Features
- **File Selection**: Browse and select PDF files with a file dialog
- **Output Directory**: Choose destination folder or use PDF's directory
- **Format Options**: Radio buttons for JPG or PNG selection
- **Quality Settings**: DPI input with validation (50-2400)
- **Batch Processing**: Configure pages per batch for memory optimization
- **Progress Tracking**: Real-time progress bar and detailed conversion log
- **Error Handling**: Clear validation messages and error reporting
- **Cancel Option**: Stop conversion mid-process if needed

### Building Standalone Executable

Choose between two build options:

#### Self-Contained Build (Recommended for Distribution)
```bash
# Build with bundled Poppler (no external dependencies)
build_with_poppler.bat
```
- ✅ Includes Poppler binaries (~50-100MB)
- ✅ Works on any Windows machine
- ✅ No external dependencies needed
- ✅ Perfect for distribution to end users

#### Standard Build (Smaller Size)
```bash
# Install build dependencies
pip install -r requirements.txt

# Run the build script (Windows)
build.bat

# Or use PyInstaller directly
pyinstaller PDF-to-Image-Converter.spec
```
- ✅ Smaller file size (~20-30MB)
- ❌ Requires Poppler to be installed separately
- ❌ May show "poppler not found" errors

The executable will be created in the `dist` folder and can be distributed without requiring Python installation.

For detailed GUI usage instructions, see [GUI_GUIDE.md](GUI_GUIDE.md).

## Output Format

The images will be named as follows:
```
[pdf_filename]_[page_number].jpg
```

Example: For a PDF named "document.pdf", the images will be "document_1.jpg", "document_2.jpg", etc.

## AWS Lambda Adaptation

To adapt this script for AWS Lambda:

1. Create a Lambda function with Python runtime
2. Package the script and dependencies as a Lambda layer
3. Configure S3 triggers for PDF uploads
4. Adjust the script to read from S3 and write back to S3 instead of local filesystem

## License

MIT
