# 💰 Expense Tracker

A simple and interactive web application to manage personal income and expenses.

## Features

- Add income and expense transactions
- Categorize transactions
- Track total income, expenses, and balance
- Visualize expenses with interactive charts
- Filter transactions by category and type
- Delete transactions
- Export transaction history to CSV
- Store transactions locally using SQLite

## Built With

- Python
- Streamlit
- Pandas
- Plotly
- SQLite

## Installation

### 1. Clone the repository

bash
git clone https://github.com/S2anassilah/expense-tracker.git
cd expense-tracker


### 2. Install dependencies

bash
python -m pip install -r requirements.txt


### 3. Run the application

bash
python -m streamlit run app.py


The application will open in your browser at:

http://localhost:8501

## Project Structure

text
expense-tracker/
├── app.py
├── database.py
├── requirements.txt
├── README.md
└── .gitignore


## Database

The application uses SQLite to store transactions in a local database file.

The database is created automatically when the application starts.

## Future Improvements

- Monthly expense reports
- Budget limits
- Search transactions
- Improved dashboard design

## Author

Created as a Python learning project.