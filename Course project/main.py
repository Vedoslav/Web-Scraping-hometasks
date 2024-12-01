import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time
from multiprocessing.dummy import Pool

"""This parser collects data about gouache paints from 4 Ukrainian websites, filters it, sorts by price and load to Excel file"""

def gouache():
    pd.set_option('max_colwidth', 120)
    pd.set_option('display.width', 500)
    
    start1 = time.time()
    artsklad_url = 'https://artsklad.ua/catalog/guash/brand-rosa/obem-500ml_280ml_100ml'
    response = requests.get(artsklad_url)
    with open('gouache1.html', 'w', encoding="utf-8") as f:
        f.write(response.text)
    with open('gouache1.html', 'r', encoding="utf-8") as f:
        text = f.read()
    soup = BeautifulSoup(text, 'lxml')
    data1 = []
    urls1 = []
    temp_urls = soup.find_all("a", {'class': 'product__title g_trigger'})
    for item in temp_urls:
        url = item.get('href')
        url = 'https://artsklad.ua/' + url
        urls1.append(url)
    with Pool(10) as p:
        data1 = p.map(artsklad_page, urls1)
    artsklad = pd.DataFrame(data = data1)
    end1 = time.time()
    print(f'Data from artsklad.ua has been parsed in {(end1-start1):.03f} sec')
    
    start2 = time.time()
    masterk_url = 'https://masterkisti.com.ua/catalog/guashevye-kraski.html?fabric%5B%5D=89&opt1%5B%5D=26&opt1%5B%5D=27&opt6%5B%5D=19&opt8%5B%5D=15&cena1=20&cena2=2145'    
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0'
    response = requests.get(masterk_url, headers={'user-agent': user_agent})
    with open('gouache1.html', 'w', encoding="utf-8") as f:
        f.write(response.text)
    with open('gouache1.html', 'r', encoding="utf-8") as f:
        text = f.read()
    soup = BeautifulSoup(text, 'lxml')
    data2 = []
    urls2 = []
    temp_urls = soup.find_all("div", {'class': 'cardname'})
    for item in temp_urls:
        url = item.find('a').get('href')
        url = 'https://masterkisti.com.ua' + url
        urls2.append(url)
    with Pool(10) as p:
        data2 = p.map(masterk_page, urls2)
    masterk = pd.DataFrame(data = data2) 
    end2 = time.time()
    print(f'Data from masterkisti.com.ua has been parsed in {(end2-start2):.03f} sec')
    
    start3 = time.time()
    kancmarket_url = 'https://kancmart.com.ua/kraski-guashevye/filter/brand=260;obem=10,30,39,60/'    
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0'
    response = requests.get(kancmarket_url, headers={'user-agent': user_agent})
    with open('gouache3.html', 'w', encoding="utf-8") as f:
        f.write(response.text)
    with open('gouache3.html', 'r', encoding="utf-8") as f:
        text = f.read()
    soup = BeautifulSoup(text, 'lxml')
    data3 = []
    urls3 = []
    temp_urls = soup.find_all("div", {'class': 'catalogCard-title'})
    for item in temp_urls:
        url = item.find('a').get('href')
        url = 'https://kancmart.com.ua' + url
        urls3.append(url)
    with Pool(10) as p:
        data3 = p.map(kancmarket_page, urls3)
    kancmarket = pd.DataFrame(data = data3)
    end3 = time.time()
    print(f'Data from kancmarket.com.ua has been parsed in {(end3-start3):.03f} sec')
    
    start4 = time.time()
    offprest_url = 'https://office-prestige.com.ua/ua/tvorchist-hobby/jivopis/farbi-guashovi/shopby/millilitr_tip-100ml-500ml-200ml-275ml/torg_marki-rosa-rosa_studio.html'    
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0'
    response = requests.get(offprest_url, headers={'user-agent': user_agent}, verify=False)
    with open('gouache4.html', 'w', encoding="utf-8") as f:
        f.write(response.text)
    with open('gouache4.html', 'r', encoding="utf-8") as f:
        text = f.read()
    soup = BeautifulSoup(text, 'lxml')
    data4 = []
    urls4 = []
    temp_urls = soup.find_all("h2", {'class': 'product-name product-name-height'})
    for item in temp_urls:
        url = item.find('a').get('href')
        urls4.append(url)
    with Pool(10) as p:
        data4 = p.map(offprest_page, urls4)
    offprestige = pd.DataFrame(data = data4) 
    end4 = time.time()
    print(f'Data from office-prestige.com.ua has been parsed in {(end4-start4):.03f} sec')
    
    start5 = time.time()
    
    #pattern to normalize different variants of price
    pattern = '(\d+\.\d+)|(\d+)' 
    
    #concatenate data from all websites in one DataFrame
    final_df = pd.concat([artsklad, masterk, kancmarket, offprestige], sort=False).reset_index(drop=True)
    
    #drop all items, which are unavailable to buy at the moment
    final_df = final_df.drop(final_df[(final_df.Status == "Немає в наявності") | (final_df.Status == "Наявність: Відсутній на складі") | (final_df.Status == 'None')].index).reset_index(drop=True)
    
    #normalize different variants of price in final DataFrame
    for index, row in final_df.iterrows():
        new_cell = re.search(pattern, row[1]).group(1)
        if not new_cell:
            new_cell = re.search(pattern, row[1]).group(0)
        row[1] = new_cell
        
    #change "Price"-column type to float and sort it from the lowest to the highest price
    final_df['Price'] = final_df['Price'].astype('float')
    final_df = final_df.sort_values(by='Price', ascending=True).reset_index(drop=True)
    
    final_df.to_excel('gouache.xlsx')
    display(final_df)
    end5 = time.time()
    print(f'Final dataframe has been formed and processed in {(end5-start5):.03f} sec')
        
