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
    same_pub = False
    if quote not in g_citations: # make sure the original paper title are not the same
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