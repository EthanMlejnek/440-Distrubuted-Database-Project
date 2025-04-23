--First two function are used for clearing misinputs into the phone_metrics and email_metrics, keeps data analytics accurate.
--Last function optimizes the table to reallocate memory Rebuilds indexes and reclaiming space allowing for faster retrieval.

DELIMITER //
CREATE PROCEDURE cleanAndOptimizePhoneEmailMetrics()
BEGIN
    DELETE FROM PHONE_METRICS
    WHERE length_of_call <= 0
    OR customer_satisfaction < 1
    OR customer_satisfaction > 5;

    DELETE FROM EMAIL_METRICS
    WHERE length_of_correspondence <= 0
    OR customer_satisfaction < 1
    OR customer_satisfaction > 10;
  OPTIMIZE TABLE PHONE_METRICS, EMAIL_METRICS, TIMECARD;
END;
//
DELIMITER ;
CALL cleanAndOptimizePhoneEmailMetrics;

-- Vince Stored Procedure. Inserting, updating, and deleting records from project-related tables like Project, Employee_Project_Task, and Project_Task tables.
DROP PROCEDURE IF EXISTS ManageProjectTasks;
CREATE PROCEDURE ManageProjectTasks(
    IN p_action VARCHAR(10),
    IN p_project_id INT,
    IN p_project_name VARCHAR(255),
    IN p_task_id INT,
    IN p_task_description VARCHAR(255),
    IN p_employee_id INT,
    IN p_task_start_date DATE,
    IN p_task_end_date DATE
)
BEGIN
    IF p_action = 'INSERT' THEN
        INSERT INTO PROJECT (project_id, project_name)
        VALUES (p_project_id, p_project_name);
        INSERT INTO PROJECT_TASK (task_id, project_id, task_description)
        VALUES (p_task_id, p_project_id, p_task_description);
        INSERT INTO EMPLOYEE_PROJECT_TASK (employee_id, task_id, task_start_date, task_end_date)
        VALUES (p_employee_id, p_task_id, p_task_start_date, p_task_end_date);
    ELSEIF p_action = 'UPDATE' THEN
        UPDATE PROJECT
        SET project_name = p_project_name
        WHERE project_id = p_project_id;
        UPDATE PROJECT_TASK
        SET task_description = p_task_description
        WHERE task_id = p_task_id AND project_id = p_project_id;
        UPDATE EMPLOYEE_PROJECT_TASK
        SET task_start_date = p_task_start_date, task_end_date = p_task_end_date
        WHERE employee_id = p_employee_id AND task_id = p_task_id;
    ELSEIF p_action = 'DELETE' THEN
        DELETE FROM EMPLOYEE_PROJECT_TASK
        WHERE employee_id = p_employee_id AND task_id = p_task_id;
        DELETE FROM PROJECT_TASK
        WHERE task_id = p_task_id AND project_id = p_project_id;
        DELETE FROM PROJECT
        WHERE project_id = p_project_id;
    END IF;
END //

CALL ManageProjectTasks('INSERT', 103, 'TestProject', 32, 'Test purposes', 29, '2025-04-20', '2025-09-20');
CALL ManageProjectTasks('Update', 103, 'TestProject', 32, 'Test purposes', 29, '2025-04-20', '2025-07-20');
CALL ManageProjectTasks('Delete', 103, 'TestProject', 32, 'Test purposes', 29, '2025-04-20', '2025-07-20');

-- Otto Stored Procedure. Insert into contract inserts into bridge tables CONTRACT_COUNTRY and LIENT_CONTRACT.
CREATE OR REPLACE PROCEDURE AddContract(
    IN C_ContractID INT(11), 
    IN C_MaxHours INT(11), 
    IN C_BillingRate DECIMAL(10,2), 
    IN C_Country INT(11),
    IN C_CleintID INT(11),
    IN C_ContractType VARCHAR(50)
    )
