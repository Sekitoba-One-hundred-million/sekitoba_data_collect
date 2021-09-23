from tqdm import tqdm
from bs4 import BeautifulSoup

import sekitoba_library as lib
import sekitoba_data_manage as dm

def father_url_get( soup ):
    table_tag = soup.findAll( "table" )

    for table in table_tag:
        class_name = table.get( "class" )

        if not class_name == None \
           and class_name[0] == "blood_table":
            td = table.find( "td" )
            a_tag = td.findAll( "a" )

            try:
                horce_name = a_tag[0].text.split( "\n" )[0].replace( " ", "" )
                check_url = "https://db.netkeiba.com/" + a_tag[2].get( "href" )
                #result[horce_name] = check_url
                return horce_name, check_url
            except:
                return "", ""
    
def father_name_link_url():
    horce_url = dm.pickle_load( "horce_url.pickle" )
    father_url_data = {}
    horce_father = {}

    for k in tqdm( horce_url.keys() ):
        horce_name = k.replace( " ", "" )
        url = horce_url[k][0:30] + "ped/" + horce_url[k][30:len(horce_url[k])]
        r, _ = lib.request( url )
        soup = BeautifulSoup( r.content, "html.parser" )
        father_name, father_url = father_url_get( soup )

        if not len( father_name ) == 0:
            father_url_data[father_name] = father_url
            horce_father[horce_name] = father_name

    dm.pickle_upload( "father_name.pickle", horce_father )
    return father_url_data

def father_grade( soup ):
    instance = {}
    table_tag = soup.findAll( "table" )

    for table in table_tag:
        class_name = table.get( "class" )

        if not class_name == None \
           and len( class_name ) == 2 \
           and class_name[0] == "nk_tb_common" \
           and class_name[1] == "race_table_01":
            tr_tag = table.findAll( "tr" )

            for i in range( 3, len( tr_tag ) ):
                td_tag = tr_tag[i].findAll( "td" )
                year = td_tag[0].text.replace( " ", "" )
                go_h_num = lib.num_check( td_tag[2].text.replace( " ", "" ) )
                win_h_num = lib.num_check( td_tag[3].text.replace( " ", "" ) )
                EI = lib.num_check( td_tag[17].text.replace( " ", "" ) )
                
                try:
                    win_rate = lib.num_check( td_tag[4].text.replace( " ", "" ) ) / lib.num_check( td_tag[5].text.replace( " ", "" ) )
                except:
                    win_rate = 0

                instance[year] = {}
                instance[year]["go_num"] = go_h_num
                instance[year]["win_num"] = win_h_num
                instance[year]["win_rate"] = win_rate
                instance[year]["EI"] = EI

    return instance
    
def father_data_collect( father_url ):
    result = {}

    for k in tqdm( father_url.keys() ):
        url = father_url[k]
        r, _ = lib.request( url )
        soup = BeautifulSoup( r.content, "html.parser" )
        data = father_grade( soup )
        result[k] = data

    dm.pickle_upload( "father_grade_data.pickle", result )

def kind_baba( soup ):
    check_baba = [ "1", "3", "2", "4" ]
    result = {}
    
    table_tag = soup.findAll( "table" )

    for i in range( 0, 2 ):
        class_name = table_tag[i].get( "class" )

        if not class_name == None \
           and len( class_name ) == 2 \
           and class_name[0] == "nk_tb_common" \
           and class_name[1] == "race_table_01":
            tr_tag = table_tag[i].findAll( "tr" )
            kind = ""

            if i == 0:
                kind = "1"
            else:
                kind = "2"
                
            for r in range( 3, len( tr_tag ) ):
                td_tag = tr_tag[r].findAll( "td" )
                year = td_tag[0].text.replace( " ", "" )
                instance = {}
                instance[kind] = {}
                #instance["ダ"] = {}
                instance[kind]["1"] = {}
                instance[kind]["3"] = {}
                instance[kind]["2"] = {}
                instance[kind]["4"] = {}
                
                for t in range( 1, len( td_tag ), 4 ):
                    try:
                        instance[kind][check_baba[int( t / 4 )]]["one"] = lib.num_check( td_tag[t].text.replace( " ", "" ) ) / lib.num_check( td_tag[t+3].text.replace( " ", "" ) )
                        instance[kind][check_baba[int( t / 4 )]]["two"] = lib.num_check( td_tag[t+1].text.replace( " ", "" ) ) / lib.num_check( td_tag[t+3].text.replace( " ", "" ) )
                        instance[kind][check_baba[int( t / 4 )]]["three"] = lib.num_check( td_tag[t+2].text.replace( " ", "" ) ) / lib.num_check( td_tag[t+3].text.replace( " ", "" ) )
                    except:
                        instance[kind][check_baba[int( t / 4 )]]["one"] = 0
                        instance[kind][check_baba[int( t / 4 )]]["two"] = 0
                        instance[kind][check_baba[int( t / 4 )]]["three"] = 0

                result[year] = instance

    return result

