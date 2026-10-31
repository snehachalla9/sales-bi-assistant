# AI Development Notes
## AI Business Intelligence Assistant – RSG Development Challenge

## 1. Project Objective

The objective of this project was to develop a Mini AI Business Intelligence Assistant that allows users to ask natural-language questions about sales data and receive accurate answers supported by actual database queries.

The application combines natural-language interpretation, Python business logic, SQL analytics, REST APIs, and data visualization.

## 2. AI Tools and Technologies Used

### AI Development Tools

**ChatGPT**
- Used for understanding project requirements.
- Assisted with application architecture planning.
- Helped write and understand Python modules.
- Assisted with debugging errors.
- Helped design automated test cases.
- Supported README and technical documentation preparation.

**Groq API**
- Integrated for natural-language question interpretation.
- Used to map user questions to predefined business intents.
- Used to extract month parameters from comparison questions.

### Development Technologies

| Technology | Usage |
|---|---|
| Python | Application development |
| Pandas | CSV processing and cleaning |
| SQLite | Database storage |
| SQLAlchemy | Database connectivity |
| FastAPI | Backend API |
| Streamlit | Frontend dashboard |
| Groq API | LLM-based question interpretation |
| Pytest | Automated testing |
| Git | Version control |

## 3. How AI Was Used in the Application

The application uses an LLM-based question interpretation approach.

For example:

**User question:**

"What is the total revenue?"

**Interpreted intent:**

`total_revenue`

**Business logic:**

The Business Query Service routes the intent to the corresponding analytics function.

**Database operation:**

A predefined SQL query calculates the total completed-sales revenue.

**Final result:**

The application returns the calculated revenue and transaction count.

The LLM is responsible for interpreting the question, not calculating the business figures.

Actual calculations are performed using deterministic SQL queries against the SQLite database.

## 4. Development Approach

The application was developed in the following stages.

### Stage 1: Requirement Analysis

- Reviewed the assessment requirements.
- Identified the five required business questions.
- Planned the application architecture and technology stack.

### Stage 2: Data Ingestion

- Loaded the supplied sales CSV using Pandas.
- Validated required columns.
- Handled missing and invalid records.
- Converted dates and numerical values.
- Calculated revenue for valid transactions.
- Loaded cleaned records into SQLite.

### Stage 3: Analytics Development

Implemented predefined SQL analytics operations for:

- Total revenue.
- Highest-revenue product.
- Monthly revenue trends.
- Highest-sales region.
- Month-to-month revenue comparison.

### Stage 4: Natural-Language Interpretation

- Integrated the Groq API.
- Created an intent-based question interpreter.
- Defined supported business intents.
- Added validation for month parameters.
- Connected interpretation results to the analytics service.

### Stage 5: Backend Development

- Developed REST API endpoints using FastAPI.
- Added request validation using Pydantic.
- Connected API routes to the business-query service.
- Tested API responses using HTTP requests and Swagger documentation.

### Stage 6: Frontend Development

- Developed the dashboard using Streamlit.
- Connected the frontend to the FastAPI backend.
- Added question input and example questions.
- Displayed revenue metrics, tables, and charts.

### Stage 7: Testing

- Created automated tests using Pytest.
- Tested analytics calculations.
- Tested intent routing.
- Tested invalid and unsupported questions.
- Verified 12 automated test cases successfully.

## 5. Challenges Encountered and Solutions

### Challenge 1: Dependency Installation

**Problem:**

Some required Python libraries were missing during initial application setup.

**Solution:**

Installed the dependencies inside the project virtual environment and verified the imports.

### Challenge 2: Groq API Authentication

**Problem:**

The Groq API returned a 401 Invalid API Key error.

**Solution:**

Reviewed the environment-variable configuration and API key setup.

### Challenge 3: Groq Model Availability

**Problem:**

The configured model returned a model-not-found error.

**Solution:**

Investigated model availability and adjusted the question interpretation configuration and error-handling approach.

