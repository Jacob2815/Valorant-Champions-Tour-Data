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

def add_where_clause(query):
    query = query[:-1] + " AND `{}` = '{}';"
	return query

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
            
def team_comp_ranks(map, region, caliber):
	count_statement = "SELECT COUNT(id) FROM vctdata.vctdata WHERE (`agent  1` = '{}' OR `agent  2` = '{}' OR `agent  3` = '{}' OR `agent  4` = '{}' OR `agent  5` = '{}') AND (`agent  1` = '{}' OR `agent  2` = '{}' OR `agent  3` = '{}' OR `agent  4` = '{}' OR `agent  5` = '{}') AND (`agent  1` = '{}' OR `agent  2` = '{}' OR `agent  3` = '{}' OR `agent  4` = '{}' OR `agent  5` = '{}') AND(`agent  1` = '{}' OR `agent  2` = '{}' OR `agent  3` = '{}' OR `agent  4` = '{}' OR `agent  5` = '{}') AND (`agent  1` = '{}' OR `agent  2` = '{}' OR `agent  3` = '{}' OR `agent  4` = '{}' OR `agent  5` = '{}');"
	results = []
	for a in range(len(agents)):
		for b in range(len(agents)):
			for c in range(len(agents)):
				for d in range(len(agents)):
	    				for e in range(len(agents)):
		    				cursor.execute(count_statement.format(agents[a], agents[a], agents[a], agents[a], agents[a], agents[b], agents[b], agents[b], agents[b], agents[b], agents[c], agents[c], agents[c], agents[c], agents[c], agents[d], agents[d], agents[d], agents[d], agents[d], agents[e], agents[e], agents[e], agents[e], agents[e]))            
                        			output = cursor.fetchall()
                        			results.append(output)
