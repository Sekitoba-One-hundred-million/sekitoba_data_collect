from tqdm import tqdm
from bs4 import BeautifulSoup

import sekitoba_library as lib
import sekitoba_data_manage as dm

def money_get( url ):
    result = {}
    r, _ = lib.request( url )
    soup = BeautifulSoup( r.content, "html.parser" )
    tr_tag = soup.findAll( "tr" )
    count = 0

    for tr in tr_tag:
        class_name = tr.get( "class" )

        if not class_name == None:
            key = ""
            td_tag = tr.findAll( "td" )
            m_data = ""
            
            try:
                m_data = td_tag[1].text.split( "円" )
            except:
                continue
            
            if class_name[0] == "Tansho":
                result["単勝"] = int( m_data[0].replace( ",", "" ) )
            elif class_name[0] == "Fukusho":
                result["複勝"] = []
                for i in range( 0, len( m_data ) - 1 ):
                    result["複勝"].append( int( m_data[i].replace( ",", "" ) ) )
            elif class_name[0] == "Umaren":
                result["馬連"] = int( m_data[0].replace( ",", "" ) )
            elif class_name[0] == "Wide":
                result["ワイド"] = []
                for i in range( 0, len( m_data ) - 1 ):
                    result["ワイド"].append( int( m_data[i].replace( ",", "" ) ) )
            elif class_name[0] == "Umatan":
                result["馬単"] = int( m_data[0].replace( ",", "" ) )
            elif class_name[0] == "Fuku3":
                result["三連複"] = int( m_data[0].replace( ",", "" ) )
            elif class_name[0] == "Tan3":
                result["三連単"] = int( m_data[0].replace( ",", "" ) )

    return result        

def main():
    #result = dm.pickle_load( "odds_data.pickle" )
    
    #if result == None:
    result = {}
        
    base_url = "https://race.netkeiba.com/race/result.html?race_id="

    race_data = dm.pickle_load( "race_data.pickle" )
    url_data = []
    key_data = []
    
    for k in race_data.keys():
        url = base_url + lib.id_get( k ) + "&rf=race_list"
        race_id = lib.id_get(k)

        if not race_id in result:
            url_data.append( url )
            key_data.append( race_id )

    add_data = lib.thread_scraping( url_data, key_data ).data_get( money_get )

    for k in add_data.keys():
        result[k] = add_data[k]
    
    dm.pickle_upload( "odds_data.pickle", result )
    
main()

