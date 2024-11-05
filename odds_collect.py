from tqdm import tqdm
from bs4 import BeautifulSoup

import SekitobaPsql as ps
import SekitobaLibrary as lib
import SekitobaDataManage as dm

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
    result = {}#dm.pickle_load( "odds_data.pickle" )    
    base_url = "https://race.netkeiba.com/race/result.html?race_id="
    
    race_id_list = ps.RaceData().get_all_race_id()
    url_data = []
    key_data = []
    
    for race_id in race_id_list:
        url = base_url + race_id + "&rf=race_list"
        url_data.append( url )
        key_data.append( race_id )

    add_data = lib.thread_scraping( url_data, key_data ).data_get( money_get )

    for k in add_data.keys():
        result[k] = add_data[k]
    
    dm.pickle_upload( "odds_data.pickle", result )
    
main()

