from table_tool import * 
import random as rn 
from faker import Faker 

bd = Builder("newout.txt")
f = Faker() 

# Department 
department_name = ["Human Resources", "Finance", "Engineering", "Sales", "Marketing",
                   "IT", "Legal", "Food Service", "Quality Assurance", "Software Development"]
department_id = [i for i in range(1, len(department_name) + 1)]

department = bd.create_table("DEPARTMENT", {
    ("department_id", "INT"): department_id,
    ("department_name", "INT"): department_name,
}, "department_id") 

# Role 
role_name = ["Intern", "Associate", "Team Lead", "Manager", "Supervisor", "Director", "Executive"]
role_id = [i for i in range(1, len(role_name) + 1)]

role = bd.create_table("ROLE", {
    ("role_id", "INT"): role_id,
    ("role_name", "VARCHAR"): role_name
}, "role_id")

# Person
num_people = 500 

person_id = [i for i in range(1, num_people + 1)]
first_name = [f.first_name() for i in range(num_people)] 
last_name = [f.last_name() for i in range(num_people)]
date_of_birth = [str(Faker().date_of_birth(minimum_age=18, maximum_age=65)) for _ in range(num_people)]

people = bd.create_table("PERSON", {
    ("person_id", "INT"): person_id,
    ("first_name", "VARCHAR"): first_name,
    ("last_name", "VARCHAR"): last_name,
    ("date_of_birth", "DATE"): date_of_birth
}, "person_id")

# Country
country_name = ["United States", "Japan", "Argentina"]
country_id = [1, 2, 3]

bd.create_table("COUNTRY", {
    ("country_id", "INT"): country_id,
    ("country_name", "VARCHAR"): country_name
}, "country_id")

# Region Type  
region_type = ["State", "Prefecture", "Province"]
region_id = [1, 2, 3] 

bd.create_table("REGION_TYPE", {
    ("region_type_id", "INT"): region_id,
    ("region_type", "VARCHAR"): region_type
}, "region_id")

# Project 
num_projects = 100 
project_id = [_ for _ in range(1, num_projects + 1)]
project_name = [(f.word() + " " + f.word()) for _ in range(num_projects)]

bd.create_table("PROJECT", {
    ("project_id", "int"): project_id,
    ("project_name", "varchar"): project_name
}, "project_id")

# Contract
num_contracts = 150
contract_id = [_ for _ in range(1, num_contracts + 1)]
contract_max_hours = [rn.randint(100, 168) for _ in range(num_contracts)]
billing_rate = [rn.randint(50, 100) for _ in range(num_contracts)]

bd.create_table("CONTRACT", {
    ("contract_id", "int"): contract_id,
    ("contract_max_hours", "int"): contract_max_hours,
    ("billing_rate", "int"): billing_rate
}, "billing_id")

# Phone 
num_phone_numbers = num_people

phone_number_generator = lambda x: f"{rn.choice(['612', '518', '415', '202'])}-{rn.randint(100, 999)}-{rn.randint(1000, 9999)}"

phone = bd.create_table("PHONE", {
    ("phone_id", "INT"): [_ for _ in range(1, num_phone_numbers + 1)],
    ("phone_number", "varchar(15)"): [phone_number_generator(i) for i in range(num_phone_numbers)],
    ("phone_type", "varchar(50)"): [rn.choice(["Mobile", "Home", "Work"]) for _ in range(num_phone_numbers)],
}, "phone_id")

# Email 
num_emails = num_people

emails = [] 
for i in range(len(first_name)):
    emails.append(f"{first_name[i]}.{last_name[i]}@email.com")

bd.create_table("EMAIL", {
    ("email_id", "INT"): person_id,
    ("email", "varchar"): emails,
    ("email_type", "varchar"): [rn.choice(["Primary", "Secondary"]) for _ in range(num_people)]
}, "email_id")

# Invoice 
num_invoices = 100 

invoice_id = [_ for _ in range(1, num_invoices + 1)]
invoice_date = [str(f.date_between(start_date="-2y", end_date="today")) for _ in range(num_invoices)]
invoice_status = [rn.choice(["Paid", "Unpaid", "Processing"]) for _ in range(num_invoices)]

bd.create_table("INVOICE", {
    ("invoice_id", "int"): invoice_id,
    ("invoice_date", "date"): invoice_date,
    ("invoice_status", "varchar"): invoice_status
}, "invoice_id")

# Company 
num_companies = 50 

company_id = [i for i in range(1, num_companies + 1)]
company_name = [f.company() for _ in range(num_companies)]

industries = [
    "Technology", "Healthcare", "Finance", "Education", "Retail", 
    "Manufacturing", "Real Estate", "Transportation", "Energy", 
    "Entertainment", "Hospitality", "Agriculture", "Telecommunications", 
    "Automotive", "Pharmaceuticals"
]

company_type = [rn.choice(industries) for _ in range(num_companies)]

bd.create_table("COMPANY", {
    ("company_id", "int"): company_id,
    ("company_name", "varchar"): company_name,
    ("company_type", "varchar"): company_type 
}, "company_id")

# Region 
us_states = [
    "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware",
    "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky",
    "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi",
    "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico",
    "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania",
    "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont",
    "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"
]

