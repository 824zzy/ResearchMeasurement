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
from selenium import webdriver
import re

headers = {
    'USER-AGENT':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    }

""" Google Schoolar
g_citations = {
    'original paper title': 'processed paper title', 'citation number', 'publish year', 'venue'
}
"""
def get_google_scholar(name):
    # Get user id
    driver = webdriver.Chrome()
    profile_url = 'https://scholar.google.com/scholar?hl=en&as_sdt=0%2C44&q={}+UTA'.format(name)
    driver.get(profile_url)
    profile_html = driver.page_source
    # profile_html = requests.get(profile_url, headers=headers).text
    profile_selector = etree.HTML(profile_html) 
    user_url = profile_selector.xpath('//*[@id="gs_res_ccl_mid"]/div[1]/table/tbody/tr/td[2]/h4/a/@href')[0]
    user_id = re.findall("\?(.*)\&hl", user_url)[0]
    driver.close()
    
    google_url = 'https://scholar.google.com/citations?hl=en&{}&view_op=list_works&sortby=pubdate&cstart=0&pagesize=1000'.format(user_id)
    google_src = requests.get(google_url, headers=headers).text
    g_selector = etree.HTML(google_src) 
    g_citations = defaultdict(list)
    g_res = defaultdict(list)
    g_pub_num = 0
    g_pub_origin = 0
    flag = True
    sum_g_citation = g_selector.xpath('//*[@id="gsc_rsb_st"]/tbody/tr[1]/td[2]/text()')[0]
    curr = ''

    for i, quote in enumerate(g_selector.xpath('//*[@id="gsc_a_b"]/tr/td[1]/a/text()')):
        # original paper number
        g_pub_origin += 1
        # normalize paper title
        g_title = quote.lower()
        for c in string.punctuation:
            g_title = g_title.replace(c, '')
        g_title = g_title.replace(' ', '')
        
        # xpath for citation number
        c_num = g_selector.xpath('//*[@id="gsc_a_b"]/tr[{}]/td[2]/a/text()'.format(i+1))
        c_num = str(c_num[0]) if c_num else '0'
        
        # xpath for publish year
        year = g_selector.xpath('//*[@id="gsc_a_b"]/tr[{}]/td[3]/span/text()'.format(i+1))
        year = str(year[0]) if year else None
        
        # xpath for publish venue
        venue = g_selector.xpath('//*[@id="gsc_a_b"]/tr[{}]/td[1]/div[2]/text()'.format(i+1))
        venue = venue[0] if venue else None 
        
        # add infomation to dict
        if quote not in g_citations: # make sure the original paper title are not the same
            same_pub = check_diff_title(g_citations, quote, g_title, year, venue)
            if not same_pub:
                g_citations[quote].append([g_title, c_num, year, venue])
                g_res[g_title].append([quote, c_num, year, venue])
        else: # if have same original paper titles, then compare year and venue
            same_pub = check_same_title(g_citations, quote, year, venue)
            if not same_pub:
                g_citations[quote].append([g_title, c_num, year, venue])
                g_res[g_title].append([quote, c_num, year, venue])
        # calculating total publication quantity
        if not same_pub:
            g_pub_num += 1
        
    g_res = OrderedDict(sorted(g_res.items()))
    g_citations = OrderedDict(sorted(g_citations.items()))
    return g_citations, g_pub_num, g_pub_origin, sum_g_citation
    # return g_res, g_pub_num, g_pub_origin, sum_g_citation


"""
please check:
1. same paper title
    1. On skyline groups
    2. Discovering and learning sensational episodes of news events
2. different paper title
""" 
if __name__ == "__main__":
    g_citations, g_pub_num, g_pub_origin, sum_g_citation = get_google_scholar("Won Hwa Kim")
    # Test
    for k, v in g_citations.items():
        print(k, v)
    
    print(g_pub_num, g_pub_origin, sum_g_citation)