import numpy as np
import pickle
import sys
from tqdm import tqdm

my_directory = "/Users/kansei/Desktop/horse/"
d = "/Users/kansei/Desktop/horse/database/"

sys.path.append( "../" )

import library as lib
import data_manage as dm

def dist_kind( str_data ):
    dist = str( int( lib.k_dist( str_data[13] ) * 1000 ) )
    _, k = lib.dist( str_data[13] )

    return dist, str( k )

def updata_append( file_name, result ):
    f = open( file_name, "r" )
    all_data = f.readlines()

    for i in range( 0, len( all_data ) ):        
        all_data[i] = all_data[i].replace( "\n", "" )
        str_data = all_data[i].split( " " )
        place_num = str( lib.place_num( str_data[1] ) )

        #対象のレースを選択
        if len( str_data ) == 22 \
           and not lib.place_num( str_data[1] ) == 0:
            dist, kind = dist_kind( str_data )

            try:
                data = float( str_data[18] )
            except:
                data = 0

            if not len( kind ) == 0:
                if not place_num in result:
                    result[place_num] = {}

                if not kind in result[place_num]:
                    result[place_num][kind] = {}

                if not dist in result[place_num][kind]:
                    result[place_num][kind][dist] = {}
                    result[place_num][kind][dist]["count"] = 1
                    result[place_num][kind][dist]["data"] = data
                else:
                    result[place_num][kind][dist]["count"] += 1
                    result[place_num][kind][dist]["data"] += data
            


def main():
    result = {}
    horce_url = dm.pickle_load( "horce_url.pickle" )

    for k in tqdm( horce_url.keys() ):
        horce_name = k.replace( " ", "" )
        updata_append( lib.my_directory + "database/" + horce_name + ".txt", result )

    for k in result.keys():
        for kk in result[k].keys():
            for kkk in result[k][kk].keys():
                result[k][kk][kkk]["data"] /= result[k][kk][kkk]["count"]

    dm.pickle_upload( "up_average.pickle", result )

main()
