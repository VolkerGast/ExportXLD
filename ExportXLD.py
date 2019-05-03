import sys
import pymysql
from collections import defaultdict

# connection variables; please specify
host = 'localhost'
user = 'user'
passwd = 'password'
database = 'database'

# further variables
domain = 'impersonals'

connection = pymysql.connect(host = host,
                             user = user,
                             passwd = passwd,
                             database = database)
cur = connection.cursor()

# get answerset columns
cur.execute("SHOW COLUMNS FROM answerset")
answerset_columns = [c[0] for c in cur.fetchall()]

# get answersets
cur.execute("SELECT * from answerset")
answerset = defaultdict()
for row in cur.fetchall():
    answerset[row[0]] = {'name': row[1],
                         'description': row[2]}
    answerset[row[0]][domain] = {}

# get answerset data
cur.execute("SHOW COLUMNS FROM answerset_data")
answerset_data_columns = [c[0] for c in cur.fetchall()]

cur.execute("SELECT * from answerset_data")
for row in cur.fetchall():
    for val in row[2:7]:
        if val is not None:
            answerset[row[7]][row[1]] = val

# get strategy columns
cur.execute("SHOW COLUMNS FROM strategy")
strategy_columns = [c[0] for c in cur.fetchall()]

# get strategies
cur.execute("SELECT * from strategy")
strategy = defaultdict()
for row in cur.fetchall():
    strategy[row[0]] = {'name': row[1],
                        'description': row[2],
                        'answerset': row[3]}

# get strategy data
cur.execute("SHOW COLUMNS FROM strategy_data")
strategy_data_columns = [c[0] for c in cur.fetchall()]

cur.execute("SELECT * from strategy_data")
for row in cur.fetchall():
    for val in row[2:7]:
        if val is not None:
            strategy[row[7]][row[1]] = val

connection.close()

# create dictionary answerset containing all the information
for strat_id, strat_data in strategy.items():
    answerset[strat_data['answerset']][domain][strat_id] = strat_data
    del answerset[strat_data['answerset']][domain][strat_id]['answerset']
    

