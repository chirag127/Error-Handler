import streamlit as st
import sqlite3
import re

# Establish a connection to the SQLite database
conn = sqlite3.connect("error_database.db")
cursor = conn.cursor()

# Create a table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS errors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        regex TEXT,
        reason TEXT,
        solution TEXT
    )
''')
conn.commit()

# Function to check if the entered error matches any regex
def check_error(error_text):
    cursor.execute("SELECT * FROM errors")
    rows = cursor.fetchall()
    for row in rows:
        if re.search(row[2], error_text):
            return (True, row[3], row[4])
    return (False, None, None)

# Streamlit app
st.title("Errorandler")

# Use st.form to group the input fields together
with st.form("error_form"):
    # User input for error
    user_error = st.text_area("Enter your error message:")

    # Submit button to check the error
    submit_button = st.form_submit_button("Check Error")

# Check the error only when the submit button is clicked
if submit_button:
    is_known, reason, solution = check_error(user_error)
    if is_known:
        st.success("This is a known error.")
        st.write("Reason:", reason)
        st.write("Solution:", solution)
    else:
        st.error("This is a new error.")
        st.write("You can add this error to the database below:")

        # Use st.form to group the input fields for adding a new error
        with st.form("add_error_form"):
            new_error_name = st.text_input("Error Name:")
            new_error_regex = st.text_input("Error Regex (in a more generalized form):")
            new_error_reason = st.text_area("Error Reason:")
            new_error_solution = st.text_area("Error Solution:")

            # Submit button to add the error to the database
            add_error_button = st.form_submit_button("Add Error to Database")

        # Add the error to the database only when the submit button is clicked
        if add_error_button:
            cursor.execute("INSERT INTO errors (name, regex, reason, solution) VALUES (?, ?, ?, ?)",
                           (new_error_name, new_error_regex, new_error_reason, new_error_solution))
            conn.commit()
            st.success("Error added to the database.")
            st.text("Refresh the page to check the newly added error.")
