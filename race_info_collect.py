from bs4 import BeautifulSoup

import SekitobaPsql as ps
import SekitobaLibrary as lib
import SekitobaDataManage as dm

def data_get( url ):
    result = {}
    result["kind"] = 0
    result["dist"] = 0
    result["baba"] = 0
    result["place"] = 0
    
    r, _ = lib.request( url )
    soup = BeautifulSoup( r.content, "html.parser" )
    div_tag = soup.findAll( "div" )

    for div in div_tag:
        class_name = div.get( "class" )

        if not class_name == None:
            if class_name[0] == "RaceData01":
                span_tag = div.findAll( "span" )
                str_dist = span_tag[0].text.replace( " ", "" )
                _, kind = lib.dist( str_dist )
                dist = int( lib.kDist( str_dist ) * 1000 )
                try:
                    baba = lib.baba( span_tag[2].text.split( ":" )[1] )
                except:
                    baba = -1
                    
                result["kind"] = kind
                result["dist"] = dist
                result["baba"] = baba
                
            elif class_name[0] == "RaceData02":
                span_tag = div.findAll( "span" )
                place = lib.placeNum( span_tag[1].text )
                result["place"] = place

    print( url, result )
    return result

def main():
    race_data = dm.pickle_load( "race_data.pickle" )
    result = dm.pickle_load( "race_info_data.pickle" )
    
    if result == None:
        result = {}
    
    url_list = []
    key_list = []

    for k in race_data.keys():
        race_id = lib.idGet( k )

        #if race_id in result:
        #    continue

        url_list.append( k )
        key_list.append( race_id )

    race_data = ps.RaceData()
    add_data = lib.thread_scraping( url_list, key_list ).data_get( data_get )
    return
    rd = dm.pickle_load( "race_course_data.pickle" )
    
    for k in add_data.keys():
        result[k] = add_data[k]

        for kind in add_data[k].keys():
            race_data.update_data( kind, add_data[k][kind], k )

    for k in result.keys():
        try:
            result[k]["out_side"] = rd[k]["out_side"]
        except:
            try:
                result[k]["out_side"] = rd[k]["外"]
            except:
                continue
            
        result[k]["direction"] = rd[k]["direction"]

    
    dm.pickle_upload( "race_info_data.pickle", result )

main()
