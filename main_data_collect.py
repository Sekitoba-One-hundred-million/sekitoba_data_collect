import numpy as np
from tqdm import tqdm
from bs4 import BeautifulSoup

import SekitobaLibrary as lib
import SekitobaDataManage as dm

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

    return current_race_data

def race_data_collect():
    race_data_storage = dm.pickle_load( "race_data.pickle" )
    horce_url = {}

    if race_data_storage == None:
        race_data_storage = {}

    base_url = "https://race.netkeiba.com/race/shutuba.html?race_id="
    test_year = int( lib.test_years[-1] )

    for y in range( 2007, 2009 ):
        print( y )
        for p in range( 1, 11 ):
            print( p )
            for m in range( 1, 11 ):
                for d in range( 1, 13 ):
                    for r in range( 1, 13 ):        
                        race_id = str( y ) + num_check( str( p ) ) + num_check( str( m ) ) + num_check( str( d ) ) + num_check( str( r ) )
                        url = base_url + race_id                        
                        race_data = race_data_search( url, horce_url )
                        if len( race_data ) != 0:
                            race_data_storage[url] = race_data
                        else:
                            break
                        
    return race_data_storage, horce_url

def main():    
    update_race_data, horce_url = race_data_collect()
    race_data = dm.pickle_load( "race_data.pickle" )
    horce_url = {}

    for k in update_race_data.keys():
        race_data[k] = update_race_data[k]
        
        for horce_id in update_race_data[k].keys():
            horce_url[horce_id] = "https://db.netkeiba.com/horse/{}".format( horce_id )

    dm.pickle_upload( "race_data.pickle", race_data )
    horce_data_storage = dm.pickle_load( "horce_data_storage.pickle" )

    for horce_id in tqdm( horce_url.keys() ):
        if not horce_id in horce_data_storage:
            url = horce_url[horce_id]
            horce_data_storage[horce_id] = horse_data_collect( url )
    
    dm.pickle_upload( "horce_data_storage.pickle", horce_data_storage )
    
main()
