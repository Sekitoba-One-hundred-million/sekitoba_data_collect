import time
import copy
import datetime
from tqdm import tqdm
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

import SekitobaLibrary as lib
import SekitobaPsql as ps
import SekitobaDataManage as dm

def data_get( driver, url, horceNumList ):
    result = {}
    xPath = "/html/body/div[1]/div[3]/div[2]/div[1]/div[3]/div[1]/div/div/div/select"
    driver, _ = lib.driverRequest( driver, url )
    time.sleep( 3 )

    for horceNum in horceNumList:
        select = Select( driver.find_element( By.XPATH, xPath ) )
        select.select_by_index( horceNum )
        time.sleep( 2 )

        html = driver.page_source.encode('utf-8')
        soup = BeautifulSoup( html, "html.parser" )
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

            lib.dicAppend( odds_data, firstWaku, {} )

            for tr in tr_tag:
                tr_class_name = tr.get( "class" )

                if not tr_class_name is None:
                    continue

                secondWaku = -1
                odds = -1
                td_tag = tr.findAll( "td" )

                if not len( td_tag ) == 2:
                    continue

                try:
                    secondWaku = int( lib.textReplace( td_tag[0].text ) )
                    odds = float( lib.textReplace( td_tag[1].text ) )
                except:
                    continue

                odds_data[firstWaku][secondWaku] = odds

        result[horceNum] = copy.deepcopy( odds_data )

    return result

def main():
    result = dm.pickle_load( "triplet_odds_data.pickle" )

    if result is None:
        result = {}
    
    raceData = ps.RaceData()
    horceData = ps.HorceData()
    raceHorceData = ps.RaceHorceData()
    race_id_list = raceData.get_all_race_id()
    driver = lib.driverStart()
    simu_race_id_list = []

    for race_id in race_id_list:
        year = race_id[0:4]

        if not year in lib.simu_years:
            continue

        if race_id in result:
            continue

        simu_race_id_list.append( race_id )

    for race_id in tqdm( simu_race_id_list ):
        raceHorceData.get_all_data( race_id )

        if len( raceHorceData.horce_id_list ) == 0:
            continue

        raceData.get_all_data( race_id )
        ymd = { "year": raceData.data["year"], \
               "month": raceData.data["month"], \
               "day": raceData.data["day"] }
        horceNumList = []
        horceData.get_multi_data( raceHorceData.horce_id_list )

        for horce_id in raceHorceData.horce_id_list:
            current_data, past_data = lib.raceCheck( horceData.data[horce_id]["past_data"], ymd )
            cd = lib.CurrentData( current_data )

            if not cd.raceCheck():
                continue
            
            horceNumList.append( int( cd.horceNumber() ) )

        url = "https://race.netkeiba.com/odds/index.html?type=b7&race_id={}&housiki=c0".format( race_id )
        result[race_id] = data_get( driver, url, horceNumList )

        if len( result ) % 100 == 0:
            dm.pickle_upload( "triplet_odds_data.pickle", result )

    dm.pickle_upload( "triplet_odds_data.pickle", result )

if __name__ == "__main__":
    main()
