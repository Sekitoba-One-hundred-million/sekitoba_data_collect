import numpy as np
from tqdm import tqdm
from bs4 import BeautifulSoup

import sekitoba_library as lib
import sekitoba_data_manage as dm

def num_check( num ):
    if len( num ) == 1:
        return "0" + num
    else:
        return num

def horse_data_collect( url ):
    horce_data = []

    r, _ = lib.request( url )
    soup = BeautifulSoup( r.content, "html.parser" )
    tr_tag = soup.findAll( "tr" )

    for i in range( 0, len( tr_tag ) ):
        td_tag = tr_tag[i].findAll( "td" )
        
        if 2 < len( td_tag ) and td_tag[3].get( "class" ) != None \
           and td_tag[3].get( "class" )[0] == "txt_right":
            data_list = []
            for r in range( 0, len( td_tag ) ):
                if r != 5 and r != 16 and r != 19 and ( r == 27 or r < 24 ):
                    data = td_tag[r].text.replace( "\n", "" )

                    if not r == 27:
                        data_list.append( data )
                    else:
                        try:
                            data_list.append( float( data ) )
                        except:
                            data_list.append( 0 )

            if len( data_list ) == 22:
                horce_data.append( data_list )
    
    return horce_data

def race_data_search( url, horce_url ):
    current_race_data = {}
    r, _ = lib.request( url )
    soup = BeautifulSoup( r.content, "html.parser" )
    span_tag = soup.findAll( "span" )
    
    for span in span_tag:
        class_name = span.get( "class" )

        if class_name != None\
           and class_name[0] == "HorseName":
            a_tag = span.find( "a" )

            if not a_tag == None:
                horce_name = a_tag.get( "title" )
                h_url = a_tag.get( "href" )
                horce_id = h_url.split( "/" )[-1]
                current_race_data[horce_id] = None
                horce_url[horce_id] = h_url

    return current_race_data, horce_url

def race_data_collect():
    race_data_storage = dm.pickle_load( "race_data.pickle" )
    horce_url = {}

    if race_data_storage == None:
        race_data_storage = {}

    base_url = "https://race.netkeiba.com/race/shutuba.html?race_id="

    for y in range( 2021, 2022 ):
        print( y )
        for p in range( 1, 11 ):
            for m in range( 1, 11 ):
                for d in range( 1, 13 ):
                    for r in range( 1, 13 ):        
                        race_id = str( y ) + num_check( str( p ) ) + num_check( str( m ) ) + num_check( str( d ) ) + num_check( str( r ) )
                        url = base_url + race_id
                        
                        try:
                            race_data_storage[url]
                        except:                        
                            race_data = race_data_search( url, horce_url )
                            print( url )
                            if len( race_data ) != 0:
                                race_data_storage[url] = race_data
                            else:
                                continue
                        
    return race_data_storage, horce_url

def main():    
    race_data, horse_url = race_data_collect()    
    dm.pickle_upload( "race_data.pickle", race_data )
    
    horse_data_storage = {}
    jockey_name_check = {}
    parent_name_data = {}
    parent_url = {}
    race_data_key = np.array( [] )

    for k in tqdm( horce_url.keys() ):
        url = horce_url[k]
        horse_data_storage[k] = horse_data_collect( url )
    
    dm.pickle_upload( "horce_data_storage.pickle", horse_data_storage )
    
main()
