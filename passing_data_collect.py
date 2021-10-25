from tqdm import tqdm
from bs4 import BeautifulSoup

import sekitoba_library as lib
import sekitoba_data_manage as dm

def passing_get( url ):
    print( url )
    r, _ = lib.request( url )
    soup = BeautifulSoup( r.content, "html.parser" )
    
    tr_tag = soup.findAll( "tr" )
    result = {}

    for i in range( 0, len( tr_tag ) ):
        td_tag = tr_tag[i].findAll( "td" )

        if 20 < len( td_tag ) and td_tag[3].get( "class" ) != None \
           and td_tag[3].get( "class" )[0] == "txt_right":
            day = td_tag[0].text.replace( " ", "" )
            passing_data = td_tag[20].text.replace( " ", "" )

            if not len( day ) == 0 \
               and not len( passing_data ) == 0:
                result[day] = passing_data                           

    return result    

def main():
    result = dm.pickle_load( "passing_data.pickle" )
    
    if result == None:
        result = {}
        
    horce_id_dict = dm.pickle_load( "horce_id_dict.pickle" )
    url_data = []
    key_data = []

    for k in tqdm( horce_id_dict.keys() ):
        horce_id = k

        try:
            result[horce_id]
        except:
            url = "https://db.netkeiba.com/horse/" + horce_id
            url_data.append( url )
            key_data.append( horce_id )

    add_data = lib.thread_scraping( url_data, key_data ).data_get( passing_get )

    for k in add_data.keys():
        result[k] = add_data[k]
        
    dm.pickle_upload( "passing_data.pickle", result )

main()
