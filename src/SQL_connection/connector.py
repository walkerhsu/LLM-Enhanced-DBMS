import csv
import json
import mysql.connector

class SQLConnector:
    def __init__(self, config:dict) -> None:
        self.config = config
        self.get_sql_config()
        self.create_database()

    def get_sql_config(self):
        self.host = self.config['host']
        self.user = self.config['user']
        self.passwd = self.config['passwd']
        self.database = self.config['database']
        self.port = self.config['port']

    def create_database(self):
        mydb = mysql.connector.connect(user=self.user, password=self.passwd, port=self.port, host=self.host)
        cursor = mydb.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")
        # cursor.execute(f"SHOW DATABASES")
        # databases = cursor.fetchall()
        # print(databases)
        cursor.close()
        mydb.close()

    def run_query(self, query:str):
        mydb = mysql.connector.connect(user=self.user, password=self.passwd, port=self.port, host=self.host, database=self.database)
        cursor = mydb.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        mydb.close()
        return result
    
    def run_modify(self, modify:str):
        mydb = mysql.connector.connect(user=self.user, password=self.passwd, port=self.port, host=self.host, database=self.database)
        cursor = mydb.cursor()
        cursor.execute(modify)
        mydb.commit()
        cursor.close()
        mydb.close()



def main():
    with open("./sql_config.json", "r") as f:
        config = json.load(f)
    connector = SQLConnector(config=config)

if __name__ == "__main__":
    main()