# -*- coding: utf-8 -*-

import requests
from lxml import etree
from collections import defaultdict
from collections import OrderedDict
from collections import Counter
from selenium import webdriver
import string
import time

""" Microsoft Academic
"""
driver = webdriver.Chrome()
driver.get('https://academic.microsoft.com/author/2145831560/publication/search?q=Chengkai%20Li&qe=Composite(AA.AuId%3D2145831560)&f=&orderBy=0&skip=10&take=10')
time.sleep(4)
ms_html = driver.page_source
m_selector = etree.HTML(ms_html) 
# Total citation from page source. TODO: change it to our own citation
sum_m_citation = m_selector.xpath('/html/body/div[1]/div/div/router-view/div/div/div/div[2]/div[3]/ma-statistics-item[2]/div/div[2]/div[1]/text()')[0].lstrip().rstrip()

# create urls for each page
m_page_num = m_selector.xpath('/html/body/div[1]/div/div/router-view/router-view/ma-edp-serp/div/div[2]/div/compose/div/div[2]/ma-pager/div/div/text()')[-1].lstrip().rstrip()
urls = []
for i in range(0, int(m_page_num)):
    urls.append('https://academic.microsoft.com/author/2145831560/publication/search?q=Chengkai%20Li&qe=Composite(AA.AuId%3D2145831560)&f=&orderBy=0&skip={}&take=10'.format(str(i*10)))
driver.close()


m_citations = defaultdict(list)
m_pub_num = 0
for i, url in enumerate(urls):
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(2)
    ms_html = driver.page_source
    m_selector = etree.HTML(ms_html) 
    
    for quote in zip(m_selector.xpath('/html/body/div[1]/div/div/router-view/router-view/ma-edp-serp/div/div[2]/div/compose/div/div[2]/ma-card/div/compose/div/div/a[1]/@data-appinsights-title')+
                     m_selector.xpath('/html/body/div[1]/div/div/router-view/router-view/ma-edp-serp/div/div[2]/div/compose/div/div[2]/ma-card/div/compose/div/div[2]/div/div/a/@data-appinsights-title'),                                   
                     m_selector.xpath('/html/body/div[1]/div/div/router-view/router-view/ma-edp-serp/div/div[2]/div/compose/div/div[2]/ma-card/div/compose/div/div/div[1]/div/a/span/text()')+
                     m_selector.xpath('/html/body/div[1]/div/div/router-view/router-view/ma-edp-serp/div/div[2]/div/compose/div/div[2]/ma-card/div/compose/div/div[2]/div/div/div[1]/a/text()')):
        m_pub_num += 1
        title = quote[0].lower()
        for c in string.punctuation:
            title = title.replace(c, '')
        title = title.replace(' ', '')
        m_citations[quote[0]].append(title)
        m_citations[quote[0]].append(str(quote[1].split()[0]))
    driver.close()
    
m_citations = OrderedDict(sorted(m_citations.items()))

# For testing
for k, v in m_citations.items():
    print(k, v)