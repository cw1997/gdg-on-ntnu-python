import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook
import time

BASE_URL = "https://www.csie.ntnu.edu.tw"
LIST_URL = f"{BASE_URL}/index.php/news/"
HEADERS = {"User-Agent": "Mozilla/5.0"}

def get_news_list(page: int):
    """抓取列表頁新聞 (回傳 [(id, link, title, date, category)])"""
    url = LIST_URL
    if page > 1:
        url += f"page/{page}/"
    res = requests.get(url, headers=HEADERS, timeout=10)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "html.parser")

    items = []
    for article in soup.select("article"):
        # 連結
        a_tag = article.select_one("h2 a")
        if not a_tag:
            continue
        link = a_tag["href"]
        title = a_tag.get_text(strip=True)
        # id 從網址最後一段取
        news_id = link.rstrip("/").split("/")[-1]

        # 日期
        date_tag = article.select_one("time")
        date = date_tag.get_text(strip=True) if date_tag else ""

        # 分類
        cat_tag = article.select_one(".cat-links a")
        category = cat_tag.get_text(strip=True) if cat_tag else ""

        items.append((news_id, link, title, date, category))
    return items

def get_news_content(link: str):
    """抓取單篇新聞正文"""
    res = requests.get(link, headers=HEADERS, timeout=10)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "html.parser")
    content_div = soup.select_one("div.entry-content")
    return content_div.get_text("\n", strip=True) if content_div else ""

def crawl_all_news():
    all_news = []
    page = 1
    while True:
        items = get_news_list(page)
        if not items:  # 沒有資料表示到底
            break
        for news_id, link, title, date, category in items:
            print(f"[{page}] 抓取 {news_id} - {title}")
            content = get_news_content(link)
            all_news.append([news_id, date, category, title, content])
            time.sleep(0.5)  # 禮貌延遲
        page += 1
    return all_news

def save_to_excel(data, filename="csie_news.xlsx"):
    wb = Workbook()
    ws = wb.active
    ws.title = "News"
    ws.append(["ID", "日期", "分類", "標題", "正文"])
    for row in data:
        ws.append(row)
    wb.save(filename)

if __name__ == "__main__":
    news_data = crawl_all_news()
    save_to_excel(news_data)
    print(f"共抓取 {len(news_data)} 篇新聞，已儲存到 csie_news.xlsx")
