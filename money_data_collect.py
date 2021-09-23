import requests
import pickle
import sys
import numpy as np
from tqdm import tqdm
from bs4 import BeautifulSoup

sys.path.append( "../" )

import library as lib
import data_manage as dm

def money_get( url ):
    result = []
    r, _ = lib.request( url )
    soup = BeautifulSoup( r.content, "html.parser" )
    tr_tag = soup.findAll( "tr" )

    for i in range( 0, len( tr_tag ) ):
        td_tag = tr_tag[i].findAll( "td" )
        
        if 2 < len( td_tag ) and td_tag[3].get( "class" ) != None \
           and td_tag[3].get( "class" )[0] == "txt_right":
            try:
                 result.append( float( td_tag[27].text.replace( "\n", "" ).replace( " ", "" ) ) )
            except:
                result.append( 0 )

    return result                        

def data_update( horce_name, money_data ):
    f = open( "../database/" + horce_name + ".txt", "r" )
    horce_data = f.readlines()
    f.close()

    for i in range( 0, len( horce_data ) ):
        horce_data[i] = horce_data[i].replace( "\n", "" )
        try:
            horce_data[i] = horce_data[i] + str( money_data[i] )
        except:
            horce_data[i] = horce_data[i] + "0"
            
    f = open( "../database/" + horce_name + ".txt", "w" )

    for i in range( 0, len( horce_data ) ):
        f.write( horce_data[i] + " \n" )

    f.close()
    

def main():
    result = {}
    count = 0
    horce_url = dm.pickle_load( "horce_url.pickle" )

    for k in tqdm( horce_url.keys() ):
        horce_name = k.replace( " ", "" )
        money_data = money_get( horce_url[k] )
        data_update( horce_name, money_data )
        
    dm.pickle_upload( "money.pickle", money_data )

main()

