import time
from bs4 import BeautifulSoup
from selenium import webdriver
from tqdm import tqdm

import sekitoba_library as lib
import sekitoba_data_manage as dm

def first_time_get( soup ):
    result = []
    count = 0
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

    driver = webdriver.Chrome()
    driver = lib.login( driver )
    count = 0

    for k in tqdm( race_data.keys() ):
        race_id = lib.id_get( k )

        try:
            a = result[race_id]
        except:
            url = "https://race.netkeiba.com/race/newspaper.html?race_id=" + race_id
            driver, _ = lib.driver_request( driver, url )
            time.sleep( 2 )
            html = driver.page_source.encode('utf-8')
            soup = BeautifulSoup( html, "html.parser" )
            result[race_id] = first_time_get( soup )
            count += 1

        if count % 100 == 0:
            dm.pickle_upload( "first_time.pickle", result )
    
    dm.pickle_upload( "first_time.pickle", result )
    driver.close()
    
main()
