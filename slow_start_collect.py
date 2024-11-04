from bs4 import BeautifulSoup
import requests

import SekitobaLibrary as lib
import SekitobaDataManage as dm

def data_collect( data ):
    result = {}
    r, _ = lib.request( data["url"], cookie = data["cookie"] )
    soup = BeautifulSoup( r.content, "html.parser" )

    tr_tag = soup.findAll( "tr" )

    for i in range( 0, len( tr_tag ) ):
        td_tag = tr_tag[i].findAll( "td" )
        
        if 2 < len( td_tag ) and td_tag[3].get( "class" ) != None \
           and td_tag[3].get( "class" )[0] == "txt_right":
            try:
                day_key = td_tag[0].text.replace( "\n", "" ).replace( " ", "" )
                slow_start_str = td_tag[25].text.replace( "\n", "" ).replace( " ", "" )
            except:
                continue

            slow_start = False
            
            if slow_start_str == "出遅れ":
                slow_start = True

            result[day_key] = slow_start

    return result

def main():
    file_name = "slow_start_data.pickle"
    cookie = lib.netkeibaLogin()
    horce_data = dm.pickle_load( "horce_data_storage.pickle" )
    key_list = []
    url_list = []

    for k in horce_data.keys():
        key_list.append( k )
        url = "https://db.netkeiba.com/horse/" + k
        url_list.append( { "url": url, "cookie": cookie } )

    add_data = lib.thread_scraping( url_list, key_list ).data_get( data_collect )
    result = dm.pickle_load( file_name )

    if result == None:
        result = {}

    for k in add_data.keys():
        result[k] = add_data[k]

    dm.pickle_upload( file_name, result )
    

if __name__ == "__main__":
    main()
