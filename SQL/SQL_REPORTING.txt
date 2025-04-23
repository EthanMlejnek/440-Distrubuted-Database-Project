-- !! report 1 Dakota!! 
-- Department Staffing Summary Report
--This query joins the DEPARTMENT table with the EMPLOYEE table  
--(and joins further to PERSON for employee names) to show how many employees belong to each department.
-- ..reporting that assists the company’s managers..

-- HOW IT MAY BE USED: Managers can see staffing levels across departments
--  uses: A project manager planning a digital campaign in Tokyo might use this 
-- to see how many marketing employees are available and how experienced they are (via hire dates).


SELECT d.department_name, COUNT(e.employee_id) AS num_employees, MIN(e.hire_date) AS first_hire, MAX(e.hire_date) AS most_recent_hire,
GROUP_CONCAT(CONCAT(p.first_name, ' ', p.last_name) ORDER BY e.hire_date ASC SEPARATOR ', ') AS employee_list
FROM DEPARTMENT d
JOIN EMPLOYEE e ON d.department_id = e.department_id
JOIN PERSON p ON e.person_id = p.person_id
GROUP BY d.department_name;


-- !! report 2 Dakota!! 
-- Project Timecard Summary Report
-- this query summarizes project performance by reporting the average
-- and total hours worked as recorded in the TIMECARD table. 
-- this query is designed to help assess workload distribution and project efficiency. 
-- ...track the effectiveness of varying types of digital marketing campaigns...

SELECT p.project_name, AVG(t.hours_worked) AS avg_hours, SUM(t.hours_worked) AS total_hours, COUNT(t.timecard_id) AS num_entries
FROM PROJECT p
JOIN TIMECARD t ON p.project_id = t.project_id
GROUP BY p.project_name;


-- !! report 3 Dakota!! 
-- Monitor of Contract Limits
--This reports helps managers see contracts limits and avoid going over for legal issues. 

SELECT con.contract_id, coun.country_name, con.contract_max_hours AS TOTAL_HOURS_LIMIT, 
SUM(tc.hours_worked) AS CURENT_TOTAL_HOURS, ((SUM(tc.hours_worked)/con.contract_max_hours) * 100) AS PERCENT_USED
FROM CONTRACT con
JOIN PROJECT_CONTRACT pc ON con.contract_id = pc.contract_id
JOIN PROJECT pro ON pc.project_id = pro.project_id
JOIN TIMECARD tc ON pro.project_id = tc.project_id
JOIN COUNTRY coun ON tc.country_id = coun.country_id
GROUP BY con.contract_id, coun.country_name, con.contract_max_hours
ORDER BY PERCENT_USED DESC;


----------------------------------------------------------------------------------------------------------------------------------------------------------


-- Vince Report 1, selects the employees, project name and shows how many hours of work they have put in to the project.
SELECT e.employee_id, CONCAT(p.first_name, ' ', p.last_name) AS employee_name, pr.project_name AS campaign_name, SUM(t.hours_worked) AS total_hours_worked
FROM EMPLOYEE_TIMECARD et
JOIN TIMECARD t ON et.timecard_id = t.timecard_id
JOIN EMPLOYEE e ON et.employee_id = e.employee_id
JOIN PERSON p ON e.person_id = p.person_id
JOIN PROJECT pr ON t.project_id = pr.project_id
GROUP BY e.employee_id, pr.project_name;

-- Optimized Report 1
CREATE INDEX idx_employee_timcard ON EMPLOYEE_TIMECARD(employee_id, timecard_id);
CREATE INDEX idx_timecard ON TIMECARD(timecard_id, project_id);
CREATE INDEX idx_employee ON EMPLOYEE(employee_id, person_id);
CREATE INDEX idx_person ON PERSON(person_id);
CREATE INDEX idx_project ON PROJECT(project_id);

