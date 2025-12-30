import fitz  # PyMuPDF
import re

class ResumeParser:
    def __init__(self):
        pass

    def parse_pdf(self, source, is_stream=False):
        """
        Extract text from a PDF file or stream.
        """
        text = ""
        try:
            if is_stream:
                doc = fitz.open(stream=source, filetype="pdf")
            else:
                doc = fitz.open(source)
                
            for page in doc:
                text += page.get_text()
            return text
        except Exception as e:
            print(f"Error parsing PDF: {e}")
            return None

    def extract_contact_info(self, text):
        """
        Simple regex extraction for emails and phone numbers.
        """
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        phone_pattern = r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'
        
        emails = re.findall(email_pattern, text)
        phones = re.findall(phone_pattern, text)
        
        return {
            "emails": emails,
            "phones": phones
        }
