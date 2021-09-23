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

def html_analyze( url ):
    all_data = {}

    r, _ = lib.request( url )
    soup = BeautifulSoup( r.content, "html.parser" )
    td = soup.findAll( "td" )

    for i in range( 0, len( td ) ):
        td_class_name = td[i].get( "class" )

        if not td_class_name == None \
           and td_class_name[0] == "txt_c":
            data = {}

            try:
                data["one_rate"] = float( "0" + td[i+16].text )
                data["two_rate"] = float( "0" + td[i+17].text )
                data["three_rate"] = float( "0" + td[i+18].text )
            except:
                data["one_rate"] = 0
                data["two_rate"] = 0
                data["three_rate"] = 0

            try:
                data["siba_rate"] = float( td[i+13].text ) / float( td[i+12].text )
                data["date_rate"] = float( td[i+15].text ) / float( td[i+14].text )
            except:
                data["siba_rate"] = 0
                data["date_rate"] = 0
                
            all_data[td[i].text] = data

    return all_data

def url_create( base_url ):
    base_url = base_url.split( "/" )
    url = ""
        
    for i in range( 0, len( base_url ) - 1):
        url += base_url[i]
        url += "/"
            
        if i == 3:
            url += "result/" 

    return url
            
def main():
    result = dm.pickle_load( "trainer_data.pickle" )
    trainer_url = dm.pickle_load( "trainer_url.pickle" )

    if result == None:
        result = {}

    url_data = []
    key_data = []

    for k in tqdm( trainer_url.keys() ):
        base_url = trainer_url[k]

        try:
            a = result[k]
        except:            
            url_data.append( url_create( base_url ) )
            key_data.append( k )

    add_data = lib.thread_scraping( url_data, key_data ).data_get( html_analyze )

    for k in add_data.keys():
        result[k] = add_data[k]
    
    dm.pickle_upload( "trainer_data.pickle", result )

main()
    
