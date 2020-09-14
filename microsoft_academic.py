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
import re

""" Microsoft Academic
"""
def get_MS_academic(name):
    driver = webdriver.Chrome()
    profile_url = 'https://academic.microsoft.com/search?q={}%20UTA&f=&orderBy=0&skip=0&take=10'.format(name)
    driver.get(profile_url)
    time.sleep(3)
    driver.find_element_by_xpath('/html/body/div[2]/div/div/router-view/ma-serp/div/div[3]/div/compose/div/ma-card[1]/div/compose/div/div/div[1]/div/div/a/span').click()
    time.sleep(3)
    ms_html = driver.page_source
    m_selector = etree.HTML(ms_html) 
    # Total citation from page source. TODO: change it to our own citation
    try:
        sum_m_citation = m_selector.xpath('/html/body/div/div/div/router-view/div/div/div/div/div[3]/ma-statistics-item[2]/div/div[2]/div[1]/text()')[0].lstrip().rstrip()
    except:
        sum_m_citation = m_selector.xpath('/html/body/div[2]/div/div/router-view/div/div/div/div/div[3]/ma-statistics-item[2]/div/div[2]/div[1]/text()')[0].lstrip().rstrip()
    
    # create urls for each page
    try:
        m_page_num = m_selector.xpath('/html/body/div/div/div/router-view/router-view/ma-edp-serp/div/div[2]/div/compose/div/div[2]/ma-pager/div/div/text()')[-1].lstrip().rstrip()
    except:
        m_page_num = 1
    urls = []
    curr_url = driver.current_url
    for i in range(0, int(m_page_num)):
        replaced_url = curr_url+'&skip={}&take=10'.format(str(i*10))
        urls.append(replaced_url)
    m_citations = defaultdict(list)
    m_res = defaultdict(list)
    m_pub_num = 0
    m_pub_origin = 0
    for i, url in enumerate(urls):
        driver.get(url)
        time.sleep(2)
        ms_html = driver.page_source.encode('utf-8')
        m_selector = etree.HTML(ms_html)
            
        for quote in zip(m_selector.xpath('/html/body/div[1]/div/div/router-view/router-view/ma-edp-serp/div/div[2]/div/compose/div/div[2]/ma-card/div/compose/div/div/a[1]/@data-appinsights-title')+
                        m_selector.xpath('/html/body/div[1]/div/div/router-view/router-view/ma-edp-serp/div/div[2]/div/compose/div/div[2]/ma-card/div/compose/div/div[2]/div/div/a/@data-appinsights-title'),                                   
                        m_selector.xpath('/html/body/div[1]/div/div/router-view/router-view/ma-edp-serp/div/div[2]/div/compose/div/div[2]/ma-card/div/compose/div/div/div[1]/div/a/span/text()')+
                        m_selector.xpath('/html/body/div[1]/div/div/router-view/router-view/ma-edp-serp/div/div[2]/div/compose/div/div[2]/ma-card/div/compose/div/div[2]/div/div/div[1]/a/text()'),
                        m_selector.xpath('/html/body/div[1]/div/div/router-view/router-view/ma-edp-serp/div/div[2]/div/compose/div/div[2]/ma-card/div/compose/div/div[1]/a[2]/span[1]/text()')+
                        m_selector.xpath('/html/body/div[1]/div/div/router-view/router-view/ma-edp-serp/div/div[2]/div/compose/div/div[2]/ma-card/div/compose/div/div[2]/div/div/div[2]/div[1]/a/span[1]/text()'),
                        m_selector.xpath('/html/body/div[1]/div/div/router-view/router-view/ma-edp-serp/div/div[2]/div/compose/div/div[2]/ma-card/div/compose/div/div[1]/a[2]/span[2]/text()')+
                        m_selector.xpath('/html/body/div[1]/div/div/router-view/router-view/ma-edp-serp/div/div[2]/div/compose/div/div[2]/ma-card/div/compose/div/div[2]/div/div/div[2]/div[1]/a/span[2]/text()')
                        ):
            m_pub_origin += 1
            # process title infomation
            orgn_title = quote[0]
            prc_title = quote[0].lower()
            for c in string.punctuation:
                prc_title = prc_title.replace(c, '')
            prc_title = prc_title.replace(' ', '').encode('ascii', 'ignore')
            # process citation information: select first number in the string
            c_num = str(quote[1].split()[0])
            # process year information: remove all the left and right space 
            year = quote[2].replace(' ', '')
            # process venue information: remove all the left&right space while keep space between words. TODO: process venue
            venue = quote[3].lstrip().rstrip()
            venue = None if venue=='Unknown Journal' else venue
            
            # add infomation to dict
            if orgn_title not in m_citations: # make sure the original paper title are not the same
                same_pub = check_diff_title(m_citations, orgn_title, prc_title, year, venue)
                if not same_pub:
                    m_citations[orgn_title].append([prc_title, c_num, year, venue])
                    m_res[prc_title].append([orgn_title, c_num, year, venue])
            else: # if have same original paper titles, then compare year and venue
                same_pub = check_same_title(m_citations, orgn_title, year, venue)
                if not same_pub:
                    m_citations[orgn_title].append([prc_title, c_num, year, venue])
                    m_res[prc_title].append([orgn_title, c_num, year, venue])
            # calculating total publication quantity
            if not same_pub:
                m_pub_num += 1
    driver.close()    
        
    m_res = OrderedDict(sorted(m_res.items()))
    m_citations = OrderedDict(sorted(m_citations.items()))

    return m_citations, m_pub_num, m_pub_origin, sum_m_citation
    # return m_res, m_pub_num, m_pub_origin, sum_m_citation

if __name__ == "__main__":
    m_citations, m_pub_num, m_pub_origin, m_citation_num = get_MS_academic('Chance Eary')
    
    # For testing
    for k, v in m_citations.items():
        print(k, v)
        # print(v)
    print(m_pub_num, m_pub_origin, m_citation_num)