import sekitoba_library as lib

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

def web_check( soup ):
    title = soup.find( "title" ).text.replace( "　", "" )

    if title == "パラメータエラーJRA":
        return False

    return True

def jra_id_get( race_id ):
    base_name = "pw155ou10"
    year = race_id[0:4]
    race_place_num = race_id[4:6] #place
    num = race_id[6:8] #回
    day = race_id[8:10] #日
    race = race_id[10:12] #?R
    jra_id = base_name + race_place_num + year + num + day + race + year
    print( jra_id )

def main():
    race_id = "202106050901"
    jra_id_get( race_id )
    return
    url = "https://www.jra.go.jp/JRADB/accessO.html"
    values = { "cname": "pw155ou10 06 2021 05 07 01 2021 1225 Z/5E" }#place_num 2021 5回7日 R 2021 12/25
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
    res = post_connect( req )
    data = gzip.decompress( res.read() )
    html_text = data.decode( 'shift_jis' )
    soup = BeautifulSoup( html_text, "html.parser" )
    web_check( soup )
    return
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
                            

    for k in result.keys():
        print( result[k] )
            
   
main()
