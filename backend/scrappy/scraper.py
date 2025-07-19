import requests
from bs4 import BeautifulSoup

# def scrape_url(url):
#     response = requests.get(url, timeout=10)
#     response.raise_for_status()
#     soup = BeautifulSoup(response.text, "html.parser")

#     # Example: return page title and all images
#     title = soup.title.string if soup.title else "No title found"
#     images = [img.get("src") for img in soup.find_all("img")]

#     return {"title": title, "images": images}

def scrape_url(url):
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    return {
        "title": soup.title.string if soup.title else None,
        "raw_html": response.text,
        "headings": [h.get_text(strip=True) for h in soup.find_all(['h1', 'h2', 'h3'])],
        "paragraphs": [p.get_text(strip=True) for p in soup.find_all('p')],
        "links": [a.get('href') for a in soup.find_all('a') if a.get('href')],
        "images": [img.get('src') for img in soup.find_all('img') if img.get('src')]
    }
