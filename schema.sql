-- Employee Management System — shared RDS schema
CREATE SCHEMA IF NOT EXISTS auth;
CREATE SCHEMA IF NOT EXISTS employee;

CREATE TABLE IF NOT EXISTS auth.users (
    id            BIGSERIAL PRIMARY KEY,
    email         VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255)        NOT NULL,
    full_name     VARCHAR(255),
    role          VARCHAR(20)         NOT NULL DEFAULT 'user',  -- 'admin' | 'user'
    created_at    TIMESTAMPTZ         NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS employee.employees (
    id          BIGSERIAL PRIMARY KEY,
    full_name   VARCHAR(255) NOT NULL,
    email       VARCHAR(255) UNIQUE NOT NULL,
    phone       VARCHAR(50),
    position    VARCHAR(100),
    department  VARCHAR(100),
    salary      NUMERIC(12,2),
    hire_date   DATE,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_emp_department ON employee.employees(department);
CREATE INDEX IF NOT EXISTS idx_emp_name       ON employee.employees(full_name);

-- Admin user is auto-seeded by auth-service on first boot
-- (admin@example.com / admin123)
