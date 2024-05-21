from SQL_connection.connector import SQLConnector

class LLM_Agent:
    def __init__(self, config:dict) -> None:
        self.config = config
        self.connector = SQLConnector(config=config)

    def query(self, prompt:str):
        print(prompt)
        pass

    def upload(self, data:str):
        print(data)
        pass