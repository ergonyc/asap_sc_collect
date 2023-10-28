# imports
import streamlit as st
import pandas as pd

from utils.io import read_file, pub_md, pub_error, pub_subheader, pub_header, pub_divider, columnize, jumptwice



def validate_table(table: pd.DataFrame, table_name: str, CDE: pd.DataFrame):

    retval = 1

    # Filter out rows specific to the given table_name from the CDE
    specific_cde_df = CDE[CDE['Table'] == table_name]
    
    # Extract fields that have a data type of "Enum" and retrieve their validation entries
    enum_fields_dict = dict(zip(specific_cde_df[specific_cde_df['DataType'] == "Enum"]['Field'], 
                               specific_cde_df[specific_cde_df['DataType'] == "Enum"]['Validation']))
    
    # Extract fields that are marked as "Required"
    required_fields = specific_cde_df[specific_cde_df['Required'] == "Required"]['Field'].tolist()
    optional_fields = specific_cde_df[specific_cde_df['Required'] == "Optional"]['Field'].tolist()

    table = force_enum_string(table, table_name, CDE)

    # Check for missing "Required" fields
    missing_required_fields = [field for field in required_fields if field not in table.columns]
    
    if missing_required_fields:
        pub_error(f"Missing Required Fields in {table_name}: {', '.join(missing_required_fields)}")
    else:
        pub_md(f"All required fields are present in *{table_name}* table.")

    jumptwice()
    # Check for empty or NaN values
    empty_fields = []
    total_rows = table.shape[0]
    for test_field,test_name in zip([required_fields, optional_fields], ["Required", "Optional"]):
        empty_or_nan_fields = {}
        for field in test_field:
            if field in table.columns:
                invalid_count = table[field].isna().sum()
                if invalid_count > 0:
                    empty_or_nan_fields[field] = invalid_count
                    
        if empty_or_nan_fields:
            pub_error(f"{test_name} Fields with Empty (nan) values:")
            # st.write(empty_or_nan_fields)
            for field, count in empty_or_nan_fields.items():
                pub_md(f"- {field}: {count}/{total_rows} empty rows")
            retval = 0
        else:
            pub_md(f"No empty entries (Nan) found in _{test_name}_ fields.")
    
    # Check for invalid Enum field values
    invalid_field_values = {}
    valid_field_values = {}

    invalid_fields = []
    invalid_nan_fields = []
    for field, validation_str in enum_fields_dict.items():
        valid_values = eval(validation_str)
        if field in table.columns:
            invalid_values = table[~table[field].isin(valid_values)][field].unique()
            if invalid_values.any():

                if 'Nan' in invalid_values:
                    invalid_nan_fields.append(field)
        
                invalids = [x for x in invalid_values if x != 'Nan' ]
                if len(invalids)>0:
                    invalid_fields.append(field)    
                    invalid_field_values[field] = invalids
                    valid_field_values[field] = valid_values
                


    jumptwice()
    if invalid_field_values:
        pub_subheader("Enums")
        pub_error("Invalid entries")
        # tmp = {key:value for key,value in invalid_field_values.items() if key not in invalid_nan_fields}
        # st.write(tmp)

        for field, values in invalid_field_values.items():
            if field in invalid_fields:
                pub_md(f"- {field}:{', '.join(map(str, values))}")
                pub_md(f"> change to: {', '.join(map(str, valid_field_values[field]))}")

        if len(invalid_nan_fields) > 0:
            pub_error("Found unexpected NULL (nan):")
            pub_md(columnize(invalid_nan_fields))

        
        retval = 0
        # if len(invalid_fields) > 0:
        #     st.text('First 10 entries invalid entries')
        #     st.write(table[invalid_fields].head(10))
        # if len(invalid_nan_fields) > 0:
        #     pub_md('First 10 entries invalid _empty_ entries')
        #     st.write(table[invalid_nan_fields].head(10))

    else:
        pub_md(f"All Enum fields have valid values in {table_name}. 🥳")

    return retval

######## HELPERS ########
# Define a function to only capitalize the first letter of a string
def capitalize_first_letter(s):
    if not isinstance(s, str) or len(s) == 0:  # Check if the value is a string and non-empty
        return s
    return s[0].upper() + s[1:]

def force_enum_string(df, df_name, CDE):

    string_enum_fields = CDE[(CDE["Table"] == df_name) & 
                                (CDE["DataType"].isin(["Enum", "String"]))]["Field"].tolist()
    # Convert the specified columns to string data type using astype() without a loop
    columns_to_convert = {col: 'str' for col in string_enum_fields if col in df.columns}
    df = df.astype(columns_to_convert)

    # enum_fields = CDE[ (CDE["Table"] == df_name) & 
    #                             (CDE["DataType"]=="Enum") ]["Field"].tolist()
    
    for col in string_enum_fields:
        if col in df.columns and col not in ["assay", "file_type"]:
            df[col] = df[col].apply(capitalize_first_letter)

    return df
