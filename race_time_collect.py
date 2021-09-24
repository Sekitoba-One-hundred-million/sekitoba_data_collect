from tqdm import tqdm
from bs4 import BeautifulSoup

import sekitoba_library as lib
import sekitoba_data_manage as dm

def time_get( soup ):
    race_time = 0
    span_tag = soup.findAll( "span" )

    for span in span_tag:
        class_name = span.get( "class" )

        if not class_name == None \
          and class_name[0] == "RaceTime":
            try:
                race_time = lib.time( span.text )
                break
            except:
                continue
            
        
    return race_time

def dist_get( soup ):
    dist = 0
    div_tag = soup.findAll( "div" )

    for div in div_tag:
        class_name = div.get( "class" )

        if not class_name == None \
          and class_name[0] == "RaceData01":
            span = div.find( "span" )
            dist = int( lib.k_dist( span.text ) * 1000 )

            if not dist == 0:
                break

    return dist

def data_get( url ):
    result = {}
    r, _ = lib.request( url )
    soup = BeautifulSoup( r.content, "html.parser" )

    result["time"] = time_get( soup )
    result["dist"] = dist_get( soup )

def main():
    result = dm.pickle_load( "race_time_data.pickle" )

    if result == None:
        result = {}
        
    race_data = dm.pickle_load( "race_data.pickle" )
    url_data = []
    key_data = []

    for k in tqdm( race_data.keys() ):
        race_id = lib.id_get( k )
        url = "https://race.netkeiba.com/race/result.html?race_id=" + race_id

        try:
            a = result[race_id]
        except:
            url_data.append( url )
            key_data.append( race_id )


    add_data = lib.thread_scraping( url_data, key_data ).data_get( data_get )

    for k in add_data.keys():
        result[k] = add_data[k]
    
    dm.pickle_upload( "race_time_data.pickle", result )
       
    
main()
