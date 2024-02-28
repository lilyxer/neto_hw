CREATE DATABASE Employee;

CREATE TABLE IF NOT EXISTS Employee(
    id SERIAL PRIMARY KEY,
    employee_name VARCHAR(120) NOT NULL
);

CREATE TABLE IF NOT EXISTS Department(
    id SERIAL PRIMARY KEY,
    department_name VARCHAR(60) NOT NULL
);

CREATE TABLE IF NOT EXISTS EmployeeList(
    id SERIAL PRIMARY KEY,
    employee_id INTEGER,
    department_id INTEGER,
    chief_id INTEGER NULL,
    FOREIGN KEY(employee_id)REFERENCES Employee(id) ON DELETE CASCADE,
    FOREIGN KEY(department_id)REFERENCES Department(id) ON DELETE CASCADE,
    FOREIGN KEY(chief_id)REFERENCES Employee(id) ON DELETE CASCADE
);