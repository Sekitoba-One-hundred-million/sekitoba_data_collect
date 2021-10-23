from argparse import ArgumentParser

import sekitoba_data_manage as dm
import sekitoba_library as lib

def main():
    parser = ArgumentParser()
    parser.add_argument( "-f", type=str, default = "", help = "optional" )

    file_name = parser.parse_args().f
    print( file_name )
    base_data = dm.pickle_load( file_name )
    horce_id_data = dm.pickle_load( "horce_id.pickle" )
    key_list = list( base_data.keys() )
    dm.pickle_upload( file_name + ".test", base_data )
    
    for k in key_list:
        h_id = horce_id_data[k]
        base_data[h_id] = base_data[k]
        del( base_data[k] )

    dm.pickle_upload( file_name, base_data )

def race_id_change():
    race_data = dm.pickle_load( "race_data.pickle" )
    horce_id_data = dm.pickle_load( "horce_id.pickle" )
    dm.pickle_upload( "race_data.pickle.test", race_data )

    for k in race_data.keys():
        key_list = list( race_data[k].keys() )

        for kk in key_list:
            horce_name = kk.replace( " ", "" )
            h_id = horce_id_data[horce_name]
            race_data[k][h_id] = race_data[k][kk]
            del( race_data[k][kk] )
            
    dm.pickle_upload( "race_data.pickle", race_data )

    

main()
