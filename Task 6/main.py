import re
import json
import requests
from bs4 import BeautifulSoup
import sqlite3

def parse_BS():
    url = 'https://www.bbc.com/sport'

    response = requests.get(url)
    with open('bbcsport.html', 'w', encoding="utf-8") as f:
        f.write(response.text)

    with open('bbcsport.html', 'r') as f:
        text = f.read()

    soup = BeautifulSoup(text, 'lxml')

    urls = []
    cards = soup.find_all("div", {'class': 'ssrcss-1f3bvyz-Stack e1y4nx260'})
    for card in cards[:5]:
        url = card.find('a').get('href')
        url = 'https://www.bbc.com' + url
        urls.append(url)
    result = []
    result1 = []
    for url in urls:        
        result.append(parse_page(url))
    result1 = [list(tup) for tup in zip([i["Link"] for i in result],([str(j["Topics"]) for j in result]))]
    with open('parse_BS.json', 'w') as f:
        json.dump(result, f, indent=2)
    return result1

    
def parse_page(url: str) -> dict:
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0'
    r = requests.get(url, headers={'user-agent': user_agent})

    if not r.ok:
        return {'Link': url, 'Topics': ''}

    soup = BeautifulSoup(r.text, 'lxml')

    pattern = 'sport\/(\w+)\/'
        
    topic = [item.text for item in soup.find_all('a', {'class': 'ssrcss-1ef12hb-StyledLink ed0g1kj0'})]        
    if len(topic) == 0:
        topic = re.findall(pattern, url)
        topic = topic[0].capitalize()
    return {'Link': url, 'Topics': topic}


def write_sql(result1: list) -> None:
    filename = 'parse_BS.db'
    conn = sqlite3.connect(filename)
    cursor = conn.cursor()
    sql = """
        create table if not exists sport_news (
            id integer primary key,
            url text,
            topic text            
        )
    """
    cursor.execute(sql)

    for item in result1:
        cursor.execute("""
            insert into sport_news(url, topic)
            values (?, ?)
        """, (item[0], item[1]))

    conn.commit()
    conn.close()

def read_sql() -> None:
    filename = 'parse_BS.db'

    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    
    sql = """SELECT * FROM sport_news"""
    rows = cursor.execute(sql).fetchall()
    print(rows)

if __name__ == '__main__':
    parse_BS()
    
    # write_csv(result1)

    # write_json()
