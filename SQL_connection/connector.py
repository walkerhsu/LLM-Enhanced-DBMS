import csv
import json
import mysql.connector

# make sure that you have your own config file named "sql_config.json" in the same directory
# the template of sql_config.json can be found in the same directory named "sql_config_template.json"

def get_sql_config():
    with open('sql_config.json') as f:
        config = json.load(f)

    host = config['host']
    user = config['user']
    passwd = config['passwd']
    database = config['database']

    return host, user, passwd, database

def main():
    host, user, passwd, database = get_sql_config()
    mydb = mysql.connector.connect(user=user, password=passwd, host=host)
    cursor = mydb.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database}")
    cursor.execute(f"SHOW DATABASES")
    databases = cursor.fetchall()
    print(databases)
    cursor.close()
    mydb.close()

if __name__ == "__main__":
    main()