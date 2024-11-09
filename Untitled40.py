#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import requests

def first_page():
    url = 'https://www.lejobadequat.com/emplois'
    resp = requests.get(url, headers={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0'})

if __name__ == '__main__':
    first_page()


# In[ ]:




