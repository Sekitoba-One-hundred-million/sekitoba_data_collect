import json
import time
from bs4 import BeautifulSoup
import requests
from tqdm import tqdm

import SekitobaPsql as ps
import SekitobaLibrary as lib
import SekitobaDataManage as dm

def time_index_collect( soup ):
    result = {}
    tr_tag = soup.findAll( "tr" )

    for i in range( 0, len( tr_tag ) ):
        td_tag = tr_tag[i].findAll( "td" )
        
        if 2 < len( td_tag ) and td_tag[3].get( "class" ) != None \
           and td_tag[3].get( "class" )[0] == "txt_right":
            time_index = td_tag[20].text.replace( "\n", "" ).replace( " ", "" )
            day_key = td_tag[0].text.replace( "\n", "" ).replace( " ", "" )

            try:
                result[day_key] = float( time_index )
            except:
                result[day_key] = 0

    return result

def horce_data_collect( soup ):
    horce_data = []
    tr_tag = soup.findAll( "tr" )

    for i in range( 0, len( tr_tag ) ):
        td_tag = tr_tag[i].findAll( "td" )

        if 2 < len( td_tag ) and td_tag[3].get( "class" ) != None \
           and td_tag[3].get( "class" )[0] == "txt_right":
            data_list = []
            for r in range( 0, len( td_tag ) ):
                if r != 5 and r != 15 and r != 17 and r != 20 and ( r == 28 or r < 25 ):
                    data = lib.text_replace( td_tag[r].text )
    
                    if not r == 28:
                        data_list.append( data )
                    else:
                        try:
                            data_list.append( float( data ) )
                        except:
                            data_list.append( 0 )

            if len( data_list ) == 22:
                horce_data.append( data_list )

    return horce_data

def baba_index_collect( soup ):
    result = {}
    tr_tag = soup.findAll( "tr" )

    for i in range( 0, len( tr_tag ) ):
        td_tag = tr_tag[i].findAll( "td" )
        
        if 2 < len( td_tag ) and td_tag[3].get( "class" ) != None \
           and td_tag[3].get( "class" )[0] == "txt_right":
            baba_index = td_tag[17].text.replace( "\n", "" ).replace( " ", "" )
            day_key = td_tag[0].text.replace( "\n", "" ).replace( " ", "" )

            try:
                result[day_key] = float( baba_index )
            except:
                result[day_key] = 0

    return result

def main():
    #time_index_data = dm.pickle_load( "time_index_data.pickle" )
    baba_index_data = dm.pickle_load( "baba_index_data.pickle" )
    driver = lib.driver_start()
    driver = lib.login( driver )

    race_id_list = ps.RaceData().get_all_race_id()
    race_horce_data = ps.RaceHorceData()
    collect_horce = {}

    for race_id in tqdm( race_id_list ):
        for horce_id in race_horce_data.get_horce_id( race_id ):
            try:
                int( horce_id )
            except:
                continue
            
            if not horce_id in baba_index_data:
                collect_horce[horce_id] = True

    aa = len( collect_horce )
    for horce_id in collect_horce.keys():
        print( aa )
        current_horce_data = {}
        c = 0
        while 1:
            try:
                driver, _ = lib.driver_request( driver, "https://db.netkeiba.com/horse/{}".format( horce_id ) )
                time.sleep( 2 )
                html = driver.page_source.encode('utf-8')
                soup = BeautifulSoup( html, "html.parser" )
            except:
                if c == 10:
                    break
                
                time.sleep( 1 )
                c += 1
                continue

            current_horce_data = horce_data_collect( soup )

            if len( current_horce_data ) == 0:
                print( "restart horce_id:{}".format( horce_id ) )
                driver = lib.driver_restart( driver )
                driver = lib.login( driver )
            else:
                break

        current_baba_index_data = baba_index_collect( soup )
        #current_time_index_data = time_index_collect( soup )
        baba_index_data[horce_id] = current_baba_index_data
        #time_index_data[horce_id] = current_time_index_data
        aa -= 1

        if aa % 100 == 0:
            dm.pickle_upload( "baba_index_data.pickle", baba_index_data )

    driver.quit()
    dm.pickle_upload( "baba_index_data.pickle", baba_index_data )
    #dm.pickle_upload( "time_index_data.pickle", time_index_data )
        
    #for horce_id in add_data.keys():
    #    ps.HorceData().update_data( "baba_index", json.dumps( baba_index_data[horce_id], ensure_ascii = False ), horce_id )
    #    ps.HorceData().update_data( "time_index", json.dumps( time_index_data[horce_id], ensure_ascii = False ), horce_id )

if __name__ == "__main__":
    for i in range( 0, 100 ):
        main()
