from tqdm import tqdm
from bs4 import BeautifulSoup

import SekitobaLibrary as lib
import SekitobaDataManage as dm

def data_collect( base_url ):
    result = {}
    count = 1
    
    while 1:
        url = base_url + str( count )
        r, requestSuccess  = lib.request( url )

        if not requestSuccess:
            print( "Error: {}".format( url ) )
            return result
        
        soup = BeautifulSoup( r.content, "html.parser" )
        tbody = soup.find( "tbody" )
        if tbody == None:
            break
        
        tr_tag = tbody.findAll( "tr" )

        if len( tr_tag ) == 0:
            break
        else:
            for tr in tr_tag:
                td_tag = tr.findAll( "td" )
                key_day = td_tag[0].text
                key_race_num = td_tag[3].text
                try:
                    horce_id = td_tag[12].find( "a" ).get( "href" ).replace( "horse", "" ).replace( "/", "" )
                except:
                    horce_id = ""
                    
                lib.dicAppend( result, key_day, {} )
                lib.dicAppend( result[key_day], key_race_num, {} )
                result[key_day][key_race_num]["place"] = td_tag[1].text
                result[key_day][key_race_num]["weather"] = td_tag[2].text
                result[key_day][key_race_num]["all_horce_num"] = td_tag[6].text
                result[key_day][key_race_num]["flame_num"] = td_tag[7].text
                result[key_day][key_race_num]["horce_num"] = td_tag[8].text
                result[key_day][key_race_num]["odds"] = td_tag[9].text
                result[key_day][key_race_num]["popular"] = td_tag[10].text
                result[key_day][key_race_num]["rank"] = td_tag[11].text
                result[key_day][key_race_num]["horce_id"] = horce_id
                result[key_day][key_race_num]["weight"] = td_tag[13].text
                result[key_day][key_race_num]["dist"] = td_tag[14].text
                result[key_day][key_race_num]["baba"] = td_tag[15].text
                result[key_day][key_race_num]["time"] = td_tag[16].text
                result[key_day][key_race_num]["diff"] = td_tag[17].text
                result[key_day][key_race_num]["passing"] = td_tag[18].text
                result[key_day][key_race_num]["pace"] = td_tag[19].text
                result[key_day][key_race_num]["up"] = td_tag[20].text
                
        count += 1
    
    return result

def main():
    base_url = "https://db.netkeiba.com/?pid=jockey_detail&id="
    jockey_id_data = dm.pickle_load( "jockey_id_data.pickle" )
    url_list = []
    key_list = []

    for k in jockey_id_data.keys():
        jockey_id = k
        url = base_url + jockey_id + "&page="
        url_list.append( url )
        key_list.append( jockey_id )

    result = lib.thread_scraping( url_list, key_list ).data_get( data_collect )
    dm.pickle_upload( "jockey_full_data.pickle", result )

if __name__ == "__main__":
    main()
