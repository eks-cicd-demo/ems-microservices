# Sprint Progress

## Sprint 1 ✅

* PostgreSQL in Docker
* pgAdmin
* Auth Service
* JWT Authentication
* Postman
* Git Repository

# Sprint 2

Objective

Develop the Employee microservice with secured CRUD operations.

Completed

* Employee Service
* Health Endpoint
* List Employees
* Search Employees
* Create Employee
* Update Employee
* Delete Employee
* JWT Authorization
* Postman Environment Variables

Result

Successfully implemented secured CRUD APIs.

Status

Completed

# Sprint 3

## Objective

Run the complete microservices application locally.

## Completed

* Auth Service
* Employee Service
* Admin Service
* Dashboard Service
* Gateway
* End-to-End Integration Testing
* Browser Testing
* Application Freeze

## Result

Successfully validated the complete application locally.

Status

Completed



**# Sprint 4 - Docker Production Hardeni**ng



\## Objective



Improve the Docker-based microservices platform by adopting production-style configuration management, health monitoring, and image versioning.



\---



\## Features Completed



\### Docker



\- Production Dockerfiles

\- Multi-stage builds (if applicable)

\- Image versioning



\### Docker Compose



\- Multi-service deployment

\- Custom bridge network

\- Persistent PostgreSQL volume



\### Health Checks



Implemented Docker health checks for:



\- Gateway

\- Auth Service

\- Employee Service

\- Admin Service

\- Dashboard Service

\- PostgreSQL



Example:



```yaml

healthcheck:

&#x20; test: \["CMD", "curl", "-f", "http://localhost:5001/health"]

```



\---



\### PostgreSQL



Added PostgreSQL health check using environment variables.



```yaml

test: \["CMD-SHELL", "pg\_isready -U $$POSTGRES\_USER -d $$POSTGRES\_DB"]

```



\---



\### Environment Variables



Introduced centralized root `.env`.



Moved common variables:



\- DATABASE\_URL

\- POSTGRES\_DB

\- POSTGRES\_USER

\- POSTGRES\_PASSWORD

\- Service URLs



Service `.env` files now contain only application-specific configuration.



\---



\### Image Versioning



Added explicit image tags.



Example:



```

ems-gateway:v1.0.0

ems-auth:v1.0.0

ems-employee:v1.0.0

ems-admin:v1.0.0

ems-dashboard:v1.0.0

```



\---



\## Validation



Successfully verified:



\- All containers start

\- Health checks report Healthy

\- PostgreSQL connectivity

\- API communication between services

\- CRUD operations

\- Docker networking

\- Root `.env` configuration



\---



\## Technologies



\- Python Flask

\- PostgreSQL

\- Docker

\- Docker Compose

\- pgAdmin



\---



\## Next Sprint



Sprint 5: GitHub Actions CI/CD

Sprint Objective

Implement a complete Continuous Integration (CI) pipeline for the EMS Microservices project by automating code quality checks, security scanning, unit testing, and database-backed integration testing using GitHub Actions.

Completed Activities
1. Code Quality Automation
Configured Black for automatic Python code formatting.
Configured isort for consistent import ordering.
Configured Flake8 for Python code style validation.
Added project-wide configuration in pyproject.toml.
Resolved all formatting and linting issues across all microservices.
2. Security Scanning
Integrated Bandit into GitHub Actions.
Created a centralized .bandit configuration file.
Configured exclusion rules for:
virtual environments
cache directories
build artifacts
Git metadata
Fixed Bandit findings:
Removed hardcoded debug=True
Configured Flask debug mode using environment variables
Uploaded Bandit reports as workflow artifacts.
3. Python Environment Standardization
Identified Bandit compatibility issues with Python 3.14.
Installed and migrated project development environment to Python 3.12.
Updated virtual environments.
Standardized local development and GitHub Actions Python versions.
4. Automated Testing Framework
Configured Pytest for automated testing.
Standardized test execution using:
python -m pytest -v
Added test execution workflow in GitHub Actions.
5. Gateway Service Tests

Implemented automated tests for:

Health endpoint
Root endpoint
Invalid endpoint (404)

Validated:

HTTP status codes
JSON responses
Service availability
6. Admin Service Tests

Implemented tests for:

Health endpoint
Protected endpoint authentication
Invalid endpoint handling

Configured:

PostgreSQL connectivity
Authentication validation
7. Employee Service Tests

Implemented tests for:

Health endpoint
Authentication-protected APIs
Invalid endpoint handling

Validated:

Authentication middleware
API response structure
8. Auth Service Tests

Implemented tests for:

Health endpoint
Invalid login scenarios
Unauthorized access handling

Configured:

Database connectivity
Admin user seeding
9. Dashboard Service Tests

