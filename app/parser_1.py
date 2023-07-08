from bs4 import BeautifulSoup
import requests
from db.models.user import News
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from datetime import datetime, timedelta
def parser():
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
    }
    res = requests.get("https://mosday.ru/news/tags.php?metro", headers=headers)

    image = []
    head = []
    date = []
    tags = []

    soup = BeautifulSoup(res.text, "html.parser")

    for i in soup.find_all(cellpadding="0", cellspacing="10", border="0", style="font-family:Arial;font-size:15px"):
        for g in i.find_all(valign="top", width="90"):
            A = g.find(border="0", height="80")
            if A == None:
                image.append("None")
            else:
                image.append("https://mosday.ru/news/" + A.get("src"))
        for k in i.find_all("font", style="font-size:16px"):
            tags.append(k.find("a").get("href"))
            head.append(k.text)
        for j in i.find_all(face="Arial", size="2", color="#666666", style="font-size:13px"):
            date.append(j.text[0:16])


    date.reverse()
    image.reverse()
    head.reverse()
    tags.reverse()


    sassion_maker = sessionmaker(bind=create_engine("postgresql+psycopg://username:password@localhost:5432/database"))


    count = -1
    with sassion_maker() as session:
        for i in tags:
            count += 1
            g = False
            for j in session.query(News.id):
                if j[0] == i:
                    g = True
            if g == True:
                continue
            else:
                try:
                    datetime_object = datetime.strptime(date[count], "%d.%m.%Y %H:%M")
                    datetime_object = datetime_object - timedelta(hours=3)
                except ValueError:
                    datetime_object = None
                print(datetime_object)

                session.add(News(id=i, name=head[count], utl=image[count], date_of_hew=datetime_object))
                session.commit()