### Challenge 4: FastAPI Integration Error

**Problem:**

The API initially returned a 500 Internal Server Error because the route called `answer()` while the actual service method was `answer_question()`.

**Solution:**

Corrected the method call and verified successful HTTP 200 responses.

### Challenge 5: Pytest Collection Error

**Problem:**

Pytest initially collected zero tests because of duplicate module names and Python import-path issues.

**Solution:**

- Renamed the old manual test scripts.
- Added `tests/__init__.py`.
- Added `tests/conftest.py`.
- Configured the project root in the Python import path.

### Challenge 6: Testing External LLM Dependencies

**Problem:**

Automated tests should not depend on an external LLM API being available.

**Solution:**

Used mocking to test business-query routing independently of Groq API availability.

## 6. Testing Results

The project currently contains 12 automated test cases.

| Test Area | Coverage |
|---|---|
| Total revenue | Verified |
| Highest-revenue product | Verified |
| Monthly revenue | Verified |
| Highest-sales region | Verified |
| Month comparison | Verified |
| Invalid month format | Verified |
| Supported business questions | Verified |
| Intent routing | Verified |
| Empty question | Verified |
| Unsupported question | Verified |

**Latest test result: 12 passed.**

Command used:

`python -m pytest -v`

## 7. Reliability and Error Handling

The application uses the following approaches:

- Request validation using Pydantic.
- Intent validation before analytics execution.
- Parameterized SQL queries.
- Predefined analytics operations.
- Controlled responses for unsupported questions.
- Environment variables for API credentials.
- Mocking for independent business-query tests.

The application does not execute arbitrary user-provided SQL.

## 8. Limitations

- The application currently supports five main categories of business questions.
- It uses a single supplied sales dataset.
- The database is SQLite rather than a production-scale database.
- Question interpretation depends on the configured LLM or any implemented fallback.
- Authentication and multi-user access are not currently implemented.
- The application has not yet been deployed to a cloud environment.

## 9. Future Improvements

Potential improvements include:

1. Support more complex business questions.
2. Add multi-dataset support.
3. Improve LLM error handling and fallback mechanisms.
4. Add authentication and role-based access control.
5. Deploy the application using AWS.
6. Add logging and monitoring.
7. Improve API and end-to-end test coverage.
8. Add more advanced business visualizations.

## 10. Conclusion

The project demonstrates how AI-assisted natural-language interpretation can be combined with deterministic database analytics to build a simple Business Intelligence Assistant.

The development process involved data processing, SQL analytics, LLM integration, REST API development, frontend visualization, automated testing, debugging, and technical documentation.
## Groq API Dependency and Test Isolation

### Runtime Dependency

The application uses the Groq API through the QuestionInterpreter
component to interpret natural-language business questions.

The application requires:
- A valid API key configured through the GROQ_API_KEY environment variable.
- An accessible model configured through the LLM_MODEL environment variable.

The API key is stored in the local .env file and must never be
committed to Git.

If the API key is missing or invalid, or the configured model is
unavailable, live question interpretation may fail.

The application currently depends on a working Groq configuration
for natural-language question interpretation. No deterministic
fallback is currently implemented.

### Automated Test Isolation

The business-query tests use Python's unittest.mock.Mock to replace
QuestionInterpreter.

The mock is installed before BusinessQueryService is instantiated.
This prevents the service from initializing a real Groq client during
these tests.

The tests provide predefined interpreter responses for supported
and unsupported questions.

This allows the tests to verify business-query routing without
making external API calls.

Therefore:
- A Groq API key is not required for these automated tests.
- The tests do not consume Groq API credits.
- The tests verify business-query routing and response handling.
- Live Groq authentication and model availability must be tested
  separately when running the application.

### Testing Command

Run the automated tests using:

python -m pytest -v

A successful test run confirms the tested application logic works
with the mocked interpreter. It does not prove that the external
Groq API is configured correctly.