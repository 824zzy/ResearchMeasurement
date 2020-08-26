# -*- coding: utf-8 -*-

import requests
from lxml import etree
from collections import defaultdict
from collections import OrderedDict
from collections import Counter
from selenium import webdriver
import string
import time
from checker import check_same_title, check_diff_title

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
        same_pub = check_diff_title(g_citations, quote, g_title, year, venue)
        if not same_pub:
            g_citations[quote].append([g_title, cnt, year, venue])
    else: # if have same original paper titles, then compare year and venue
        same_pub = check_same_title(g_citations, quote, year, venue)
        if not same_pub:
            g_citations[quote].append([g_title, cnt, year, venue])
        
    # calculating total publication quantity
    if not same_pub:
        g_pub_num += 1
    
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