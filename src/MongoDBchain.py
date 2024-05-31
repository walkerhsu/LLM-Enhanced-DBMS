import json
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
from pymongo import MongoClient
from langchain_core.prompts import ChatPromptTemplate
import re

from utils.correct_unmatched_bracklets import correct_unmatched_brackets

QUERY_TEMPLATES = [
    """Based on the data structure below, write a MongoDB command that could answer the user's question by querying the db.{collection_name}:
{template_data}

Question: {question}
Here are some common MongoDB query commands:
- db.{collection_name}.find()
- db.{collection_name}.find().limit()
- db.{collection_name}.find().sort()
- db.{collection_name}.find_one()
- db.{collection_name}.count_documents()
- db.{collection_name}.update_one()
- db.{collection_name}.update_many()
Please put all keys and values in double quotes.
You can write multiple commands in one line by separating them with a comma if needed.
MongoDB command:""" , 
    """Based on the data structure, question, sql query, and sql response below, write a natural language response:
{template_data}

Question: {question}
MongoDB command: {query}
MongoDB Atlas Response: {response}""",
]

UPLOAD_TEMPLATES = [
    """Based on the desired JSON template below, please extract all related data from the User Data and return the output as a list of JSON object using the desired JSON template:
{desired_attr}.
User Data: {data}

Output:""" ,
]

class MongoDB_Chain:
    def __init__(self, config:dict) -> None:
        # initial login
        self.config = config
        self.db_name = config["database"]
        self.collection_name = config["collection"]
        self.client = MongoClient(config["connection_string"])
        self.set_template()
        self.llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

        # upload chain
        self.extract_chain = (
            RunnablePassthrough.assign(desired_attr=self.get_attr)
            | self.extract_prompt
            | self.llm.bind(stop=["\nOutput:"])
            | StrOutputParser()
        )

        # query chain
        self.query_forward_chain = (
            RunnablePassthrough.assign(template_data=self.get_template)
            | self.query_prompt
            | self.llm.bind(stop=["\nSQLResult:"])
            | StrOutputParser()
        )
        self.query_full_chain = (
            RunnablePassthrough.assign(query=self.query_forward_chain).assign(
                template_data=self.get_template,
                response=lambda vars: self.run_commands(vars["query"]),
            )
            | self.execute_prompt
            | self.llm
            | StrOutputParser()
        )

    def get_attr(self, e):
        desired_template = "{"
        input_attr = self.desired_attr.split(",")
        for i, sttr in enumerate(input_attr):
            desired_template += f'{sttr}: "value {i}", '
        desired_template = desired_template[:-2] + "}"
        return desired_template
    
    def get_template(self, e):
        collection = self.client[self.db_name][self.collection_name]
        template_data = collection.find_one({"special_dataType": "template_data"}, {"_id": 0, "special_dataType": 0})
        return template_data
    
    def run_commands(self, command:str):
        # db would be used in the exec function
        # db = self.client[self.db_name]
        command = self.filter_command(command)
        print(command)
        command = correct_unmatched_brackets(command)

        # This could be extremely dangerous for prompt injection attack!!!
        try:
            local_vars = {}
            command = "result = " + command
            exec(command, {"db": self.client[self.db_name]}, local_vars)
            if "find(" in command:
                result = list(local_vars["result"])
                return str(result)

            return str(local_vars["result"])
        
        except Exception as e:
            return str(e)

        
    
    def run_upload_chain(self, data:str, desired_attr:str):
        self.desired_attr = desired_attr
        extract_data = self.extract_chain.invoke({"data": data})
        # extract_data = json.loads(extract_data)

        return extract_data
    
    def run_insert(self, edited_data:str):
        collection = self.client[self.db_name][self.collection_name]
        edited_data = json.loads(edited_data)

        # if template_data doesn't exist, insert one
        if collection.count_documents({"special_dataType": "template_data"}) == 0:
            collection.insert_one({"special_dataType": "template_data"})
        
        # update template_data to keep up the full key space
        for data in edited_data:
            for key, _ in data.items():
                collection.update_one({"special_dataType": "template_data"}, {"$set": {key: f"{key}_value"}})

        collection.insert_many(edited_data)

    
    def run_query_chain(self, prompt:str):
        result = self.query_full_chain.invoke({"question": prompt, "collection_name": self.collection_name})
        print("A: " + result)
        return result
    
    def set_template(self):
        self.extract_prompt = ChatPromptTemplate.from_template(UPLOAD_TEMPLATES[0])
        self.query_prompt = ChatPromptTemplate.from_template(QUERY_TEMPLATES[0])
        self.execute_prompt = ChatPromptTemplate.from_template(QUERY_TEMPLATES[1])

    def filter_command(self, command:str):
        pattern = r'\$(\w+)'
        # Define the replacement function
        def replacer(match):
            return f'"${match.group(1)}"'
        
        # Use re.sub with the pattern and replacer function
        command = re.sub(pattern, replacer, command)
        command = command.replace('""', '"')
        command = command.replace("findOne", "find_one")
        command = command.replace("updateOne", "update_one")
        command = command.replace("updateMany", "update_many")

        return command
    
    def correct_unmatched_brackets(self, command:str):
        # brackets type: (), {}, []
        stack = []
        i = 0
        while i < len(command):
            if command[i] == "(":
                stack.append("(")
            elif command[i] == "{":
                stack.append("{")
            elif command[i] == "[":
                stack.append("[")

            if command[i] == ")" or command[i] == "}" or command[i] == "]":
                count_append = 0
                while stack[-1] != command[i]:
                    command = command[:i] + stack[-1] + command[i:]
                    count_append += 1
                    stack.pop()
                i += count_append
            
            i += 1
        