BEGIN
    INSERT INTO CONTRACT (contract_id, contract_max_hours, billing_rate)
    VALUES (C_ContractID, C_MaxHours, C_BillingRate);

    INSERT INTO CONTRACT_COUNTRY (contract_id, country_id)
    VALUES (C_ContractID, C_Country);

    INSERT INTO CLIENT_CONTRACT (client_id, contract_id, contract_type)
    VALUES (C_CleintID, C_ContractID, C_ContractType);
END;
/

CALL AddContract(3000, 120, 150.00, 2, 45, 'fixed');



-- Wesley stored procedure

-- Inserts
INSERT INTO CONTRACT (contract_id, contract_max_hours, billing_rate)
VALUES (9001, 0, 120.00);


INSERT INTO CONTRACT (contract_id, contract_max_hours, billing_rate)
VALUES (9002, 80, 100.00);


INSERT INTO BILLING (billing_id, billed_hours, bill_rate, billed_total)
VALUES (8001, 100, 100.00, 10000.00);


INSERT INTO BILLING_CONTRACT (billing_id, contract_id)
VALUES (8001, 9002);

INSERT INTO BILLING (billing_id, billed_hours, bill_rate, billed_total)
VALUES (8002, 30, 90.00, 2700.00);

-- Report for showing proof of stored procedure
SELECT
    (SELECT COUNT(*) 
     FROM BILLING B
     JOIN BILLING_CONTRACT BC ON B.billing_id = BC.billing_id
     JOIN CONTRACT C ON BC.contract_id = C.contract_id
     WHERE B.billed_hours > C.contract_max_hours) AS overbilled_entries,

    (SELECT COUNT(*) 
     FROM CONTRACT 
     WHERE contract_max_hours = 0 AND billing_rate != 0) AS zero_hour_contracts_with_rate,

    (SELECT COUNT(*) 
     FROM BILLING 
     WHERE billing_id NOT IN (SELECT billing_id FROM BILLING_CONTRACT)) AS orphaned_billing_entries;
DROP PROCEDURE IF EXISTS CleanAndSyncData;

DELIMITER //

CREATE PROCEDURE CleanAndSyncData()
BEGIN
    -- 1. Cap any billed_hours that exceed contract_max_hours
    UPDATE BILLING B
    JOIN BILLING_CONTRACT BC ON B.billing_id = BC.billing_id
    JOIN CONTRACT C ON BC.contract_id = C.contract_id
    SET B.billed_hours = C.contract_max_hours
    WHERE B.billed_hours > C.contract_max_hours;


    -- 2. Set billing_rate to 0 for contracts that have 0 max hours
    UPDATE CONTRACT
    SET billing_rate = 0
    WHERE contract_max_hours = 0;

    -- 3. Delete billing records that aren't linked to any contract to keep clutter out 
    DELETE FROM BILLING
    WHERE billing_id NOT IN (
        SELECT billing_id FROM BILLING_CONTRACT
    );
END //

DELIMITER ;

CALL CleanAndSyncData();


-- Ethan M Procedure #1: Generate paritioned data for Japan 
-- NOTE: Database must have db_japan created before running this procedure.

-- Run this first before: 
USE dbmain; 
DROP PROCEDURE IF EXISTS GenerateJapanPartitionedData;

DELIMITER //

CREATE PROCEDURE GenerateJapanPartitionedData()    
BEGIN
    CREATE TABLE IF NOT EXISTS db_japan.JAPAN_TIMECARD AS
    SELECT * FROM TIMECARD WHERE country_id = 2;

    CREATE TABLE IF NOT EXISTS db_japan.JAPAN_EMPLOYEE_TIMECARD AS
    SELECT * FROM EMPLOYEE_TIMECARD WHERE timecard_id IN (SELECT timecard_id FROM TIMECARD WHERE country_id = 2);

    -- For Employees working on projects in Japan. 
    CREATE TABLE IF NOT EXISTS db_japan.JAPAN_EMPLOYEE AS
    SELECT * FROM EMPLOYEE WHERE employee_id IN (SELECT employee_id FROM EMPLOYEE_TIMECARD WHERE timecard_id IN (SELECT timecard_id FROM TIMECARD WHERE country_id = 2));

    CREATE TABLE IF NOT EXISTS db_japan.JAPAN_PROJECT AS 
    SELECT * FROM PROJECT WHERE project_id IN (SELECT project_id FROM TIMECARD WHERE country_id = 2);

    CREATE TABLE IF NOT EXISTS db_japan.JAPAN_PROJECT_TASK AS
    SELECT * FROM PROJECT_TASK WHERE project_id IN (SELECT project_id FROM TIMECARD WHERE country_id = 2);

    CREATE TABLE IF NOT EXISTS db_japan.JAPAN_EMPLOYEE_PROJECT_TASK AS
    SELECT * FROM EMPLOYEE_PROJECT_TASK WHERE task_id IN (SELECT task_id FROM PROJECT_TASK WHERE project_id IN (SELECT project_id FROM TIMECARD WHERE country_id = 2));

