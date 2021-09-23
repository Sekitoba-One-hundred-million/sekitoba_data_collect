import requests
import pickle
import sys
import numpy as np
from tqdm import tqdm
from bs4 import BeautifulSoup

sys.path.append( "../" )

import library as lib
import data_manage as dm

def horce_name_get( soup ):
    result = []
    div_tag = soup.findAll( "div" )

    for div in div_tag:
        class_name = div.get( "class" )
        
        if not class_name == None \
           and len( class_name ) == 1 \
           and class_name[0] == "Horse_Name":
            h_text = div.text
            h_text = h_text.replace( "\n", "" )
            h_text = h_text.replace( " ", "" )
            result.append( h_text )
            
    return result

def train_condition_get( soup ):
    result = []
    td_tag = soup.findAll( "td" )
    
    for i in range( 0, len( td_tag ) ):
        class_name = td_tag[i].get( "class" )

        if not class_name == None \
           and len( class_name ) == 1 \
           and class_name[0] == "Training_Critic":
            c_text = td_tag[i].text.replace( "\n", "" ).replace( " ", "" )
            ce_text = td_tag[i+1].text.replace( "\n", "" ).replace( " ", "" )
            instance = {}
            instance["comment"] = c_text
            instance["eveluation"] = ce_text

            result.append( instance )

    return result
    
def main():
    result = dm.pickle_load( "train_condition.pickle" )
    c_check = dm.pickle_load( "train_condition_chenge.pickle" )    

    base_url = "https://race.netkeiba.com/race/oikiri.html?race_id="    
    race_data = dm.pickle_load( "race_data.pickle" )


    for k in tqdm( race_data.keys() ):
        try:
            a = result[id_get(k)]
        except:
            url = base_url + lib.id_get( k ) + "&type=3&rf=shutuba_submenu"
            r, _ = lib.request( url )
            soup = BeautifulSoup( r.content, "html.parser" )
            h_name = horce_name_get( soup )
            c_data = train_condition_get( soup )
            result[lib.id_get(k)] = {}

            for i in range( 0, len( h_name ) ):
                result[lib.id_get(k)][h_name[i]] = c_data[i]
            
            for i in range( 0, len( c_data ) ):
                try:
                    a = c_check["comment"][c_data[i]["comment"]]
                except:
                    c_check["comment"][c_data[i]["comment"]] = len( c_check["comment"] ) + 1

                try:
                    a = c_check["eveluation"][c_data[i]["eveluation"]]
                except:
                    c_check["eveluation"][c_data[i]["eveluation"]] = len( c_check["eveluation"] ) + 1

                result[lib.id_get(k)][h_name[i]]["comment"] = c_check["comment"][c_data[i]["comment"]]
                result[lib.id_get(k)][h_name[i]]["eveluation"] = c_check["eveluation"][c_data[i]["eveluation"]]
                

    dm.pickle_upload( "train_condition.pickle", result )
    dm.pickle_upload( "condition_change.pickle", c_check )
            
main()
