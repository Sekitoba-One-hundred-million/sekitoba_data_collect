from bs4 import BeautifulSoup

import SekitobaLibrary as lib
import SekitobaDataManage as dm

def time_get( url ):
    r,_  = lib.request( url )
    soup = BeautifulSoup( r.content, "html.parser" )
    div_tag = soup.findAll( "div" )
    time_data = {}
    time_data["hour"] = 0
    time_data["minute"] = 0
    
    for i in range( 0, len( div_tag ) ):
        class_name = div_tag[i].get( "class" )

        if not class_name == None \
           and class_name[0] == "RaceData01":
            text_data = div_tag[i].text.replace( "\n", "" )
            text_data = text_data.replace( " ", "" )
            split_text = text_data.split( "/" )
            time_str = split_text[0].replace( "発走", "" )
            
            try:
                time_data["hour"] = int( time_str.split( ":" )[0] )
                time_data["minute"] = int( time_str.split( ":" )[1] )
            except:
                return time_data
            
            break

    return time_data

def main():
    race_data = dm.pickle_load( "race_data.pickle" )
    url_list = []
    key_list = []

    for k in race_data.keys():
        url_list.append( k )
        key_list.append( lib.idGet( k ) )
        
    result = lib.thread_scraping( url_list, key_list ).data_get( time_get )
    dm.pickle_upload( "race_start_time.pickle", result )

main()
