import requests
from pprint import pprint

matches = requests.get(r'http://worldcup.sfg.io/matches')

template = "{} - {}: {}-{}"
results = []
for match in matches.json():
    results.append(template.format(match['away_team']['country'], match['home_team']['country'], match['away_team']['goals'],
                              match['home_team']['goals']))

pprint(results)
