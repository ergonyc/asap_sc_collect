# imports
import streamlit as st
import pandas as pd
import logging
from utils.qcutils import *
import datetime as dt


# Step 1: Create a custom logging handler
class StringHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self.log_content = ""

    def emit(self, record):
        msg = self.format(record)
        self.log_content += msg + '\n'

# Define some custom functions
def read_file(data_file):
    if data_file.type == "text/csv":
        df = pd.read_csv(data_file)
    elif data_file.type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
        df = pd.read_excel(data_file, sheet_name=0)
    return (df)

# def to_log(df):
#     """It returns an excel object sheet with the QC sample manifest
#     and clinical data written in separate
#     """
#     today = dt.datetime.today()
#     version = f'{today.year}{today.month}{today.day}'
#     study_code = df.study.unique()[0]
#     ext = "log"
    
#     filename = "{s}_clinial_data_selfQC_{v}.{e}".format(s=study_code, v = version, e = ext)
    
#     output = BytesIO()
#     writer = pd.ExcelWriter(output, engine='xlsxwriter')
#     df.to_excel(writer, index=False, sheet_name='sample_manifest')
#     writer.save()
#     processed_data = output.getvalue()
#     return processed_data, filename


def setup_logging(log_file):
    """Configure logging settings."""
    logging.basicConfig(filename=log_file,
                        level=logging.INFO)
    # ,
    #                     format='%(asctime)s - %(levelname)s - %(message)s')

def get_log(log_file):
    """ grab logged information from the log file."""
    with open(log_file, 'r') as f:
        report_content = f.read()
    return report_content


def pub_md( msg, to_log=True):
    """Wrapper to print to screen and log file."""
    st.markdown(msg)
    if to_log:
        logging.info(msg)

def pub_error( msg, to_log=True):
    """Wrapper to print to screen and log file."""
    st.error(msg)
    if to_log:
        # logging.error(f"> :warning: **{msg}**")    
        logging.error(f"[!WARNING] **{msg}**")


def pub_subheader( msg, to_log=True):
    """Wrapper to print to screen and log file formatted as subheader."""
    st.subheader(msg)
    if to_log:
        logging.info(f"## {msg}")

def pub_header( msg, to_log=True):
    """Wrapper to print to screen and log file formatted as a header."""
    st.header(msg)
    if to_log:
        logging.info(f"# {msg}")

def pub_divider( to_log=True):
    """Wrapper to print a divider to screen and log file."""
    st.divider()
    if to_log:
        logging.info(60*"-")


def jumptwice():
    pub_md("##")
    pub_md("##")


def columnize( itemlist ):
    NEWLINE_DASH = ' \n- '
    if len(itemlist) > 1:
        return f"- {itemlist[0]}{NEWLINE_DASH.join(itemlist[1:])}"
    else:
        return f"- {itemlist[0]}"