END //

DELIMITER ;

CALL GenerateJapanPartitionedData();

-- Switch back to dbmain after creating the partitioned data.
USE dbmain; 

-- Ethan M Procedure #2: Assign an employee to a project task.  
DROP PROCEDURE IF EXISTS AssignEmployeeToTask;
DELIMITER //

CREATE PROCEDURE AssignEmployeeToTask(
    IN emp_id INT,
    IN task_id INT,
    IN start_date DATE,
    IN end_date DATE
)
BEGIN
    INSERT INTO EMPLOYEE_PROJECT_TASK (employee_id, task_id, task_start_date, task_end_date)
    VALUES (emp_id, task_id, start_date, end_date);
END //

DELIMITER ;

CALL AssignEmployeeToTask(101, 2, '2025-01-01', '2025-12-31');
CALL AssignEmployeeToTask(102, 3, '2025-01-01', '2025-12-31');

SELECT * FROM EMPLOYEE_PROJECT_TASK WHERE employee_id IN (101, 102);

-- Ethan M Stored Procedure #3: Insert a new policy for a country 
DELIMITER //

DROP PROCEDURE IF EXISTS InsertCountryPolicy;
CREATE PROCEDURE InsertCountryPolicy(
    IN country_id INT,
    IN policy_id INT,
    IN policy_type VARCHAR(255),
    IN max_weekly_hours INT
)
BEGIN 
    INSERT INTO POLICY (policy_id, policy_type)
    VALUES (policy_id, policy_type);
    
    INSERT INTO COUNTRY_POLICY (country_id, policy_id, max_weekly_hours)
    VALUES (country_id, policy_id, max_weekly_hours);
END //

DELIMITER ;

CALL InsertCountryPolicy(2, 6, 'Japan Policy', 40);

SELECT * FROM COUNTRY_POLICY WHERE country_id = 2;

SELECT * FROM POLICY; 

-- Luke R Stored Procedure

DELIMITER //
DROP PROCEDURE IF EXISTS NewCompany;
CREATE PROCEDURE NewCompany (
    IN new_company_name varchar(255),
    IN new_company_type varchar(255),
    IN new_person_fname varchar(255),
    IN new_person_lname varchar(255),
    IN new_person_dob date
)
BEGIN
    DECLARE new_company_id INT;
    DECLARE new_person_id INT;
    DECLARE new_client_id INT;
    
    SELECT IFNULL(MAX(company_id), 0) + 1 INTO new_company_id FROM COMPANY;
    SELECT IFNULL(MAX(person_id), 0) + 1 INTO new_person_id FROM PERSON;
    SELECT IFNULL(MAX(client_id), 0) + 1 INTO new_client_id FROM CLIENT;
    
    INSERT INTO COMPANY (company_id, company_name, company_type)
    VALUES (new_company_id, new_company_name, new_company_type);

    INSERT INTO PERSON (person_id, first_name, last_name, date_of_birth)
    VALUES (new_person_id, new_person_fname, new_person_lname, new_person_dob);

    INSERT INTO CLIENT (client_id, person_id, company_id)
    VALUES (new_client_id, new_person_id, new_company_id);
END;
//
DELIMITER ;

CALL NewCompany('Tech Innovations', 'Technology', 'Alice', 'Smith', '1990-05-15');
