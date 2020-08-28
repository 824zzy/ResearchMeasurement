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

""" Microsoft Academic
"""
def get_MS_academic():
    driver = webdriver.Chrome()
    driver.get('https://academic.microsoft.com/author/2145831560/publication/search?q=Chengkai%20Li&qe=Composite(AA.AuId%3D2145831560)&f=&orderBy=0&skip=10&take=10')
    time.sleep(4)
    ms_html = driver.page_source
    m_selector = etree.HTML(ms_html) 
    # Total citation from page source. TODO: change it to our own citation
    # sum_m_citation = m_selector.xpath('/html/body/div[1]/div/div/router-view/div/div/div/div[2]/div[3]/ma-statistics-item[2]/div/div[2]/div[1]/text()')[0].lstrip().rstrip()
    
    sum_m_citation = m_selector.xpath('/html/body/div/div/div/router-view/div/div/div/div/div[3]/ma-statistics-item[2]/div/div[2]/div[1]/text()')[0].lstrip().rstrip()
                                       
    # create urls for each page
    m_page_num = m_selector.xpath('/html/body/div[1]/div/div/router-view/router-view/ma-edp-serp/div/div[2]/div/compose/div/div[2]/ma-pager/div/div/text()')[-1].lstrip().rstrip()
    urls = []
    for i in range(0, int(m_page_num)):
        urls.append('https://academic.microsoft.com/author/2145831560/publication/search?q=Chengkai%20Li&qe=Composite(AA.AuId%3D2145831560)&f=&orderBy=0&skip={}&take=10'.format(str(i*10)))
    driver.close()

    m_citations = defaultdict(list)
    m_res = defaultdict(list)
    m_pub_num = 0
    m_pub_origin = 0
    for i, url in enumerate(urls):
        driver = webdriver.Chrome()
        driver.get(url)
        time.sleep(2)
        ms_html = driver.page_source
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
            prc_title = prc_title.replace(' ', '')
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
    m_citations, m_pub_num, m_pub_origin, m_citation_num = get_MS_academic()
    
    # For testing
    for k, v in m_citations.items():
        print(k, v)
    print(m_pub_num, m_pub_origin, m_citation_num)