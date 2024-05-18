import csv
import json
import mysql.connector

# make sure that you have your own config file named "sql_config.json" in the same directory
# the template of sql_config.json can be found in the same directory named "sql_config_template.json"


class SQLConnector:
    def __init__(self) -> None:
        self.get_sql_config()
        self.create_database()

    def get_sql_config(self):
        with open('sql_config.json') as f:
            config = json.load(f)

        self.host = config['host']
        self.user = config['user']
        self.passwd = config['passwd']
        self.database = config['database']

    def create_database(self):
        mydb = mysql.connector.connect(user=self.user, password=self.passwd, host=self.host)
        cursor = mydb.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")
        cursor.execute(f"SHOW DATABASES")
        databases = cursor.fetchall()
        print(databases)
        cursor.close()
        mydb.close()

def main():
    connector = SQLConnector()
    

if __name__ == "__main__":
    main()