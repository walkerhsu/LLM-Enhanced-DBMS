# LLM-Enhanced-DBMS-Importer

## Overview

**LLM-Enhanced-DBMS-Importer** is a project that integrates a Large Language Model (LLM) into a Database Management System (DBMS) to facilitate the extraction of important data from documents and automate the insertion of this data into the database. This is achieved by introducing a new SQL statement that simplifies the process.

## Features

- **Automated Data Extraction**: Utilize an LLM to extract key data from documents.
- **SQL Integration**: Introduce a new SQL statement to create tables and insert extracted data seamlessly.
- **Ease of Use**: Simplify data import processes with minimal user intervention.
- **Customizable**: Adapt the LLM for various document types and data formats.

## Getting Started

### Prerequisites

- Python 3.8+
- [OpenAI API Key](https://beta.openai.com/signup/)
- A supported DBMS (e.g., MySQL, PostgreSQL, SQLite)

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/LLM-Enhanced-DBMS-Importer.git
    cd LLM-Enhanced-DBMS-Importer
    ```

2. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### Configuration

1. Set up your OpenAI API key:
    ```bash
    export OPENAI_API_KEY='your-api-key'
    ```

2. Configure your database connection settings in `config.py`.

### Usage

To use the new SQL statement for creating a table and inserting data:

1. Prepare your document for data extraction.
2. Use the provided script to run the process:
    ```bash
    python main.py --document your_document.txt --table-name your_table_name
    ```

This will extract the relevant data from `your_document.txt` and insert it into `your_table_name` in the database.

## Examples

Here's an example of the new SQL statement:

```sql
CREATE TABLE your_table_name FROM DOCUMENT 'your_document.txt' USING LLM;
