import sekitoba_library as lib
import sekitoba_data_manage as dm

import requests
import time
import json
from requests.exceptions import Timeout
import urllib.request, urllib.parse
import gzip
from bs4 import BeautifulSoup

def post_connect( req ):
    for i in range( 0, 30 ):
        try:
            response = urllib.request.urlopen( req, timeout = 3 )

            return response
        except:        
            print( "timeout" )
            time.sleep( 2 )

    return None

def req_create( cname ):
    url = "https://www.jra.go.jp/JRADB/accessO.html"
    values = { "cname": cname }#place_num 2021 5回7日 R 2021 12/25
    data = urllib.parse.urlencode(values)
    data = data.encode('ascii') # data should be bytes
    headers = { "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "ja,en-US;q=0.9,en;q=0.8",
                "Cache-Control": "max-age=0",
                "Connection": "keep-alive",
                "Content-Length": 41,
                "Content-Type": "application/x-www-form-urlencoded",
                "Host": "www.jra.go.jp",
                "Origin": "https://www.jra.go.jp",
                "Referer": "https://www.jra.go.jp/JRADB/accessO.html",
                "sec-ch-ua": '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
                "sec-ch-ua-mobile": 70,
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "same-origin",
                "Sec-Fetch-User": "?1",
                "Upgrade-Insecure-Requests": 1,
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36" }
    
    req = urllib.request.Request(url, data, headers )

    return req

def web_check( soup ):
    title = soup.find( "title" ).text.replace( "　", "" )

    if title == "パラメータエラーJRA":
        return False

    return True

def jra_id_get( race_id, ymd ):
    base_name = "pw155ou10"
    year = race_id[0:4]
    race_place_num = race_id[4:6] #place
    num = race_id[6:8] #回
    race_day = race_id[8:10] #日
    race = race_id[10:12] #?R

    if ymd["month"] < 10:
        month = "0" + str( int( ymd["month"] ) )
    else:
        month = str( int( ymd["month"] ) )

    if ymd["day"] < 10:
        day = "0" + str( int( ymd["day"] ) )
    else:
        day = str( int( ymd["day"] ) )

    jra_id = base_name + race_place_num + year + num + race_day + race + year + month + day + "Z/"
    return jra_id

def data_collect( soup ):
    result = {}
    ul_tag = soup.findAll( "ul" )    
    
    for ul in ul_tag:
        class_name = ul.get( "class" )

        if not class_name == None \
          and class_name[0] == "wide_list":
            li_tag = ul.findAll( "li" )

            for li in li_tag:
                caption = li.find( "caption" )
                horce_num1 = caption.text.replace( " ", "" )
                tr_tag = li.findAll( "tr" )
                lib.dic_append( result, horce_num1, {} )

                for tr in tr_tag:
                    instance = {}
                    instance["min"] = 0
                    instance["max"] = 0
                    th = tr.find( "th" )
                    horce_num2 = th.text.replace( " ", "" )
                    td = tr.find( "td" )
                    span_tag = td.findAll( "span" )

                    for span in span_tag:
                        span_class_name = span.get( "class" )
                        
                        if not span_class_name == None:
                            #print( span )
                            if span_class_name[0] == "min":
                                #print( span.text )
                                instance["min"] = lib.data_check( span.text )
                            elif span_class_name[0] == "max":
                                #print( span.text )
                                instance["max"] = lib.data_check( span.text )

                    result[horce_num1][horce_num2] = instance

    return result

def main():
    result = dm.pickle_load( "wide_odds_data.pickle")
    race_day = dm.pickle_load( "race_day.pickle" )
    race_data = dm.pickle_load( "race_data.pickle" )

    if result == None:
        result = {}

    for k in race_data.keys():
        race_id = lib.id_get( k )
        year = race_id[0:4]

        if not year == "2021":
            continue
        
        try:
            a = result[race_id]            
            continue
        except:
            check = False
        
        try:
            base_cname = jra_id_get( race_id, race_day[race_id] )
        except:
            continue

        for i in range( 0, 256 ):
            d = hex(i)[2:].upper()

            if len( d ) == 1:
                d = "0" + d
        
            cname = base_cname + d
            req = req_create( cname )
            res = post_connect( req )
            data = gzip.decompress( res.read() )
            html_text = data.decode( 'shift_jis' )
            soup = BeautifulSoup( html_text, "html.parser" )
    
            if web_check( soup ):
                check = True
                break

        if check:
            result[race_id] = data_collect( soup )
            print( "success {}".format( race_id ) )
        else:
            print( "error {}".format( race_id ) )

        lib.dm.pickle_upload( "wide_odds_data.pickle", result )
   
main()
