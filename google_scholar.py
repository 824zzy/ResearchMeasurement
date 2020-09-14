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
    'USER-AGENT':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
    'cookie': 'CONSENT=YES+CN.zh-CN+20161016-15-2; ANID=AHWqTUnVQhoVBPnJQYoCcORm65SwC1wGWDJkgZYP71DdguUMtEnSdlEcF61v0mZu; GSP=LM=1590885779:S=chPQMZ8Oa_0roIgY; HSID=AMMhz5In4VkzrQcHv; SSID=AcctHpUKuD-MP7GwW; APISID=cMVmBSA-KnEtFSST/Ah84vthXMgghX_uF2; SAPISID=Sc4J6syXW3EEmZQO/AZLInF6oRVcetG6l9; __Secure-3PAPISID=Sc4J6syXW3EEmZQO/AZLInF6oRVcetG6l9; OGP=-19018928:; SEARCH_SAMESITE=CgQIrpAB; OGPC=19018621-1:19018928-1:19019681-1:; SID=0gcVx4hUqogXPbay2DED_knyTzM1GbcvP9TLDDpz7ZfIF2ALZr-izFA0Ge5q4yH05Y5Ayg.; __Secure-3PSID=0gcVx4hUqogXPbay2DED_knyTzM1GbcvP9TLDDpz7ZfIF2AL00AWmTKOSRtQZGm5PZJ4RQ.; NID=204=yqFzImrMWMyFskFz-FZOKzWV1hGmqWzYh6nXTEMNrkkh7Az7RqyRtTiqG7UgR1zXTCazIBErE2oZAPBYkpGhXcuHUEq4RKqw6axx__giNp5gbM9wMGm-pr4HqT2PeNrDDvh81do8tCBOQza7fKwMc0XLSoj8U4JcPvMUOu9r89qA9PwPFKRWOq7X-KPzntF_G-mqpWjOQWBqOxcY2PdHFfcTr7xkwkvpEBIT1izKomXVa4K1ogSobqFAb3xmrMWD1HpftoaBMCXd5P1hPbkBAzyGLgdx29wZUoNWe6lAnBW2nGRIYfWZjCpfggQ; 1P_JAR=2020-08-29-04; SIDCC=AJi4QfHgh9DalG8ReHL8NB9t2mx1c-fcABJRBQ9UGTab-4puP6E4V0GJSreVxLpyA0nJZ_1JAaao; __Secure-3PSIDCC=AJi4QfHBNRHAJ_VfFlQ920cmW4iHFSSfZUv0rCdY452Bt-jhEpAjTUovzVwY0i0EvMIa_wDAenU',
    'x-client-data': 'CKe1yQEIibbJAQimtskBCMS2yQEIqZ3KAQiZocoBCIa1ygEImbXKAQj+vMoBCOfGygEI58jKAQjpyMoBCJXWygEIvNfKAQ==',
    'upgrade-insecure-requests': '1',
    }

""" Google Schoolar
g_citations = {
    'original paper title': 'processed paper title', 'citation number', 'publish year', 'venue'
}
"""
def get_google_scholar(user_id):
    """
    The codes for getting user_id have deprecated because serveral professors' id can not display by "name+UTA"
    """
    # driver = webdriver.Chrome()
    # profile_url = 'https://scholar.google.com/scholar?hl=en&as_sdt=0%2C44&q={}+UTA'.format(name)
    # # print(profile_url)
    # driver.get(profile_url)
    # time.sleep(4)
    # profile_html = driver.page_source
    # profile_selector = etree.HTML(profile_html)
    # user_url = profile_selector.xpath('//*[@id="gs_res_ccl_mid"]/div[1]/table/tbody/tr/td[2]/h4/a/@href')[0]
    # user_id = re.findall("\?(.*)\&hl", user_url)[0]
    # # print(user_id)
    
    driver = webdriver.Chrome()
    google_url = 'https://scholar.google.com/citations?hl=en&user={}&view_op=list_works&sortby=pubdate&cstart=0&pagesize=1000'.format(user_id)
    driver.get(google_url)
    time.sleep(2)

    # By default google scholar only show 200 papers, so have to simulate click `load more`
    for _ in range(40):
        try:
            driver.find_element_by_xpath('//*[@id="gsc_bpf_more"]/span/span[2]').click()
            time.sleep(3)
        except:
            break
    
    # while clickable:
    # try:
    #     driver.find_element_by_xpath('//*[@id="gsc_bpf_more"]/span/span[2]').click()
    #     time.sleep(0.1)
    # except:
    #     clickable = False
    
    # google_src = requests.get(google_url, headers=headers).text
    google_src = driver.page_source
    g_selector = etree.HTML(google_src) 
    driver.close()
    
    g_citations = defaultdict(list)
    g_res = defaultdict(list)
    g_pub_num = 0
    g_pub_origin = 0
    flag = True
    sum_g_citation = g_selector.xpath('//*[@id="gsc_rsb_st"]/tbody/tr[1]/td[2]/text()')[0]
    curr = ''
    
    for i, quote in enumerate(g_selector.xpath('//*[@id="gsc_a_b"]/tr/td[1]')):
        # original paper number
        g_pub_origin += 1
        # normalize paper title, remove svg: it will affect later title extraction
        quote = ' '.join(quote.xpath('a/text()'))
        g_title = quote.lower()
        for c in string.punctuation:
            g_title = g_title.replace(c, '')
        g_title = g_title.replace(' ', '').encode('ascii', 'ignore')
        
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
    # g_citations, g_pub_num, g_pub_origin, sum_g_citation = get_google_scholar("Junzhou Huang")
    g_citations, g_pub_num, g_pub_origin, sum_g_citation = get_google_scholar("Y26XykAAAAAJ")
    # Test
    for k, v in g_citations.items():
        print(k)
    
    print(g_pub_num, g_pub_origin, sum_g_citation)