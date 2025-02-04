import time
import datetime
from tqdm import tqdm
from bs4 import BeautifulSoup
from selenium import webdriver

import SekitobaLibrary as lib
import SekitobaDataManage as dm
import SekitobaPsql as ps

def data_get( driver, url ):
    driver, _ = lib.driverRequest( driver, url )
    time.sleep( 1 )
    baseNum = 1
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
                    odds_text = lib.textReplace( td.text )
                    min_odds = ""
                    max_odds = ""
                    max_flag = False

                    for i in range( 0, len( odds_text ) ):
                        if not max_flag:
                            min_odds += odds_text[i]

                            if not i == 0 and odds_text[i-1] == ".":
                                max_flag = True
                        else:
                            max_odds += odds_text[i]

                    min_odds = float( min_odds )
                    max_odds = float( max_odds )
                except:
                    before_num = -1
                    continue

                if not before_num == -1:
                    instance_odds_data[before_num] = { "min": min_odds, "max": max_odds }
                    before_num = -1

        if len( instance_odds_data ) == 0:
            baseNum += 1
            continue

        odds_data[baseNum] = instance_odds_data
        baseNum += 1

    return odds_data

def main():
    driver = lib.driverStart()
    result = dm.pickle_load( "wide_odds_data.pickle" )
    raceIdList = ps.RaceData().get_all_race_id()

    for raceId in tqdm( raceIdList ):
        year = raceId[0:4]
        
        if not year in lib.test_years or raceId in result:
            continue

        url = "https://race.netkeiba.com/odds/index.html?type=b5&race_id={}&housiki=c0".format( raceId )
        result[raceId] = data_get( driver, url )

        if len( result ) % 100 == 0:
            dm.pickle_upload( "wide_odds_data.pickle", result )

    driver.quit()
    dm.pickle_upload( "wide_odds_data.pickle", result )

main()
    
