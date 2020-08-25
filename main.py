# -*- coding: utf-8 -*-
from google_scholar import *
from microsoft_academic import *

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
