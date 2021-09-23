import sys
from tqdm import tqdm
from bs4 import BeautifulSoup

sys.path.append( "../" )

import library as lib
import data_manage as dm

def data_get( soup ):
    data = {}
    tr_tag = soup.findAll( "tr" )

    for i in range( 0, len( tr_tag ) ):
        td_tag = tr_tag[i].findAll( "td" )
        
        if 2 < len( td_tag ) and td_tag[3].get( "class" ) != None \
           and td_tag[3].get( "class" )[0] == "txt_right":
            year_key = td_tag[0].text.replace( "\n", "" ).replace( " ", "" )
            
            try:
                passing_data = td_tag[20].text.replace( "\n", "" ).replace( " ", "" ).split( "-" )

                for r in range( 0, len( passing_data ) ):
                    passing_data[r] = float( passing_data[r] )

                data[year_key] = passing_data
            except:
                continue

    return data
    
def main():
    result = dm.pickle_load( "passing_data.pickle" )

    if result == None:
        result = {}

    horce_url = dm.pickle_load( "horce_url.pickle" )
    count = 0

    for k in tqdm( horce_url.keys() ):
        horce_name = k.replace( " ", "" )
        url = horce_url[k]
        
        try:
            a = result[horce_name]
        except:
            r, _ = lib.request( url )
            soup = BeautifulSoup( r.content, "html.parser" )
            result[horce_name] = data_get( soup )

        count += 1
        if count % 100 == 0:
            dm.pickle_upload( "passing_data.pickle", result )

    dm.pickle_upload( "passing_data.pickle", result )
    
main()
