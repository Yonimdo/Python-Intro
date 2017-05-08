from csv import DictReader
from math import radians, cos, sin, asin, sqrt

ISRAEL_LAT, ISRAEL_LON = 31.5, 34.75


def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    km = 6367 * c
    return km


templates = {
    'ul': '<ul>{}</ul>',
    'li': '<li><img src="http://static.10x.org.il/flags/{1}.png">{0}</li>',
}

content = ""


with open('cow.csv', encoding='UTF8') as f:
    reader = DictReader(f)
    for d in reader:
        tmp_data = "{}: {} km".format(d['name'],
                                      haversine(ISRAEL_LON, ISRAEL_LAT, float(d['lon']), float(d['lat'])))
        content += templates['li'].format(tmp_data, d['short_name'].lower())

with open('index.html', 'w') as f:
    f.write(templates['ul'].format(content))
