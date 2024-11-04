import copy
from bs4 import BeautifulSoup

import SekitobaPsql as ps
import SekitobaLibrary as lib
import SekitobaDataManage as dm

def data_collect( url ):
    result = {}
    r, _ = lib.request( url )
    soup = BeautifulSoup( r.content, "html.parser" )
    tr_tag = soup.findAll( "tr" )

    for tr in tr_tag:
        class_name = tr.get( "class" )
        
        if not class_name == None and "HorseList" in class_name:
            horce_id = ""
            jockey_id = ""
            td_tag = tr.findAll( "td" )
            for td in td_tag:
                td_class_name = td.get( "class" )
                
                if not td_class_name == None:
                    if td_class_name[0] == "HorseInfo":
                        a = td.find( "a" )
                        try:
                            href = a.get( "href" )
                            horce_id = href.split( "/" )[-1]
                        except:
                            continue
                        
                    elif td_class_name[0] == "Jockey":
                        a = td.find( "a" )
                        try:
                            href = a.get( "href" )
                            jockey_id = href.split( "/" )[-2]
                        except:
                            continue

            if not len( horce_id ) == 0 and not len( jockey_id ) == 0:
                result[horce_id] = jockey_id

    return result            

def main():
    race_data = dm.pickle_load( "race_data.pickle" )
    race_jockey_id_data = dm.pickle_load( "race_jockey_id_data.pickle" )
    jockey_id_data = dm.pickle_load( "jockey_id_data.pickle" )
    race_horce_data = ps.RaceHorceData()
    key_list = []
    url_list = []

    for k in race_data.keys():
        url = k
        race_id = lib.idGet( k )

        if not race_id in race_jockey_id_data:
            key_list.append( race_id )
            url_list.append( url )

    update_jockey_id_data = {}
    add_data = lib.thread_scraping( url_list, key_list ).data_get( data_collect )

    for k in add_data.keys():
        race_jockey_id_data[k] = copy.deepcopy( add_data[k] )

        for kk in add_data[k].keys():
            jockey_id = copy.copy( add_data[k][kk] )
            jockey_id_data[jockey_id] = True
            update_jockey_id_data[jockey_id] = True
            race_horce_data.update_data( "jockey_id", jockey_id, k, kk )

    ps.JockeyData().insert_data( list( update_jockey_id_data.keys() ) )
    dm.pickle_upload( "race_jockey_id_data.pickle", race_jockey_id_data )
    dm.pickle_upload( "jockey_id_data.pickle", jockey_id_data )

if __name__ == "__main__":
    main()
