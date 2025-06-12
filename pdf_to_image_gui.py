#!/usr/bin/env python3
"""
PDF to Image Converter - GUI Application
A user-friendly interface for converting PDF files to images.
"""

import os
import sys
import threading
import time
from pathlib import Path
import FreeSimpleGUI as sg
from pdf_to_image import convert_pdf_to_images, get_page_dimensions

def get_poppler_path():
    """Get the path to bundled Poppler or system Poppler"""
    if getattr(sys, 'frozen', False):
        # Running as PyInstaller bundle
        bundle_dir = Path(sys._MEIPASS)
        poppler_path = bundle_dir / "poppler" / "bin"
        if poppler_path.exists():
            return str(poppler_path)
    
    # Check if poppler is in the script directory (for development)
    script_dir = Path(__file__).parent
    local_poppler = script_dir / "poppler"
    for item in local_poppler.iterdir() if local_poppler.exists() else []:
        if item.is_dir() and "poppler" in item.name.lower():
            bin_path = item / "Library" / "bin"
            if bin_path.exists():
                return str(bin_path)
    
    # Return None to use system PATH
    return None

# Set PySimpleGUI theme
sg.theme('LightBlue3')

class PDFConverterGUI:
    def __init__(self):
        self.window = None
        self.conversion_thread = None
        self.cancel_conversion = False
        
    def create_layout(self):
        """Create the GUI layout"""
        
        # File selection section
        file_frame = [
            [sg.Text('Select PDF File:', font=('Arial', 10, 'bold'))],
            [sg.Input(key='-PDF_FILE-', size=(50, 1), readonly=True),
             sg.FileBrowse('Browse', file_types=(("PDF Files", "*.pdf"),), size=(8, 1))],
            [sg.Text('Output Directory:', font=('Arial', 10, 'bold'))],
            [sg.Input(key='-OUTPUT_DIR-', size=(50, 1)),
             sg.FolderBrowse('Browse', size=(8, 1))],
            [sg.Checkbox('Use same directory as PDF file', key='-SAME_DIR-', default=True, 
                        enable_events=True)]
        ]
        
        # Conversion settings section
        settings_frame = [
            [sg.Text('Conversion Settings:', font=('Arial', 10, 'bold'))],
            [sg.Text('Image Format:'), 
             sg.Radio('JPG', 'FORMAT', key='-JPG-', default=True),
             sg.Radio('PNG', 'FORMAT', key='-PNG-')],
            [sg.Text('DPI (Resolution):'), 
             sg.Input('150', key='-DPI-', size=(10, 1)),
             sg.Text('(Higher = better quality, larger files)')],
            [sg.Text('Batch Size:'), 
             sg.Input('5', key='-BATCH_SIZE-', size=(10, 1)),
             sg.Text('(Pages processed at once - lower for large PDFs)')],
            [sg.Text('Timeout (seconds):'), 
             sg.Input('300', key='-TIMEOUT-', size=(10, 1)),
             sg.Text('(Maximum time per batch)')],
            [sg.Checkbox('Overwrite existing files', key='-OVERWRITE-', default=False)]
        ]
        
        # Progress section
        progress_frame = [
            [sg.Text('Progress:', font=('Arial', 10, 'bold'))],
            [sg.ProgressBar(100, orientation='h', size=(50, 20), key='-PROGRESS-')],
            [sg.Text('Ready to convert...', key='-STATUS-', size=(60, 1))],
            [sg.Multiline('', key='-OUTPUT-', size=(70, 10), 
                         autoscroll=True, disabled=True, background_color='white')]
        ]
        
        # Buttons section
        button_frame = [
            [sg.Button('Convert PDF', key='-CONVERT-', size=(12, 1), button_color=('white', 'green')),
             sg.Button('Cancel', key='-CANCEL-', size=(12, 1), disabled=True),
             sg.Button('Clear Log', key='-CLEAR-', size=(12, 1)),
             sg.Button('Exit', key='-EXIT-', size=(12, 1))]
        ]
        
        # Main layout
        layout = [
            [sg.Frame('File Selection', file_frame, font=('Arial', 9), expand_x=True)],
            [sg.Frame('Settings', settings_frame, font=('Arial', 9), expand_x=True)],
            [sg.Frame('Progress', progress_frame, font=('Arial', 9), expand_x=True)],
            [sg.Frame('Actions', button_frame, font=('Arial', 9), expand_x=True)]
        ]
        
        return layout
    
    def create_window(self):
        """Create the main window"""
        layout = self.create_layout()
        
        # Try to find the icon file
        icon_path = None
        if os.path.exists('pdf_to_image.ico'):
            icon_path = 'pdf_to_image.ico'
        elif getattr(sys, 'frozen', False):
            # Check if icon is bundled in executable
            bundle_dir = Path(sys._MEIPASS)
            bundled_icon = bundle_dir / 'pdf_to_image.ico'
            if bundled_icon.exists():
                icon_path = str(bundled_icon)
        
        self.window = sg.Window(
            'PDF to Image Converter v2.0',
            layout,
            finalize=True,
            resizable=True,
            icon=icon_path,  # Use custom icon
            location=(100, 100)
        )
        
        # Set initial state
          # Set initial state
        self.window['-OUTPUT_DIR-'].update(disabled=True)
        self.window.Element('-OUTPUT_DIR-').Widget.configure(state='disabled')
          # Check and display Poppler status
        poppler_path = get_poppler_path()
        if poppler_path:
            status_msg = "✓ Bundled Poppler detected - no external dependencies needed\n"
        else:
            status_msg = "ℹ Using system Poppler (must be installed separately)\n"
        
        self.window['-OUTPUT-'].update(status_msg)
        
    def validate_inputs(self, values):
        """Validate user inputs"""
        errors = []
        
        # Check PDF file
        if not values['-PDF_FILE-']:
            errors.append("Please select a PDF file")
        elif not os.path.isfile(values['-PDF_FILE-']):
            errors.append("Selected PDF file does not exist")
        
        # Check output directory
        if not values['-SAME_DIR-'] and not values['-OUTPUT_DIR-']:
            errors.append("Please specify an output directory or use same directory as PDF")
        
        # Check DPI
        try:
            dpi = int(values['-DPI-'])
            if dpi < 50 or dpi > 2400:
                errors.append("DPI must be between 50 and 2400")
        except ValueError:
            errors.append("DPI must be a valid number")
        
        # Check batch size
        try:
            batch_size = int(values['-BATCH_SIZE-'])
            if batch_size < 1 or batch_size > 50:
                errors.append("Batch size must be between 1 and 50")
        except ValueError:
            errors.append("Batch size must be a valid number")
        
        # Check timeout
        try:
            timeout = int(values['-TIMEOUT-'])
            if timeout < 30 or timeout > 3600:
                errors.append("Timeout must be between 30 and 3600 seconds")
        except ValueError:
            errors.append("Timeout must be a valid number")
        
        return errors
    
    def update_output(self, message):
        """Update the output log"""
        if self.window:
            current_text = self.window['-OUTPUT-'].get()
            timestamp = time.strftime('%H:%M:%S')
            new_text = f"[{timestamp}] {message}\n"
            self.window['-OUTPUT-'].update(current_text + new_text)
            self.window.refresh()
    
    def update_status(self, message):
        """Update the status line"""
        if self.window:
            self.window['-STATUS-'].update(message)
            self.window.refresh()
    
    def update_progress(self, percentage):
        """Update the progress bar"""
        if self.window:
            self.window['-PROGRESS-'].update(percentage)
            self.window.refresh()
    
    def conversion_worker(self, pdf_path, output_dir, dpi, img_format, overwrite, batch_size, timeout):
        """Worker function for PDF conversion in a separate thread"""
        try:
            self.update_output(f"Starting conversion of: {os.path.basename(pdf_path)}")
            self.update_output(f"Output directory: {output_dir}")
            self.update_output(f"Settings: {img_format.upper()}, {dpi} DPI, batch size {batch_size}")
            
            # Get PDF info first
            try:
                page_dimensions = get_page_dimensions(pdf_path)
                total_pages = len(page_dimensions)
                self.update_output(f"PDF has {total_pages} pages")
                
                # Display page info
                for i, (width_pt, height_pt) in enumerate(page_dimensions[:5]):  # Show first 5 pages
                    width_in = width_pt / 72
                    height_in = height_pt / 72
                    width_px = int(width_in * dpi)
                    height_px = int(height_in * dpi)
                    self.update_output(f"Page {i+1}: {width_in:.1f}\"×{height_in:.1f}\" → {width_px}×{height_px}px")
                
                if total_pages > 5:
                    self.update_output(f"... and {total_pages - 5} more pages")
                
            except Exception as e:
                self.update_output(f"Error reading PDF info: {str(e)}")
                total_pages = 1  # Fallback
            
            # Custom conversion with progress updates
            self.convert_with_progress(pdf_path, output_dir, dpi, img_format, overwrite, batch_size, timeout, total_pages)
            
        except Exception as e:
            self.update_output(f"Error during conversion: {str(e)}")
            self.update_status("Conversion failed!")
        finally:
            # Re-enable convert button and disable cancel
            if self.window:
                self.window['-CONVERT-'].update(disabled=False)
                self.window['-CANCEL-'].update(disabled=True)
    
    def convert_with_progress(self, pdf_path, output_dir, dpi, img_format, overwrite, batch_size, timeout, total_pages):
        """Convert PDF with progress updates"""
        from pdf2image import convert_from_path
        from PIL import Image
        
        # Get PDF base name
        pdf_name = Path(pdf_path).stem
        fmt = img_format.lower()
        save_format = "JPEG" if fmt == "jpg" else "PNG"
        file_ext = f".{fmt}"
        
        # Process pages in batches
        pages_processed = 0
        
        for batch_start in range(0, total_pages, batch_size):
            if self.cancel_conversion:
                self.update_output("Conversion cancelled by user")
                self.update_status("Conversion cancelled")
                return
            
            batch_end = min(batch_start + batch_size, total_pages)
            
            self.update_output(f"Processing pages {batch_start + 1}-{batch_end} of {total_pages}...")
            self.update_status(f"Processing pages {batch_start + 1}-{batch_end} of {total_pages}")
            
            try:
                # Convert batch
                images = convert_from_path(
                    pdf_path,
                    dpi=dpi,
                    first_page=batch_start + 1,
                    last_page=batch_end,
                    timeout=timeout
                )
                
                # Save each image in the batch
                for i, image in enumerate(images):
                    if self.cancel_conversion:
                        return
                    
                    page_num = batch_start + i + 1
                    output_filename = f"{pdf_name}_{page_num}{file_ext}"
                    output_path = Path(output_dir) / output_filename
                    
                    if os.path.exists(output_path) and not overwrite:
                        self.update_output(f"Skipping page {page_num}: {output_filename} (already exists)")
                        continue
                    
                    # Save image
                    if fmt == 'jpg':
                        image.save(output_path, save_format, quality=95, optimize=True)
                    else:  # png
                        image.save(output_path, save_format, optimize=True)
                    
                    pages_processed += 1
                    progress = int((pages_processed / total_pages) * 100)
                    self.update_progress(progress)
                    self.update_output(f"Saved page {page_num}: {output_filename}")
            
            except Exception as e:
                self.update_output(f"Error processing pages {batch_start + 1}-{batch_end}: {str(e)}")
                continue
        
        if not self.cancel_conversion:
            self.update_output(f"Conversion completed! {pages_processed} pages converted.")
            self.update_status("Conversion completed successfully!")
            self.update_progress(100)
        
    def run(self):
        """Main application loop"""
        self.create_window()
        
        while True:
            event, values = self.window.read(timeout=100)
            
            if event in (sg.WIN_CLOSED, '-EXIT-'):
                break
            
            elif event == '-SAME_DIR-':
                # Toggle output directory input
                disabled = values['-SAME_DIR-']
                self.window['-OUTPUT_DIR-'].update(disabled=disabled)
                if disabled:
                    self.window['-OUTPUT_DIR-'].update('')
            
            elif event == '-CONVERT-':
                # Validate inputs
                errors = self.validate_inputs(values)
                if errors:
                    sg.popup_error('Input Errors:\n\n' + '\n'.join(errors), title='Validation Error')
                    continue
                
                # Get conversion parameters
                pdf_path = values['-PDF_FILE-']
                
                if values['-SAME_DIR-']:
                    output_dir = os.path.dirname(pdf_path)
                else:
                    output_dir = values['-OUTPUT_DIR-']
                
                dpi = int(values['-DPI-'])
                img_format = 'jpg' if values['-JPG-'] else 'png'
                overwrite = values['-OVERWRITE-']
                batch_size = int(values['-BATCH_SIZE-'])
                timeout = int(values['-TIMEOUT-'])
                
                # Reset progress and status
                self.update_progress(0)
                self.update_status("Starting conversion...")
                self.cancel_conversion = False
                
                # Disable convert button and enable cancel
                self.window['-CONVERT-'].update(disabled=True)
                self.window['-CANCEL-'].update(disabled=False)
                
                # Start conversion in separate thread
                self.conversion_thread = threading.Thread(
                    target=self.conversion_worker,
                    args=(pdf_path, output_dir, dpi, img_format, overwrite, batch_size, timeout)
                )
                self.conversion_thread.daemon = True
                self.conversion_thread.start()
            
            elif event == '-CANCEL-':
                # Cancel ongoing conversion
                self.cancel_conversion = True
                self.update_status("Cancelling conversion...")
                self.window['-CANCEL-'].update(disabled=True)
            
            elif event == '-CLEAR-':
                # Clear the output log
                self.window['-OUTPUT-'].update('')
                self.update_progress(0)
                self.update_status("Ready to convert...")
        
        self.window.close()

def main():
    """Main entry point for the GUI application"""
    try:
        app = PDFConverterGUI()
        app.run()
    except Exception as e:
        sg.popup_error(f'Application Error:\n\n{str(e)}', title='Error')
        sys.exit(1)

if __name__ == '__main__':
    main()
