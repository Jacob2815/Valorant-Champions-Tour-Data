'''
This program is written to analyze the SQL date on my behalf and output them in pre-defined tables for quick and easy inputting into
a more visually appealing medium for public dissemination. 
'''

#import relevant libraries
import requests
import pandas as pd
import pyodbc
import MySQLdb
from prettytable import PrettyTable

#connecting to my local SQL database
db = MySQLdb.connect(
    host="localhost",
    user="scraping_user",
    passwd="scrapyboi",
    db="vctdata"
            )
print(db)

cursor = db.cursor()

#initializing lists of potential WHERE clause modifiers. Some are empty and some may be unused.
agent_list = ['astra', 'breach', 'brimstone', 'cypher', 'jett', 'kayo', 'killjoy', 'omen', 'phoenix', 'raze', 'reyna', 'sage', 'skye', 'sova', 'viper', 'yoru']

maps = ['ascent', 'bind', 'breeze', 'haven', 'icebox', 'split']

round_types = ["attack wins", "attack losses", "defense wins", "defense losses"]

calibers = []

regions = []

#defining a function to return a table that sorts the pick rate for every agent on every map
def pick_rate_table():
    pick_card = PrettyTable()
    pick_card.field_names = ["Pick Rates"] + maps
    for x in range(len(agent_list)):
        row_list = [agent_list[x]]
        for i in range(len(maps)):
            row_list.append(pick_rate(agent_list[x], maps[i]))
        pick_card.add_row(row_list)
    return pick_card

#defining a function to return a table that sorts the win rate for every agent on every map
def win_rate_table():
    win_card = PrettyTable()
    win_card.field_names = ["Win Rates"] + maps
    for x in range(len(agent_list)):
        row_list = [agent_list[x]]
        for i in range(len(maps)):
            row_list.append(win_rate(agent_list[x], maps[i]))
        win_card.add_row(row_list)
    return win_card

#defining a function to calculate the pick rate for a specified agent on a specified map
def pick_rate(agent, map):
    statement = "SELECT * FROM vctdata.vctdata WHERE (`agent 1` = '{}' OR `agent 2` = '{}' or `agent 3` = '{}' or `agent 4` = '{}' or `agent 5` = '{}') AND `map` = '{}';"
    output = cursor.execute(statement.format(agent, agent, agent, agent, agent, map))
    total = cursor.execute("SELECT * FROM vctdata.vctdata WHERE `map` = '" + map + "';")
    return round(((output / total) * 100), 1)

#defining a function to calculate the win rate for a specified agent on a specified map
def win_rate(agent, map):
    statement = "SELECT SUM(`win`) FROM vctdata.vctdata WHERE (`agent 1` = '{}' OR `agent 2` = '{}' or `agent 3` = '{}' or `agent 4` = '{}' or `agent 5` = '{}') AND `map` = '{}';"
    cursor.execute(statement.format(agent, agent, agent, agent, agent, map))
    output = cursor.fetchall()
    for x in output:
        output = x[0]
    total = "SELECT COUNT(id) FROM vctdata.vctdata WHERE (`agent 1` = '{}' OR `agent 2` = '{}' or `agent 3` = '{}' or `agent 4` = '{}' or `agent 5` = '{}') AND `map` = '{}';"
    cursor.execute(total.format(agent, agent, agent, agent, agent, map))
    total_output = cursor.fetchall()
    for x in total_output:
        total_output = x[0]
    return round(((output / total_output) * 100), 1)

#defining a function to calculate the attack round win rate for a specified agent on a specified map
def attack_win_rate(agent, map):
    statement = "SELECT (sum(`attack wins`) / (sum(`attack wins`) + sum(`attack losses`)) * 100) FROM vctdata.vctdata WHERE (`agent 1` = '{}' OR `agent 2` = '{}' or `agent 3` = '{}' or `agent 4` = '{}' or `agent 5` = '{}') AND `map` = '{}';"
    cursor.execute(statement.format(agent, agent, agent, agent, agent, map))
    output = cursor.fetchall()
    for x in output:
        output = x[0]
    return round(output, 1)

#defining a function to calculate the defense round win rate for a specified agent on a specified map
def defense_win_rate(agent, map):
    statement = "SELECT (sum(`defense wins`) / (sum(`defense wins`) + sum(`defense losses`)) * 100) FROM vctdata.vctdata WHERE (`agent 1` = '{}' OR `agent 2` = '{}' or `agent 3` = '{}' or `agent 4` = '{}' or `agent 5` = '{}') AND `map` = '{}';"
    cursor.execute(statement.format(agent, agent, agent, agent, agent, map))
    output = cursor.fetchall()
    for x in output:
        output = x[0]
    return round(output, 1)

#defining a function to act as a main menu
#currently unused as the program is limited to in-house work
def main_menu():
    print("Main Menu")
    print("1 Agent Profile")
    print("2 Map Profile")
    print("3 Top Teams")
    choice = raw(input("Enter your choice: "))
    return choice

#defining a function to list off every agent for a secondary menu
#currently unused as the program is limited to in-house work
def agent_menu():
    for x in range(len(agent_list)):
        print(str(x+1) + ". " + str(agent_list[x]))
    response = input("Enter your choice: ")
    agent_choice = agent_list[int(response)-1]

#defining a function to generate the data for a agent profile card, like a baseball card, showing that agent's key stats on each map. 
#designed to be scalable based on any new agents or maps added to the game and VCT events.
def agent_profile_generator(agent):
    profile_card = PrettyTable()
    profile_card.field_names = [agent] + ["Pick Rate", "Win Rate", "Attack Rate", "Defense Rate"]
    for x in range(len(maps)):
        profile_card.add_row([maps[x], pick_rate(agent, maps[x]), win_rate(agent, maps[x]), attack_win_rate(agent, maps[x]), defense_win_rate(agent, maps[x])])
    return profile_card

#defining a main function to house menu functions, which would house core table generating functions.
def main():
    choice = main_menu()
    if int(choice) == 1:
        agent = agent_menu()
'''
to-do list:
define function for a map profile card?
add win rate and pick rate to the main menu function.
figure out a way to analyze team comps and rank them by pick rates/win rates?
define function to rank agent pick/win rates by map, or map pick/win rates by agent.
'''
print(win_rate_table())
