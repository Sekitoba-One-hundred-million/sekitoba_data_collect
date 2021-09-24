from tqdm import tqdm
from bs4 import BeautifulSoup

import sekitoba_library as lib
import sekitoba_data_manage as dm

def money_get( url ):
    result = {}
    r, _ = lib.request( url )
    soup = BeautifulSoup( r.content, "html.parser" )
    td_tag = soup.findAll( "td" )
    count = 0

    for td in td_tag:
        class_name = td.get( "class" )

        if not class_name == None \
           and class_name[0] == "Payout":
            count += 1
            m_data = td.text.split( "円" )
            
            if count == 1:
                result["単勝"] = int( m_data[0].replace( ",", "" ) )
            elif count == 2:
                result["複勝"] = []
                for i in range( 0, len( m_data ) - 1 ):
                    result["複勝"].append( int( m_data[i].replace( ",", "" ) ) )
            elif count == 4:
                result["馬連"] = int( m_data[0].replace( ",", "" ) )
            elif count == 5:
                result["ワイド"] = []
                for i in range( 0, len( m_data ) - 1 ):
                    result["ワイド"].append( int( m_data[i].replace( ",", "" ) ) )
            elif count == 6:
                result["馬単"] = int( m_data[0].replace( ",", "" ) )
            elif count == 7:
                result["三連複"] = int( m_data[0].replace( ",", "" ) )
            elif count == 8:
                result["三連単"] = int( m_data[0].replace( ",", "" ) )

    return result
        
                    

def main():
    result = dm.pickle_load( "odds_data.pickle" )
    
    if result == None:
        result = {}
        
    base_url = "https://race.netkeiba.com/race/result.html?race_id="

    race_data = dm.pickle_load( "race_data.pickle" )
    url_data = []
    key_data = []

    
    for k in tqdm( race_data.keys() ):
        url = base_url + lib.id_get( k ) + "&rf=race_list"

        try:
            a = result[lib.id_get(k)]
        except:
            url_data.append( url )
            key_data.append( lib.id_get( k ) )

    add_data = lib.thread_scraping( url_data, key_data ).data_get( money_get )

    for k in add_data.keys():
        result[k] = add_data[k]
    
    dm.pickle_upload( "odds_data.pickle", result )
    
main()

