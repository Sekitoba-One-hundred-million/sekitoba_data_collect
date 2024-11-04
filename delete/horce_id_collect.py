import SekitobaLibrary as lib
import SekitobaDataManage as dm

def main():
    result = {}
    horce_url = dm.pickle_load( "horce_url.pickle" )

    for k in horce_url.keys():
        result[k] = horce_url[k].split( "/" )[-1]

    dm.pickle_upload( "horce_id.pickle", result )
    
main()

    
