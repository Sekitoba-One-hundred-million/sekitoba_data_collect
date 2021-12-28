from tqdm import tqdm
from bs4 import BeautifulSoup

import sekitoba_library as lib
import sekitoba_data_manage as dm

def data_collect( base_url ):
    result = {}
    count = 1
    
    while 1:
        url = base_url + str( count )
        r,_  = lib.request( url )
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
                lib.dic_append( result, key_day, {} )
                lib.dic_append( result[key_day], key_race_num, {} )
                result[key_day][key_race_num]["place"] = td_tag[1].text
                result[key_day][key_race_num]["weather"] = td_tag[2].text
                result[key_day][key_race_num]["all_horce_num"] = td_tag[6].text
                result[key_day][key_race_num]["flame_num"] = td_tag[7].text
                result[key_day][key_race_num]["horce_num"] = td_tag[8].text
                result[key_day][key_race_num]["odds"] = td_tag[9].text
                result[key_day][key_race_num]["popular"] = td_tag[10].text
                result[key_day][key_race_num]["rank"] = td_tag[11].text
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
    check_str = "/jockey/"
    data_storage = {}

    url_list = []
    key_list = []
    use_id = {}
    jockey_id_data = dm.pickle_load( "jockey_id_data.pickle" )

    for k in jockey_id_data.keys():
        for kk in jockey_id_data[k].keys():
            jockey_id = jockey_id_data[k][kk]

            if jockey_id == None:
                continue
            
            try:
                use_id[jockey_id]
            except:
                url = base_url + jockey_id + "&page="
                url_list.append( url )
                key_list.append( jockey_id )
                use_id[jockey_id] = True

    data_storage = lib.thread_scraping( url_list, key_list ).data_get( data_collect )
    dm.pickle_upload( "jockey_full_data.pickle", data_storage )

def key_organaize( data = None ):
    if data == None:
        data = dm.pickle_load( "jockey_full_data.pickle" )
        
    result = {}

    for jockey_id in tqdm( data.keys() ):
        result[jockey_id] = {}
        result[jockey_id]["key_list"] = []
        result[jockey_id]["key_num"] = {}
        
        for day in data[jockey_id].keys():
            for race_num in data[jockey_id][day].keys():
                ymd = day.split( "/" )
                try:
                    if len( ymd[1] ) == 1:
                        ymd[1] = "0" + ymd[1]

                    if len( ymd[2] ) == 1:
                        ymd[2] = "0" + ymd[2]

                    if len( race_num ) == 1:
                        new_race_num = "0" + race_num
                
                    new_key = ymd[0] + ymd[1] + ymd[2] + new_race_num
                    result[jockey_id][new_key] = data[jockey_id][day][race_num]
                    result[jockey_id]["key_list"].append( new_key )
                except:
                    continue

        for i in range( 0, len( result[jockey_id]["key_list"] ) ):
            key = result[jockey_id]["key_list"][i]
            result[jockey_id]["key_num"][key] = i

    dm.pickle_upload( "jockey_full_data.pickle.backup", data )
    dm.pickle_upload( "jockey_full_data.pickle", result )

#main()
key_organaize()
