import SekitobaPsql as ps
import SekitobaLibrary as lib
import SekitobaDataManage as dm

import json
import time
import datetime
from bs4 import BeautifulSoup
from tqdm import tqdm

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
    race_data = ps.RaceData()
    race_horce_data = ps.RaceHorceData()
    race_id_list = race_data.get_all_race_id()
    null_horce_id_data = {}
    check_race_id_list = []

    for race_id in race_id_list:
        year = race_id[0:4]

        if not year == "2024":
            continue

        check_race_id_list.append( race_id )

    for race_id in tqdm( check_race_id_list ):
        race_data.get_all_data( race_id )
        race_horce_data.get_all_data( race_id )

        for horce_id in race_horce_data.horce_id_list:
            try:
                int( horce_id )
            except:
                continue
                
            if not horce_id in null_horce_id_data:
                null_horce_id_data[horce_id] = race_id

    horce_data = dm.pickle_load( "horce_data_storage.pickle" )
    baba_index_data = dm.pickle_load( "baba_index_data.pickle" )
    time_index_data = dm.pickle_load( "time_index_data.pickle" )
    #check_horce_id_list = []
    check_horce_id_list = dm.pickle_load( "check_horce_id_data.pickle" )
    driver = lib.driver_start()
    driver = lib.login( driver )
    aa = len( null_horce_id_data.keys() )
                
    for horce_id in null_horce_id_data.keys():
        print( aa )
        
        if horce_id in check_horce_id_list:
            aa -= 1
            continue
        
        url = "https://db.netkeiba.com/horse/{}".format( horce_id )
        
        while 1:
            try:
                driver, _ = lib.driver_request( driver, url )
                time.sleep( 2 )
                html = driver.page_source.encode('utf-8')
                soup = BeautifulSoup( html, "html.parser" )
            except:
                time.sleep( 1 )
                continue

            current_horce_data = horce_data_collect( soup )

            if len( current_horce_data ) == 0:
                print( "restart horce_id:{}".format( horce_id ) )
                driver = lib.driver_restart( driver )
                driver = lib.login( driver )
            else:
                break

        current_time_index_data = time_index_collect( soup )
        current_baba_index_data = baba_index_collect( soup )
        horce_data[horce_id] = current_horce_data
        baba_index_data[horce_id] = current_baba_index_data
        time_index_data[horce_id] = current_time_index_data
        check_horce_id_list.append( horce_id )
        aa -= 1

        if aa % 50 == 0:
            dm.pickle_upload( "check_horce_id_data.pickle", check_horce_id_list )
            dm.pickle_upload( "horce_data_storage.pickle", horce_data )
            dm.pickle_upload( "baba_index_data.pickle", baba_index_data )
            dm.pickle_upload( "time_index_data.pickle", time_index_data )

    #dm.pickle_upload( "check_horce_id_data.pickle", check_horce_id_list )
    #dm.pickle_upload( "horce_data_storage.pickle", horce_data )
    #dm.pickle_upload( "baba_index_data.pickle", baba_index_data )
    #dm.pickle_upload( "time_index_data.pickle", time_index_data )

    psql_horce_data = ps.HorceData()

    for horce_id in tqdm( check_horce_id_list ):
        psql_horce_data.update_data( "past_data", horce_data[horce_id], horce_id )
        psql_horce_data.update_data( "baba_index", json.dumps( baba_index_data[horce_id], ensure_ascii = False ), horce_id )
        psql_horce_data.update_data( "time_index", json.dumps( time_index_data[horce_id], ensure_ascii = False ), horce_id )


if __name__ == "__main__":
    main()
