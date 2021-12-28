import requests

r = requests.get( "https://race.netkeiba.com/odds/index.html?type=b5&race_id=202109050202&housiki=c0" )
print( r.headers )

