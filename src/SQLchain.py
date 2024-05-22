from SQL_connection.connector import SQLConnector
from langchain_community.utilities import SQLDatabase


from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

class SQL_Chain:
    def __init__(self, config:dict) -> None:
        self.config = config
        # self.connector = SQLConnector(config=config)
        db_uri = f"mysql+mysqlconnector://{config['user']}:{config['passwd']}@{config['host']}:{config['port']}/{config['database']}"
        print(db_uri)
        self.database = SQLDatabase.from_uri(db_uri)
        self.set_template()
        # print(database.get_usable_table_names())

        self.llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
        self.sql_chain = (
            RunnablePassthrough.assign(schema=self.get_schema)
            | self.query_prompt
            | self.llm.bind(stop=["\nSQLResult:"])
            | StrOutputParser()
        )
        self.full_chain = (
            RunnablePassthrough.assign(query=self.sql_chain).assign(
                schema=self.get_schema,
                response=lambda vars: self.run_query(vars["query"]),
            )
            | self.execute_prompt
            | self.llm
            | StrOutputParser()
        )

    def upload(self, data:str):
        print(data)
        pass

    def get_schema(self, db:SQLDatabase):
        schema = self.database.get_table_info()
        return schema
    
    def run_chain(self, prompt:str):
        print(prompt)
        # prompt = 'how many students are there?'
        result = self.full_chain.invoke({"question": prompt})
        print(result)
        return result

    def run_query(self, query):
        return self.database.run(query)
    
    def set_template(self):
        self.template = """Based on the table schema below, write a SQL query that would answer the user's question:
{schema}

Question: {question}
SQL Query:"""
        self.query_prompt = ChatPromptTemplate.from_template(self.template)

        self.template = """Based on the table schema, question, sql query, and sql response below, write a natural language response:
{schema}

Question: {question}
SQL Query: {query}
SQL Response: {response}"""
        self.execute_prompt = ChatPromptTemplate.from_template(self.template)