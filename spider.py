# -*- coding: utf-8 -*-

import requests
from lxml import etree
from collections import defaultdict
from collections import OrderedDict
from collections import Counter
from selenium import webdriver
import string
import time

headers = {
    'USER-AGENT':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    }

""" Google Schoolar
g_citations = {
    'original paper title': 'processed paper title', 'citation number', 'publish year', 'venue'
}
"""
google_src = requests.get('https://scholar.google.com/citations?hl=en&user=v8ZQDf8AAAAJ&view_op=list_works&sortby=pubdate&cstart=0&pagesize=1000', headers=headers).text                           
g_selector = etree.HTML(google_src) 
g_citations = defaultdict(list)
g_pub_num = 0
flag = True
sum_g_citation = g_selector.xpath('//*[@id="gsc_rsb_st"]/tbody/tr[1]/td[2]/text()')[0]
curr = ''

for i, quote in enumerate(g_selector.xpath('//*[@id="gsc_a_b"]/tr/td[1]/a/text()')):
    # calculating total publication quantity
    g_pub_num += 1
    
    # normalize paper title
    g_title = quote.lower()
    for c in string.punctuation:
        g_title = g_title.replace(c, '')
    g_title = g_title.replace(' ', '')
    
    # xpath for citation number
    cnt = g_selector.xpath('//*[@id="gsc_a_b"]/tr[{}]/td[2]/a/text()'.format(i+1))
    cnt = str(cnt[0]) if cnt else '0'
    
    # xpath for publish year
    year = g_selector.xpath('//*[@id="gsc_a_b"]/tr[{}]/td[3]/span/text()'.format(i+1))
    year = str(year[0]) if year else None
    
    # xpath for publish venue
    venue = g_selector.xpath('//*[@id="gsc_a_b"]/tr[{}]/td[1]/div[2]/text()'.format(i+1))
    venue = venue[0] if venue else None 
    
    # append infomation
    if quote not in g_citations: # make sure the original paper title are not the same
        same_pub = False
        for k, v in g_citations.items():
            for info in v:
                if g_title==info[0]: # If the paper title are similar
                    if (not year or not info[2]) and (not venue or not info[3]):
                        same_pub = True
                    elif not year or not info[2]:
                        if venue==info[3]:
                            same_pub = True
                    elif not venue or not info[3]:
                        if year==info[2]:
                            same_pub = True
                
        if same_pub:
            print('Similar titles are:')
            print('Are they the same paper:', same_pub)
            print('\tTitle1:', quote)
            print('\tTitle2:', k)
            print('\tPublish year:', info[2], year)
            print('\tPublish Venue:', info[3], venue)
        else:
            g_citations[quote].append([g_title, cnt, year, venue])
                    
    else: # if have same original paper titles, then compare year and venue
        
        same_pub = False
        for info in g_citations[quote]:
            cur_year = info[2]
            curr_venue = info[3]
            if cur_year==year and curr_venue==venue:
                same_pub = True
        # Test
        print('Identical titles are:')
        print('Is the same paper:', same_pub)
        print("\tpaper info:")
        print("\tpaper title:", quote)
        print('\tProcessed title', g_title)
        print('\tCitation number', cnt)
        print('\tPublished Year and original year', year, cur_year)
        print('\tPublished venue and original venue', venue, curr_venue)
        if not same_pub:
            g_citations[quote].append([g_title, cnt, year, venue])
        

g_citations = OrderedDict(sorted(g_citations.items()))

# Test
# for k, v in g_citations.items():
#     print(k, v)
"""
please check:
1. same paper title
    1. On skyline groups
    2. Discovering and learning sensational episodes of news events
2. different paper title
""" 

# """ Microsoft Academic
# """
# driver = webdriver.Chrome()
# driver.get('https://academic.microsoft.com/author/2145831560/publication/search?q=Chengkai%20Li&qe=Composite(AA.AuId%3D2145831560)&f=&orderBy=1&skip=10&take=10')
# time.sleep(4)
# ms_html = driver.page_source
# m_selector = etree.HTML(ms_html) 
# m_page_num = m_selector.xpath('/html/body/div[1]/div/div/router-view/router-view/ma-edp-serp/div/div[2]/div/compose/div/div[2]/ma-pager/div/div/text()')[-1].lstrip().rstrip()
# sum_m_citation = m_selector.xpath('/html/body/div[1]/div/div/router-view/div/div/div/div[2]/div[3]/ma-statistics-item[2]/div/div[2]/div[1]/text()')[0].lstrip().rstrip()
# driver.close()                            
# urls = []
# for i in range(0, int(m_page_num)):
#     urls.append('https://academic.microsoft.com/author/2145831560/publication/search?q=Chengkai%20Li&qe=Composite(AA.AuId%3D2145831560)&f=&orderBy=1&skip={}&take=10'.format(str(i*10)))


