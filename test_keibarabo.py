import sys

sys.path.append( "../" )

import library as lib

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
            #the_page = response.read()
            #body = json.loads(response.read().e)
            #headers = response.getheaders() # ヘッダー(dict)
            #status = response.getcode() # ステータスコード
            #data = gzip.decompress(response.read())
            #text = data.decode( 'shift_jis' )
            #print( text )

            return response
        except:        
            print( "timeout" )
            time.sleep( 2 )

    return None
            
def main():
    url = "https://www.jra.go.jp/JRADB/accessS.html"
    values = { "cname": "pw01ses1001 2016 01 03 2016 0806 /E5" }#2016 1回札幌3日 8/6
    values = { "cname": "pw01ses1010 2016 02 03 2016 0806 /F5" }#2016 ２回小倉３日 8/6
    values = { "cname": "pw01ses10062018030520180407/C0" }#2018 3回中山5日 4/7
    #values = { "cname": "pw01srl1006 2020 04 09 2020 1004 /4E" }#2018 3回中山5日 4/7

    #values = { "cname": "pw01ses10102016020320160806/F5" }
        
    data = urllib.parse.urlencode(values)
    data = data.encode('ascii') # data should be bytes
    headers = { "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "ja,en-US;q=0.9,en;q=0.8",
                "Cache-Control": "max-age=0",
                "Connection": "keep-alive",
                "Content-Length": 38,
                "Content-Type": "application/x-www-form-urlencoded",
                "Host": "www.jra.go.jp",
                "Origin": "https://www.jra.go.jp",
                "Referer": "https://www.jra.go.jp/JRADB/accessS.html",
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
    div_tag = soup.findAll( "div" )

    for div in div_tag:
        class_name = div.get( "class" )

        if not class_name == None \
           and class_name[0] == "race_result_unit":
            id_name = div.get( "id" )
            id_name = id_name[0]            
            race_num = ""

            for i in range( 0, len( id_name ) ):
                if str.isdecimal( id_name[i] ):
                    race_num += id_name[i]

            tbody = div.find( "tbody" )
            tr_tag = tbody.findAll( "tr" )
            print( tr_tag )
main()
