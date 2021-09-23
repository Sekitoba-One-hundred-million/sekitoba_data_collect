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

def data_collect( url ):    
    r, _ = lib.request( url )
    soup = BeautifulSoup( r.content, "html.parser" )
    jockey_data = {}
    
    td_tag = soup.findAll( "td" )

    for i in range( 0, len( td_tag ) ):
        class_name = td_tag[i].get( "class" )

        if not class_name == None \
           and class_name[0] == "txt_c":

            try:
                money_text = str( td_tag[i+19].text ).replace( ",", "" )
                jockey_data[td_tag[i].text] = float( money_text )
            except:
                jockey_data[td_tag[i].text] = 0
    
    return jockey_data
        
def main():
    base_url = "https://db.netkeiba.com/jockey/result/"
    check_str = "/jockey/"
    result = {}

    jockey_name_url = dm.pickle_load( "jockey_name.pickle" )
    url_data = []
    key_data = []

    for k in tqdm( jockey_name_url.keys() ):
        base = k.split( "/" )
        url = base_url + base[4]
        url_data.append( url )
        key_data.append( jockey_name_url[k] )

    result = lib.thread_scraping( url_data, key_data ).data_get( data_collect )
    lib.pickle_save( "jockey_money_data.pickle", result )
    
main()
