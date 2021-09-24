import time
from tqdm import tqdm
from bs4 import BeautifulSoup
from selenium import webdriver

import sekitoba_library as lib
import sekitoba_data_manage as dm

def first_time_get( soup, result ):
    count = 0
    dl_tag = soup.findAll( "dl" )

    for dl in dl_tag:
        class_name = dl.get( "class" )

        if not class_name == None \
           and class_name[0] == "HorseList":
            dd_tag = dl.findAll( "dd" )

            for dd in dd_tag:
                class_name = dd.get( "class" )

                if not class_name == None \
                   and len( class_name ) == 3 \
                   and class_name[0] == "Past_Wrapper" \
                   and class_name[1] == "HorseListSort":
                    li_tag = dd.findAll( "li" )

                    for li in li_tag:
                        class_name = li.get( "class" )

                        if not class_name == None \
                           and class_name[0] == "Past":
                            div_box = li.find( "div" )
                            div_tag = div_box.findAll( "div" )
                            if len( div_tag ) >= 6:
                                race_id_tag = div_tag[1]                            
                                horce_num_tag = div_tag[2]
                                first_time_tag = div_tag[5]
                                time_span = first_time_tag.find( "span" )
                                num_span = horce_num_tag.findAll( "span" )
                                try:
                                    horce_num = str( int( num_span[3].text.replace( "番", "" ) ) )
                                    race_id = race_id_tag.find( "a" ).get( "href" ).split( "/" )[4]
                                    first_time = float( time_span.text.replace( "前", "" ) )
                                    lib.dic_append( result, race_id, {} )
                                    lib.dic_append( result[race_id], horce_num, 0 )
                                    result[race_id][horce_num] = first_time
                                except:
                                    continue


def main():
    result = {}#dm.pickle_load( "first_yp3_halon.pickle" )
    base_url = "https://race.netkeiba.com/race/newspaper.html?race_id="
    race_data = dm.pickle_load( "race_data.pickle" )
    
    driver = webdriver.Chrome()
    driver = lib.login( driver )
    count = 1

    for k in tqdm( race_data.keys() ):
        race_id = lib.id_get( k )
        y = race_id[0:4]
        url = base_url + race_id
        driver, _ = lib.driver_request( driver, url )
        time.sleep( 1 )
        html = driver.page_source.encode('utf-8')
        soup = BeautifulSoup( html, "html.parser" )
        first_time_get( soup, result )

    driver.close()
    dm.pickle_upload( "first_yp3_halon.pickle", result )
    
def test():
    race_data = dm.pickle_load( "race_data.pickle" )
    test_data = dm.pickle_load( "first_yp3_halon.pickle" )

    for k in race_data.keys():
        race_id = lib.id_get( k )
        y = race_id[0:4]
        if y == "2015":
            try:
                test_data[race_id]
                print( race_id, test_data[race_id].keys() )
            except:
                print( race_id )

main()
