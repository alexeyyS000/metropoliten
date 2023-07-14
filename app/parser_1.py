from bs4 import BeautifulSoup
import requests
import re


def parse_latest_posts():
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
    }
    res = requests.get("https://mosday.ru/news/tags.php?metro", headers=headers)

    soup = BeautifulSoup(res.text, "html.parser")

    data = []

    for i in soup.select('table[width="95%"] tr'):
        try:
            tag = int(re.findall(r"\d+", i.find("font", style="font-size:16px").find("a").get("href"))[0])
            headline = i.find("font", style="font-size:16px").text
            image_url = i.find(valign="top", width="90").find(border="0", height="80")

            if image_url is not None:
                image_url = "https://mosday.ru/news/" + image_url.get("src")
            data.append({"tag": tag, "headline": headline, "url": image_url})
        except AttributeError:
            pass

    data.reverse()
    return data
