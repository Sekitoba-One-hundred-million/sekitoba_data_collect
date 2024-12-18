import json
from bs4 import BeautifulSoup

import SekitobaPsql as ps
import SekitobaLibrary as lib
import SekitobaDataManage as dm

def wrap_get( url ):
    result = {}
    r, _ = lib.request( url )
    soup = BeautifulSoup( r.content, "html.parser" )
    
    table_tag = soup.findAll( "table" )

    for table in table_tag:
        summary = table.get( "summary" )

        if not summary == None \
           and summary == "ラップタイム":
            tr_tag = table.findAll( "tr" )
            dist_data = tr_tag[0].findAll( "th" )
            wrap_time = tr_tag[2].findAll( "td" )

            for i in range( 0, len( dist_data ) ):
                dist = dist_data[i].text.replace( "m", "" )
                wrap = float( wrap_time[i].text )
                result[dist] = wrap

    return result

def main():    
    base_url = "https://race.netkeiba.com/race/result.html?race_id="
    race_data = dm.pickle_load( "race_data.pickle" )
    result = dm.pickle_load( "wrap_data.pickle" )
    
    if result == None:
        result = {}

    url_list = []
    key_list = []

    for k in race_data.keys():
        race_id = lib.idGet( k )

        if not race_id in result:
            url = base_url + race_id
            url_list.append( url )
            key_list.append( race_id )
    
    add_data = lib.thread_scraping( url_list, key_list ).data_get( wrap_get )
    
    for k in add_data.keys():
        result[k] = add_data[k]
        ps.RaceData().update_data( "wrap", json.dumps( add_data[k], ensure_ascii = False ), k )
    
    dm.pickle_upload( "wrap_data.pickle", result )

main()

