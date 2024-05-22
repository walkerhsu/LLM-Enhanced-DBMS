import json
from SQL_connection.connector import SQLConnector
from langchain_community.utilities import SQLDatabase


from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

QUERY_TEMPLATES = [
    """Based on the table schema below, write a SQL query that would answer the user's question:
{schema}

Question: {question}
SQL Query:""" , 
    """Based on the table schema, question, sql query, and sql response below, write a natural language response:
{schema}

Question: {question}
SQL Query: {query}
SQL Response: {response}""",
]

UPLOAD_TEMPLATES = [
    """Based on the table schema below, please extract related data from the User Data and return the output as a JSON object with the table name as the key and the extracted JSON data as the value:
{schema}

User Data: {data}

Output:""" , 
    """Based on the table schema below, upload JSON data, write a SQL query that start with 'Insert IGNORE Into' and would upload the user's JSON data to the database:
{schema}

Upload JSON data: {data}

SQL Query:""" , 
]

class SQL_Chain:
    def __init__(self, config:dict) -> None:
        self.config = config
        self.connector = SQLConnector(config=config)
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

        self.extract_chain = (
            RunnablePassthrough.assign(schema=self.get_schema)
            | self.extract_prompt
            | self.llm.bind(stop=["\nOutput:"])
            | StrOutputParser()
        )

        self.upload_chain = (
            RunnablePassthrough.assign(schema=self.get_schema)
            | self.insert_prompt
            | self.llm.bind(stop=["\nSQL Query:"])
            | StrOutputParser()
        )

    def get_schema(self, db:SQLDatabase):
        self.database._sample_rows_in_table_info = 0
        schema = self.database.get_table_info()
        return schema
    
    def run_query_chain(self, prompt:str):
        result = self.full_chain.invoke({"question": prompt})
        return result
    
    def run_upload_chain(self, data:str):
        def organize_data(data:str):
            data_json = json.loads(data)
            for key in data_json:
                data_table = data_json[key]
                for data_row in data_table:
                    if (data_row == "department" or data_row == "school") and len(data_table[data_row].split()) > 1:
                        data_department = data_table[data_row].split()
                        # abbreviate department names
                        data_department = [word[0].upper() for word in data_department]
                        data_table[data_row] = "".join(data_department)
                    elif (data_row == "student_ID") and len(data_table[data_row]) >= 1:
                        data_table[data_row] = data_table[data_row][0].lower() + data_table[data_row][1:]
                        
            return json.dumps(data_json)
        
        extract_data = self.extract_chain.invoke({"data": data})
        extract_data = organize_data(extract_data)
        print(extract_data)
        self.SQL_insertion = self.upload_chain.invoke({"data": extract_data}).split(";")
        # add ; to the end of the query
        self.SQL_insertion = [insertion.strip('').strip('\n') + ";" for insertion in self.SQL_insertion if (insertion != "" and insertion != "\n")]
        print(self.SQL_insertion)
        return extract_data

    def run_query(self, query):
        try:
            response = self.database.run(query)
            print(response)
            return response
        except Exception as e:
            return e
    
    def run_insert(self):
        if(len(self.SQL_insertion) == 0):
            return
        for i in range(len(self.SQL_insertion)):
            self.database.run(self.SQL_insertion[i])
    
    def set_template(self):
        self.query_prompt = ChatPromptTemplate.from_template(QUERY_TEMPLATES[0])
        self.execute_prompt = ChatPromptTemplate.from_template(QUERY_TEMPLATES[1])
        self.extract_prompt = ChatPromptTemplate.from_template(UPLOAD_TEMPLATES[0])
        self.insert_prompt = ChatPromptTemplate.from_template(UPLOAD_TEMPLATES[1])

