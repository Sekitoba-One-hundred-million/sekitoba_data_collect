import time
import datetime
from tqdm import tqdm
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

import SekitobaLibrary as lib
import SekitobaDataManage as dm

def data_get( driver, url ):
    xPath = "/html/body/div[1]/div[3]/div[2]/div[1]/div[3]/div[1]/div/div/div/select"
    driver, _ = lib.driverRequest( driver, url )
    time.sleep( 3 )
    select = Select( driver.find_element( By.XPATH, xPath ) )
    select.select_by_index( 3 )
    time.sleep( 3 )

    html = driver.page_source.encode('utf-8')
    soup = BeautifulSoup( html, "html.parser" )
    div_tag = soup.findAll( "div" )
    horce_num = -1

    for div in div_tag:
        class_name = div.get( "class" )

        if class_name == None or len( class_name ) == 0 or not class_name[0] == "Axis_Horse":
            continue

        horce_num = int( lib.textReplace( div.find( "span" ).text ) )

    table_tag = soup.findAll( "table" )
    odds_data = {}

    for table in table_tag:
        class_name = table.get( "class" )
        
        if class_name == None or len( class_name ) == 0 or not class_name[0] == "Odds_Table":
            continue

        tr_tag = table.findAll( "tr" )
        firstWaku = -1

        for tr in tr_tag:
            tr_class_name = tr.get( "class" )

            if tr_class_name is None or len( tr_class_name ) == 0 or not tr_class_name[0] == "col_label":
                continue

            firstWaku = int( lib.textReplace( tr.text ) )
            break


def main():
    driver = lib.driverStart()
    data_get( driver, "https://race.netkeiba.com/odds/index.html?type=b7&race_id=202405040501&housiki=c0")
    return
    result = {}
    race_data = dm.pickle_load( "race_data.pickle" )

    for k in tqdm( race_data.keys() ):
        race_id = lib.idGet( k )
        year = race_id[0:4]
        
        if not year in lib.test_years or race_id in result:
            continue

        url = "https://race.netkeiba.com/odds/index.html?type=b5&race_id={}&housiki=c0".format( race_id )
        result[race_id] = data_get( driver, url )

        if len( result ) % 100 == 0:
            dm.pickle_upload( "wide_odds_data.pickle", result )

    driver.quit()
    dm.pickle_upload( "wide_odds_data.pickle", result )

main()
    