EXPLAIN SELECT e.employee_id, CONCAT(p.first_name, ' ', p.last_name) AS employee_name, pr.project_name AS campaign_name, SUM(t.hours_worked) AS total_hours_worked
FROM EMPLOYEE_TIMECARD et
JOIN TIMECARD t ON et.timecard_id = t.timecard_id
JOIN EMPLOYEE e ON et.employee_id = e.employee_id
JOIN PERSON p ON e.person_id = p.person_id
JOIN PROJECT pr ON t.project_id = pr.project_id
GROUP BY e.employee_id, pr.project_name;

-- Vince Report 2, looks into the project, gathers the phone metrics, and summarizes it.
SELECT pr.project_name AS campaign_name, SUM(pm.length_of_call) AS total_call_length, COUNT(pm.phone_metrics_id) AS num_calls, AVG(pm.customer_satisfaction) AS avg_customer_satisfaction, SUM(pm.length_of_call) / COUNT(pm.phone_metrics_id) AS avg_length_per_call
FROM PROJECT pr
JOIN TIMECARD t ON pr.project_id = t.project_id
JOIN EMPLOYEE_TIMECARD et ON t.timecard_id = et.timecard_id
JOIN PERSON_PHONE pp ON et.employee_id = pp.person_id
JOIN PHONE_METRICS pm ON pp.phone_id = pm.phone_id
GROUP BY pr.project_name;

-- Optimized Report 2
EXPLAIN SELECT pr.project_name AS campaign_name, SUM(pm_metrics.length_of_call) AS total_call_length, COUNT(pm_metrics.phone_metrics_id) AS num_calls, AVG(pm_metrics.customer_satisfaction) AS avg_customer_satisfaction, SUM(pm_metrics.length_of_call) / COUNT(pm_metrics.phone_metrics_id) AS avg_length_per_call
FROM PROJECT pr
JOIN TIMECARD t ON pr.project_id = t.project_id
JOIN EMPLOYEE_TIMECARD et ON t.timecard_id = et.timecard_id
JOIN (SELECT 
        pp.phone_id, 
        pm.length_of_call, 
        pm.phone_metrics_id, 
        pm.customer_satisfaction
     FROM PERSON_PHONE pp
     JOIN PHONE_METRICS pm ON pp.phone_id = pm.phone_id) AS pm_metrics
ON et.employee_id = pm_metrics.phone_id
GROUP BY pr.project_name;

-- Vince Report 3 Looks for all the employees that did overtime for the last week.
EXPLAIN SELECT * 
FROM EMPLOYEE_TIMECARD et
JOIN TIMECARD t ON et.timecard_id = t.timecard_id
JOIN EMPLOYEE e ON et.employee_id = e.employee_id
JOIN PERSON p ON e.person_id = p.person_id
JOIN COUNTRY_POLICY cp ON t.country_id = cp.country_id
WHERE et.timecard_date BETWEEN DATE_SUB(CURDATE(), INTERVAL 7 DAY) AND CURDATE()
GROUP BY e.employee_id, cp.max_weekly_hours
HAVING SUM(t.hours_worked) > cp.max_weekly_hours;

-- Optimized Report 3
SELECT e.employee_id, CONCAT(p.first_name, ' ', p.last_name) AS employee_name, SUM(t.hours_worked) AS total_hours_worked, cp.max_weekly_hours
FROM EMPLOYEE_TIMECARD et
JOIN TIMECARD t ON et.timecard_id = t.timecard_id
JOIN EMPLOYEE e ON et.employee_id = e.employee_id
JOIN PERSON p ON e.person_id = p.person_id
JOIN COUNTRY_POLICY cp ON t.country_id = cp.country_id
WHERE et.timecard_date BETWEEN DATE_SUB(CURDATE(), INTERVAL 7 DAY) AND CURDATE()
GROUP BY e.employee_id, cp.max_weekly_hours
HAVING total_hours_worked > cp.max_weekly_hours;


----------------------------------------------------------------------------------------------------------------------------------------------------------


