""" Цей скрипт чомусь працює лише для однієї сторінки, не вдається пропустити його через цикл (як у випадку з простим списком вакансій), 
щоб він охоплював одразу кілька сторінок. """

import requests
import re
import itertools
import pprint

   
def get_titles():
    titles_gen = [] 
    data = []     
    payload = {
        "action": "facetwp_refresh",
        "data": {
            "facets": {
                "recherche": [],
                "ou": [],
                "type_de_contrat": [],
                "fonction": [],
                "load_more": [
                    2
                ]
            },
            "frozen_facets": {
                "ou": "hard"
            },
            "http_params": {
                "get": [],
                "uri": "emplois",
                "url_vars": []
            },
            "template": "wp",
            "extras": {
                "counts": True,
                "sort": "default"
            },
            "soft_refresh": 1,
            "is_bfcache": 1,
            "first_load": 0,
            "paged": 1
        }} 
    response = requests.post('https://www.lejobadequat.com/emplois', json=payload)
    content = response.json()['template']
    pattern = '<h3 class="jobCard_title m-0">.+</h3>'
    page = re.findall(pattern, content)
    for idx, item in enumerate(page):
        if '<h3 class="jobCard_title m-0">' in item:
            item = item.replace('<h3 class="jobCard_title m-0">', '')
            item = item.replace('</h3>', '')
            page[idx] = item
    titles_gen = titles_gen + page
    pattern1 = '<a.+class="jobCard_link".+>'
    pattern2 = 'https[a-z0-9\-\/\:\.]+'
    urls = re.findall(pattern1, content)
    urls = str(urls)
    list2 = re.findall(pattern2, urls)
    for list_it, title in zip(list2, titles_gen):
        data.append({
            'title' : title,
            'url': list_it
            })
    with open("titles.txt", "w", encoding="utf-8") as file:
        pprint.pprint(data, stream=file)

if __name__ == '__main__':
    get_titles()
