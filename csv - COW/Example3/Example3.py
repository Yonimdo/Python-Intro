import csv

countries = []
continents = {}
continents_pages_content = {}
main_content = ""
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


def moody_run_once(country):
    global main_content
    country['short_name'] = country['short_name'].lower()
    with open('{}.html'.format(country['short_name']), 'w') as page:
        page.write(templates['template'].format(**country))
        page.write(templates['space'])
        page.write(templates['link'].format('index', 'Index'))
        page.write(templates['space'])
        page.write(
            templates['link'].format(templates['continent'].format(country['continent']), 'Go to my continent'))
    tmp_name_link = templates['link'].format(country['short_name'], country['name'])
    tmp_data = "{}: {} km".format(tmp_name_link,
                                  haversine(ISRAEL_LON, ISRAEL_LAT, float(country['lon']), float(country['lat'])))
    main_content += templates['li'].format(tmp_data, country['short_name'].lower())
    # continent_page = continents_pages_content.get(country['continent'], "")
    # continent_page += templates['li'].format(tmp_data, country['short_name'])
    if country['continent'] in continents_pages_content:
        continents_pages_content[country['continent']] += templates['li'].format(tmp_data, country['short_name'])
    else:
        continents_pages_content[country['continent']] = ""
    return country['continent']


templates = {
    'ul': '<ul>{}</ul>',
    'li': '<li><img src="http://static.10x.org.il/flags/{1}.png">{0}</li>',
    'link': '<a href="{}.html">{}</a>',
    'space': '<br><br>',
    'continent': 'continent_{}'
}

with open(r'template.txt', encoding='UTF8') as template:
    templates['template'] = template.read()

with open('../cow.csv', encoding='UTF8') as f:
    countries = [country for country in csv.DictReader(f)]

continents = {moody_run_once(country) for country in countries}

for key in continents_pages_content:
    with open('{}.html'.format(templates['continent'].format(key)), 'w') as page:
        page.write(templates['link'].format('index','Index'))
        page.write(templates['space'])
        page.write(templates['ul'].format(continents_pages_content[key]))

with open('index.html', 'w') as f:
    f.write(templates['ul'].format(main_content))


print(continents_pages_content)
