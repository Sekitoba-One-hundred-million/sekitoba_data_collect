import time
from tqdm import tqdm
from bs4 import BeautifulSoup
from selenium import webdriver

import sekitoba_library as lib
import sekitoba_data_manage as dm


def data_get( driver, url, year, race_num, place ):
    driver, _ = lib.driver_request( driver, url )
    html = driver.page_source.encode('utf-8')
    soup = BeautifulSoup( html, "html.parser" )        

    #soup = BeautifulSoup( r.content, "html.parser" )
    race_id = year

    td_tag = soup.findAll( "td" )
    instance = []
    
    for td in td_tag:
        class_name = td.get( "class" )

        if not class_name == None \
           and len( class_name ) == 2 \
           and class_name[0] == "tC" \
           and "cyaku" in class_name[1]:
            try:
                instance.append( float( td.text ) )
            except:
                instance.append( 0 )
            
    if len( instance ) == 0:
        return "", []
    
    p_tag = soup.findAll( "p" )
    r_day = ""
    r_count = ""
                
    for p in p_tag:
        itemprop_name = p.get( "itemprop" )
        class_name = p.get( "class" )
        
        if not itemprop_name == None \
           and not class_name == None \
           and itemprop_name == "about" \
           and class_name[0] == "bold":
            num_data = p.text.split( "\n" )

            count = 0

            for i in range( 0, len( num_data[1] ) ):
                try:
                    r_count += str( int( num_data[1][i] ) )
                except:
                    count = i
                    break

            finish = False
            
            for i in range( count, len( num_data[1] ) ):
                try:
                    r_day += str( int( num_data[1][i] ) )
                    finish = True
                except:
                    if finish:
                        break

    if len( str( place ) ) == 1:
        race_id += "0"
        
    race_id += str( place )

    if len( str( r_count ) ) == 1:
        race_id += "0"
        
    race_id += str( r_count )

    if len( str( r_day ) ) == 1:
        race_id += "0"
        
    race_id += str( r_day )

    if len( str( race_num ) ) == 1:
        race_id += "0"
        
    race_id += str( race_num )
    
    return race_id, instance
    
def main():
    base_url = "https://www.keibalab.jp/db/race/"
    driver = webdriver.Chrome()
    result = dm.pickle_load( "omega_index_data.pickle" )

    if result == None:
        result = {}

    for y in range( 2020, 2021 ):#年
        for m in range( 1, 13 ):#月
            print( y, m )
            for d in range( 1, 32 ):#日
                for p in range( 1, 11 ):
                    for r in range( 1, 13 ):#レースR
                        url = base_url + str( y )

                        if len( str( m ) ) == 1:
                            url += "0"

                        url += str( m )

                        if len( str( d ) ) == 1:
                            url += "0"

                        url += str( d )

                        if len( str( p ) ) == 1:
                            url += "0"

                        url += str( p )
                        
                        if len( str( r ) ) == 1:
                            url += "0"

                        url += str( r )

                        url += "/syutsuba.html"

                        #url = "https://www.keibalab.jp/db/race/202011220904/syutsuba.html"
                        race_id, data = data_get( driver, url, str( y ), str( r ), str( p ) )
                        time.sleep( 1 )
                        if len( data ) == 0:
                            break

                        result[race_id] = data

    dm.pickle_upload( "omega_index_data.pickle", result )
                        
main()
    
