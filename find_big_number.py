import tkinter as tk
from tkinter import filedialog


# Import your existing modules
from pdf_processor import PDFProcessor
import number_extraction as ne

def main():
    """
    Main function to run the program
    """
    # Create a Tkinter root window (but hide it)
    root = tk.Tk()
    root.withdraw()
    
    # Open file dialog to select a PDF
    pdf_path = filedialog.askopenfilename(
        title="Select a PDF file",
        filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
    )
    
    if not pdf_path:
        print("No file selected. Exiting.")
        return
    
    print(f"Analyzing: {pdf_path}")
    print("Processing PDF... (this may take a few moments)")
    
    # Process the PDF using your PDFProcessor class
    processor = PDFProcessor(pdf_path)
    processor.extract_text()
    
    print(f"Extracted {processor.get_page_count()} pages")
    print("Analyzing numbers...")
    
    # Find the largest numbers using the function from number_extraction
    results = ne.analyze_numbers(processor)
    
    # Clean up
    processor.close()
    
    # Print results
    print("\n=== RESULTS ===\n")
    
        # Print the results
    print("LARGEST RAW NUMBER:")
    print(f"Value: {results['largest_raw']['value']}")
    print(f"Original text: {results['largest_raw']['original']}")
    print(f"Page: {results['largest_raw']['page']}")
    print(f"Context: {results['largest_raw']['context'][:150]}...")

    print("\nLARGEST MODIFIED NUMBER:")
    print(f"Modified value: {results['largest_modified']['value']}")
    print(f"Raw value: {results['largest_modified']['raw_value']}")
    print(f"Original text: {results['largest_modified']['original']}")
    print(f"Page: {results['largest_modified']['page']}")
    print(f"Multiplier: {results['largest_modified']['multiplier']} ({results['largest_modified']['multiplier_value']})")
    print(f"Context: {results['largest_modified']['context'][:150]}...")


if __name__ == "__main__":
    main()