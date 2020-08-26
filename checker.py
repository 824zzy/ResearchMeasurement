def check_diff_title(source_dict, query_title, prc_title, pub_year, pub_venue):
    same_pub = False
    similar_title = ''
    curr_year = 0
    curr_venue = ''
    for orgn_title, infos in source_dict.items():
        for info in infos:
            if prc_title==info[0]: # If the processed titles are similar
                similar_title = orgn_title
                curr_year = info[2]
                curr_venue = info[3]
                if (not pub_year or not curr_year) and (not pub_venue or not curr_venue):
                        same_pub = True
                elif not pub_year or not curr_year:
                    if pub_venue==curr_venue:
                        same_pub = True
                elif not pub_venue or not curr_venue:
                    if pub_year==curr_year:
                        same_pub = True
    if similar_title: # TODO: this logic may be problematic
        print('Similar titles are:{} | {}'.format(similar_title, query_title))
        print('\tAre they the same paper:', same_pub)
        print('\tPublished Year of two paper:', curr_year, pub_year)
        print('\tPublished venue of two paper:', curr_venue, pub_venue)
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
    
    print('Identified identical titles are:', query_title)
    print('\tAre they the same paper:', same_pub)
    # print('\tProcessed title', query_title)
    print('\tPublished Year of two paper:', pub_year, curr_year)
    print('\tPublished venue of two paper:', pub_venue, curr_venue)
    return same_pub
