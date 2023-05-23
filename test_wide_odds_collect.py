import time
from tqdm import tqdm
from bs4 import BeautifulSoup
from selenium import webdriver

import sekitoba_library as lib
import sekitoba_data_manage as dm

def data_get( soup ):
    result = {}
    table_tag = soup.findAll( "table" )

    for table in table_tag:
        class_name = table.get( "class" )

        if not class_name == None and class_name[0] == "Odds_Table":
            tr_tag = table.findAll( "tr" )
            try:
                key_min_horce_num = lib.text_replace( tr_tag[0].text )
                lib.dic_append( result, key_min_horce_num, {} )
            except:
                continue
            
            for i in range( 1, len( tr_tag ) ):
                td_tag = tr_tag[i].findAll( "td" )
                
                if len( td_tag ) == 2:
                    key_max_horce_num = lib.text_replace( td_tag[0].text )
                    odds = lib.text_replace( td_tag[1].text )
                    try:
                        point = odds.index( "." ) + 2
                        min_odds = float( odds[0:point] )
                        max_odds = float( odds[point:len(odds)] )
                        result[key_min_horce_num][key_max_horce_num] = { "min": min_odds, "max": max_odds }
                    except:
                        continue
                    
    return result

def main():
    result = dm.pickle_load( "test_wide_odds.pickle" )
    
    if result == None:
        result = {}
        
    base_url = "https://race.netkeiba.com/odds/index.html?type=b5&race_id="
    driver = webdriver.Chrome()
    
    race_data = dm.pickle_load( "race_data.pickle" )
    url_data = []
    key_data = []
    check_race_id = []
    count = 0

    for k in race_data.keys():
        race_id = lib.id_get( k )
        year = race_id[0:4]
        
        if year in lib.test_years and not race_id in result:
            check_race_id.append( race_id )
            
    for race_id in tqdm( check_race_id ):
        count += 1
        url = base_url + race_id
        driver, _ = lib.driver_request( driver, url )
        time.sleep( 1 )
        html = driver.page_source.encode('utf-8')
        soup = BeautifulSoup( html, "html.parser" )
        result[race_id] = data_get( soup )

        if count % 100 == 0:
            dm.pickle_upload( "test_wide_odds.pickle", result )
            
    dm.pickle_upload( "test_wide_odds.pickle", result )

if __name__ == "__main__":
    main()
