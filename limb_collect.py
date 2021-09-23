import time
import pickle
from bs4 import BeautifulSoup
from selenium.webdriver.common.alert import Alert
from selenium import webdriver
from tqdm import tqdm
import sys

sys.path.append( "../" )

import library as lib
import data_manage as dm

def html_analyze( html ):
    result = {}
    soup = BeautifulSoup( html, "html.parser" )
    dt_tag = soup.findAll( "dt" )

    for i in range( 0, len( dt_tag ) ):
        class_name = dt_tag[i].get( "class" )

        if not class_name == None \
           and class_name[0] == "Horse02":
            horse_name = dt_tag[i].text.replace( "\n", "" )
            horse_name = horse_name.replace( " ", "" )
            div_class = dt_tag[i+6].find( "div" ).get( "class" )
            result[horse_name] = {}
            
            try:
                if div_class[1] == "Type01":
                    result[horse_name] = 1
                elif div_class[1] == "Type02":
                    result[horse_name] = 2
                elif div_class[1] == "Type03":
                    result[horse_name] = 3
                elif div_class[1] == "Type04":
                    result[horse_name] = 4
                else:
                    result[horse_name] = 0                    
            except:
                result[horse_name] = 0

    return result

def main():
    result = dm.pickle_load( "limb_data.pickle" )
    
    if result == None:
        result = {}
    
    count = 0
    base_url = "https://race.netkeiba.com/race/newspaper.html?race_id="

    race_data = dm.pickle_load( "race_data.pickle" )

    driver = webdriver.Chrome()
    driver = lib.login( driver )
    
    for k in tqdm( race_data.keys() ):
        count += 1
        race_id = lib.id_get( k )
        
        try:
            a = result[race_id]
        except:
            url = base_url + race_id + "&rf=shutuba_submenu"
            driver, _ = lib.driver_request( driver, url )
            time.sleep( 1 )
            html = driver.page_source.encode('utf-8')
            data = html_analyze( html )
            result[race_id] = data
            
        if count % 100 == 0:
            dm.pickle_upload( "limb_data.pickle", result )

    dm.pickle_upload( "limb_data.pickle", result )
    driver.quit()

main()
