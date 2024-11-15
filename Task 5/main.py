import requests
import re
import itertools
import csv
import json
import xml.etree.ElementTree as ET
import sqlite3
   
def get_titles():    
    url = 'https://www.lejobadequat.com/emplois'
    resp = requests.get(url, headers={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0'})
    content = resp.text
    pattern = '<h3 class="jobCard_title m-0">(.+?)</h3>'
    titles = re.findall(pattern, content)
    pattern1 = '<a\shref="(https[a-z0-9\-\/\:\.]+)".+class="jobCard_link".+>'
    urls = re.findall(pattern1, content)
    data = [list(tup) for tup in zip(titles, urls)]
    return data
    
def write_csv(data: list) -> None:
    filename = 'output.csv'

    with open(filename, mode='w', newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(['Title', 'URL'])
        writer.writerows(data)
        
def write_json(data: list) -> None:
    filename = 'output.json'

    data = [
        {
            'Title': item[0],
            'URL': item[1]            
        }
        for item in data
    ]

    with open(filename, mode='w') as f:
        json.dump(data, f, indent=2)

def write_xml(data: list) -> None:
    filename = 'output.xml'

    root = ET.Element('Vacancies')
    for item in data:
        offer = ET.SubElement(root, 'Offers')
        ET.SubElement(offer, 'Title').text = item[0]
        ET.SubElement(offer, 'URL').text = item[1]
        
    tree = ET.ElementTree(root)
    tree.write(filename, encoding='utf-8', xml_declaration=True)    

def write_sql(data: list) -> None:
    filename = 'output.db'

    conn = sqlite3.connect(filename)
    cursor = conn.cursor()

    sql = """
        create table if not exists vacancies (
            id integer primary key,
            title text,
            url text            
        )
    """
    cursor.execute(sql)

    for item in data:
        cursor.execute("""
            insert into vacancies (title, url)
            values (?, ?)
        """, (item[0], item[1]))

    conn.commit()
    conn.close()    

def read_sql() -> None:
    filename = 'output.db'

    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    
    sql = """SELECT title, max(length(title)) as long_title FROM vacancies"""
    rows = cursor.execute(sql).fetchall()
    #print(rows)
    
    sql = """SELECT * FROM vacancies where title == 'Inventoriste  H/F' """
    rows = cursor.execute(sql).fetchall()
    print(rows)
    connection.close()

if __name__ == '__main__':
    get_titles()
    # write_csv(data)
    # write_json(data)
    # write_xml(data)
    # write_sql(data)
    # read_sql()
