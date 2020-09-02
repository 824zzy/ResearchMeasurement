# -*- coding: utf-8 -*-

def check_diff_title(source_dict, query_title, prc_title, pub_year, pub_venue):
    same_pub = False
    similar_title = ''
    curr_year = 0
    curr_venue = ''
    for orgn_title, infos in source_dict.items():
        # print(infos)
        for info in infos:
            if prc_title==info[0]: # If the processed titles are similar
                similar_title = orgn_title
                curr_year = info[2]
                curr_venue = info[3]
                if (not pub_year or not curr_year) and (not pub_venue or not curr_venue):
                        same_pub = True
                elif not pub_year or not curr_year:
                    # Unknown Journal for Microsoft Academic
                    if pub_venue==curr_venue: 
                        same_pub = True
                elif not pub_venue or not curr_venue:
                    if pub_year==curr_year:
                        same_pub = True
                elif curr_venue==pub_venue and curr_year==pub_year:
                    same_pub = True
        if same_pub:
            break
        
    # For testing
    # if similar_title:
    #     pub_venue = 'None' if not pub_venue else pub_venue
    #     print('Similar titles are: {} | {}'.format(similar_title, query_title))
    #     print('\tAre they the same paper: {}'.format(same_pub))
    #     print('\tPublished Year of two paper: {} | {}'.format(curr_year, pub_year))
    #     print('\tPublished venue of two paper: {} | {}'.format(curr_venue, pub_venue))
    return same_pub


def check_same_title(source_dict, query_title, pub_year, pub_venue):
    same_pub = False
    curr_year = 0
    curr_venue = ''
    for info in source_dict[query_title]:
            curr_year = info[2]
            curr_venue = info[3]
            if curr_year==pub_year and curr_venue==pub_venue:
                same_pub = True
    
    # For testing
    # print('Identified identical titles are:', query_title)
    # print('\tAre they the same paper:{}'.format(same_pub))
    # print('\tPublished Year of two paper: {} | {}'.format(pub_year, curr_year))
    # print('\tPublished venue of two paper: {} | {}'.format(pub_venue, curr_venue))
    return same_pub

def gen_title(citation):
    # get whole processed titles from source
    t = []
    for i, (k, v) in enumerate(citation.items()):
        for info in v:
            t.append(info[0])
    return t

def gen_origin(origin, titles, citations):
    res = []
    for t in titles:
        res.append([origin[t], citations[origin[t]][1]])
    return res


def gen_diff_origin(origin, titles, citations):
    res = []
    for t in titles:
        orgn_title = origin[t]
        citation_num = citations[origin[t]][0][1]
        pub_year = citations[origin[t]][0][2]
        
        if not citations[origin[t]][0][3]:
            pub_venue = "Null"
        else:    
            pub_venue = citations[origin[t]][0][3]
        res.append([orgn_title, 
                    citation_num, 
                    pub_year,
                    pub_venue] 
                    )
    return res
    
def check_duplicate(prc1, prc2):
    dedup1 = []
    dedup2 = []
    for p in prc1:
        same = False
        for q in prc2:
            if p in q or q in p:
                same = True
        if not same:
            dedup1.append(p)
            
    for p in prc2:
        same = False
        for q in prc1:
            if p in q or q in p:
                same = True
        if not same:
            dedup2.append(p)
    return dedup1, dedup2
