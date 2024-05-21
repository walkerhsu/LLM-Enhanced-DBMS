import csv
import json
import mysql.connector

class SQLConnector:
    def __init__(self, config) -> None:
        self.config = config
        self.get_sql_config()
        self.create_database()

    def get_sql_config(self):
        self.host = self.config['host']
        self.user = self.config['user']
        self.passwd = self.config['passwd']
        self.database = self.config['database']

    def create_database(self):
        mydb = mysql.connector.connect(user=self.user, password=self.passwd, host=self.host)
        cursor = mydb.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")
        # cursor.execute(f"SHOW DATABASES")
        # databases = cursor.fetchall()
        # print(databases)
        cursor.close()
        mydb.close()


def main():
    with open("./sql_config.json", "r") as f:
        config = json.load(f)
    connector = SQLConnector(config=config)

if __name__ == "__main__":
    main()