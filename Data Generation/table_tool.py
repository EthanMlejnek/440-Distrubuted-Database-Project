"""
Written by Ethan Mlejnek 

This script creates a tool used to define tables and columns and how data will be generated for them. 
"""
import pandas as pd 
import mysql.connector
from mysql.connector import Error 

class Table:
    def __init__(self, table_name, primary_keys=None, foreign_keys=None,
                 dataframe=None):
        self.table_name = table_name 
        self.primary_keys = primary_keys
        self.foreign_keys = foreign_keys

        self.columns = [] 
        self.column_data = {}  # Store column data in a dictionary
        self.df = dataframe if dataframe else pd.DataFrame({})

    class TableColumn:
        def __init__(self, col_name, col_dtype, data=None):
            self.col_name = col_name
            self.col_dtype = col_dtype
            self.data = data if data else [] 

        def view_data(self):
            return self.data 
    
        def __repr__(self): 
            return f"{self.col_name} {self.col_dtype}"
        
    def add_column(self, name, datatype, data=None):
        column = self.TableColumn(name, datatype, data) 
        self.columns.append(column) 
        self.column_data[name] = data if data else [] 
        self.df = pd.DataFrame(self.column_data)  # Reconstruct DataFrame

        return column 
    
    def fetch_column_values(self, name):
        return self.df[name].tolist() 
    
    def generate_create_table(self, include_drop=True):
        statement = "" 

        if include_drop:
            statement += f"DROP TABLE IF EXISTS {self.table_name};\n"

        statement += f"CREATE TABLE {self.table_name} (\n\t"
        for c in self.columns:
            statement += f"{c.col_name} {c.col_dtype}, \n\t"

        if self.primary_keys:
            if isinstance(self.primary_keys, (list, tuple)):
                primary_keys = ", ".join(self.primary_keys)
            else:
                primary_keys = self.primary_keys

            statement += f"PRIMARY KEY ({primary_keys})\n"
            statement += ");"

        else:
            statement = statement[:-2] + "\n);"

        return statement

    def generate_insert(self):
            # Start constructing the INSERT statement
            statement = f"INSERT INTO {self.table_name} ("
            
            # Add column names to the statement
            for c in self.columns:
                statement += f"{c.col_name}, "
            statement = statement[:-2] + ") VALUES\n"  # Remove trailing comma and add VALUES keyword
            
            # Iterate through each row in the DataFrame
            for _, row in self.df.iterrows():
                statement += "("
                for i in row:
                    # Handle NULL values
                    if i is None:
                        statement += "NULL, "
                    # Handle string values by enclosing them in single quotes
                    elif isinstance(i, str):
                        statement += f"'{i}', "
                    # Handle other data types (e.g., integers, floats)
                    else:
                        statement += f"{i}, "
                statement = statement[:-2] + "),\n"  # Remove trailing comma and close the row
            
            # Remove the trailing comma and newline, then add a semicolon to end the statement
            return statement[:-2] + ";"
    
    def generate_create_insert(self):
        create_statement = self.generate_create_table()
        insert_statement = self.generate_insert()

        return create_statement + "\n\n" + insert_statement
    
class Builder: 
    def __init__(self, outfile=None, tables=None):
        """
        Initialize the Builder class.

        Parameters:
        - outfile (str): The file path where generated SQL statements will be written. Defaults to "queryoutput.txt".
            with open(file_path, 'w', encoding='utf-8') as file:
        """
        self.tables = tables if tables else []  
        self.outfile = outfile if outfile else "queryoutput.txt" 

    def write_to_file(self, file_path, content):
        try:
            with open(file_path, 'w') as file:
                file.write(content) 
            print(f"Content written to: {file_path}")
        except Exception as e: 
            print(f"Failed to write: {e}")

    def add_table(self, table):
        if isinstance(table, Table):
            self.tables.append(table) 
        else:
            raise TypeError("Argument must be an instance of Table") 
        
    def create_table(self, table_name, columns={}, 
                     primary_keys=None, foreign_keys=None):
        table = Table(table_name, primary_keys, foreign_keys)
        self.add_table(table)  

        if len(columns) > 0: 
            for (name, dtype), data in columns.items():
                table.add_column(name, dtype, data)

        return table
    
    def generate_create_statements(self, write=False):
        statements = "" 
        for table in self.tables: 
            create_table = table.generate_create_table() 
            statements += create_table + "\n\n"

        if write: 
            self.write_to_file(self.outfile, statements)

        return statements
    
    def generate_insert_statements(self, write=False):
        statements = ""
        for table in self.tables: 
            insert_statements = table.generate_insert()
            statements += insert_statements + "\n\n" 

        if write: 
            self.write_to_file(self.outfile, statements) 

        return statements
    
    def generate_all_statements(self, write=False):
        statements = "" 
        for table in self.tables:
            create_table = table.generate_create_table()
            insert_table = table.generate_insert() 
            statements += create_table + "\n\n" + insert_table + "\n\n"

        if write:
            self.write_to_file(self.outfile, statements)

        return statements
    
    def __repr__(self):
        string = "" 
        for table in self.tables:
            string += f"{table.table_name}: {[_ for _ in table.columns]}" 

        return string 
    
