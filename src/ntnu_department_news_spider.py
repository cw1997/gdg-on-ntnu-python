import re

import requests
from bs4 import BeautifulSoup
import time

BASE_URL = "https://www.csie.ntnu.edu.tw"
LIST_URL = f"{BASE_URL}/index.php/news/"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"}

def get_news_list(page: int):
    """get all news slug(URL segment ) from news list page"""
    url = LIST_URL
    if page > 1:
        url += f"page/{page}/"
    res = requests.get(url, headers=HEADERS, timeout=10)
    res.raise_for_status()
    html = res.text
    soup = BeautifulSoup(html, "html.parser")

    items = []
    for article in soup.select(".blog-entry-inner"):
        a_tag = article.select_one("a")
        if not a_tag:
            continue
        text = a_tag.get_text(strip=True)
        link = a_tag["href"]
        news_id = link.rstrip("/").split("/")[-1]
        items.append((text, news_id))

    return items

def get_news_detail(slug: str):
    """get one news content from the news detail page, parameter 'slug' is the URL segment"""
    url = LIST_URL + slug
    res = requests.get(url, headers=HEADERS, timeout=10)
    res.raise_for_status()

    soup = BeautifulSoup(res.text, "html.parser")

    # title
    # title_soup = soup.select_one("div.entry-content p")
    # title_text = title_soup.get_text() if title_soup else ""

    # date
    date_soup = soup.select_one("li.meta-date")
    date_text = date_soup.get_text().replace("Post published:", "") if date_soup else ""

    # author
    author_soup = soup.select_one("li.meta-author")
    author_text = author_soup.get_text().replace("Post author:", "") if author_soup else ""

    # content
    content_soup = soup.select_one("div.entry-content")
    content_text = content_soup.get_text(separator="\n", strip=True) if content_soup else ""

    return date_text, author_text, content_text

def write_text_to_file(filename: str, text: str, mode: str = "w", encoding: str = "utf-8") -> None:
    """
    Write text to a file.

    :param filename: The name (or path) of the file.
    :param text: The content you want to write.
    :param mode: File open mode ("w" to overwrite, "a" to append).
    :param encoding: Text encoding, default is "utf-8".
    """
    # Open the file with the given mode and encoding
    with open("./news/" + sanitize_filename(filename), mode, encoding=encoding) as file:
        # Write the provided text into the file
        file.write(text)
    # After exiting the 'with' block, the file is automatically closed


def sanitize_filename(filename: str, replacement: str = "_") -> str:
    """
    Make a filename safe for most operating systems.

    :param filename: Original filename (may contain invalid characters)
    :param replacement: Character to replace invalid ones with
    :return: A safe filename string
    """
    # Define a set of characters not allowed on Windows and POSIX
    illegal_pattern = r'[<>:"/\\|?*\x00-\x1F]'
    safe = re.sub(illegal_pattern, replacement, filename)

    # Remove trailing dots and spaces (Windows restriction)
    safe = safe.rstrip(" .")

    # If the name becomes empty, use a default
    if not safe:
        safe = "untitled"

    return safe

if __name__ == "__main__":
    news_list = get_news_list(1)
    # print(news_list)

    # news_detail = get_news_detail("2025-09-09-2")

    for title_text, slug in news_list:
        print("start to crawl:", title_text, slug)
        date_text, author_text, content_text = get_news_detail(slug)
        print("title:", title_text)
        write_text_to_file(f"[{date_text}][{author_text}]{title_text}.txt", content_text)
        print("crawl done:", title_text, slug)
        time.sleep(1)  # polite delay