def kind_dist( soup ):
    check_dist = [ "1400", "1800", "2200", "2600", "2601" ]
    result = {}
    
    table_tag = soup.findAll( "table" )

    for i in range( 0, 2 ):
        class_name = table_tag[i].get( "class" )

        if not class_name == None \
           and len( class_name ) == 2 \
           and class_name[0] == "nk_tb_common" \
           and class_name[1] == "race_table_01":
            tr_tag = table_tag[i].findAll( "tr" )
            kind = ""

            if i == 0:
                kind = "1"
            else:
                kind = "2"
                
            for r in range( 3, len( tr_tag ) ):
                td_tag = tr_tag[r].findAll( "td" )
                year = td_tag[0].text.replace( " ", "" )
                instance = {}
                instance["1400"] = {}
                instance["1800"] = {}
                instance["2200"] = {}
                instance["2600"] = {}
                instance["2601"] = {}
                instance["1400"][kind] = {}
                instance["1800"][kind] = {}    
                instance["2200"][kind] = {}    
                instance["2600"][kind] = {}
                instance["2601"][kind] = {}

                
                for t in range( 1, len( td_tag ), 4 ):
                    try:
                        instance[check_dist[int( t / 4 )]][kind]["one"] = lib.num_check( td_tag[t].text.replace( " ", "" ) ) / lib.num_check( td_tag[t+3].text.replace( " ", "" ) )
                        instance[check_dist[int( t / 4 )]][kind]["two"] = lib.num_check( td_tag[t+1].text.replace( " ", "" ) ) / lib.num_check( td_tag[t+3].text.replace( " ", "" ) )
                        instance[check_dist[int( t / 4 )]][kind]["three"] = lib.num_check( td_tag[t+2].text.replace( " ", "" ) ) / lib.num_check( td_tag[t+3].text.replace( " ", "" ) )
                    except:
                        instance[check_dist[int( t / 4 )]][kind]["one"] = 0
                        instance[check_dist[int( t / 4 )]][kind]["two"] = 0
                        instance[check_dist[int( t / 4 )]][kind]["three"] = 0

                result[year] = instance
                        
    return result

def father_grade_kind_data_collect( father_url ):
    result = {}
    
    for k in tqdm( father_url.keys() ):
        f_url = father_url[k]
        f_url = f_url.split( "/" )
        base_url = "https://db.netkeiba.com/?pid=horse_sire&id=" + f_url[6] + ""
        r, _ = lib.request( base_url + "&course=1&mode=1&type=2" )
        soup = BeautifulSoup( r.content, "html.parser" )
        kd_data = kind_dist( soup )

        r, _ = lib.request( base_url + "&course=1&mode=1&type=1" )
        soup = BeautifulSoup( r.content, "html.parser" )
        kb_data = kind_baba( soup )
        result[k] = {}
        result[k]["kb"] = kb_data
        result[k]["kd"] = kd_data
        
    dm.pickle_upload( "father_condition_grade.pickle", result )
    
def main():
    father_url = father_name_link_url()
    father_data_collect( father_url )
    father_grade_kind_data_collect( father_url )
    
main()
