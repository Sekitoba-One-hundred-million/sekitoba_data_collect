import time
import sys
from bs4 import BeautifulSoup

import library as lib
import data_manage as dm

def pace_get( url ):
    r, _ = lib.request( url )
    soup = BeautifulSoup( r.content, "html.parser" )    
    div_tag = soup.findAll( "div" )
    pace = ""

    for div in div_tag:
        class_name = div.get( "class" )

        if not class_name == None \
           and class_name[0] == "RapPace_Title":
            pace = div.find( "span" ).text.replace( " ", "" )
            break

    return pace

def main():
    result = dm.pickle_load( "pace_data.pickle" )
    
    if result == None:
        result = {}

    base_url =  "https://race.netkeiba.com/race/result.html?race_id="
    race_data = dm.pickle_upload( "race_data.pickle" )
    url_data = []
    key_data = []

    for k in race_data.keys():
        race_id = lib.id_get( k )

        try:
            a = result[race_id]
        except:
            url_data.append( url )
            key_data.append( race_id )

    add_data = lib.thread_scraping( url_data, key_data ).data_get( pace_get )

    for k in add_data.keys():
        result[k] = add_data[k]
    
    dm.pickle_upload( "pace_data.pickle", result )
    
main()
