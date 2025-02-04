import time
import datetime
from tqdm import tqdm
from bs4 import BeautifulSoup
from selenium import webdriver

import SekitobaLibrary as lib
import SekitobaPsql as ps
import SekitobaDataManage as dm

def data_get( driver, url ):
    driver, _ = lib.driverRequest( driver, url )
    time.sleep( 1 )
    html = driver.page_source.encode('utf-8')
    soup = BeautifulSoup( html, "html.parser" )      
    table_tag = soup.findAll( "table" )
    base_num = 1
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
                    before_num = int( lib.textReplace( td.text ) )
                except:
                    continue

            if len( class_name ) == 2 and class_name[0] == "Odds" and class_name[1] == "Popular":
                try:
                    odds_text = lib.textReplace( td.text )
                    odds = float( odds_text )
                except:
                    before_num = -1
                    continue

                if not before_num == -1:
                    instance_odds_data[before_num] = odds
                    before_num = -1

        if len( instance_odds_data ) == 0:
            continue

        odds_data[base_num] = instance_odds_data
        base_num += 1

    return odds_data

def main():
    race_id_list = ps.RaceData().get_all_race_id()
    driver = lib.driverStart()
    result = {}

    for race_id in tqdm( race_id_list ):
        year = race_id[0:4]
        
        if not year in lib.test_years or race_id in result:
            continue

        url = "https://race.netkeiba.com/odds/index.html?type=b6&race_id={}&housiki=c0".format( race_id )
        result[race_id] = data_get( driver, url )

        if len( result ) % 100 == 0:
            dm.pickle_upload( "quinella_odds_data.pickle", result )

    driver.quit()
    dm.pickle_upload( "quinella_odds_data.pickle", result )

main()
    
