# download_nltk_data.py
import nltk

def download_nltk_resources():
    """Download necessary NLTK resources."""
    nltk.download('punkt')
    nltk.download('wordnet')

if __name__ == "__main__":
    download_nltk_resources()
