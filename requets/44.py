import requests

r = requests.get('http://api.openweathermap.org/data/2.5/weather',
                 {
                     'q': 'Jerusalem, Israel',
                     'APPID': 'c477f6b3dab7a958564af48c326012f7'
                 })

print(r.json())
