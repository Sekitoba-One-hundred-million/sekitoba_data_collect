from bs4 import BeautifulSoup
import requests

import sekitoba_library as lib
import sekitoba_data_manage as dm

def data_collect( data ):
    result = {}
    r, _ = lib.request( data["url"], cookie = data["cookie"] )
    soup = BeautifulSoup( r.content, "html.parser" )
    tr_tag = soup.findAll( "tr" )

    for i in range( 0, len( tr_tag ) ):
        td_tag = tr_tag[i].findAll( "td" )
        
        if 2 < len( td_tag ) and td_tag[3].get( "class" ) != None \
           and td_tag[3].get( "class" )[0] == "txt_right":
            time_index = td_tag[19].text.replace( "\n", "" ).replace( " ", "" )
            day_key = td_tag[0].text.replace( "\n", "" ).replace( " ", "" )

            try:
                result[day_key] = float( time_index )
            except:
                result[day_key] = 0

    return result

def main():    
    cookie = lib.netkeiba_login()
    horce_data = dm.pickle_load( "horce_data_storage.pickle" )
    key_list = []
    url_list = []

    for k in horce_data.keys():
        key_list.append( k )
        url = "https://db.netkeiba.com/horse/" + k
        url_list.append( { "url": url, "cookie": cookie } )

    add_data = lib.thread_scraping( url_list, key_list ).data_get( data_collect )
    result = dm.pickle_load( "time_index_data.pickle" )

    if result == None:
        result = {}

    for k in add_data.keys():
        result[k] = add_data[k]
        
    dm.pickle_upload( "time_index_data.pickle", result )

if __name__ == "__main__":
    main()
    
