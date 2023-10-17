# imports
import streamlit as st
import pandas as pd
import numpy as np



# Define some custom functions
def read_file(data_file):
    if data_file.type == "text/csv":
        df = pd.read_csv(data_file)
    elif data_file.type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
        df = pd.read_excel(data_file, sheet_name=0)
    return (df)



# Show template that ppl must fill in 
# We can split the template in chunks and process each template sepparatedly if we like
# As this is just the beginning, let's keep it simple and process all data on a single app. Then, we can easily make it nicer



# Define optional columns
optional_cols = ["PI_ORCHID", "PI_google_scholar_id", "metadata_version_date", "primary_diagnosis_text",
                 "preprocessing_references", "DV200" , "pm_PH", "donor_id", "other_reference", "smoking_years",
                 "path_autopsy_second_dx", "path_autopsy_third_dx", "path_autopsy_fourth_dx" "path_autopsy_fifth_dx",
                 "path_autopsy_sixth_dx", "path_autopsy_seventh_dx" "path_autopsy_eight_dx"]


# Provide template
st.markdown('<p class="big-font"> ASAP single cell data fields self-QC </p>', unsafe_allow_html=True)
st.markdown('<p class="medium-font"> This app is intended to make sure ASAP contributing with single cell data provide standard ASAP required fields </p>', unsafe_allow_html=True)
st.markdown('<p class="medium-font"> Download the template from the link below. Once you open the link, go to "File"> "Download" > "xlsx" or "csv" format </p>', unsafe_allow_html=True)
st.markdown('[Access the data dictionary and template](https://docs.google.com/spreadsheets/d/1ePEyitq8Gy7EZ8hZ4KbF4iAew2g3n_RS/edit#gid=263869186)', unsafe_allow_html=True)



# Read file from streamlit
data_file = st.sidebar.file_uploader("Upload Your Sample manifest (CSV/XLSX)", type=['xlsx', 'csv'])

if data_file is not None:
    data = read_file(data_file)
else:
    st.stop()



# Check all columns are present in the input 
# We can do something such as checking the number of columns matches what we would expect ( a bit unsafe tho)
# Otherwise, create a list with all col names



# Check all required columns are not missing
required_cols = [col for col in data.columns if col not in optional_cols]

data_non_miss_check = data[required_cols].copy()

if data_non_miss_check.isna().sum().sum()>0:
    st.error('There are some missing entries in the required columns. Please fill the missing cells ')
    st.text('First 30 entries with missing data in any required fields')
    st.write(data_non_miss_check[data_non_miss_check.isna().sum(1)>0].head(30))
    st.stop()
else:
    st.text('Check missing data in the required fields --> OK')



# Perform numeric variables specific checks (ie, are thay on a sensible range or we can detect errors?)


