# PDF Number Finder

A tool to extract and identify the largest numbers in PDF documents, with intelligent context recognition for numerical modifiers.

## Overview

This project finds both the largest raw number and the largest contextually modified number in a PDF document. It's particularly useful for financial documents where numbers may be expressed in different scales (thousands, millions, billions) indicated by context.

## Features

- Extracts text from PDF documents
- Detects tables and their structures
- Recognizes numerical modifiers like "millions" or "billions" from context
- Identifies both raw and contextually-modified numbers
- Handles various number formats (with commas, decimals, scientific notation)
- Provides detailed context information for verification

## Installation

1. Clone this repository or download the source files
2. Install the required dependencies:

```bash
pip install -r requirements.txt

```

## File Structure

- `pdf_processor.py`: Contains the PDFProcessor class that handles PDF text extraction
- `number_extraction.py`: Contains functions for number extraction and context analysis
- `find_big_number.py`: Main script with file dialog and result presentation

## Usage

1. Run the main script:

```bash
python find_big_number.py
```

2. Select a PDF file when prompted by the file dialog
3. The script will process the document and display the results, showing:
   - The largest raw number found
   - The largest contextually modified number found
   - Page numbers for each
   - Context information including table titles if applicable

## How It Works

1. **PDF Processing**: Extracts text from each page of the PDF
2. **Table Detection**: Identifies tables and their boundaries within the document
3. **Number Extraction**: Finds all numbers and their positions in the text
4. **Context Analysis**: For each number:
   - Checks if it's within a table and identifies the table context
   - Looks for modifiers like "millions" or "billions" in the table title or headers
   - Checks surrounding text for context clues
5. **Modifier Application**: Applies appropriate multipliers based on context
6. **Result Reporting**: Returns both the largest raw number and the largest modified number with context


