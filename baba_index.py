from bs4 import BeautifulSoup
from selenium import webdriver
from tqdm import tqdm

import sekitoba_library as lib
import sekitoba_data_manage as dm

def html_analyze( soup ):
    result = {}
    baba_index_data = []
    day_list = []
    place_list = []
    cource_data = []
    check = False
    td_tag = soup.findAll( "td" )

    for i in range( 0, len( td_tag ) ):
        class_name = td_tag[i].get( "class" )
        a = td_tag[i].find( "a" )

        if not a == None:
            href_name = a.get( "href" )

            if not href_name == None \
               and "/race/list/" in href_name:
                day = td_tag[i].text
                
                try:
                    baba_text = td_tag[i+16].text
                    baba_text = baba_text.replace( "\n", "" )
                    baba_text = baba_text.replace( " ", "" )
                    result[day] = float( baba_text )
                except:
                    result[day] = 0

    return result

def main():
    count = 0
    result = {}
    horce_url = dm.pickle_load( "horce_url.pickle" )
    
    driver = webdriver.Chrome()
    driver = lib.login( driver )

    for k in tqdm( horce_url.keys() ):
        horse_name = k.replace( " ", "" )
        count += 1
        url = horce_url[k]
        driver, _ = lib.driver_request( driver, url )
        html = driver.page_source.encode('utf-8')
        soup = BeautifulSoup( html, "html.parser" )     
        result[horse_name] = html_analyze( soup )
        
        if count % 100 == 0:
            dm.pickle_upload( "baba_index_data.pickle", result )

    dm.pickle_upload( "baba_index_data.pickle", result )
    driver.quit()

main()

