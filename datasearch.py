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
from itertools import combinations

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
def main():
    i = 1
    while i == 1:
        print("---------------")
        print("Main Menu")
        print("---------------")
        print("1 Pick Rates")
        print("2 Win Rates")
        print("3 Agent Profile")
        print("4 Map Profile")
        print("5 Top Teams")
        print("6 Rankings")
        print()
        print("Enter 0 to End.")
        print("---------------")
        choice = input("Enter your choice: ")
        if int(choice) == 1:
            table = pick_rate_table()
            print(table)
            continue
        elif int(choice) == 2:
            table = win_rate_table()
            print(table)
            continue
        elif int(choice) == 3:
            agent_menu()
            response = input("Enter your choice: ")
            output = agent_list[int(response)-1]
            print(agent_profile_generator(output))
            continue
        elif int(choice) == 4:
            maps_menu()
            response = input("Enter your choice: ")
            output = maps[int(response)-1]
            print(map_profile_generator(output))
            continue
        elif int(choice) == 5:
            print("---------------")
            print("1 All Maps")
            print("2 Specify Map")
            print("---------------")
            top_teams_response = input("Enter your choice: ")
            if int(top_teams_response) == 1:
                team_comp_rankings_all_maps()
            elif int(top_teams_response) == 2:
                team_comp_rankings()
            else:
                print("Try again.")
            continue
        elif int(choice) == 6:
            rankings()
            continue
        elif int(choice) == 0:
            print("Terminating.")
            i = 0
        else:
            print("---------------")
            print("Try again.")
            continue

#defining functions for submenus
def agent_menu():
    print("---------------")
    for x in range(len(agent_list)):
        print(str(x+1) + ". " + str(agent_list[x]))
    print("---------------")

def maps_menu():
    print("---------------")
    for x in range(len(maps)):
        print(str(x+1) + ". " + str(maps[x]))
    print("---------------")

def rankings():
    print("---------------")
    print("1 Pick Rate")
    print("2 Win Rate")
    print("---------------")
    response = input("Enter your choice: ")
    print("---------------")
    print("Specify Map or Agent?")
    print("---------------")
    print("1 Map")
    print("2 Agent")
    print("---------------")
    specify = input("Enter your choice: ")
    if int(response) == 1:
        if int(specify) == 1:
            maps_menu()
            choice = input("Enter your choice: ")
            output = maps[int(choice)-1]
            table = PrettyTable()
            table.field_names = [output] + ["Pick Rate"]
            for x in range(len(agent_list)):
                table.add_row([agent_list[x], pick_rate(agent_list[x], output)])
            print(table.get_string(sortby="Pick Rate", reversesort=True))
        elif int(specify) == 2:
            agent_menu()
            choice = input("Enter your choice: ")
            output = agent_list[int(choice)-1]
            table = PrettyTable()
            table.field_names = [output] + ["Pick Rate"]
            for x in range(len(maps)):
                table.add_row([maps[x], pick_rate(output, maps[x])])
            print(table.get_string(sortby="Pick Rate", reversesort=True))
        else:
            print("Try again.")
    elif int(response) == 2:
        if int(specify) == 1:
            maps_menu()
            choice = input("Enter your choice: ")
            output = maps[int(choice)-1]
            table = PrettyTable()
            table.field_names = [output] + ["Win Rate"]
            for x in range(len(agent_list)):
                table.add_row([agent_list[x], win_rate(agent_list[x], output)])
            print(table.get_string(sortby="Win Rate", reversesort=True))
        elif int(specify) == 2:
            agent_menu()
            choice = input("Enter your choice: ")
            output = agent_list[int(choice)-1]
            table = PrettyTable()
            table.field_names = [output] + ["Win Rate"]
            for x in range(len(maps)):
                table.add_row([maps[x], win_rate(output, maps[x])])
            print(table.get_string(sortby="Win Rate", reversesort=True))
        else:
            print("Try again.")
    else:
        print("Try again.")

#defining functions to generate the data for an agent or map profile card, like a baseball card, showing that agent's key stats on each map, or all the agents stats on a given map. 
#designed to be scalable based on any new agents or maps added to the game and VCT events.
def agent_profile_generator(agent):
    profile_card = PrettyTable()
    profile_card.field_names = [agent] + ["Pick Rate", "Win Rate", "Attack Rate", "Defense Rate"]
    for x in range(len(maps)):
        profile_card.add_row([maps[x], pick_rate(agent, maps[x]), win_rate(agent, maps[x]), attack_win_rate(agent, maps[x]), defense_win_rate(agent, maps[x])])
    return profile_card

