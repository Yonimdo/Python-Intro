import requests
from pprint import pprint

yellow_cards_count = 0
matches = requests.get(r'http://worldcup.sfg.io/matches')

teams_cards_count = {}

for match in matches.json():
    for event in match['home_team_events']:
        if event['type_of_event'] == 'yellow-card':
            yellow_cards_count += 1
            teams_cards_count[match['home_team']['code']] = teams_cards_count.get(match['home_team']['code'],0)+1
    for event in match['away_team_events']:
        if event['type_of_event'] == 'yellow-card':
            yellow_cards_count += 1
            teams_cards_count[match['away_team']['code']] = teams_cards_count.get(match['home_team']['code'],0)+1

teams_cards_count = [(key,teams_cards_count[key]) for key in teams_cards_count]


pprint(sorted(teams_cards_count,key=lambda x:x[1])[::-1])
