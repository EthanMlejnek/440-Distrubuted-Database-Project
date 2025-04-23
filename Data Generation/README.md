# Data Generation 
This directory contains the scripts used to generate the data for this project. A deliverable for this project was to generate realistic data for our database. This was accomplished by writting a custom 
Python script so we could have more customization and control over how data was generated for each of the tables. 

To generate realistic data, I used the following libraries: 
* Pandas
* random
* Faker

**All scripts written by Ethan Mlejnek** 

# **table_tool.py** 
This script creates a tool that allows you to define a table, its columns, their data types, and how data should be generated for it. Once a table is defined, you can generate the create table and 
insert statements for that table and its data. If multiple tables are defined, the statements will be generated for all those tables. 

## Example Usage 
```python
import random
# Define a new instance of the tool. Optionally define an output file for the statements. 
bd = Builder("outfile.txt")

# Create a table
person_table = bd.create_table("TABLE_NAME", {
    ("column 1", "datatype"): [list of data],  # Specify any type of list containing data
    ("person_id", "INT"): [i for i in range(1, 50)],  # Example
}, "person_id")  # Define the primary key for the table.

# Call functions to generate create table, insert, or all statements for all defined tables.
# Optionally specify if the statements should be written to the outfile. 
create_statements = bd.generate_create_statement()
insert_statements = bd.generate_insert_statements()
all_statements = bd.generate_all_statements(True)

# Print statements directly or view them in the specifed output file.
print(all_statements) 
```

# data_generation.py 
This script contains the code that utilizes the created tool to generate data for this project. Below is an example, where data is generated for the "role" table. 

```python
role_name = ["Intern", "Associate", "Team Lead", "Manager", "Supervisor", "Director", "Executive"]
role_id = [i for i in range(1, len(role_name) + 1)]

role = bd.create_table("ROLE", {
    ("role_id", "INT"): role_id,
    ("role_name", "VARCHAR"): role_name
}, "role_id")
```
