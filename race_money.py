from bs4 import BeautifulSoup

import SekitobaLibrary as lib
import SekitobaDataManage as dm


def race_money_get( url ):
    money = 0
    r, _ = lib.request( url ) #requests.get( url )
    soup = BeautifulSoup( r.content, "html.parser" )
    div_tag = soup.findAll( "div" )

    for div in div_tag:
        class_name = div.get( "class" )

        if not class_name == None \
           and class_name[0] == "RaceData02":
            span_tag = div.findAll( "span" )

            for span in span_tag:
                text = span.text.replace( "\n", "" )
                split_text = text.split( "," )

                if len( split_text ) > 1 \
                   and "本賞金" in split_text[0]:
                    try:
                        money = float( split_text[0].split( ":" )[1] )
                    except:
                        money = 0
                    break
            break

    return money

def main():
    result = dm.pickle_load( "race_money_data.pickle" )

    if result == None:
        result = {}
    
    base_url = "https://race.netkeiba.com/race/result.html?race_id="
    race_data = dm.pickle_load( "race_data.pickle" )

    url_data = []
    key_data = []

    for k in race_data.keys():
        race_id = lib.idGet( k )
        url = base_url + race_id

        if not race_id in result:
            url_data.append( url )
            key_data.append( race_id )

    add_data = lib.thread_scraping( url_data, key_data ).data_get( race_money_get )

    for k in add_data.keys():
        result[k] = add_data[k]
    
    dm.pickle_upload( "race_money_data.pickle", result )

main()

