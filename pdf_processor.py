import pymupdf  # PyMuPDF
import pymupdf4llm

class PDFProcessor:
    """
    Handles PDF document processing and text extraction using pymupdf4llm,
    converting each page to markdown format.
    """
    
    def __init__(self, pdf_path):
        """
        Initialize the PDF processor with the path to the PDF file.
        
        Args:
            pdf_path (str): Path to the PDF file to process
        """
        self.pdf_path = pdf_path
        self.pages = []  # Will store markdown for each page
        self.page_count = 0
        self.document = None
    
    def extract_text(self):
        """
        Extract text from all pages in the PDF using pymupdf4llm's markdown conversion.
        
        Returns:
            list: List of markdown strings, one for each page
        """
        
        
        try:
            # Open the document
            self.document = pymupdf.open(self.pdf_path)
            self.page_count = len(self.document)
            
            # Extract markdown page by page
            for page_num in range(self.page_count):
                
                # Convert page to markdown using pymupdf4llm
                markdown = pymupdf4llm.to_markdown(self.pdf_path, pages = [page_num])
                self.pages.append(markdown)
            
            return self.pages
            
        except Exception as e:
            print(f"Error extracting text from PDF: {e}")
            return []
    
    def get_page_text(self, page_num):
        """
        Get the extracted markdown for a specific page.
        
        Args:
            page_num (int): The page number (0-indexed)
            
        Returns:
            str: The markdown content of the page
        """
        if 0 <= page_num < len(self.pages):
            return self.pages[page_num]
        return ""
    
    def get_all_text(self):
        """
        Get all extracted markdown concatenated into a single string.
        
        Returns:
            str: All markdown from the PDF
        """
        return "\n\n".join(self.pages)
    
    def get_page_count(self):
        """
        Get the total number of pages in the document.
        
        Returns:
            int: Number of pages
        """
        return self.page_count
    

    
    def close(self):
        """
        Close the document to free resources.
        """
        if self.document:
            self.document.close()