import streamlit as st
import requests
import pandas as pd

# ---------------- CONFIGURATION ----------------

API_URL = "http://127.0.0.1:8000/api/v1/ask"

st.set_page_config(
    page_title="AI Business Intelligence Assistant",
    page_icon="📊",
    layout="wide"
)

# ---------------- HEADER ----------------

st.title("📊 AI Business Intelligence Assistant")
st.write("Ask questions about your sales data using natural language.")

st.divider()

# ---------------- EXAMPLE QUESTIONS ----------------

st.subheader("Try these questions")

examples = [
    "What is the total revenue?",
    "Which product generated the highest revenue?",
    "Show me monthly revenue",
    "Which region has the highest sales?",
    "Compare January 2026 and February 2026"
]

cols = st.columns(2)

for i, question in enumerate(examples):
    if cols[i % 2].button(question, use_container_width=True):
        st.session_state["question"] = question

# ---------------- USER INPUT ----------------

question = st.text_input(
    "Enter your business question:",
    value=st.session_state.get("question", ""),
    placeholder="Example: What is the total revenue?"
)

if st.button("Get Answer", type="primary"):
    if not question.strip():
        st.warning("Please enter a question.")

    else:
        try:
            with st.spinner("Analyzing your sales data..."):

                response = requests.post(
                    API_URL,
                    json={"question": question},
                    timeout=30
                )

            if response.status_code == 200:

                data = response.json()

                st.success("Answer generated successfully!")

                st.subheader("Your Answer")

                result = data.get("result", {})
                intent = data.get("intent", "")

                # Total revenue
                if intent == "total_revenue":
                    col1, col2 = st.columns(2)

                    col1.metric(
                        "Total Revenue",
                        f"₹{result['total_revenue']:,.2f}"
                    )

                    col2.metric(
                        "Completed Transactions",
                        result["total_transactions"]
                    )

                # Highest revenue product
                elif intent == "top_product":
                    col1, col2 = st.columns(2)

                    col1.metric("Top Product", result["product"])

                    col2.metric(
                        "Revenue",
                        f"₹{result['total_revenue']:,.2f}"
                    )

                    st.write("Units Sold:", result["units_sold"])

                # Highest sales region
                elif intent == "top_region":
                    col1, col2 = st.columns(2)

                    col1.metric("Top Region", result["region"])

                    col2.metric(
                        "Revenue",
                        f"₹{result['total_revenue']:,.2f}"
                    )

                    st.write(
                        "Transactions:",
                        result["total_transactions"]
                    )

                # Monthly revenue
                elif intent == "monthly_revenue":
                    df = pd.DataFrame(result)

                    st.subheader("Monthly Revenue")

                    st.bar_chart(
                        df.set_index("month")["revenue"]
                    )

                    st.dataframe(df, use_container_width=True)

                # Compare months
                elif intent == "compare_months":
                    col1, col2, col3 = st.columns(3)

                    col1.metric(
                        result["month1"],
                        f"₹{result['revenue1']:,.2f}"
                    )

                    col2.metric(
                        result["month2"],
                        f"₹{result['revenue2']:,.2f}"
                    )

                    col3.metric(
                        "Revenue Change",
                        f"₹{result['difference']:,.2f}",
                        f"{result['percentage_change']}%"
                    )

                # Display raw supporting figures
                with st.expander("View supporting data"):
                    st.json(result)

                st.caption(f"Detected intent: {intent}")

            else:
                st.error(f"API Error: {response.text}")

        except requests.exceptions.ConnectionError:
            st.error(
                "Cannot connect to FastAPI. "
                "Please start the backend first."
            )

        except requests.exceptions.Timeout:
            st.error("The request timed out. Please try again.")

        except Exception as e:
            st.error(f"Unexpected error: {e}")