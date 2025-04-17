import requests
from bs4 import BeautifulSoup
import time
import random


def scrape_full_description(url):
    # List of user agents to choose from
    USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        # Add more user agents as needed
    ]
    
    # Randomly select a user agent from the list
    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Referer": "https://www.google.com/",
        "DNT": "1",  # Do Not Track header
        "Upgrade-Insecure-Requests": "1",
    }

    try:
        # Sleep randomly between 1.5s and 3.5s to avoid hitting server too fast
        time.sleep(random.uniform(1.5, 3.5))
        
        # Make the request with the selected user-agent
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")

        # Navigate to the outermost container
        outer_div = soup.find("div", class_="ui-foreign-click-description-canvas mb-8")
        if not outer_div:
            return "❌ Outer container not found"

        # Then the middle div
        inner_div = outer_div.find("div", class_="ui-foreign-click-description")
        if not inner_div:
            return "❌ Inner container not found"

        # Then the actual job description section
        section = inner_div.find("section", class_="adp-body mx-4 text-sm md:mx-0 md:text-base")
        if not section:
            return "❌ Description section not found"
        
        return section.get_text(separator="\n", strip=True)

    except requests.exceptions.RequestException as req_err:
        return f"❌ Request error: {req_err}"
    except Exception as e:
        return f"❌ General error: {e}"