-- Otto's Report 1: Employees with an average customer satisfaction rating under 5
SELECT e.employee_id, p.first_name, p.last_name, AVG(pm.customer_satisfaction) AS avg_customer_satisfaction
FROM EMPLOYEE e
JOIN PERSON p ON p.person_id = e.person_id
JOIN PERSON_PHONE pp ON pp.person_id = e.person_id
JOIN PHONE_METRICS pm ON pp.phone_id = pm.phone_id
GROUP BY e.employee_id, p.first_name, p.last_name
HAVING avg_customer_satisfaction < 5
ORDER BY avg_customer_satisfaction;

-- Otto's Report 2: Project data based on email metrics.
SELECT pr.project_name, em.length_of_correspondence, AVG(em.customer_satisfaction) AS Avg_Cust_Sat, em.length_of_correspondence / AVG(em.customer_satisfaction) AS Email2Sat_Ratio
FROM PROJECT pr
JOIN TIMECARD t ON t.project_id = pr.project_id
JOIN EMPLOYEE_TIMECARD et ON et.timecard_id = t.timecard_id
JOIN EMPLOYEE e ON e.employee_id = et.employee_id
JOIN PERSON_EMAIL pe ON pe.person_id = e.person_id
JOIN EMAIL_METRICS em ON em.email_id = pe.email_id
GROUP BY pr.project_name
ORDER BY em.customer_satisfaction DESC;

-- Otto's Report 3: Employees average customer satisfaction rating by email and phone
SELECT e.employee_id, p.first_name, p.last_name, AVG(pm.customer_satisfaction) AS avg_phone_satisfaction, 
    AVG(em.customer_satisfaction) AS avg_email_satisfaction
FROM EMPLOYEE e
JOIN PERSON p ON p.person_id = e.person_id
JOIN PERSON_PHONE pp ON pp.person_id = e.person_id
JOIN PHONE_METRICS pm ON pp.phone_id = pm.phone_id
JOIN PERSON_EMAIL pe ON pe.person_id = e.person_id
JOIN EMAIL_METRICS em ON em.email_id = pe.email_id
GROUP BY e.employee_id, p.first_name, p.last_name
ORDER BY avg_phone_satisfaction, avg_email_satisfaction;


----------------------------------------------------------------------------------------------------------------------------------------------------------

-- Ethan's Report 1: Find how much work has been billed for each client, what contract they have, and whether they are nearing their hourly limits.
EXPLAIN
SELECT 
    c.company_name, 
    CONCAT(p.first_name, ' ', p.last_name) AS client_name,
    co.CONTRACT_TYPE AS contract_type,
    ct.contract_max_hours AS contract_max_hours,
    b.billed_hours AS billed_hours, 
    b.bill_rate AS billed_rate,
    b.billed_total AS total_billed
FROM COMPANY c JOIN CLIENT ON c.company_id = CLIENT.company_id
JOIN PERSON p ON CLIENT.person_id = p.person_id
JOIN CLIENT_CONTRACT co ON CLIENT.client_id = co.client_id
JOIN CONTRACT ct ON co.contract_id = ct.contract_id
JOIN BILLING_CONTRACT bc ON bc.contract_id = ct.contract_id
JOIN BILLING b ON b.billing_id = bc.billing_id; 

-- Ethan Report 2: Generate a policy compliance report for each country and policy type.
EXPLAIN
SELECT 
    cp.country_id,
    co.country_name,
    po.policy_type,
    cp.max_weekly_hours
FROM COUNTRY_POLICY cp
JOIN COUNTRY co ON cp.country_id = co.country_id
JOIN POLICY po ON cp.policy_id = po.policy_id;

-- Ethan Report 3: Generate a report of all company locations with their addresses.
EXPLAIN
SELECT 
    cl.company_id,
    co.company_name,
    cl.location_name,
    a.street_address,
    a.postal_code
