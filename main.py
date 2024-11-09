#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import requests
import re
from tqdm import tqdm

def get_titles_while():
    titles_gen = []
    n = 0    
    while True:
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
            "paged": f'{n}'
        }
    } 
        n += 1
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
        if response.status_code != 200:
            break
    with open("titles.txt", "w", encoding="utf-8") as file:
        print(*titles_gen, file=file, sep="\n")
    
    
def get_titles_for():
    titles_gen = []    
    for i in tqdm(range(10)):
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
            "paged": f'{i}'
        }
    } 
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
    with open("titles.txt", "w", encoding="utf-8") as file:
        print(*titles_gen, file=file, sep="\n")
        
        
if __name__ == '__main__':
    #get_titles_while()
    get_titles_for()

