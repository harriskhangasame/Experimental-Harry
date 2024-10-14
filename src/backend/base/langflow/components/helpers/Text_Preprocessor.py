from langflow.custom import Component
from langflow.io import FileInput, Output
from langflow.schema.message import Message
import pandas as pd
import pypdf
import re
import os
import nltk

# Ensure required resources are available
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('punkt')
    nltk.download('wordnet')

from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer

class TextPreprocessingComponent(Component):
    display_name = "Text Preprocessor"
    description = "Processes text from .pdf and .csv files, applies cleaning, tokenization, and lemmatization."
    icon = "file-alt"
    name = "TextPreprocessor"
    
    inputs = [
        FileInput(
            name="input_file",
            display_name="Upload File",
            info="Upload a .pdf or .csv file for text processing.",
            file_types=["pdf", "csv"]
        ),
    ]

    outputs = [
        Output(display_name="Processed Text", name="processed_text", method="build_output"),
    ]

    async def build_output(self) -> Message:
        """Extracts, cleans, tokenizes, lemmatizes text, and returns it as a Message."""
        if not self.input_file:
            raise ValueError("Please, upload a valid .pdf or .csv file.")

        # Extract text based on file type
        file_extension = os.path.splitext(self.input_file)[1].lower()

        if file_extension == ".pdf":
            extracted_text = self.extract_text_from_pdf(self.input_file)
        elif file_extension == ".csv":
            extracted_text = self.extract_text_from_csv(self.input_file)
        else:
            raise ValueError("Unsupported file type. Please upload a .pdf or .csv file.")

        # Clean, tokenize, and lemmatize the extracted text
        cleaned_text = self.clean_text(extracted_text)
        tokenized_text = self.tokenize_text(cleaned_text)
        lemmatized_text = self.lemmatize_text(tokenized_text)

        return Message(text=lemmatized_text)

    def extract_text_from_pdf(self, file) -> str:
        """Extracts text from a PDF file using pypdf."""
        reader = pypdf.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()  # Extract text from each page
        return text

    def extract_text_from_csv(self, file) -> str:
        """Extracts text from a CSV file by concatenating all rows."""
        df = pd.read_csv(file)
        text = " ".join(df.astype(str).apply(" ".join, axis=1))
        return text

    def clean_text(self, text: str) -> str:
        """Cleans text by removing unwanted characters and normalizing spaces."""
        text = re.sub(r'\s+', ' ', text)  # Remove extra whitespace
        text = re.sub(r'[^\w\s]', ' ', text)  # Remove punctuation
        text = text.lower()  # Convert to lowercase
        return text.strip()

    def tokenize_text(self, text: str) -> list:
        """Tokenizes the text."""
        tokens = nltk.word_tokenize(text)
        return tokens

    def lemmatize_text(self, tokens: list) -> str:
        """Lemmatizes the tokens to their base form."""
        lemmatizer = WordNetLemmatizer()
        lemmatized_tokens = [lemmatizer.lemmatize(token) for token in tokens]
        return " ".join(lemmatized_tokens)
