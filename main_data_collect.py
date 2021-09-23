import requests
import pickle
import sys
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

def write_data( horse_data_storage ):
    d = "../database/"
    for k in horse_data_storage.keys():
        f = open( k + ".txt", mode="w" )

        for day_key in horse_data_storage[k].keys():
            f.write( day_key )
            f.write( " " )
            for i in range( 0, len( horse_data_storage[k][day_key]) ):
                f.write( horse_data_storage[k][day_key][i] )
                f.write( " " )
            f.write( "\n" )
        f.close()
    
def horse_data_collect( url, jockey_name_check ):
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
                #print( td_tag[r], r )
                if r != 5 and r != 16 and r != 19 and ( r == 27 or r < 24 ):
                    data = td_tag[r].text.replace( "\n", "" )

                    if not td_tag[r].find( "a" ) == None:
                        check_url = td_tag[r].find( "a" ).get( "href" )
                        check = check_url.split( "/" )
                        j_name = td_tag[r].find( "a" ).get( "title" )

                        if len( check ) >= 2 \
                           and check[1] == "jockey":
                            jockey_url = "https://db.netkeiba.com" + check_url

                            try:
                                data = jockey_name_check[jockey_url]
                            except:
                                jockey_name = j_name

                                if not len( jockey_name ) == 0:
                                    data = jockey_name
                                    jockey_name_check[jockey_url] = jockey_name

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

def race_data_collect():
    horse_url = {}
    race_data_storage = {}
    base_url = "https://race.netkeiba.com/race/shutuba.html?race_id="

    for y in range( 2009, 2021 ):
        print( y )
        for p in range( 1, 11 ):
            for m in range( 1, 11 ):
                for d in range( 1, 13 ):
                    for r in range( 1, 13 ):
                        race_id = str( y ) + num_check( str( p ) ) + num_check( str( m ) ) + num_check( str( d ) ) + num_check( str( r ) )
                        url = base_url + race_id
                        race_data, horse_url = race_data_search( url, horse_url )

                        if len( race_data ) != 0:
                            race_data_storage[ url ] = race_data
                        else:
                            continue
                        
    return race_data_storage, horse_url


def race_data_search( url, horse_url ):
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
                current_race_data[ horce_name ] = []
                hore_url[ horce_name ] = h_url

    return current_race_data, hore_url

def number1_rate( test_cace, race_data ):
    rate = 0.0
    
    for i in range( 0, len( test_cace ) ):
        for k in race_data[test_cace[i]].keys():
            if race_data[test_cace[i]][k][0] == "1":
                if race_data[test_cace[i]][k][9] == "1":
                    rate += 1
                break

    print( rate / len( test_cace ) )    


def main():
    #race_data, horse_url = race_data_collect()
    
    #dm.pickle_upload( "horce_url.pickle", horse_url )
    #dm.pickle_upload( "race_data.pickle", race_data )
    race_data = dm.pickle_load( "race_data.pickle" )
    horce_url = dm.pickle_load( "horce_url.pickle" )
    
    horse_data_storage = {}
    jockey_name_check = {}
    parent_name_data = {}
    parent_url = {}
    race_data_key = np.array( [] )

    for k in tqdm( horce_url.keys() ):
        url = horce_url[k]
        horce_name = k
        horce_name = horce_name.replace( " ", "" )
        horse_data_storage[ horce_name ] = horse_data_collect( url,
                                                               jockey_name_check )
    
    #write_data( horse_data_storage )
    dm.pickle_upload( "jockey_name.pickle", jockey_name_check )
    dm.pickle_upload( "horce_data_storage.pickle", horse_data_storage )
    
main()