japan_prefectures = [
    "Hokkaido", "Aomori", "Iwate", "Miyagi", "Akita", "Yamagata", "Fukushima",
    "Ibaraki", "Tochigi", "Gunma", "Saitama", "Chiba", "Tokyo", "Kanagawa",
    "Niigata", "Toyama", "Ishikawa", "Fukui", "Yamanashi", "Nagano", "Gifu", "Shizuoka", "Aichi",
    "Mie", "Shiga", "Kyoto", "Osaka", "Hyogo", "Nara", "Wakayama",
    "Tottori", "Shimane", "Okayama", "Hiroshima", "Yamaguchi",
    "Tokushima", "Kagawa", "Ehime", "Kochi",
    "Fukuoka", "Saga", "Nagasaki", "Kumamoto", "Oita", "Miyazaki", "Kagoshima", "Okinawa"
]

argentina_provinces = [
    "Buenos Aires",  # Autonomous city and name-shared province
    "Buenos Aires Province", "Catamarca", "Chaco", "Chubut", "Córdoba", "Corrientes", "Entre Ríos",
    "Formosa", "Jujuy", "La Pampa", "La Rioja", "Mendoza", "Misiones", "Neuquén", "Río Negro",
    "Salta", "San Juan", "San Luis", "Santa Cruz", "Santa Fe", "Santiago del Estero",
    "Tierra del Fuego", "Tucumán"
]

region_id = [_ for _ in range(1, 122)]
region_type_id = [1 for _ in range(50)] + [2 for _ in range(47)] + [3 for _ in range(24)]
region_name = us_states + japan_prefectures + argentina_provinces

bd.create_table("REGION", {
    ("region_id", "INT"): region_id,
    ("region_type_id", "INT"): region_type_id,
    ("region_name", "VARCHAR"): region_name
}, "region_type_id") 

# Employee
num_employees = int(num_people / 2) 
num_per_dept = int(num_employees / len(department_id)) 

emp_start_date = [str(f.date_between(start_date="-5y", end_date="today")) for _ in range(num_employees)]

emp_dept_id = [] 
for dept_num in department_id:
    for b in range(num_per_dept):
        emp_dept_id.append(dept_num) 
rn.shuffle(emp_dept_id)

p_id_thru = int(len(person_id) / 2)

emp_person_id = person_id[0:(p_id_thru)]
rn.shuffle(emp_person_id) 

bd.create_table("EMPLOYEE", {
    ("employee_id", "INT"): [_ for _ in range(1, num_employees + 1)],
    ("department_id", "int"): emp_dept_id,
    ("person_id", "int"): emp_person_id,
    ("hire_date", "date"): emp_start_date 
}, "employee_id")

# Client 
num_clients = num_employees
client_id = [i for i in range(1, num_clients + 1)]
client_p_id = person_id[p_id_thru:]
client_company_id = [rn.choice(company_id) for _ in range(num_clients)]

bd.create_table("CLIENT", {
    ("client_id", "int"): client_id, 
    ("person_id", "int"): client_p_id,
    ("company_id", "int"): client_company_id

}, "client_id")

# Timecard 
num_timecards = 100 
timecard_id = [_ for _ in range(1, num_timecards + 1)]
project_id = [rn.choice(project_id) for _ in range(num_timecards)]
country_id = [rn.choice(country_id) for _ in range(num_timecards)]
hours_worked = [rn.randint(1, 12) for _ in range(num_timecards)]

bd.create_table("TIMECARD", {
    ("timecard_id", "INT"): timecard_id,
    ("project_id", "INT"): project_id,
    ("country_id", "INT"): country_id, 
    ("hours_worked", "INT"): hours_worked
}, "timecard_Id")

# Country Policy 
policy_id = [i for i in range(1, 26)]
country_policy_id = [1] * 5 + [2] * 5 + [3] * 5 

policy_types = ["Work Hours Regulation", "Overtime Limit",
               "Standard Weekly Hours", "Holiday Work Policy",
               "Night Shift Limit"] * 3 

policy_max_hours = [40, 45, 48, 8, 10] * 3 

bd.create_table("COUNTRY_POLICY", {
    ("policy_id", "INT"): [i for i in range(1, 16)],
    ("country_id", "INT"): country_policy_id,
    ("policy_type", "VARCHAR"): policy_types,
    ("policy_max_hours", "INT"): policy_max_hours
}, "policy_id")

# Contract Policy 
# Fill in the rest with SQL 

contract_policy_id = contract_id
rn.shuffle(contract_policy_id) 

bd.create_table("CONTRACT_POLICY", {
    ("contract_id", "INT"): contract_policy_id,
    ("country_id", "INT"): [rn.randint(1, 3) for _ in range(150)] 
}, "contract_id")

city_id = [i for i in range(1, 92)]

def select_with_minimum_once(items, total_selections):
    if total_selections < len(items):
        raise ValueError("Total selections must be at least the number of unique items.")

    # Step 1: Ensure each item is selected at least once
    selections = rn.sample(items, len(items))

    # Step 2: Fill the rest randomly
    remaining = total_selections - len(items)
    selections += rn.choices(items, k=remaining)

    # Optional: Shuffle the final list so initial guaranteed picks aren't in order
    rn.shuffle(selections)
    return selections

city_id = [i for i in range(1, 92)]
print(select_with_minimum_once(city_id, 100))


bd.create_table("ADDRESS_CITY", {
    ("address_id", "INT"): [i for i in range(1, 101)],
    ("city_id", "INT"): select_with_minimum_once(city_id, 100)
}, "address_id")

# INSERT STATEMENTS 
statements = bd.generate_insert_statements("newout.txt") 
print(statements)  

