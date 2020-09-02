# -*- coding: utf-8 -*-
from google_scholar import get_google_scholar
from microsoft_academic import get_MS_academic
from checker import gen_title, gen_origin, gen_diff_origin, check_duplicate
from collections import Counter

if __name__ == "__main__":
    professor_list = [("https://scholar.google.com/citations?user=vhpbMX8AAAAJ", 'Song Jiang')]
    """ Generate Report
    """
    for url, name in professor_list:
        # print("Report For google scholar:")
        g_citations, g_pub_num, g_pub_origin, g_citation_num = get_google_scholar(url)
        
        # print("-----"*10)
        # print("Report For Microsoft academic:")
        m_citations, m_pub_num, m_pub_origin, m_citation_num = get_MS_academic(name)
        
        # For testing
        # print(g_pub_num, g_pub_origin, g_citation_num)
        # print(m_pub_num, m_pub_origin, m_citation_num)
        
        # List for processed titles
        g_prc_titles = gen_title(g_citations) # whole google scholar processed titles
        m_prc_titles = gen_title(m_citations) # whole ms academic processed titles
        # generate dictionary has processed title: original title
        g_origin = {v[0][0]:k for k, v in g_citations.items()} 
        m_origin = {v[0][0]:k for k, v in m_citations.items()}
        
        # overlap processed paper titles from MS academic and google scholar
        overlap = list((Counter(g_prc_titles) & Counter(m_prc_titles)).elements()) # 77
        
        # For testing
        # print(overlap, len(overlap))
        # print(set(overlap), len(set(overlap)))
        
        # # # In Microsoft not in goolge
        # print(len(g_prc_titles)) # 92
        # print(len(m_prc_titles)) # 94
        

        ms1g0 = list((Counter(m_prc_titles) - Counter(overlap)).elements())
        ms0g1 = list((Counter(g_prc_titles) - Counter(overlap)).elements())
        # make sure there is not similar titles. 
        # e.g.:Computational Journalism: A Call to Arms to Database Researchers
        #      C. Yu. Computational journalism: A call to arms to database researchers
        ms1g0, ms0g1 = check_duplicate(ms1g0, ms0g1)
        
        # # For testing
        # print(ms0g1, len(ms0g1))
        # print(ms1g0, len(ms1g0))
        
        ms1g0_origin = gen_diff_origin(m_origin, ms1g0, m_citations)
        ms0g1_origin = gen_diff_origin(g_origin, ms0g1, g_citations)


        print("There are {} papers in Google Scholar and {} papers in Microsoft Academic"
            .format(g_pub_num, m_pub_num))
        print("Total citations from Google Scholar is {}, Microsoft Academic is {}"
            .format(g_citation_num, m_citation_num))
        print('------'*20)
        print('Please note that the duplicated paper titles may appear in the other source')
        print("There are {} Papers appear in Microsoft Academic but not in Google Scholar:"
            .format(len(ms1g0_origin)))
        for i, v in enumerate(sorted(ms1g0_origin)):
            print("\t{}: {}\n\t\tMicrofost Academic citation: {}; Published year: {}; Published venue: {}."
                .format(i+1, v[0].encode('utf-8'), v[1], v[2], v[3].encode('utf-8')))
        print("There are {} Papers appear in Google Schoolar but not in MS Academic".format(len(ms0g1_origin)))
        for i, v in enumerate(sorted(ms0g1_origin)):
            print("\t{}: {}\n\t\tGoogle Scholar citation: {}; Published year: {}; Published venue: {}."
                .format(i+1, v[0].encode('utf-8'), v[1], v[2], v[3].encode('utf-8')))
        print('------'*20)

        g_t_c = {v[0][0]:v[0][1] for k, v in g_citations.items() if v[0][0] in overlap and len(v)==1}
        m_t_c = {v[0][0]:v[0][1] for k, v in m_citations.items() if v[0][0] in overlap and len(v)==1}
        print("For the overlapped and not duplicated papers, those papers's citation are different:\n")
        sum_g = 0
        for t in sorted(set(g_prc_titles+m_prc_titles)):
            if t in overlap:
                try:
                    if g_t_c[t] != m_t_c[t]:
                        print("{}\ngoogle scholar citation: {}, microsoft academic citation: {}"
                            .format(g_origin[t], g_t_c[t], m_t_c[t]))
                        print("------"*10)
                except:
                    pass