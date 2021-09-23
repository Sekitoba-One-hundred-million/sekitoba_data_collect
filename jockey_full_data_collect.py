import requests
import pickle
import sys
import math
import numpy as np
from tqdm import tqdm
from bs4 import BeautifulSoup

sys.path.append( "../" )

import library as lib
import data_manage as dm

def data_collect( base_url ):
    result = {}
    count = 1
    
    while 1:
        url = base_url + str( count )
        r,_  = lib.request( url )
        soup = BeautifulSoup( r.content, "html.parser" )
        
        tbody = soup.find( "tbody" )
        if tbody == None:
            break
        
        tr_tag = tbody.findAll( "tr" )

        if len( tr_tag ) == 0:
            break
        else:
            for tr in tr_tag:
                td_tag = tr.findAll( "td" )
                key_day = td_tag[0].text
                key_race_num = td_tag[3].text                
                lib.dic_append( result, key_day, {} )
                lib.dic_append( result[key_day], key_race_num, {} )
                result[key_day][key_race_num]["place"] = td_tag[1].text
                result[key_day][key_race_num]["weather"] = td_tag[2].text
                result[key_day][key_race_num]["all_horce_num"] = td_tag[6].text
                result[key_day][key_race_num]["flame_num"] = td_tag[7].text
                result[key_day][key_race_num]["horce_num"] = td_tag[8].text
                result[key_day][key_race_num]["odds"] = td_tag[9].text
                result[key_day][key_race_num]["popular"] = td_tag[10].text
                result[key_day][key_race_num]["rank"] = td_tag[11].text
                result[key_day][key_race_num]["weight"] = td_tag[13].text
                result[key_day][key_race_num]["dist"] = td_tag[14].text
                result[key_day][key_race_num]["baba"] = td_tag[15].text
                result[key_day][key_race_num]["time"] = td_tag[16].text
                result[key_day][key_race_num]["diff"] = td_tag[17].text
                
        count += 1
    
    return result
        
def main():
    base_url = "https://db.netkeiba.com/?pid=jockey_detail&id="
    check_str = "/jockey/"
    data_storage = {}

    url_list = []
    key_list = []
    jockey_name_url = dm.pickle_load( "jockey_name.pickle" )

    for k in jockey_name_url.keys():
        base = k.split( "/" )
        url = base_url + base[4] + "&page="
        url_list.append( url )
        key_list.append( jockey_name_url[k] )

    data_storage = lib.thread_scraping( url_list, key_list ).data_get( data_collect )
    dm.pickle_upload( "jockey_full_data.pickle", data_storage )
    
main()
