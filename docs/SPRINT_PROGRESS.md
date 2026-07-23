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



Sprint 5



\- GitHub Actions CI/CD

\- Amazon ECR

\- Automatic image versioning

\- OIDC Authentication

\- Continuous Deployment preparation

