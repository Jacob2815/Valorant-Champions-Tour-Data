'''
Guide source is: https://realpython.com/beautiful-soup-web-scraper-python/
'''
#import relevant libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd
import pyodbc
import MySQLdb

#specify URL, page, and parse it with BS
URL = input('Enter the URL: ')
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')

def extract_alt(agent_list):
    new_list = []
    for agent in agent_list:
        new_list.append(agent['alt'])
    return new_list

#isolate match header for event/round names
match_header = soup.find('a', class_='match-header-event')
event_name = match_header.find('div', style='font-weight: 700;')
event_round = match_header.find('div', class_='match-header-event-series')
event_name = event_name.get_text(strip=True)
event_round = event_round.get_text(strip=True)

#isolate left team vs right team names, everything on vlr.gg uses left vs right and the order never changes
left_team_name = soup.find('div', class_='match-header-link-name mod-1')
right_team_name = soup.find('div', class_='match-header-link-name mod-2')
left_team_name = left_team_name.find('div', class_='wf-title-med')
right_team_name = right_team_name.find('div', class_='wf-title-med')
left_team_name = left_team_name.get_text(strip=True)
right_team_name = right_team_name.get_text(strip=True)

#pull the agents from the tables
agents = soup.find_all('table', class_='wf-table-inset mod-overview')
#each match page has an overview that muddies the data that always positions itself in the HTML code as the second entry. removes both teams from that entry.
remove1 = agents.pop(2)
remove2 = agents.pop(2)

#isolate each team's agent choices based on map
left_team_map_one_agents_source = agents[0].find_all('img', alt=True)
right_team_map_one_agents_source = agents[1].find_all('img', alt=True)
left_team_map_two_agents_source = agents[2].find_all('img', alt=True)
right_team_map_two_agents_source = agents[3].find_all('img', alt=True)
left_team_map_three_agents_source = []
right_team_map_three_agents_source = []

left_team_map_one_agents = extract_alt(left_team_map_one_agents_source)
right_team_map_one_agents = extract_alt(right_team_map_one_agents_source)
left_team_map_two_agents = extract_alt(left_team_map_three_agents_source)
right_team_map_two_agents = extract_alt(right_team_map_three_agents_source)

#isolates the header for each map.
map_header = soup.find_all("div", class_='vm-stats-game-header')
#finds the map information and step-by-step isolates the map/s name
maps = soup.find_all('div', class_='map')
map_one_and_duration = map_header[0].find('div', class_='map')
map_two_and_duration = map_header[1].find('div', class_='map')
map_three_and_duration = []
map_one = map_one_and_duration.find('span')
map_two = map_two_and_duration.find('span')
map_one = map_one.get_text(strip=True)
map_two = map_two.get_text(strip=True)

attack_round_wins = soup.find_all('span', class_='mod-t')
defense_round_wins = soup.find_all('span', class_='mod-ct')

left_team_map_one_attack_wins = attack_round_wins[0].get_text()
left_team_map_one_defense_wins = defense_round_wins[0].get_text()
right_team_map_one_attack_wins = attack_round_wins[1].get_text()
right_team_map_one_defense_wins = defense_round_wins[1].get_text()

left_team_map_two_attack_wins = attack_round_wins[2].get_text()
left_team_map_two_defense_wins = defense_round_wins[2].get_text()
right_team_map_two_attack_wins = attack_round_wins[3].get_text()
right_team_map_two_defense_wins = defense_round_wins[3].get_text()

if len(maps) == 3:
    left_team_map_three_agents_source = agents[4].find_all('img', alt=True)
    right_team_map_three_agents_source = agents[5].find_all('img', alt=True)
    left_team_map_three_agents = extract_alt(left_team_map_three_agents_source)
    right_team_map_three_agents = extract_alt(right_team_map_three_agents_source)
    map_three_and_duration = map_header[2].find('div', class_='map')
    map_three = map_three_and_duration.find('span')
    map_three = map_three.get_text(strip=True)
    left_team_map_three_attack_wins = attack_round_wins[4].get_text(strip=True)
    left_team_map_three_defense_wins = defense_round_wins[4].get_text(strip=True)
    right_team_map_three_attack_wins = attack_round_wins[5].get_text(strip=True)
    right_team_map_three_defense_wins = defense_round_wins[5].get_text(strip=True)
    left_team_won_map_three = False
    right_team_won_map_three = False
    if left_team_map_three_attack_wins + left_team_map_three_defense_wins > right_team_map_three_attack_wins + right_team_map_three_defense_wins:
        left_team_won_map_three = True
    else:
        right_team_won_map_three = True


left_team_won_map_one = False
right_team_won_map_one = False
left_team_won_map_two = False
right_team_won_map_two = False

if left_team_map_one_attack_wins + left_team_map_one_defense_wins > right_team_map_one_attack_wins + right_team_map_one_defense_wins:
    left_team_won_map_one = True
else:
    right_team_won_map_one = True

if left_team_map_two_attack_wins + left_team_map_two_defense_wins > right_team_map_two_attack_wins + right_team_map_two_defense_wins:
    left_team_won_map_two = True
else:
    right_team_won_map_two = True

print(str(event_name))
print(str(event_round))
print(str(left_team_name) + ' vs ' + str(right_team_name))
print("Map one: " + str(map_one))
print("Map two: " + str(map_two))
if len(maps) == 3:
    print("Map three: " + str(map_three))


#db = MySQLdb.connect(
#        host="localhost",
#        user="scraping_user",
#        passwd="scrapyboi",
#        db="vctdata"
#        )

#print(db)

#cursor = db.cursor()

#update_table_map_one = cursor.execute("");
#update_table_map_two = cursor.execute("");

#if len(maps) == 3:
    #update_table_map_three = cursor.execute("");


#db.close()
