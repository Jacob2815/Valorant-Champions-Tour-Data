import requests
import pandas as pd
import pyodbc
import MySQLdb

db = MySQLdb.connect(
    host="localhost",
    user="scraping_user",
    passwd="scrapyboi",
    db="vctdata"
            )
print(db)

cursor = db.cursor()

agents = ['astra', 'breach', 'brimstone', 'cypher', 'jett', 'kayo', 'killjoy', 'omen', 'phoenix', 'raze', 'reyna', 'sage', 'skye', 'sova', 'viper', 'yoru']

maps = ['ascent', 'bind', 'breeze', 'haven', 'icebox', 'split']

round_types = ["attack wins", "attack losses", "defense wins", "defense losses"]

calibers = []

regions = []


def agent_picks_per_map():
    statement = "SELECT * FROM vctdata.vctdata WHERE (`agent 1` = '{}' OR `agent 2` = '{}' or `agent 3` = '{}' or `agent 4` = '{}' or `agent 5` = '{}') AND `map` LIKE '{}%';"
    for x in range(len(agents)):
        print('-------------------------------------------')
        print(agents[x])
        for i in range(len(maps)):
                print()
                print(maps[i])
                print(cursor.execute(statement.format(agents[x], agents[x], agents[x], agents[x], agents[x], maps[i])))

def map_win_rates(agent):
    statement = "SELECT map, SUM(`{}`) FROM vctdata.vctdata WHERE (`agent 1` = '{}' OR `agent 2` = '{}' or `agent 3` = '{}' or `agent 4` = '{}' or `agent 5` = '{}') GROUP BY `map` ORDER BY `map`  ;"
    print(agent)
    for i in range(len(round_types)):
        print('-------------------------------------------')
        print(round_types[i])
        print()
        cursor.execute(statement.format(round_types[i], agent, agent, agent, agent, agent))
        output = cursor.fetchall()
        for x in output:
            print(x[0])
            print(x[1])
            print()

map_win_rates(agent_list[0])
