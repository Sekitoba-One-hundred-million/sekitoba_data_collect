from tqdm import tqdm
from bs4 import BeautifulSoup

import SekitobaLibrary as lib
import SekitobaDataManage as dm

def closs_get( url ):
    result = []

    r, _ = lib.request( url )
    soup = BeautifulSoup( r.content, "html.parser" )    
    div_tag = soup.findAll( "div" )

    for div in div_tag:
        class_name = div.get( "class" )
        
        if not class_name == None and class_name[0] == "blood_cross":
            tr_tag = div.findAll( "tr" )

            for tr in tr_tag:
                td_tag = tr.findAll( "td" )

                try:
                    name = td_tag[0].text
                    rate = float( td_tag[1].text.replace( "%", "" ) )
                    result.append( { "name": name, "rate": rate } )
                except:
                    continue

            break

    return result

def main():
    result = dm.pickle_load( "blood_closs_data.pickle" )
    result = {}
    
    horce_data_storage = dm.pickle_load( "horce_data_storage.pickle" )
    key_list = []
    url_list = []
    
    for k in horce_data_storage.keys():
        try:
            a = result[k]
        except:
            horce_id = k
            url = "https://db.netkeiba.com/horse/ped/" + horce_id
            url_list.append( url )
            key_list.append( k )

    add_data = lib.thread_scraping( url_list, key_list ).data_get( closs_get )

    for k in add_data.keys():
        result[k] = add_data[k]
    
    dm.pickle_upload( "blood_closs_data.pickle", result )
            
main()
