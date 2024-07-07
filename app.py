import streamlit as st
import pandas as pd
import numpy as np
import io
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows

def generate_sample_input_excel():
    df = pd.DataFrame({
        'Date': pd.date_range(start='1/1/2023', periods=12, freq='M'),
        'Revenue': np.random.randint(10000, 100000, 12),
        'Expenses': np.random.randint(5000, 50000, 12),
        'Profit': np.random.randint(1000, 20000, 12)
    })
    return df

def simulate_api_categorization(df):
    categories = ['Income', 'Expense', 'Profit']
    df['Category'] = np.random.choice(categories, len(df))
    return df

def create_output_excel(df):
    wb = Workbook()
    ws = wb.active
    ws.title = "T12 Categorized"

    # Categories section
    ws.append(["Categories"])
    categories = df['Category'].unique()
    for category in categories:
        ws.append([category])
    ws.append([])

    # Overrides section
    ws.append(["Overrides"])
    ws.append(["No overrides applied"])
    ws.append([])

    # Line Items for T12 section
    ws.append(["Line Items for T12"])
    for r in dataframe_to_rows(df, index=False, header=True):
        ws.append(r)

    output = io.BytesIO()
    wb.save(output)
    output.seek(0)
    return output

def main():
    st.title("T12 Line Item Categorization")

    st.header("Input Excel Sheet")
    input_file = st.file_uploader("Upload T12 Excel file", type="xlsx")

    if input_file is not None:
        df = pd.read_excel(input_file)
    else:
        if st.button("Generate Sample Input"):
            df = generate_sample_input_excel()
            st.write("Sample Input Data:")
            st.write(df)
        else:
            st.write("Please upload an Excel file or generate a sample input.")
            return

    if st.button("Categorize"):
        st.write("Categorizing T12 line items...")
        categorized_df = simulate_api_categorization(df)
        st.write("Categorization complete. Preview of categorized data:")
        st.write(categorized_df)

        output_excel = create_output_excel(categorized_df)
        st.download_button(
            label="Download Categorized Excel",
            data=output_excel,
            file_name="T12_Categorized_Output.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

if __name__ == "__main__":
    main()
