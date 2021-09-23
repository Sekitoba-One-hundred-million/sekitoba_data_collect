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

#[ 勝率, 連対率, 複勝率 ]
def data_collect( url ):    
    r = requests.get( url )
    soup = BeautifulSoup( r.content, "html.parser" )
    jockey_data = {}
    
    td_tag = soup.findAll( "td" )

    for i in range( 0, len( td_tag ) ):
        class_name = td_tag[i].get( "class" )

        if not class_name == None \
           and class_name[0] == "txt_c":
            siba_rate = 0
            date_rate = 0

            try:
                siba_rate = float( td_tag[i+12].text.replace( ",", "" ) ) / float( td_tag[i+13].text.replace( ",", "" ) )
            except:
                siba_rate = 0

            try:
                date_rate = float( td_tag[i+14].text.replace( ",", "" ) ) / float( td_tag[i+15].text.replace( ",", "" ) )
            except:
                date_rate = 0

            try:
                jockey_data[td_tag[i].text] = [ float( td_tag[i+16].text ),
                                                float( td_tag[i+17].text ),
                                                float( td_tag[i+18].text ),
                                                siba_rate,
                                                date_rate ]
            except:
                break
    
    return jockey_data
        
def main():
    base_url = "https://db.netkeiba.com/jockey/result/"
    check_str = "/jockey/"
    result = {}

    jockey_name_url = dm.pickle_load( "jockey_name.pickle" )
    url_list = []
    key_list = []

    for k in jockey_name_url.keys():
        url_list.append( url )
        key_list.append( jockey_name_url[k] )

    result = lib.thread_scraping( url_list, key_list ).data_get( data_collect )
    dm.pickle_upload( "jockey_data.pickle", result )
    
main()
