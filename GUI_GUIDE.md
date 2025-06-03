# PDF to Image Converter - GUI Application Guide

## Overview

The PDF to Image Converter GUI provides a user-friendly interface for converting PDF files to high-quality images without requiring technical knowledge or command-line usage.

## Features

### User Interface
- **File Browser**: Easy PDF file selection with file dialog
- **Output Directory**: Choose where to save converted images
- **Format Selection**: Radio buttons for JPG or PNG output
- **DPI Setting**: Text input for custom resolution (50-2400 DPI)
- **Batch Processing**: Configure how many pages to process simultaneously
- **Progress Tracking**: Real-time progress bar and detailed logging
- **Error Handling**: Clear error messages and validation

### Conversion Options
- **Image Format**: Choose between JPG (smaller files) or PNG (lossless quality)
- **Resolution (DPI)**: Higher values = better quality but larger files
- **Batch Size**: Lower values use less memory for large PDFs
- **Timeout**: Maximum processing time per batch
- **Overwrite Protection**: Option to skip existing files or overwrite them

## How to Use

### Step 1: Select PDF File
1. Click the "Browse" button next to "Select PDF File"
2. Choose your PDF file from the file dialog
3. The file path will appear in the text field

### Step 2: Choose Output Location
- **Option A**: Check "Use same directory as PDF file" (default)
- **Option B**: Uncheck the box and browse to select a different output folder

### Step 3: Configure Settings
- **Image Format**: Select JPG (recommended for photos) or PNG (recommended for documents)
- **DPI**: Enter desired resolution (150 is good for screen viewing, 300+ for printing)
- **Batch Size**: Keep default (5) unless you have memory issues with large PDFs
- **Timeout**: Keep default (300 seconds) unless pages are very complex
- **Overwrite**: Check if you want to replace existing image files

### Step 4: Convert
1. Click "Convert PDF" to start the process
2. Watch the progress bar and log for updates
3. Click "Cancel" if you need to stop the conversion
4. When complete, find your images in the specified output directory

## Settings Guide

### DPI (Dots Per Inch) Recommendations
- **72-96 DPI**: Web viewing, email sharing
- **150 DPI**: General purpose, good quality/size balance
- **300 DPI**: Print quality, professional documents
- **600+ DPI**: High-resolution archival, large format printing

### Format Selection
- **JPG**: 
  - Smaller file sizes
  - Good for photos and complex images
  - Some quality loss (but usually imperceptible)
  - Faster processing
  
- **PNG**:
  - Larger file sizes
  - Perfect quality preservation
  - Best for text, line art, and simple graphics
  - Supports transparency

### Batch Size Guidelines
- **Large PDFs (100+ pages)**: Use 1-3 pages per batch
- **Standard PDFs (10-50 pages)**: Use 3-7 pages per batch
- **Small PDFs (1-10 pages)**: Use 5-10 pages per batch
- **High DPI conversions**: Use smaller batches regardless of PDF size

## Troubleshooting

### Common Issues

**"Poppler not found" Error**
- Install Poppler for Windows (see main README.md)
- Ensure poppler/bin is in your system PATH
- Restart the application after installation

**Memory Errors**
- Reduce batch size to 1-2 pages
- Lower the DPI setting
- Close other applications to free memory
- Try converting in smaller sections

**Slow Performance**
- Reduce batch size
- Lower DPI for testing
- Check if antivirus is scanning the output folder
- Ensure sufficient disk space

**Conversion Stops/Hangs**
- Increase timeout setting
- Check if the PDF file is corrupted
- Try a different PDF to isolate the issue
- Reduce batch size to 1 page

### Error Messages

**"Please select a PDF file"**
- You must choose a PDF file before converting

**"DPI must be between 50 and 2400"**
- Enter a valid number in the DPI field within the allowed range

**"Batch size must be between 1 and 50"**
- Enter a reasonable batch size number

**"Timeout must be between 30 and 3600 seconds"**
- Enter a timeout value between 30 seconds and 1 hour

## Performance Tips

### For Best Results
1. **Test with low DPI first**: Try 150 DPI to ensure everything works
2. **Check output quality**: Examine a few converted images before processing large batches
3. **Monitor disk space**: High DPI conversions can create very large files
4. **Use appropriate format**: JPG for photos, PNG for documents/diagrams

### For Large PDFs
1. **Start small**: Test with a few pages first
2. **Reduce batch size**: Use 1-2 pages per batch
3. **Increase timeout**: Allow more time for complex pages
4. **Monitor progress**: Watch the log for any error messages
5. **Be patient**: Large conversions can take significant time

## Output Information

### File Naming
- Format: `[original_pdf_name]_[page_number].[format]`
- Example: `manual.pdf` → `manual_1.jpg`, `manual_2.jpg`, etc.

### Log Information
The application provides detailed information including:
- PDF page dimensions in inches
- Resulting image dimensions in pixels
- Processing progress for each page
- Any errors or warnings encountered
- Total conversion time

## Building the Executable

### Prerequisites
- Python 3.7+ installed
- All dependencies installed (`pip install -r requirements.txt`)

### Build Steps
1. **Automatic Build**: Run `build_exe.bat` (Windows)
2. **Manual Build**: Run `pyinstaller pdf_converter.spec`
3. **Find Executable**: Check the `dist` folder for the .exe file

### Distribution
- The executable is self-contained and can be shared
- No Python installation required on target computers
- Include Poppler installation instructions for end users
- Consider creating an installer using the provided Inno Setup script

## Technical Notes

### Dependencies
- FreeSimpleGUI for the user interface
- pdf2image for PDF conversion
- Pillow for image processing
- PyPDF2 for PDF analysis
- Threading for non-blocking conversion

### Threading
- Conversion runs in a separate thread to keep the UI responsive
- Cancel functionality allows stopping long-running conversions
- Progress updates occur in real-time during conversion
