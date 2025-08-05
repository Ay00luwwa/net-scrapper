import requests
from bs4 import BeautifulSoup
import fitz  # PyMuPDF
import os
from urllib.parse import urlparse, urljoin

PDF_FOLDER = "pdfs"
os.makedirs(PDF_FOLDER, exist_ok=True)


def download_and_save_pdf(url):
    try:
        print(f"Downloading: {url}")
        response = requests.get(url)
        response.raise_for_status()
        filename = os.path.basename(urlparse(url).path)
        if not filename.endswith(".pdf"):
            filename += ".pdf"
        filepath = os.path.join(PDF_FOLDER, filename)

        with open(filepath, "wb") as f:
            f.write(response.content)

        print(f"Saved to: {filepath}")
        return filepath
    except Exception as e:
        print(f"Failed to download: {e}")
        return None


def extract_text_from_pdf(file_path):
    try:
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    except Exception as e:
        return f"Failed to extract: {e}"


def scrape_url(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    MAX_PDFS = 5

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        all_links = [a.get('href') for a in soup.find_all('a') if a.get('href')]

        # Normalize PDF URLs
        pdf_links = []
        for link in all_links:
            if link.lower().endswith('.pdf'):
                full_url = urljoin(url, link)
                pdf_links.append(full_url)

        limited_pdfs = pdf_links[:MAX_PDFS]
        pdf_texts = {}

        for pdf_url in limited_pdfs:
            file_path = download_and_save_pdf(pdf_url)
            if file_path:
                pdf_texts[pdf_url] = extract_text_from_pdf(file_path)

        return {
            "title": soup.title.string if soup.title else None,
            "raw_html": response.text,
            "headings": [h.get_text(strip=True) for h in soup.find_all(['h1', 'h2', 'h3'])],
            "paragraphs": [p.get_text(strip=True) for p in soup.find_all('p')],
            "links": all_links,
            "images": [img.get('src') for img in soup.find_all('img') if img.get('src')],
            "pdfs": limited_pdfs,
            "pdf_texts": pdf_texts
        }

    except Exception as e:
        print(f"Failed to scrape {url}: {e}")
        return {}
