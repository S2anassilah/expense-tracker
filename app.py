import streamlit as st
import pandas as pd
import plotly.express as px

from datetime import date
from database import (
    init_db,
    add_transaction,
    get_transactions,
    delete_transaction,
)

st.set_page_config(
    page_title="Expense Tracker",
    page_icon="💰",
    layout="wide",
)

# Initialize database
init_db()

st.title("💰 Expense Tracker")
st.caption("Manage your income and expenses easily.")

# Load transactions
transactions = get_transactions()
df = pd.DataFrame(transactions)

# Calculate totals
if not df.empty:
    income = df.loc[df["kind"] == "Income", "amount"].sum()
    expenses = df.loc[df["kind"] == "Expense", "amount"].sum()
else:
    income = 0.0
    expenses = 0.0

balance = income - expenses

# Dashboard
col1, col2, col3 = st.columns(3)

col1.metric("Total Income", f"{income:.2f} MAD")
col2.metric("Total Expenses", f"{expenses:.2f} MAD")
col3.metric("Balance", f"{balance:.2f} MAD")

st.divider()

# Add transaction
st.subheader("➕ Add a transaction")

with st.form("transaction_form", clear_on_submit=True):
    kind = st.selectbox(
        "Transaction type",
        ["Expense", "Income"],
    )

    amount = st.number_input(
        "Amount (MAD)",
        min_value=0.01,
        value=10.0,
        step=10.0,
    )

    if kind == "Expense":
        categories = [
            "Food", "Transport", "Housing",
            "Education", "Entertainment", "Health", "Other"
        ]
    else:
        categories = [
            "Salary", "Freelance", "Gift", "Other"
        ]

    category = st.selectbox("Category", categories)
    transaction_date = st.date_input("Date", value=date.today())
    description = st.text_input("Description")

    submitted = st.form_submit_button("Save transaction")

    if submitted:
        add_transaction(
            kind,
            amount,
            category,
            transaction_date.isoformat(),
            description.strip(),
        )
        st.success("Transaction saved!")
        st.rerun()

# Refresh data
transactions = get_transactions()
df = pd.DataFrame(transactions)

st.divider()
st.subheader("📋 Transaction history")

if df.empty:
    st.info("No transactions yet. Add your first transaction.")
else:
    df["date"] = pd.to_datetime(df["date"])

    # Filters
    categories = sorted(df["category"].unique().tolist())

    selected_categories = st.multiselect(
        "Filter by category",
        categories,
        default=categories,
    )

    selected_kind = st.selectbox(
        "Filter by type",
        ["All", "Income", "Expense"],
    )

    filtered = df[df["category"].isin(selected_categories)]

    if selected_kind != "All":
        filtered = filtered[filtered["kind"] == selected_kind]

    st.dataframe(
        filtered[
            ["id", "date", "kind", "category", "amount", "description"]
        ],
        use_container_width=True,
        hide_index=True,
    )

    # Expense chart
    expense_df = df[df["kind"] == "Expense"]

    if not expense_df.empty:
        st.subheader("📊 Expenses by category")

        chart_data = expense_df.groupby(
            "category", as_index=False
        )["amount"].sum()

        fig = px.pie(
            chart_data,
            names="category",
            values="amount",
            title="Expense distribution",
            hole=0.4,
        )

        st.plotly_chart(fig, use_container_width=True)

    # Export to CSV
    csv_data = filtered.to_csv(index=False).encode("utf-8-sig")

    st.download_button(
        "⬇️ Export transactions to CSV",
        data=csv_data,
        file_name="transactions.csv",
        mime="text/csv",
    )

    # Delete transaction
    st.subheader("🗑️ Delete a transaction")

    transaction_ids = filtered["id"].astype(int).tolist()

    if transaction_ids:
        selected_id = st.selectbox(
            "Choose transaction ID",
            transaction_ids,
        )

        confirm_delete = st.checkbox(
            f"Confirm deletion of transaction #{selected_id}"
        )

        if st.button("Delete selected transaction"):
            if confirm_delete:
                delete_transaction(int(selected_id))
                st.success("Transaction deleted.")
                st.rerun()
            else:
                st.warning("Please confirm deletion first.")