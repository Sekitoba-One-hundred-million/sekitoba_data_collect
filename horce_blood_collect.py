from bs4 import BeautifulSoup

import sekitoba_library as lib
import sekitoba_data_manage as dm

# 1: サンダーサイレンス
# 2: ターントゥ
# 3: ノーザンダンサー
# 4: ナスルーラ
# 5: ネイティヴダンサー
# 6: ハンプトン
# 7: セントサイモン
# 8: その他

blood = { "#C4F2F9": 1, "#C6FFAA": 2, "#E0B7FF": 3, "#FFA6E2": 4,  "#FFD28E": 5, "#E8BF9B": 6, "#FFF99": 7, "#DDDDDD": 8 }

def data_collect( data ):
    result = {}
    #r, _ = lib.request( url )
    r, _ = lib.request( data["url"], cookie = data["cookie"] )
    soup = BeautifulSoup( r.content, "html.parser" )    
    tr_tag = soup.findAll( "tr" )

    for tr in tr_tag:
        class_name = tr.get( "class" )

        if not class_name == None and len( class_name ) == 2 and class_name[0] == "List" and class_name[1] == "HorseList":
            td_tag = tr.findAll( "td" )
            try:
                horce_number = td_tag[1].text.replace( " ", "" ).replace( "\n", "" )
                father_style = td_tag[4].get( "style" ).replace( "background:", "" ).replace( ";", "" )
                mother_father_style = td_tag[5].get( "style" ).replace( "background:", "" ).replace( ";", "" )
                result[horce_number] = { "father": blood[father_style], "mother_father": blood[mother_father_style] }
            except:
                continue

    print( result )
    return result

def main():
    race_data = dm.pickle_load( "race_data.pickle" )
    cookie = lib.netkeiba_login()
    key_list = []
    url_list = []

    for k in race_data.keys():
        race_id = lib.id_get( k )
        url = "https://race.netkeiba.com/race/bias.html?race_id=" + race_id
        url_list.append( { "url": url, "cookie": cookie } )
        key_list.append( race_id )
    
    add_data = lib.thread_scraping( url_list, key_list ).data_get( data_collect )
    result = dm.pickle_load( "horce_blood_data.pickle" )

    if result == None:
        result = {}

    for k in add_data.keys():
        result[k] = add_data[k]
        
    dm.pickle_upload( "horce_blood_data.pickle", result )
    

if __name__ == "__main__":
    main()
