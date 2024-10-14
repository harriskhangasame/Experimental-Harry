from langflow.custom import Component
from langflow.io import FileInput, Output
from pathlib import Path
import pypdf
from docx import Document
import pytesseract
from PIL import Image
from langflow.schema.message import Message  # Import Message

# Set the path to Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'  # Adjust as necessary

class TextExtractorComponent(Component):
    display_name = "Text Extractor"
    description = "Extracts text from various file types (PDF, DOCX, TXT, Images)."
    icon = "file-text"
    name = "TextExtractor"

    inputs = [
        FileInput(
            name="file_path",
            display_name="Document File",
            file_types=["pdf", "jpg", "jpeg", "png", "txt", "docx"],  # Supported file types
            info="Upload a PDF, image, docx, or text file to extract text."
        ),
    ]

    outputs = [
        Output(display_name="Extracted Data", name="extracted_data", method="build_output"),
    ]

    async def build_output(self) -> Message:
        """Processes the uploaded file and returns the extracted text as a Message object."""
        if not self.file_path:
            raise ValueError("Please, upload a file to extract text.")

        # Resolve the file path
        resolved_path = self.resolve_path(self.file_path)
        extension = Path(resolved_path).suffix[1:].lower()

        # Extract text based on the file type
        if extension == "pdf":
            extracted_text = self.extract_text_from_pdf(resolved_path)
        elif extension == "docx":
            extracted_text = self.extract_text_from_docx(resolved_path)
        elif extension == "txt":
            extracted_text = self.extract_text_from_txt(resolved_path)
        elif extension in ["jpg", "jpeg", "png"]:
            extracted_text = self.extract_text_from_image(resolved_path)
        else:
            raise ValueError(f"Unsupported file type: {extension}. Only PDF, DOCX, TXT, and images are supported.")
        
        # Return extracted text as a Message object
        return Message(text=extracted_text)

    def extract_text_from_pdf(self, pdf_path):
        """Extract text from a PDF file using pypdf."""
        extracted_text = ""
        try:
            with open(pdf_path, 'rb') as file:
                reader = pypdf.PdfReader(file)
                for page in reader.pages:
                    extracted_text += page.extract_text() or ""
        except Exception as e:
            extracted_text = f"Error processing PDF: {str(e)}"
        return extracted_text

    def extract_text_from_docx(self, docx_path):
        """Extract text from a DOCX file."""
        extracted_text = ""
        try:
            doc = Document(docx_path)
            for paragraph in doc.paragraphs:
                extracted_text += paragraph.text + "\n"
        except Exception as e:
            extracted_text = f"Error processing DOCX: {str(e)}"
        return extracted_text

    def extract_text_from_txt(self, txt_path):
        """Extract text from a TXT file."""
        extracted_text = ""
        try:
            with open(txt_path, 'r', encoding="utf-8") as file:
                extracted_text = file.read()
        except Exception as e:
            extracted_text = f"Error processing TXT file: {str(e)}"
        return extracted_text

    def extract_text_from_image(self, image_path):
        """Extract text from an image using OCR."""
        extracted_text = ""
        try:
            image = Image.open(image_path)
            extracted_text = pytesseract.image_to_string(image)
        except Exception as e:
            extracted_text = f"Error processing image: {str(e)}"
        return extracted_text

