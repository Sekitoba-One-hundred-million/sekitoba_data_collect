import time
from tqdm import tqdm
from bs4 import BeautifulSoup
from selenium import webdriver

import sekitoba_library as lib
import sekitoba_data_manage as dm

def first_time_get( soup ):
    result = []
    count = 0
    dl_tag = soup.findAll( "dl" )

    for dl in dl_tag:
        dl_class_name = dl.get( "class" )
        
        if not dl_class_name == None and not len( dl_class_name ) == 0 and dl_class_name[0] == "HorseList":
            horce_id = ""
            dt_tag = dl.findAll( "dt" )
            
            for dt in dt_tag:
                dt_class_name = dt.get( "class" )

                if not dt_class_name == None and not len( dt_class_name ) == 0 and dt_class_name[0] == "Horse02":
                    try:
                        href = dt.find( "a" ).get( "href" )
                        horce_id = href.split( "/" )[-2]
                    except:
                        continue

            if len( horce_id ) == 0:
                continue

            dd_tag = dl.findAll( "dd" )

            for dd in dd_tag:
                dd_class_name = dd.get( "class" )

                if not dd_class_name == None and len( dd_class_name ) == 3 and dd_class_name[0] == "Past_Wrapper":
                    li_tag = dd.findAll( "li" )
                    
                    for li in li_tag:
                        li_class_name = li.get( "class" )
                        
                        if not li_class_name == None and not len( li_class_name ) == 0 and li_class_name[0] == "Past":
                            div_tag = li.findAll( "div" )
                            
                            if not len( div_tag ) == 8:
                                continue

                            race_id = ""
                            span_tag = div_tag[2].findAll( "span" )

                            for span in span_tag:
                                span_class_name = span.get( "class" )
                                
                                if not span_class_name == None and not len( span_class_name ) == 0 and span_class_name[0] == "RaceName":
                                    print( span.find( "a" ).get( "href" ) )
                                    try:
                                        href = span.find( "a" ).get( "href" )
                                        race_id = href.split( "/" )[-2]
                                    except:
                                        continue

                            print( race_id )
            return 0

    return result

def main():
    result = {}#dm.pickle_load( "first_up3_halon.pickle" )
    base_url = "https://race.netkeiba.com/race/newspaper.html?race_id="
    race_data = dm.pickle_load( "race_data.pickle" )
    
    driver = webdriver.Chrome()
    driver = lib.login( driver )
    url = "https://race.netkeiba.com/race/newspaper.html?race_id=202204030612"
    driver, _ = lib.driver_request( driver, url )
    time.sleep( 3 )
    html = driver.page_source.encode('utf-8')
    soup = BeautifulSoup( html, "html.parser" )
    first_time_get( soup )
    return
    count = 1

    for k in tqdm( race_data.keys() ):
        race_id = lib.id_get( k )
        url = base_url + race_id
        driver, _ = lib.driver_request( driver, url )
        time.sleep( 1 )
        html = driver.page_source.encode('utf-8')
        soup = BeautifulSoup( html, "html.parser" )

        try:
            result[race_id]
        except:
            result[race_id] = first_time_get( soup )

        if count % 100:
            dm.pickle_upload( "first_up3_halon.pickle", result )

    driver.close()
    dm.pickle_upload( "first_up3_halon.pickle", result )
    
main()
