from bs4 import BeautifulSoup

import sekitoba_library as lib
import sekitoba_data_manage as dm

def data_collect( url ):
    result = {}
    r, _ = lib.request( url )
    soup = BeautifulSoup( r.content, "html.parser" )    

    tr_tag = soup.findAll( "tr" )

    for i in range( 0, len( tr_tag ) ):
        td_tag = tr_tag[i].findAll( "td" )
        
        if 2 < len( td_tag ) and td_tag[3].get( "class" ) != None \
           and td_tag[3].get( "class" )[0] == "txt_right":        
            day_key = td_tag[0].text.replace( "\n", "" ).replace( " ", "" )
            try:
                jockey_id = td_tag[12].find( "a" ).get( "href" ).split( "/" )[2]
                result[day_key] = jockey_id
            except:
                result[day_key] = None

    return result
            

def main():
    horce_data_storage = dm.pickle_load( "horce_data_storage.pickle" )

    key_list = []
    url_list = []
    base_url = "https://db.netkeiba.com/horse/"

    for horce_id in horce_data_storage.keys():
        key_list.append( horce_id )
        url_list.append( base_url + horce_id )

    result = lib.thread_scraping( url_list, key_list ).data_get( data_collect )
    dm.pickle_upload( "jockey_id_data.pickle", result )

if __name__ == "__main__":
    main()
