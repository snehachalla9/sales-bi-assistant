# System Architecture – AI Business Intelligence Assistant

## 1. Project Overview

The AI Business Intelligence Assistant is a natural-language-based analytics application that allows users to ask questions about sales data and receive answers supported by actual database queries.

The application follows a layered architecture using Streamlit, FastAPI, Python, Groq LLM integration, SQLAlchemy, and SQLite.

The main objective is to convert business questions into predefined analytics operations and return accurate, structured results.

## 2. Technology Stack

| Component | Technology | Responsibility |
|---|---|---|
| Frontend | Streamlit | User interface and data visualization |
| Backend | FastAPI | REST API and request handling |
| Programming Language | Python | Application logic |
| Data Processing | Pandas | CSV loading and data cleaning |
| Database | SQLite | Sales transaction storage |
| ORM / Connectivity | SQLAlchemy | Database connection and query execution |
| LLM Integration | Groq API | Natural-language question interpretation |
| Testing | Pytest | Automated testing |

## 3. High-Level Architecture

```text
                    USER
                      |
                      v
             STREAMLIT FRONTEND
                      |
                      | HTTP POST Request
                      v
              FASTAPI BACKEND
                      |
                      v
           BUSINESS QUERY SERVICE
                      |
                      v
             QUESTION INTERPRETER
                  (Groq LLM)
                      |
                      v
              INTENT VALIDATION
                      |
                      v
              INTENT-BASED ROUTING
                      |
                      v
               ANALYTICS SERVICE
                      |
                      | SQL Queries
                      v
                SQLITE DATABASE
                      |
                      v
              STRUCTURED RESULTS
                      |
                      v
              FASTAPI RESPONSE
                      |
                      v
              STREAMLIT DASHBOARD
                      |
                      v
                  USER
```

## 4. Architecture Components

### 4.1 Data Ingestion Layer

**File:** `app/services/data_loader.py`

Responsibilities:

- Read the supplied sales CSV using Pandas.
- Validate required columns.
- Handle missing and invalid values.
- Convert dates and numerical columns into appropriate formats.
- Exclude invalid transaction records.
- Calculate transaction revenue.
- Load cleaned records into the SQLite database.

Revenue calculation:

```text
Revenue = Quantity × Unit Price − Discount Amount
```

Returned transactions are retained for traceability but excluded from completed-sales revenue calculations.

**Database initialization:**

`app/database/init_db.py`

This module initializes the database and loads the cleaned sales data.

### 4.2 Database Layer

**File:** `app/database/connection.py`

SQLite is used to store sales transaction records.

SQLAlchemy provides database connectivity and manages database interactions.

The sales table contains transaction details such as:

- Transaction ID
- Order date
- Product
- Category
- Region
- Sales channel
- Quantity
- Unit price
- Discount amount
- Status
- Revenue

Indexes are created on frequently queried columns to improve query performance.

### 4.3 Question Interpretation Layer

**File:** `app/services/question_interpreter.py`

This layer interprets natural-language questions using the configured Groq LLM.

It maps questions into predefined business intents.

Supported intents:

1. `total_revenue`
2. `top_product`
3. `monthly_revenue`
4. `top_region`
5. `compare_months`
6. `unsupported`

For month-comparison questions, it extracts the two month parameters.

The interpreter validates the returned intent and month formats before passing the interpretation to the business-query service.

### 4.4 Business Query Layer

**File:** `app/services/business_query_service.py`

This layer connects question interpretation with the analytics service.

Responsibilities:

- Receive the interpreted question.
- Identify the business intent.
- Route the intent to the corresponding analytics function.
- Handle unsupported questions.
- Return structured results.

For example:

```text
Question:
"What is the total revenue?"

Intent:
total_revenue

Action:
Call get_total_revenue()

Output:
Total revenue and completed transaction count.
```

### 4.5 Analytics Layer

**File:** `app/services/analytics_service.py`

This layer performs deterministic business calculations using SQL queries.

It supports five main analytics operations.

