from tqdm import tqdm
from bs4 import BeautifulSoup

import sekitoba_library as lib
import sekitoba_data_manage as dm

def passing_get( soup ):    
    r, _ = lib.request( url )
    soup = BeautifulSoup( r.content, "html.parser" )
    
    tr_tag = soup.findAll( "tr" )
    result = {}

    for i in range( 0, len( tr_tag ) ):
        td_tag = tr_tag[i].findAll( "td" )
        
        if 2 < len( td_tag ) and td_tag[3].get( "class" ) != None \
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
        
    horce_url = dm.pickle_load( "horce_url.pickle" )
    url_data = []
    key_data = []

    for k in tqdm( horce_url.keys() ):
        horce_name = k.replace( " ", "" )


        try:
            a = result[horce_name]
        except:
            url = horce_url[k]            
            url_data.append( url )
            key_data.append( horce_name )

    add_data = lib.thread_scraping( url_data, key_data ).data_get( passing_get )
    dm.pickle_upload( "passing_data.pickle", result )

main()
