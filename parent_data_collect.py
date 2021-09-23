import requests
import pickle
import sys
import math
import numpy as np
from tqdm import tqdm
from urllib.request import urlopen
from bs4 import BeautifulSoup
import chardet

sys.path.append( "../" )

import data_manage as dm
import library as lib

def parent_data_get( urls ):
    result = {}
    result["father"] = {}
    result["father"]["dist"] = 0
    result["father"]["race_kind"] = 0
    result["father"]["rank"] = 0
    result["father"]["diff"] = 0
    result["father"]["up_time"] = 0
    
    result["mother"] = {}
    result["mother"]["dist"] = 0
    result["mother"]["race_kind"] = 0
    result["mother"]["rank"] = 0
    result["mother"]["diff"] = 0
    result["mother"]["up_time"] = 0
    
    for k in urls.keys():
        count = 0
        dist_class = {}
        
        r, _ = lib.request( urls[k] )
        soup = BeautifulSoup( r.content, "html.parser" )
        tr_tag = soup.findAll( "tr" )
    
        for i in range( 0, len( tr_tag ) ):
            td_tag = tr_tag[i].findAll( "td" )
        
            if 2 < len( td_tag ) and td_tag[3].get( "class" ) != None \
            and td_tag[3].get( "class" )[0] == "txt_right":
                try:
                    dist, race_kind = lib.dist( td_tag[14].text.replace( "\n", "" ) )
                    result[k]["dist"] += dist
                    result[k]["race_kind"] += race_kind
                    result[k]["rank"] += lib.data_check( td_tag[11].text.replace( "\n", "" ) )
                    result[k]["diff"] += lib.data_check( td_tag[18].text.replace( "\n", "" ) )
                    result[k]["up_time"] += lib.data_check( td_tag[22].text.replace( "\n", "" ) )
                    count += 1
                except:
                    continue

        if not count == 0:
            for kk in result[k].keys():
                result[k][kk] /= count

    return result
    
def parent_url_get( url ):
    result = {}
    result["father"] = ""
    result["mother"] = ""
    
    r, _ = lib.request( url )
    soup = BeautifulSoup( r.content, "html.parser" )
    td_tag = soup.findAll( "td" )

    for td in td_tag:
        rowspan = td.get( "rowspan" )

        if not rowspan == None \
          and rowspan == "2":
            a = td.find( "a" )
            p_url = "https://db.netkeiba.com/horse/" + a.get( "href" ).split( "/" )[3]
            
            if len( result["father"] ) == 0:
                result["father"] = p_url
            else:
                result["mother"] = p_url

    return result

def main():
    parent_url_data = dm.pickle_load( "parent_url_data.pickle" )
    url_list = []
    key_list = []

    if parent_url_data == None:
        horce_url = dm.pickle_load( "horce_url.pickle" )
        for k in horce_url.keys():
            horce_name = k.replace( " ", "" )
            url_list.append( horce_url[k] )
            key_list.append( horce_name )


        parent_url_data = lib.thread_scraping( url_list, key_list ).data_get( parent_url_get )
        dm.pickle_upload( "parent_url_data.pickle", parent_url_data )

    url_list.clear()
    key_list.clear()
    
    for k in parent_url_data.keys():
        url_list.append( parent_url_data[k] )
        key_list.append( k )

    parent_data = lib.thread_scraping( url_list, key_list ).data_get( parent_data_get )
    dm.pickle_upload( "parent_data.pickle", parent_data )
    
    
main()
