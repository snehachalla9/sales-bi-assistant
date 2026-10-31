# AI Business Intelligence Assistant

## Overview

The AI Business Intelligence Assistant is a mini BI application that allows users to ask natural-language questions about sales data and receive answers supported by database queries.

The application uses Python, FastAPI, Streamlit, SQLite, Pandas, and Groq LLM integration.

## Features

- Load sales CSV data into an SQLite database.
- Clean invalid and missing records during ingestion.
- Ask business questions using natural language.
- Identify the intent of a user's question.
- Execute predefined SQL analytics queries.
- Display revenue, top products, monthly trends, and regional performance.
- Compare revenue between two months.
- Visualize monthly revenue using charts.
- Validate inputs and handle unsupported questions.
- Automated tests using Pytest.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core application logic |
| Pandas | CSV processing and data cleaning |
| SQLite | Store sales transactions |
| SQLAlchemy | Database connectivity |
| FastAPI | Backend REST API |
| Streamlit | Frontend dashboard |
| Groq API | Natural-language question interpretation |
| Pytest | Automated testing |

## Architecture

```text
             User
              |
              v
        Streamlit UI
              |
              v
        FastAPI Backend
              |
              v
     Business Query Service
              |
              v
      Question Interpreter
         (Groq LLM)
              |
              v
       Intent Validation
              |
              v
       Analytics Service
              |
              v
       SQLite Database
              |
              v
       Structured Results
              |
              v
        Streamlit UI
```

The application uses predefined analytics queries rather than allowing unrestricted SQL generation. This helps prevent destructive database operations and keeps business calculations deterministic.

## Supported Business Questions

1. What is the total revenue?
2. Which product generated the highest revenue?
3. Show me monthly revenue.
4. Which region has the highest sales?
5. Compare January 2026 and February 2026.

## Data Processing

The supplied sales CSV is processed using Pandas before being loaded into SQLite.

Data-cleaning operations include:

- Checking required columns.
- Handling missing and invalid values.
- Converting order dates into a consistent format.
- Converting numeric columns into appropriate types.
- Excluding invalid records such as non-positive quantities and unit prices.
- Calculating revenue using:

`Revenue = Quantity × Unit Price − Discount Amount`

Returned transactions are retained for traceability but excluded from completed-sales revenue calculations.

## Database Analytics

The Analytics Service executes SQL queries for:

- Total revenue and completed transaction count.
- Highest-revenue product.
- Monthly revenue aggregation.
- Highest-revenue region.
- Month-to-month revenue comparison.
## Sample Results

| Metric | Result |
|---|---:|
| Total Revenue | 1,439,200 |
| Completed Transactions | 48 |
| Top Product | Monitor |
| Top Product Revenue | 473,000 |
| Top Region | South |
| Top Region Revenue | 411,200 |
| January 2026 Revenue | 210,250 |
| February 2026 Revenue | 234,600 |
| Revenue Growth | 11.58% |

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Application status |
| GET | `/health` | Health check |
| POST | `/api/v1/ask` | Submit a business question |

Example request:

```json
{
  "question": "What is the total revenue?"
}
```

Example response:

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

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/snehachalla9/sales-bi-assistant.git
cd sales-bi-assistant
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
LLM_MODEL=your_available_groq_model
DATABASE_URL=sqlite:///./sales.db
```

Use a valid Groq API key and a model available to your account. Never commit `.env` to GitHub.

### 5. Initialize the database

```bash
python -m app.database.init_db
```

### 6. Start the FastAPI backend

```bash
uvicorn app.main:app --reload
```

API documentation:

`http://127.0.0.1:8000/docs`

### 7. Start the Streamlit frontend

Open another terminal:

```bash
source venv/bin/activate
streamlit run ui/app.py
```

Open:

`http://localhost:8501`

## Running Automated Tests

Run:

```bash
python -m pytest -v
```

The project includes 12 automated test cases covering:

- Total revenue.
- Highest-revenue product.
- Monthly revenue.
- Highest-sales region.
- Monthly comparison.
- Invalid month format.
- Supported business questions.
- Intent routing.
- Empty questions.
- Unsupported questions.

Latest test result: **12 passed**.

## Security and Reliability

- Analytics are performed using predefined SQL queries.
- Month comparisons use validated inputs and parameterized database queries.
- The application does not expose arbitrary destructive SQL execution through the question interface.
- API keys are stored in environment variables.
- Unsupported questions receive a controlled response.

## Future Improvements

- Add more business analytics questions.
- Support multiple CSV datasets.
- Add authentication and role-based access.
- Improve LLM interpretation and error handling.
- Deploy the application using AWS.
- Add logging, monitoring, and API performance metrics.

## Project Structure

```text
sales_bi_assistant/
│
├── app/
│   ├── api/
│   │   └── routes.py
│   ├── core/
│   ├── database/
│   │   ├── connection.py
│   │   └── init_db.py
│   ├── models/
│   ├── schemas/
│   │   └── query.py
│   ├── services/
│   │   ├── analytics_service.py
│   │   ├── business_query_service.py
│   │   ├── data_loader.py
│   │   └── question_interpreter.py
│   └── main.py
│
├── data/
│   └── sales_data.csv
│
├── tests/
│   ├── conftest.py
│   ├── test_analytics.py
│   └── test_business_query.py
│
├── ui/
│   └── app.py
│
├── docs/
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```
