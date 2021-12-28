from bs4 import BeautifulSoup
import requests

import sekitoba_library as lib
import sekitoba_data_manage as dm

def data_collect( data ):
    result = {}
    count = 1
    r, _ = lib.request( data["url"], cookie = data["cookie"] )
    soup = BeautifulSoup( r.content, "html.parser" )
    ul_tag = soup.findAll( "ul" )

    for ul in ul_tag:
        class_name = ul.get( "class" )

        if not class_name == None \
          and class_name[0] == "TrainingTimeDataList":            
            li_tag = ul.findAll( "li" )
            key = str( int( count ) )           
            lib.dic_append( result, key, { "time": [], "wrap": [] } )
            count += 1
            
            for li in li_tag:
                text_list = li.text.replace( ")", "" ).split( "(" )

                if not len( text_list ) == 2:
                    continue

                train_time = text_list[0]
                wrap_time = text_list[1]

                try:
                    result[key]["time"].append( float( train_time ) )
                    result[key]["wrap"].append( float( wrap_time ) )
                except:
                    continue

    return result

def main():
    race_data = dm.pickle_load( "race_data.pickle" )
    cookie = lib.netkeiba_login()
    key_list = []
    url_list = []

    for k in race_data.keys():
        race_id = lib.id_get( k )
        url = "https://race.netkeiba.com/race/oikiri.html?race_id=" + race_id
        key_list.append( race_id )
        url_list.append( { "url": url, "cookie": cookie } )

    result = lib.thread_scraping( url_list, key_list ).data_get( data_collect )
    dm.pickle_upload( "train_time_data.pickle", result )

if __name__ == "__main__":
    main()