# def main():
#     with open("./MongoDB_connection/mongoDB_config.json", "r") as f:
#         config = json.load(f)
#     chain = MongoDB_Chain(config=config)
#     chain.run_upload_chain("""David is a student in the National Taiwan University. His major is EE.
#                            Walker is also a student in the National Taiwan University. He has two majors, which are EE and FL.""")
    
#     chain.run_upload_chain("""In National Young University, a diverse group of students brought unique talents and personalities to the table. 
#                            Maria, a budding artist with a flair for painting, often dazzled her classmates with her colorful and imaginative artwork. 
#                            Next to her sat Jamal, the class math whiz, whose quick thinking and problem-solving skills made him a favorite in group projects. 
#                            Emily, known for her love of reading, could always be found with her nose in a book, ready to share fascinating facts or stories with her friends. 
#                            At the back of the room, Ravi, a natural leader and soccer enthusiast, organized impromptu games during recess and encouraged teamwork among his peers. 
#                            Finally, there's Sophie, whose knack for storytelling and drama made her the star of every school play, captivating audiences with her expressive performances. Together, these five students created a vibrant and dynamic classroom environment where creativity, intellect, and camaraderie thrived.""")
    
#     print("\nQ: What is the major of David?")
#     chain.run_query_chain("What is the major of David?")

#     print("\nQ: How many students are there that study in National Taiwan University?")
#     chain.run_query_chain("How many students are there that study in National Taiwan University?")

#     print("\nQ: Choose a number from 1 ~ 5 for me, and add it as a creativity score to each student in National Young University.")
#     chain.run_query_chain("Choose a number from 1 ~ 5 for me, and add it as a creativity score to each student in National Young University.")

#     print("\nQ: Please change a student's creative score to 10.")
#     chain.run_query_chain("Please change a student's creative score to 10.")

#     print("\nQ: Who is the student in National Young University with the highest imaginative_score?")
#     chain.run_query_chain("Who is the student in National Young University with the highest imaginative_score?")

#     print("\nQ: David has a major in EE. Who else has a major in EE?")
#     chain.run_query_chain("David has a major in EE. Who else has a major in EE?")
    

# if __name__ == "__main__":
#     main()