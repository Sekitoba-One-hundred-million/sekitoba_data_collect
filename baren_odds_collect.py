import time
import datetime
from tqdm import tqdm
from bs4 import BeautifulSoup
from selenium import webdriver
import timeout_decorator

import SekitobaLibrary as lib
import SekitobaDataManage as dm

def data_get( driver, url ):
    driver, check = lib.driverRequest( driver, url )

    if not check:
        return None
    
    time.sleep( 1 )
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
                    before_num = int( lib.textReplace( td.text ) )
                except:
                    continue

            if len( class_name ) == 2 and class_name[0] == "Odds" and class_name[1] == "Popular":
                try:
                    odds = float( lib.textReplace( td.text ) )
                except:
                    before_num = -1
                    continue

                if not before_num == -1:
                    instance_odds_data[before_num] = odds
                    before_num = -1

        if len( instance_odds_data ) == 0:
            continue
        
        base_num = min( instance_odds_data.keys() ) - 1
        odds_data[base_num] = instance_odds_data

    return odds_data

@timeout_decorator.timeout( 10 )
def main( result ):
    base_url = "https://race.netkeiba.com/odds/index.html?type=b4&race_id="
    driver = webdriver.Chrome()
    race_data = dm.pickle_load( "race_data.pickle" )

    for k in tqdm( race_data.keys() ):
        race_id = lib.idGet( k )
        year = race_id[0:4]
        
        if not year in lib.test_years:
            continue

        if race_id in result:
            continue

        url = "https://race.netkeiba.com/odds/index.html?type=b4&race_id={}&housiki=c0".format( race_id )
        odds_data = data_get( driver, url )

        if odds_data == None:
            return False
        
        result[race_id] = odds_data

        if len( result ) % 100 == 0:
            dm.pickle_upload( "baren_odds_data.pickle", result )

    driver.quit()
    dm.pickle_upload( "baren_odds_data.pickle", result )
    return True

if __name__ == "__main__":
    result = dm.pickle_load( "baren_odds_data.pickle" )
    print( len( result ) )
    
    while 1:
        check = main( result )

        if check:
            break

        print( len( result ) )
        dm.pickle_upload( "baren_odds_data.pickle", result )
