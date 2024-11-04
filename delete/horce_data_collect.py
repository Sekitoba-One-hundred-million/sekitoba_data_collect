import sys
from tqdm import tqdm
from bs4 import BeautifulSoup

import SekitobaLibrary as lib
import SekitobaDataManage as dm

def http_analyze( url, horce_data, trainer_url, h_name ):
    data = {}

    r, _ = lib.request( url )
    soup = BeautifulSoup( r.content, "html.parser" )
    
    h_sex = sex_collect( soup )
    h_birth = horce_birthday( soup )
    t_name, t_url = horse_trainer( soup )
    cha = horce_charactor( soup )

    data["sex"] = h_sex
    data["birth"] = h_birth
    data["trainer"] = t_name
    data["charactor"] = cha
    horce_data[h_name] = data
    trainer_url[t_name] = t_url

def horce_charactor( soup ):
    img = soup.findAll( "img" )
    count = 0
    cha = {}
    cha["course"] = 0
    cha["dist"] = 0
    cha["foot"] = 0
    cha["growth"] = 0
    cha["heavy_baba"] = 0
    
    for i in range( 0, len( img ) ):
        if count == 5:
            break

        alt = img[i].get( "alt" )
        if not alt == None:
            if alt == "芝":
                cha["course"] = cha_check( img, i )
                count += 1
            elif alt == "短い":
                cha["dist"] = cha_check( img, i )
                count += 1
            elif alt == "逃げ":
                cha["foot"] = cha_check( img, i )
                count += 1
            elif alt == "早熟":
                cha["growth"] = cha_check( img, i )
                count += 1
            elif alt == "得意":
                cha["heavy_baba"] = cha_check( img, i )
                count += 1

    return cha

def cha_check( img, i ):
    s1 = img[i+1].get( "width" )
    s2 = img[i+3].get( "width" )
    if s2 < s1:
        return 1
    elif s1 < s2:
        return 2
    else:
        return 3

    return 0

def horse_trainer( soup ):
    table = soup.findAll( "table" )
    trainer_name = ""
    trainer_url = ""
    
    for i in range( 0, len( table ) ):
        table_class_name = table[i].get( "class" )
        if not table_class_name == None \
           and table_class_name[0] == "db_prof_table":
            a = table[i].find( "a" )
            href = a.get( "href" )
            title = a.get( "title" )
            trainer_name = title.replace( " ", "" )
            trainer_url = "https://db.netkeiba.com" + href
            break

    return trainer_name, trainer_url

def horce_birthday( soup ):
    table = soup.findAll( "table" )
    year = ""
    
    for i in range( 0, len( table ) ):
        table_class_name = table[i].get( "class" )
        if not table_class_name == None \
           and table_class_name[0] == "db_prof_table":
            td = table[i].find( "td" )
            
            for r in range( 0, len( td.text ) ):
                if str.isdecimal( td.text[r] ):
                    year += td.text[r]
                else:
                    break
            break

    try:
        year = int( year )
    except:
        year = 0

    return year

def horse_name( soup ):
    horse_name = ""
    div = soup.findAll( "div" )

    for i in range( 0, len( div ) ):
        div_class_name = div[i].get( "class" )
        if not div_class_name == None \
           and div_class_name[0] == "horse_title":
            h1 = div[i].find( "h1" )
            horse_name = h1.text
            horse_name = horse_name.replace( " ", "" )
            break

    return horse_name
            
def sex_collect( soup ):
    horse_sex = 0
    div = soup.findAll( "div" )

    for i in range( 0, len( div ) ):
        div_class_name = div[i].get( "class" )
        if not div_class_name == None \
           and div_class_name[0] == "horse_title":
            p = div[i].findAll( "p" )

            for r in range( 0, len( p ) ):
                p_class_name = p[r].get( "class" )
                if not p_class_name == None \
                   and p_class_name[0] == "txt_01":
                    for t in range( 0, len( p[r].text ) ):
                        if p[r].text[t] == "牡":
                            horse_sex = 1
                        elif p[r].text[t] == "牝":
                            horse_sex = 2                        
                    break
            break

    return horse_sex

def main():
    horce_data = dm.pickle_load( "horce_data.pickle" )
    
    if horce_data == None:
        horce_data = {}
        
    trainer_url = {}
    count = 0

    horce_url = dm.pickle_load( "horce_url.pickle" )

    for k in tqdm( horce_url.keys() ):
        count += 1
        url = horce_url[k]
        
        try:
            aa = horce_data[k]
        except:
            http_analyze( url, horce_data, trainer_url, k )

        if count % 100 == 0:
            dm.pickle_upload( "horce_data.pickle", horce_data )
            dm.pickle_upload( "trainer_url.pickle", trainer_url )

    dm.pickle_upload( "horce_data.pickle", horce_data )
    dm.pickle_upload( "trainer_url.pickle", trainer_url )

main()