def map_profile_generator(map):
    map_card = PrettyTable()
    map_card.field_names = [map] + ["Pick Rate", "Win Rate", "Attack Rate", "Defense Rate"]
    for x in range(len(agent_list)):
        map_card.add_row([agent_list[x], pick_rate(agent_list[x], map), win_rate(agent_list[x], map), attack_win_rate(agent_list[x], map), defense_win_rate(agent_list[x], map)])
    return map_card

#defining a function to analyze every possible team composition on a map and rank them by win rate, followed by the same function specified for all maps
def team_comp_rankings():
    maps_menu()
    choice = input("Enter your choice: ")
    response = maps[int(choice)-1]
    statement = "SELECT COUNT(`id`) FROM vctdata.vctdata WHERE (`agent 1` = '{}' OR `agent 2` = '{}' or `agent 3` = '{}' or `agent 4` = '{}' or `agent 5` = '{}') \
    AND (`agent 1` = '{}' OR `agent 2` = '{}' or `agent 3` = '{}' or `agent 4` = '{}' or `agent 5` = '{}') \
    AND (`agent 1` = '{}' OR `agent 2` = '{}' or `agent 3` = '{}' or `agent 4` = '{}' or `agent 5` = '{}') \
    AND (`agent 1` = '{}' OR `agent 2` = '{}' or `agent 3` = '{}' or `agent 4` = '{}' or `agent 5` = '{}') \
    AND (`agent 1` = '{}' OR `agent 2` = '{}' or `agent 3` = '{}' or `agent 4` = '{}' or `agent 5` = '{}') \
    AND `map` = '{}';"
    table = PrettyTable()
    table.field_names = [response] + ["Pick Rate"] + ["Win Rate"] + ["Total Picks"]
    comb = combinations(agent_list, 5)
    for i in list(comb):
        output = cursor.execute(statement.format(i[0], i[0], i[0], i[0], i[0], \
                            i[1], i[1], i[1], i[1], i[1], \
                            i[2], i[2], i[2], i[2], i[2], \
                            i[3], i[3], i[3], i[3], i[3], \
                            i[4], i[4], i[4], i[4], i[4], response))
        outputstat = cursor.fetchall()
        for x in outputstat:
            outputstat = x[0]
        win_statement = "SELECT COUNT(`id`) FROM vctdata.vctdata WHERE (`agent 1` = '{}' OR `agent 2` = '{}' or `agent 3` = '{}' or `agent 4` = '{}' or `agent 5` = '{}') \
                        AND (`agent 1` = '{}' OR `agent 2` = '{}' or `agent 3` = '{}' or `agent 4` = '{}' or `agent 5` = '{}') \
                        AND (`agent 1` = '{}' OR `agent 2` = '{}' or `agent 3` = '{}' or `agent 4` = '{}' or `agent 5` = '{}') \
                        AND (`agent 1` = '{}' OR `agent 2` = '{}' or `agent 3` = '{}' or `agent 4` = '{}' or `agent 5` = '{}') \
                        AND (`agent 1` = '{}' OR `agent 2` = '{}' or `agent 3` = '{}' or `agent 4` = '{}' or `agent 5` = '{}') \
                        AND `map` = '{}' AND `win` is TRUE;"
        win_total = cursor.execute(win_statement.format(i[0], i[0], i[0], i[0], i[0], \
                            i[1], i[1], i[1], i[1], i[1], \
                            i[2], i[2], i[2], i[2], i[2], \
                            i[3], i[3], i[3], i[3], i[3], \
                            i[4], i[4], i[4], i[4], i[4], response))
        win_total_stat = cursor.fetchall()
        for x in win_total_stat:
            win_total_stat = x[0]
        total = cursor.execute("SELECT COUNT(`id`) FROM vctdata.vctdata WHERE `map` = '" + response + "';")
        totalstat = cursor.fetchall()
        for x in totalstat:
            totalstat = x[0]
        final_pick_rate = round(((outputstat / totalstat) * 100), 1)
        final_win_rate = round((((win_total_stat / outputstat) if outputstat != 0 else 0) * 100), 1)
        if final_pick_rate == 0:
            continue
        else:
            table.add_row([i, final_pick_rate, final_win_rate, outputstat])   
    print("Sorted by Pick Rate:")
    print(table.get_string(sortby="Pick Rate", reversesort=True, start=0, end=10))
    print("Sorted by Win Rate:")
    print(table.get_string(sortby="Win Rate", reversesort=True, start=0, end=10))