FROM COMPANY_LOCATION cl
JOIN COMPANY co ON cl.company_id = co.company_id
JOIN ADDRESS a ON cl.address_id = a.address_id;

----------------------------------------------------------------------------------------------------------------------------------------------------------
-- Wesley's Report 1: Revenue by Client Type
CREATE INDEX idx_company_type_id ON COMPANY(company_type, company_id);

SELECT 
    COM.company_type AS marketing_channel,
    SUM(B.billed_total) AS total_revenue
FROM CLIENT CL
JOIN COMPANY COM ON CL.company_id = COM.company_id
JOIN CLIENT_CONTRACT CC ON CL.client_id = CC.client_id
JOIN CONTRACT CT ON CC.contract_id = CT.contract_id
JOIN BILLING_CONTRACT BC ON CT.contract_id = BC.contract_id
JOIN BILLING B ON BC.billing_id = B.billing_id
GROUP BY COM.company_type
ORDER BY total_revenue DESC;

-- Wesley's Report 2: Unpaid Invoices by Campaign Type, uses same index as Report 1
SELECT 
    COM.company_type AS campaign_type,
    COUNT(I.invoice_id) AS unpaid_invoices
FROM INVOICE I
JOIN CLIENT_INVOICE CI ON I.invoice_id = CI.invoice_id
JOIN CLIENT CL ON CI.client_id = CL.client_id
JOIN COMPANY COM ON CL.company_id = COM.company_id
WHERE I.invoice_status = 'Unpaid'
GROUP BY COM.company_type
ORDER BY unpaid_invoices DESC;

-- Wesley's Report 3: Total Billed Hours by Client Company
CREATE INDEX idx_client_company_id ON CLIENT(company_id);

SELECT 
    COM.company_name,
    SUM(B.billed_hours) AS total_hours_billed
FROM CLIENT CL
JOIN COMPANY COM ON CL.company_id = COM.company_id
JOIN CLIENT_CONTRACT CC ON CL.client_id = CC.client_id
JOIN CONTRACT CT ON CC.contract_id = CT.contract_id
JOIN BILLING_CONTRACT BC ON CT.contract_id = BC.contract_id
JOIN BILLING B ON BC.billing_id = B.billing_id
GROUP BY COM.company_name
ORDER BY total_hours_billed DESC;

----------------------------------------------------------------------------------------------------------------------------------------------------------

 -- Luke Report 1: Number of contracts and total billed amount for each region

select region_name, count(CONTRACT.contract_id) as num_contracts, sum(billed_total) as total_billed
from REGION join CONTRACT_COUNTRY on REGION.region_id = CONTRACT_COUNTRY.country_id
    join CONTRACT on CONTRACT_COUNTRY.contract_id = CONTRACT.contract_id
    join BILLING_CONTRACT on CONTRACT.contract_id = BILLING_CONTRACT.contract_id
    join BILLING on BILLING_CONTRACT.billing_id = BILLING.billing_id
group by region_name;

 -- Luke Report 2: Show each policy for each country, the maximum weekly hours

select country_name, max_weekly_hours, policy_type
from COUNTRY join COUNTRY_POLICY on COUNTRY.country_id = COUNTRY_POLICY.country_id
    join POLICY on COUNTRY_POLICY.policy_id = POLICY.policy_id
group by country_name, policy_type;

 -- Luke Report 3: Show the length of time each employee has been on calls and the total number of calls for each employee

select EMPLOYEE.employee_id, count(PHONE_METRICS.phone_metrics_id) as number_of_calls, sum(PHONE_METRICS.length_of_call) as total_call_duration
from EMPLOYEE join PERSON on EMPLOYEE.person_id = PERSON.person_id
    join PERSON_PHONE on PERSON.person_id = PERSON_PHONE.person_id
    join PHONE on PERSON_PHONE.phone_id = PHONE.phone_id
    join PHONE_METRICS on PHONE.phone_id = PHONE_METRICS.phone_id
group by EMPLOYEE.employee_id;