# m_citations = defaultdict(list)
# m_pub_num = 0
# for i, url in enumerate(urls):
#     driver = webdriver.Chrome()
#     driver.get(url)
#     time.sleep(2)
#     ms_html = driver.page_source
#     m_selector = etree.HTML(ms_html) 
#     x = m_selector.xpath('/html/body/div[1]/div/div/router-view/router-view/ma-edp-serp/div/div[2]/div/compose/div/div[2]/ma-card/div/compose/div/div/a[1]/@data-appinsights-title')+m_selector.xpath('/html/body/div[1]/div/div/router-view/router-view/ma-edp-serp/div/div[2]/div/compose/div/div[2]/ma-card/div/compose/div/div[2]/div/div/a/@data-appinsights-title')
#     y = m_selector.xpath('/html/body/div[1]/div/div/router-view/router-view/ma-edp-serp/div/div[2]/div/compose/div/div[2]/ma-card/div/compose/div/div/div[1]/div/a/span/text()')+m_selector.xpath('/html/body/div[1]/div/div/router-view/router-view/ma-edp-serp/div/div[2]/div/compose/div/div[2]/ma-card/div/compose/div/div[2]/div/div/div[1]/a/text()')
    
#     for quote in zip(m_selector.xpath('/html/body/div[1]/div/div/router-view/router-view/ma-edp-serp/div/div[2]/div/compose/div/div[2]/ma-card/div/compose/div/div/a[1]/@data-appinsights-title')+
#                      m_selector.xpath('/html/body/div[1]/div/div/router-view/router-view/ma-edp-serp/div/div[2]/div/compose/div/div[2]/ma-card/div/compose/div/div[2]/div/div/a/@data-appinsights-title'),                                   
#                      m_selector.xpath('/html/body/div[1]/div/div/router-view/router-view/ma-edp-serp/div/div[2]/div/compose/div/div[2]/ma-card/div/compose/div/div/div[1]/div/a/span/text()')+
#                      m_selector.xpath('/html/body/div[1]/div/div/router-view/router-view/ma-edp-serp/div/div[2]/div/compose/div/div[2]/ma-card/div/compose/div/div[2]/div/div/div[1]/a/text()')):
#         m_pub_num += 1
#         title = quote[0].lower()
#         for c in string.punctuation:
#             title = title.replace(c, '')
#         title = title.replace(' ', '')
#         m_citations[quote[0]].append(title)
#         m_citations[quote[0]].append(str(quote[1].split()[0]))
#     driver.close()
    
# m_citations = OrderedDict(sorted(m_citations.items()))

# print(g_citations, len(g_citations))
# print(m_citations, len(m_citations))

# """ Generate Report
# """
# ## In Microsoft not in goolge
# def gen_title(citation):
#     t = []
#     for i, (k, v) in enumerate(citation.items()):
#         for i in range(0, len(v), 2):
#             t.append(v[i])
#     return t

# g_titles = gen_title(g_citations)
# m_titles = gen_title(m_citations)
# print(len(g_titles)) # 97
# print(len(m_titles)) # 110
# overlap = list((Counter(g_titles) & Counter(m_titles)).elements())
# print(overlap, len(overlap))
# # g_origin = {v[0]:k for k, v in g_citations.items()}
# # m_origin = {v[0]:k for k, v in m_citations.items()}
# # ms1g0 = list((Counter(m_titles) - Counter(overlap)).elements())
# # ms0g1 = list((Counter(g_titles) - Counter(overlap)).elements())

# # def get_origin(origin, titles, citations):
# #     res = []
# #     for t in titles:
# #         res.append([origin[t], citations[origin[t]][1]])
# #     return res
            
# # ms1g0_origin = get_origin(m_origin, ms1g0, m_citations)
# # ms0g1_origin = get_origin(g_origin, ms0g1, g_citations)

# # print("There are {} papers in Google Scholar and {} papers in Microsoft Academic".format(g_pub_num, m_pub_num))
# # print("Total citations from Google Scholar is {}, Microsoft Academic is {}".format(sum_g_citation, sum_m_citation))
# # print('------'*20)
# # print("There are {} Papers appear in Microsoft Academic but not in Google Scholar:".format(len(ms1g0_origin)))
# # for i, v in enumerate(sorted(ms1g0_origin)):
# #     print("\t{}: {}. Microfost Academic citation: {}".format(i+1, v[0], v[1]))
# # print("There are {} Papers appear in Google Schoolar but not in MS Academic".format(len(ms0g1_origin)))
# # for i, v in enumerate(sorted(ms0g1_origin)):
# #     print("\t{}: {}. Google Scholar citation: {}".format(i+1, v[0], v[1]))
# # print('------'*20)

# # g_t_c = {v[0]:v[1] for k, v in g_citations.items() if v[0] in overlap and len(v)==2}
# # m_t_c = {v[0]:v[1] for k, v in m_citations.items() if v[0] in overlap and len(v)==2}
# # print("For the overlapped and not duplicated papers, those papers's citation are different:\n")
# # sum_g = 0
# # for t in sorted(set(g_titles+m_titles)):
# #     if t in overlap:
# #         try:
# #             if g_t_c[t] != m_t_c[t]:
# #                 print("{}\ngoogle scholar citation: {}, microsoft academic citation: {}".format(g_origin[t], g_t_c[t], m_t_c[t]))
# #                 print("------"*10)
# #         except:
# #             pass
