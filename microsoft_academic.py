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
driver.get('https://academic.microsoft.com/author/2145831560/publication/search?q=Chengkai%20Li&qe=Composite(AA.AuId%3D2145831560)&f=&orderBy=1&skip=10&take=10')
time.sleep(4)
ms_html = driver.page_source
m_selector = etree.HTML(ms_html) 
m_page_num = m_selector.xpath('/html/body/div[1]/div/div/router-view/router-view/ma-edp-serp/div/div[2]/div/compose/div/div[2]/ma-pager/div/div/text()')[-1].lstrip().rstrip()
sum_m_citation = m_selector.xpath('/html/body/div[1]/div/div/router-view/div/div/div/div[2]/div[3]/ma-statistics-item[2]/div/div[2]/div[1]/text()')[0].lstrip().rstrip()
driver.close()                            
urls = []
for i in range(0, int(m_page_num)):
    urls.append('https://academic.microsoft.com/author/2145831560/publication/search?q=Chengkai%20Li&qe=Composite(AA.AuId%3D2145831560)&f=&orderBy=1&skip={}&take=10'.format(str(i*10)))


m_citations = defaultdict(list)
m_pub_num = 0
for i, url in enumerate(urls):
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(2)
    ms_html = driver.page_source
    m_selector = etree.HTML(ms_html) 
    x = m_selector.xpath('/html/body/div[1]/div/div/router-view/router-view/ma-edp-serp/div/div[2]/div/compose/div/div[2]/ma-card/div/compose/div/div/a[1]/@data-appinsights-title')+m_selector.xpath('/html/body/div[1]/div/div/router-view/router-view/ma-edp-serp/div/div[2]/div/compose/div/div[2]/ma-card/div/compose/div/div[2]/div/div/a/@data-appinsights-title')
    y = m_selector.xpath('/html/body/div[1]/div/div/router-view/router-view/ma-edp-serp/div/div[2]/div/compose/div/div[2]/ma-card/div/compose/div/div/div[1]/div/a/span/text()')+m_selector.xpath('/html/body/div[1]/div/div/router-view/router-view/ma-edp-serp/div/div[2]/div/compose/div/div[2]/ma-card/div/compose/div/div[2]/div/div/div[1]/a/text()')
    
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

print(g_citations, len(g_citations))
print(m_citations, len(m_citations))

""" Generate Report
"""
## In Microsoft not in goolge
def gen_title(citation):
    t = []
    for i, (k, v) in enumerate(citation.items()):
        for i in range(0, len(v), 2):
            t.append(v[i])
    return t

g_titles = gen_title(g_citations)
m_titles = gen_title(m_citations)
print(len(g_titles)) # 97
print(len(m_titles)) # 110
overlap = list((Counter(g_titles) & Counter(m_titles)).elements())
print(overlap, len(overlap))
# g_origin = {v[0]:k for k, v in g_citations.items()}
# m_origin = {v[0]:k for k, v in m_citations.items()}
# ms1g0 = list((Counter(m_titles) - Counter(overlap)).elements())
# ms0g1 = list((Counter(g_titles) - Counter(overlap)).elements())

# def get_origin(origin, titles, citations):
#     res = []
#     for t in titles:
#         res.append([origin[t], citations[origin[t]][1]])
#     return res
            
# ms1g0_origin = get_origin(m_origin, ms1g0, m_citations)
# ms0g1_origin = get_origin(g_origin, ms0g1, g_citations)

# print("There are {} papers in Google Scholar and {} papers in Microsoft Academic".format(g_pub_num, m_pub_num))
# print("Total citations from Google Scholar is {}, Microsoft Academic is {}".format(sum_g_citation, sum_m_citation))
# print('------'*20)
# print("There are {} Papers appear in Microsoft Academic but not in Google Scholar:".format(len(ms1g0_origin)))
# for i, v in enumerate(sorted(ms1g0_origin)):
#     print("\t{}: {}. Microfost Academic citation: {}".format(i+1, v[0], v[1]))
# print("There are {} Papers appear in Google Schoolar but not in MS Academic".format(len(ms0g1_origin)))
# for i, v in enumerate(sorted(ms0g1_origin)):
#     print("\t{}: {}. Google Scholar citation: {}".format(i+1, v[0], v[1]))
# print('------'*20)

# g_t_c = {v[0]:v[1] for k, v in g_citations.items() if v[0] in overlap and len(v)==2}
# m_t_c = {v[0]:v[1] for k, v in m_citations.items() if v[0] in overlap and len(v)==2}
# print("For the overlapped and not duplicated papers, those papers's citation are different:\n")
# sum_g = 0
# for t in sorted(set(g_titles+m_titles)):
#     if t in overlap:
#         try:
#             if g_t_c[t] != m_t_c[t]:
#                 print("{}\ngoogle scholar citation: {}, microsoft academic citation: {}".format(g_origin[t], g_t_c[t], m_t_c[t]))
#                 print("------"*10)
#         except:
#             pass
