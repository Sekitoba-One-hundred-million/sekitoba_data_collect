import math
import json
import random
from tqdm import tqdm
from bs4 import BeautifulSoup

import SekitobaLibrary as lib
import SekitobaDataManage as dm
import SekitobaPsql as ps

def horse_data_collect( url ):
    horce_data = []
    r, requestSucess = lib.request( url )

    if not requestSucess:
        print( "Error: {}".format( data["url"] ) )
        return horce_data
    
    soup = BeautifulSoup( r.content, "html.parser" )
    tr_tag = soup.findAll( "tr" )

    for i in range( 0, len( tr_tag ) ):
        td_tag = tr_tag[i].findAll( "td" )
        
        if 2 < len( td_tag ) and td_tag[3].get( "class" ) != None \
           and td_tag[3].get( "class" )[0] == "txt_right":
            data_list = []
            for r in range( 0, len( td_tag ) ):
                #print( td_tag[r], r )
                if r != 5 and r != 16 and r != 19 and ( r == 27 or r < 24 ):
                    data = td_tag[r].text.replace( "\n", "" )

                    if not r == 27:
                        data_list.append( data )
                    else:
                        try:
                            data_list.append( float( data ) )
                        except:
                            data_list.append( 0 )

            if len( data_list ) == 22:
                horce_data.append( data_list )
                
    return horce_data

def main():
    horceData = ps.HorceData()
    data = horceData.get_select_all_data( "parent_id" )
    parentKeyData = {}

    for horce_id in data.keys():
        if not type( data[horce_id] ) == str:
            continue
            
        data[horce_id] = json.loads( data[horce_id] )
        
        if type( data[horce_id] ) == int:
            continue
        
        mother_id = data[horce_id]["mother"]
        father_id = data[horce_id]["father"]

        if not len( mother_id ) == 0 and not mother_id in data:
            parentKeyData[mother_id] = True

        if not len( father_id ) == 0 and not father_id in data:
            parentKeyData[father_id] = True

    urlList = []
    parentIdList = list( parentKeyData.keys() )

    for parentId in parentIdList:
        urlList.append( "https://db.netkeiba.com/horse/{}".format( parentId ) )

    result = lib.thread_scraping( urlList, parentIdList ).data_get( horse_data_collect )
    dm.pickle_upload( "parent_horce_data.pickle", result )

if __name__ == "__main__":
    main()
