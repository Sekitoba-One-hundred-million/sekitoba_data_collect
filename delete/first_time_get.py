import time
from bs4 import BeautifulSoup
from selenium import webdriver
from tqdm import tqdm

import sekitoba_library as lib
import sekitoba_data_manage as dm

def data_collect( data ):
    result = []
    count = 0
    
    r, _ = lib.request( data["url"], cookie = data["cookie"] )
    soup = BeautifulSoup( r.content, "html.parser" )    
    dl_tag = soup.findAll( "dl" )

    for dl in dl_tag:
        class_name = dl.get( "class" )

        if not class_name == None \
           and class_name[0] == "HorseList":
            dd_tag = dl.findAll( "dd" )
            dt_tag = dl.findAll( "dt" )

            for dt in dt_tag:
                class_name = dt.get( "class" )

                if not class_name == None \
                   and class_name[0] == "Horse02":
                    horce_name = dt.text.replace( " ", "" ).replace( "\n", "" )
                    result.append( { "name": horce_name, "time": [] } )

            for dd in dd_tag:
                class_name = dd.get( "class" )

                if not class_name == None \
                   and class_name[0] == "Past_Wrapper":
                    li_tag = dd.findAll( "li" )

                    for li in li_tag:
                        class_name = li.get( "class" )

                        if not class_name == None \
                           and class_name[0] == "Past":
                            span_tag = li.findAll( "span" )

                            for span in span_tag:
                                class_name = span.get( "class" )

                                if not class_name == None \
                                   and class_name[0] == "Data19":
                                    try:
                                        result[count]["time"].append( float( span.text.replace( "前", "" ) ) )
                                    except:
                                        continue
                                    
                    count += 1

    return result
    
def main():
    count = 0
    result = dm.pickle_load( "first_time.pickle" )

    if result == None:
        result = {}
    
    race_data = dm.pickle_upload( "race_data.pickle" )
    cookie = lib.netkeiba_login()
    key_list = []
    url_list = []

    for k in tqdm( race_data.keys() ):
        race_id = lib.id_get( k )

        try:
            result[race_id]
        except:
            url = "https://race.netkeiba.com/race/newspaper.html?race_id=" + race_id
            key_list.append( race_id )
            url_list.append( { "url": url, "cookie": cookie } )

    add_data = lib.thread_scraping( url_list, key_list ).data_get( data_collect )

    for k in add_data.keys():
        result[k] = add_data[k]    
    
    dm.pickle_upload( "first_time.pickle", result )
    
main()
