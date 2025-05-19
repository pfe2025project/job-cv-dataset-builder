import requests
from bs4 import BeautifulSoup


def scrape_full_description(url):

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Referer": "https://www.google.com/",
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        # response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")

        outer = soup.find("div", class_="ui-foreign-click-description-canvas mb-8")
        inner = outer.find("div", class_="ui-foreign-click-description") if outer else None
        section = inner.find("section", class_="adp-body mx-4 text-sm md:mx-0 md:text-base") if inner else None

        if section:
            return section.get_text(separator="\n", strip=True)
        else:
            return "❌ Could not find the full job description."
    except Exception as e:
        return f"❌ Error: {e}"





