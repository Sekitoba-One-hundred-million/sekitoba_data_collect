import sys
from bs4 import BeautifulSoup

import SekitobaPsql as ps
import SekitobaLibrary as lib
import SekitobaDataManage as dm

def data_collect( url ):
    horce_sex = 0
    r, _ = lib.request( url )
    soup = BeautifulSoup( r.content, "html.parser" )
    div = soup.findAll( "div" )

    for i in range( 0, len( div ) ):
        div_class_name = div[i].get( "class" )
        if not div_class_name == None \
           and div_class_name[0] == "horse_title":
            p = div[i].findAll( "p" )

            for r in range( 0, len( p ) ):
                p_class_name = p[r].get( "class" )
                if not p_class_name == None \
                   and p_class_name[0] == "txt_01":
                    for t in range( 0, len( p[r].text ) ):
                        if p[r].text[t] == "牡":
                            horce_sex = 1
                        elif p[r].text[t] == "牝":
                            horce_sex = 2                        
                    break
            break

    return horce_sex

def main():
    result = dm.pickle_load( "horce_sex_data.pickle" )

    if result == None:
        result = {}
    
    horce_data = dm.pickle_load( "horce_data_storage.pickle" )
    base_url = "https://db.netkeiba.com/horse/"
    url_list = []
    key_list = []

    for horce_id in horce_data.keys():
        if horce_id in result:
            continue
        
        url = base_url + horce_id
        key_list.append( horce_id )
        url_list.append( url )

    add_data = lib.thread_scraping( url_list, key_list ).data_get( data_collect )

    for horce_id in add_data.keys():
        result[horce_id] = add_data[horce_id]
        ps.HorceData().update_data( "sex", add_data[horce_id], horce_id )
        
    dm.pickle_upload( "horce_sex_data.pickle", result )

main()
