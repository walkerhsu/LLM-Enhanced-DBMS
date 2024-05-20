# LLM-Enhanced-DBMS

## Abstract
The Database Management System Chatbot is a user-friendly interface built using Tkinter, allowing users to interact with a database using natural language commands. The chatbot provides features such as querying the database, extracting information from audio/PDF files, and generating SQL queries dynamically. It leverages language processing tools like LangChain for query generation and PyMuPDF for extracting data from PDF files.

## Features
- **Chatbot Interface**: Users can interact with the database using natural language commands.
- **Query Generation**: LangChain is used to generate SQL queries from user input.
- **Data Extraction from Files**: Users can choose audio/PDF files, and the chatbot extracts relevant information to insert into the database.
- **Natural Language Response**: Query results are returned in natural language for easy interpretation.

## How to Run the Project
1. **Clone the Repository**: 
   ```sh
   git clone https://github.com/walkerhsu/LLM-Enhanced-DBMS
   cd LLM-Enhanced-DBMS
    ```

2. **Install Dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

3. **Run the Chatbot**:
    ```sh
    cd src 
    python main.py
    ```

This will open the a window with chatbot interface, where you can interact with the database using natural language commands.