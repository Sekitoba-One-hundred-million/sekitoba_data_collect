import json
from bs4 import BeautifulSoup
import requests

import SekitobaPsql as ps
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
            baba_index = td_tag[16].text.replace( "\n", "" ).replace( " ", "" )
            day_key = td_tag[0].text.replace( "\n", "" ).replace( " ", "" )

            try:
                result[day_key] = float( baba_index )
            except:
                result[day_key] = 0

    return result

def main():
    result = {}
    cookie = lib.netkeibaLogin()
    horce_data = dm.pickle_load( "horce_data_storage.pickle" )
    key_list = []
    url_list = []

    for k in horce_data.keys():
        try:
            year = int( k[0:4] )
        except:
            continue
        
        if 2009 < year:
            continue
        
        key_list.append( k )
        url = "https://db.netkeiba.com/horse/" + k
        url_list.append( { "url": url, "cookie": cookie } )

    result = lib.thread_scraping( url_list, key_list ).data_get( data_collect )

    for horce_id in result.keys():
        ps.HorceData().update_data( "baba_index", json.dumps( result[horce_id], ensure_ascii = False ), horce_id )
        
    dm.pickle_upload( "baba_index_data.pickle", result )

if __name__ == "__main__":
    main()
    