Implemented tests for:

Health endpoint
Authentication-protected statistics endpoint
Invalid endpoint handling

Validated:

Service health
Authentication middleware
Dashboard API accessibility
10. GitHub Actions Matrix Strategy

Implemented matrix-based execution for:

Gateway
Auth Service
Employee Service
Admin Service
Dashboard Service

Each service executes independently, improving pipeline scalability and reducing execution time.

11. Docker Compose Integration

Integrated Docker Compose into the CI pipeline.

Automated:

PostgreSQL startup
Service initialization
Network creation
Container cleanup
12. PostgreSQL Test Environment

Configured GitHub Actions to:

Start PostgreSQL container
Wait until database becomes healthy
Initialize database schema
Support integration tests
13. Environment Configuration

Implemented dynamic .env creation during workflow execution.

Configured:

PostgreSQL credentials
Database URL
JWT Secret
Service URLs
Flask configuration

Integrated GitHub Repository Secrets for secure credential management.

14. Authentication Initialization

Automated startup of the Auth Service during CI to:

Seed default administrator account
Initialize authentication data
Support dependent service testing
15. CI Workflow Validation

Successfully validated complete CI pipeline consisting of:

Source checkout
Dependency installation
Code formatting validation
Import sorting validation
Linting
Security scanning
Database initialization
Authentication initialization
Automated testing
Resource cleanup




\- Amazon ECR

\- Automatic image versioning

\- OIDC Authentication

\- Continuous Deployment preparation


Sprint 6 Progress Notes

Sprint: Docker Image Build & Security Scanning

Sprint Objective

Implement automated Docker image build and vulnerability scanning for all EMS microservices using GitHub Actions before pushing images to Amazon ECR.

Completed Activities
1. Docker Build Pipeline
Created a dedicated GitHub Actions workflow for Docker image build.
Configured workflow to trigger on pushes to the docker-build branch.
Implemented matrix strategy to build all microservices in parallel.

Services included:

Gateway
Auth Service
Employee Service
Admin Service
Dashboard Service
2. Docker Image Build

Configured automated Docker image creation using:

docker build

Implemented GitHub SHA-based image tagging:

ems-gateway:<github-sha>

Benefits:

Immutable image versions
Easy rollback
Traceability
Production-ready tagging strategy
3. Matrix Strategy

Implemented GitHub Actions Matrix to build all services simultaneously.

Benefits:

Faster execution
Independent build jobs
Easy scalability for additional services
4. Docker Image Verification

Added verification step after image build.

Validated:

Image successfully created
Image available on GitHub runner
Docker image metadata
5. Trivy Image Scanning

Integrated Aqua Security Trivy into GitHub Actions.

Configured:

Docker image scanning
High severity detection
Critical severity detection
Ignore unfixed vulnerabilities
Report-only mode (exit-code: 0)
6. Build Validation

Successfully built Docker images for:

Gateway
Auth Service
Employee Service
Admin Service
Dashboard Service

Verified:

Docker build success
Image availability
Trivy scan execution
7. GitHub Actions Improvements

Evaluated different pipeline architectures.

Compared:

Multiple independent workflows
Quality
Security
Tests
Build
Single CI workflow using needs
Chained workflows using workflow_run

Documented advantages and limitations of each approach.

8. CI/CD Design Decision

Selected the following approach for the learning project:

Separate workflows during development
Refactor later if required
Terraform maintained as an independent project
9. Infrastructure Planning

Planned separation of repositories.

Application Repository
ems-microservices

Responsibilities:

Python
Docker
GitHub Actions
Trivy
Amazon ECR
Amazon EKS Deployment
Infrastructure Repository
ems-terraform

Responsibilities:

Terraform
AWS Infrastructure
Reusable Modules
ECR
IAM
GitHub OIDC
VPC
EKS
Sprint Deliverables
Docker
✅ Docker Build Workflow
✅ Matrix Build Strategy
✅ Docker Image Verification
Security
✅ Trivy Integration
✅ Image Vulnerability Scan
CI/CD
✅ Parallel Docker Builds
✅ SHA-based Image Tagging
Architecture
✅ CI/CD Repository Design
✅ Terraform Repository Planning
Sprint Outcome

Successfully implemented a production-style Docker image build pipeline with automated security scanning for all microservices. The pipeline now validates source code, builds immutable Docker images, scans them for vulnerabilities using Trivy, and prepares them for publication to Amazon ECR.

Next Sprint

Sprint 7

Create AWS infrastructure using Terraform (separate repository)
Provision Amazon ECR
Configure GitHub OIDC
Create IAM Role
Integrate GitHub Actions with Amazon ECR
Push Docker images automatically
