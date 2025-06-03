<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# PDF to Image Converter

This project is a Python script that converts multipage PDFs to images. The script takes a PDF file as input and converts each page to an image with specified format (JPG/PNG), DPI, and output location.

Key requirements and functionality:
- Convert multipage PDFs to JPG or PNG images
- Allow setting image resolution in DPI
- Calculate DPI for each page based on page size
- Support different PDF sizes (from 2"x2" to 24"x26")
- Use naming format: [pdf_name]_[page_number].[format]
- Option to overwrite existing files
- Default behavior: 150 DPI JPG in the same directory as source PDF

The script should be designed to run locally first but be adaptable to AWS Lambda in the future.