def team_comp_rankings_all_maps():
    statement = "SELECT COUNT(`id`) FROM vctdata.vctdata WHERE (`agent 1` = '{}' OR `agent 2` = '{}' or `agent 3` = '{}' or `agent 4` = '{}' or `agent 5` = '{}') \
    AND (`agent 1` = '{}' OR `agent 2` = '{}' or `agent 3` = '{}' or `agent 4` = '{}' or `agent 5` = '{}') \
    AND (`agent 1` = '{}' OR `agent 2` = '{}' or `agent 3` = '{}' or `agent 4` = '{}' or `agent 5` = '{}') \
    AND (`agent 1` = '{}' OR `agent 2` = '{}' or `agent 3` = '{}' or `agent 4` = '{}' or `agent 5` = '{}') \
    AND (`agent 1` = '{}' OR `agent 2` = '{}' or `agent 3` = '{}' or `agent 4` = '{}' or `agent 5` = '{}') \
    ;"
    table = PrettyTable()
    table.field_names = ["Top Ten Teams"] + ["Pick Rate"] + ["Win Rate"] + ["Total Picks"]
    comb = combinations(agent_list, 5)
    for i in list(comb):
        output = cursor.execute(statement.format(i[0], i[0], i[0], i[0], i[0], \
                            i[1], i[1], i[1], i[1], i[1], \
                            i[2], i[2], i[2], i[2], i[2], \
                            i[3], i[3], i[3], i[3], i[3], \
                            i[4], i[4], i[4], i[4], i[4]))
        outputstat = cursor.fetchall()
        for x in outputstat:
            outputstat = x[0]
        win_statement = "SELECT COUNT(`id`) FROM vctdata.vctdata WHERE (`agent 1` = '{}' OR `agent 2` = '{}' or `agent 3` = '{}' or `agent 4` = '{}' or `agent 5` = '{}') \
                        AND (`agent 1` = '{}' OR `agent 2` = '{}' or `agent 3` = '{}' or `agent 4` = '{}' or `agent 5` = '{}') \
                        AND (`agent 1` = '{}' OR `agent 2` = '{}' or `agent 3` = '{}' or `agent 4` = '{}' or `agent 5` = '{}') \
                        AND (`agent 1` = '{}' OR `agent 2` = '{}' or `agent 3` = '{}' or `agent 4` = '{}' or `agent 5` = '{}') \
                        AND (`agent 1` = '{}' OR `agent 2` = '{}' or `agent 3` = '{}' or `agent 4` = '{}' or `agent 5` = '{}') \
                        AND `win` is TRUE;"
        win_total = cursor.execute(win_statement.format(i[0], i[0], i[0], i[0], i[0], \
                            i[1], i[1], i[1], i[1], i[1], \
                            i[2], i[2], i[2], i[2], i[2], \
                            i[3], i[3], i[3], i[3], i[3], \
                            i[4], i[4], i[4], i[4], i[4]))
        win_total_stat = cursor.fetchall()
        for x in win_total_stat:
            win_total_stat = x[0]
        total = cursor.execute("SELECT COUNT(`id`) FROM vctdata.vctdata;")
        totalstat = cursor.fetchall()
        for x in totalstat:
            totalstat = x[0]
        final_pick_rate = round(((outputstat / totalstat) * 100), 1)
        final_win_rate = round((((win_total_stat / outputstat)) * 100), 1) if outputstat != 0 else 0
        if final_pick_rate == 0:
            continue
        else:
            table.add_row([i, final_pick_rate, final_win_rate, outputstat])    
    print("Sorted by Pick Rate:")
    print(table.get_string(sortby="Pick Rate", reversesort=True, start=0, end=10))
    print("Sorted by Win Rate:")
    print(table.get_string(sortby="Win Rate", reversesort=True, start=0, end=10))
'''
to-do list:
duplicate SQL database with only stage 3 data to get a better read on current meta
'''

main()
