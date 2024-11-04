import SekitobaLibrary as lib
import SekitobaDataManage as dm

from tqdm import tqdm
from bs4 import BeautifulSoup
from selenium import webdriver

def data_get( driver, url ):
    result = []
    driver, _ = lib.driverRequest( driver, url )
    html = driver.page_source.encode('utf-8')
    soup = BeautifulSoup( html, "html.parser" )        

    div_tag = soup.findAll( "div" )

    for div in div_tag:
        class_name = div.get( "class" )

        if not class_name == None \
          and len( class_name ) == 4 \
          and class_name[0] == "DeployRace_SlideBoxItem" \
          and class_name[1] == "slick-slide" \
          and class_name[2] == "slick-current" \
          and class_name[3] == "slick-active":
            dl_tag = div.findAll( "dl" )
            
            for dl in dl_tag:
                li_tag = dl.findAll( "li" )
                instance = []
                
                for li in li_tag:
                    span = li.find( "span" )
                    instance.append( span.text )

                result.append( instance )

    return result

def main():
    result = {}
    race_data = dm.pickle_load( "race_data.pickle" )
    driver = webdriver.Chrome()

    for k in tqdm( race_data.keys() ):
        race_id = lib.idGet( k )
        year = race_id[0:4]
        
        if year == "2020":
            url = "https://race.netkeiba.com/race/shutuba.html?race_id=" + race_id
            result[race_id] = data_get( driver, url )

    dm.pickle_upload( "deployment2020.pickle", result )

if __name__ == "__main__":
    main()
