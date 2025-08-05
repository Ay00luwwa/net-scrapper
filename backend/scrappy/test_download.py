import os
import requests
from urllib.parse import urlparse

PDF_FOLDER = "pdfs"
os.makedirs(PDF_FOLDER, exist_ok=True)

def download_and_save_pdf(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()

        filename = os.path.basename(urlparse(url).path)
        if not filename.endswith(".pdf"):
            filename += ".pdf"

        filepath = os.path.join(PDF_FOLDER, filename)
        with open(filepath, "wb") as f:
            f.write(response.content)

        print(f"PDF saved to {filepath}")
    except Exception as e:
        print(f"Download failed: {e}")

# Test URL again
download_and_save_pdf("https://www.orimi.com/pdf-test.pdf")