def artsklad_page(url: str) -> dict:
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0'
    r = requests.get(url, headers={'user-agent': user_agent})
    soup = BeautifulSoup(r.text, 'lxml')       
    title = soup.find('h1', {'class': 'section__title section__title_big'}).text        
    price = soup.find('span', {'class': 'fn_price'}).text.strip()    
    try:
        status = soup.find('span', {'class': 'in_stock fn_in_stock'}).text
    except:
        status = soup.find('span', {'class': 'no_stock fn_not_stock'}).text
    return {'Title': title, 'Price': price, 'Status': status, 'URL': url}

def masterk_page(url: str) -> dict:
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0'
    r = requests.get(url, headers={'user-agent': user_agent})
    soup = BeautifulSoup(r.text, 'lxml')       
    title = soup.find('h1', {'itemprop': 'name'}).text        
    price = soup.find('span', {'class': 'pricecurrent'}).text.strip() 
    try:
        status = soup.find('div', {'class': 'isstock'}).text.strip() 
    except:
        status = 'None'
    return {'Title': title, 'Price': price, 'Status': status, 'URL': url}

def kancmarket_page(url: str) -> dict:
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0'
    r = requests.get(url, headers={'user-agent': user_agent})
    soup = BeautifulSoup(r.text, 'lxml')       
    title = soup.find('h1', {'class': 'product-title'}).text        
    price = soup.find('div', {'class': 'product-price__item'}).text.strip()
    try:
        status = soup.find('div', {'class': 'product-header__availability'}).text.strip()
    except:
        status = soup.find('div', {'class': 'product-header__availability product-header__availability--out-of-stock'}).text.strip()
    return {'Title': title, 'Price': price, 'Status': status, 'URL': url}

def offprest_page(url: str) -> dict:
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0'
    r = requests.get(url, headers={'user-agent': user_agent}, verify=False)
    soup = BeautifulSoup(r.text, 'lxml')       
    title = soup.find('h1').text
    try:
        price = soup.find('span', {'class': 'regular-price'}).text
    except:
        price = '0'
    try:
        status = soup.find('p', {'class': 'availability in-stock'}).text
    except:
        status = soup.find('p', {'class': 'availability out-of-stock'}).text
    return {'Title': title, 'Price': price, 'Status': status, 'URL': url}


if __name__ == '__main__':
    gouache()
