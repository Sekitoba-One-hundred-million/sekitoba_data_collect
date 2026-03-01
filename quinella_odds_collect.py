import time
import datetime
from tqdm import tqdm
from bs4 import BeautifulSoup
from selenium import webdriver

import SekitobaLibrary as lib
import SekitobaDataManage as dm
import SekitobaPsql as ps

def data_get( driver, url ):
    driver, _ = lib.driver_request( driver, url )
    time.sleep( 1 )
    base_num = 1
    html = driver.page_source.encode('utf-8')
    soup = BeautifulSoup( html, "html.parser" )      
    table_tag = soup.findAll( "table" )
    odds_data = {}

    for table in table_tag:
        class_name = table.get( "class" )
        
        if class_name == None or len( class_name ) == 0 or not class_name[0] == "Odds_Table":
            continue

        instance_odds_data = {}
        td_tag = table.findAll( "td" )
        before_num = -1

        for td in td_tag:
            class_name = td.get( "class" )

            if class_name == None:
                continue

            if len( class_name ) == 1 and class_name[0] == "Waku_Normal":
                try:
                    before_num = int( lib.text_replace( td.text ) )
                except:
                    continue

            if len( class_name ) == 2 and class_name[0] == "Odds" and class_name[1] == "Popular":
                try:
                    odds_text = lib.text_replace( td.text )
                    odds = float( odds_text )
                except:
                    before_num = -1
                    continue

                if not before_num == -1:
                    instance_odds_data[before_num] = odds
                    before_num = -1

        if len( instance_odds_data ) == 0:
            base_num += 1
            continue

        odds_data[base_num] = instance_odds_data
        base_num += 1

    return odds_data

def main():
    FILE_NAME = "quinella_odds_data.pickle"
    result = dm.pickle_load( FILE_NAME )

    if result == None:
        result = {}

    race_id_list = ps.RaceData().get_all_race_id()
    use_race_id_list = []

    for race_id in race_id_list:
        year = race_id[0:4]

        if year in lib.simu_years and ( not race_id in result or len( result[race_id] ) == 0 ):
            use_race_id_list.append( race_id )

    driver = lib.driver_start()

    for race_id in tqdm( use_race_id_list ):
        url = "https://race.netkeiba.com/odds/index.html?type=b4&race_id={}&housiki=c0".format( race_id )

        while 1:
            data = data_get( driver, url )

            if not len( data ) == 0:
                break
            else:
                driver = lib.driver_restart( driver )

        result[race_id] = data

        if len( result ) % 100 == 0:
            dm.pickle_upload( FILE_NAME, result )

    driver.quit()
    dm.pickle_upload( FILE_NAME, result )

if __name__ == "__main__":
    main()