**1. Total Revenue**

Calculates total completed-sales revenue and the number of completed transactions.

**2. Top Product**

Groups transactions by product and identifies the product generating the highest revenue.

**3. Monthly Revenue**

Groups transaction revenue by month to identify monthly sales trends.

**4. Top Region**

Groups transactions by region and identifies the region with the highest revenue.

**5. Month Comparison**

Compares revenue between two selected months and calculates:

- Revenue in the first month.
- Revenue in the second month.
- Absolute revenue difference.
- Percentage change.

The analytics layer uses SQL aggregation functions such as `SUM()`, `COUNT()`, `GROUP BY`, and `ORDER BY`.

Month comparison uses parameterized SQL queries.

### 4.6 API Layer

**Files:**
- `app/main.py`
- `app/api/routes.py`
- `app/schemas/query.py`

FastAPI exposes REST endpoints for communication with the frontend.

Available endpoints:

| HTTP Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Application status |
| GET | `/health` | Health check |
| POST | `/api/v1/ask` | Submit a business question |

Example API request:

```json
{
    "question": "What is the total revenue?"
}
```

Example API response:

```json
{
    "success": true,
    "question": "What is the total revenue?",
    "intent": "total_revenue",
    "result": {
        "total_revenue": 1439200.0,
        "total_transactions": 48
    }
}
```

Pydantic schemas validate incoming request data and maintain a structured API interface.

### 4.7 Frontend Layer

**File:** `ui/app.py`

Streamlit provides the user interface.

Responsibilities:

- Accept natural-language questions.
- Send requests to the FastAPI backend.
- Display business analytics results.
- Present revenue metrics.
- Display monthly revenue charts.
- Show supporting figures and structured results.

The frontend communicates with the backend using HTTP requests.

## 5. End-to-End Request Flow

The application follows these steps when a user submits a question:

1. The user enters a business question in the Streamlit dashboard.
2. Streamlit sends the question to the FastAPI `/api/v1/ask` endpoint.
3. FastAPI validates the incoming request.
4. BusinessQueryService receives the question.
5. QuestionInterpreter identifies the corresponding business intent.
6. The intent and extracted parameters are validated.
7. BusinessQueryService routes the request to AnalyticsService.
8. AnalyticsService executes the corresponding SQL query against SQLite.
9. The database returns the calculated result.
10. The backend returns a structured JSON response.
11. Streamlit displays the answer using metrics, tables, and charts.

## 6. Security and Reliability

The application follows these practices:

- Uses predefined analytics operations instead of unrestricted SQL generation.
- Uses parameterized SQL queries for month comparisons.
- Validates user questions and extracted month parameters.
- Handles unsupported business questions.
- Stores API credentials in environment variables.
- Avoids committing sensitive credentials to GitHub.
- Uses deterministic SQL calculations for business results.

The LLM is used for question interpretation, while actual revenue calculations are performed by the database.

## 7. Testing Architecture

**Testing framework:** Pytest

The project contains automated tests for both the analytics layer and business-query layer.

Analytics tests verify:

- Total revenue.
- Highest-revenue product.
- Monthly revenue.
- Highest-sales region.
- Month comparison.
- Invalid month format.

Business-query tests verify:

- Supported business questions.
- Intent-based routing.
- Empty questions.
- Unsupported questions.

The current automated test suite contains 12 passing test cases.

## 8. Future Enhancements

Possible future improvements include:

- Support for additional business questions.
- Multiple dataset and database support.
- More advanced natural-language interpretation.
- Improved LLM fallback and error handling.
- Authentication and role-based access control.
- AWS deployment.
- Logging, monitoring, and performance optimization.
- Additional API integration and end-to-end tests.

## 9. Conclusion

The AI Business Intelligence Assistant combines natural-language question interpretation with deterministic SQL analytics.

Its modular architecture separates data ingestion, question interpretation, business logic, analytics, API communication, and frontend visualization.

This approach provides a maintainable and extensible foundation for building AI-assisted business intelligence applications.