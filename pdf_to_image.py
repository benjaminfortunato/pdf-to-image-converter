#!/usr/bin/env python
# filepath: C:\Users\BenjaminFort_5rlaw0g\source\repos\utilities\pdf-to-image\pdf_to_image.py
import os
import argparse
import time
from pathlib import Path
from PyPDF2 import PdfReader
from pdf2image import convert_from_path
from pdf2image.exceptions import PDFPageCountError


def parse_arguments():
    parser = argparse.ArgumentParser(description='Convert PDF to images.')
    parser.add_argument('pdf_path', help='Path to the PDF file')
    parser.add_argument('--output-dir', help='Output directory for the images')
    parser.add_argument('--dpi', type=int, default=150, help='Image resolution in DPI (default: 150)')
    parser.add_argument('--format', choices=['jpg', 'png'], default='jpg', help='Image format (jpg or png)')
    parser.add_argument('--overwrite', action='store_true', help='Overwrite existing files')
    parser.add_argument('--batch-size', type=int, default=5, help='Number of pages to process at once (default: 5)')
    parser.add_argument('--timeout', type=int, default=300, help='Timeout per batch in seconds (default: 300)')
    return parser.parse_args()


def get_output_directory(pdf_path, output_dir=None):
    if output_dir:
        output_directory = Path(output_dir)
    else:
        # Default to the same directory as the PDF
        output_directory = Path(pdf_path).parent
    
    # Create the directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)
    
    return output_directory


def get_page_dimensions(pdf_path):
    """Get dimensions of each page in the PDF in points"""
    pdf_reader = PdfReader(pdf_path)
    dimensions = []
    
    for page in pdf_reader.pages:
        # Extract page dimensions in points (1/72 inch)
        width = page.mediabox.width
        height = page.mediabox.height
        dimensions.append((width, height))
    
    return dimensions


def display_page_info(page_dimensions, dpi):
    """Display page dimensions and resulting image size information"""
    print("\nPDF Page Information:")
    print("---------------------")
    
    for i, (width_pt, height_pt) in enumerate(page_dimensions):
        # Convert from points to inches (1 point = 1/72 inch)
        width_in = width_pt / 72
        height_in = height_pt / 72
        
        # Calculate resulting image dimensions in pixels
        width_px = int(width_in * dpi)
        height_px = int(height_in * dpi)
        
        print(f"Page {i+1}: {width_in:.2f}\" x {height_in:.2f}\" → {width_px} x {height_px} pixels at {dpi} DPI")


def convert_pdf_to_images(pdf_path, output_dir=None, dpi=150, format='jpg', overwrite=False, batch_size=5, timeout=300):
    """
    Convert PDF to images with improved handling for large files.
    
    Args:
        pdf_path: Path to the PDF file
        output_dir: Output directory for the images
        dpi: Image resolution in DPI
        format: Image format (jpg or png)
        overwrite: Whether to overwrite existing files
        batch_size: Number of pages to process at once
        timeout: Timeout per batch in seconds
    """
    start_time = time.time()
    
    try:
        # Get PDF information
        pdf_reader = PdfReader(pdf_path)
        page_count = len(pdf_reader.pages)
        page_dimensions = get_page_dimensions(pdf_path)
        
        # Get output directory
        output_directory = get_output_directory(pdf_path, output_dir)
        
        # Get file basename without extension for naming
        pdf_name = Path(pdf_path).stem
        
        # Display page dimensions and estimated image sizes
        display_page_info(page_dimensions, dpi)
        
        print(f"\nConverting PDF: {pdf_path}")
        print(f"Total pages: {page_count}")
        print(f"Format: {format}, DPI: {dpi}")
        print(f"Output directory: {output_directory}")
        print(f"Processing in batches of {batch_size} pages")
        
        # Process pages in batches to conserve memory
        for batch_start in range(0, page_count, batch_size):
            batch_end = min(batch_start + batch_size, page_count)
            
            print(f"\nProcessing pages {batch_start + 1}-{batch_end} of {page_count}...")
            
            # Process a batch of pages
            try:
                images = convert_from_path(
                    pdf_path,
                    dpi=dpi,
                    first_page=batch_start + 1,
                    last_page=batch_end,
                    timeout=timeout
                )
                
                # Save each image in the batch
                for i, image in enumerate(images):
                    page_num = batch_start + i + 1
                    output_filename = f"{pdf_name}_{page_num}.{format}"
                    output_path = output_directory / output_filename
                    
                    if os.path.exists(output_path) and not overwrite:
                        print(f"  Skipping page {page_num}: {output_filename} (already exists)")
                        continue
                    
                    # Save image with appropriate format settings
                    if format == 'jpg':
                        image.save(output_path, 'JPEG', quality=95, optimize=True)
                    else:  # png
                        image.save(output_path, 'PNG', optimize=True)
                    
                    print(f"  Saved page {page_num}: {output_filename}")
            
            except Exception as e:
                print(f"Error processing pages {batch_start + 1}-{batch_end}: {str(e)}")
                # Continue processing next batch even if this one failed
        
        total_time = time.time() - start_time
        print(f"\nConversion completed in {total_time:.1f} seconds")
        print(f"Images saved to: {output_directory}")
        
    except PDFPageCountError:
        print("Error: Could not determine the page count of the PDF. The file may be corrupted.")
        return 1
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1
    
    return 0


def main():
    args = parse_arguments()
    
    return convert_pdf_to_images(
        args.pdf_path,
        args.output_dir,
        args.dpi,
        args.format,
        args.overwrite,
        args.batch_size,
        args.timeout
    )


if __name__ == "__main__":
    exit(main())
