import SekitobaLibrary as lib
import SekitobaDataManage as dm

def main():
    race_data = dm.pickle_load( "race_data.pickle" )
    key_list = list( race_data.keys() )
    
    for k in key_list:
        race_id = lib.idGet( k )
        year = race_id[0:4]

        if year == "2021":
            race_data.pop( k )

    dm.pickle_upload( "race_data.pickle", race_data )

if __name__ == "__main__":
    main()
