"""
A tool to drive Excel using the Capital IQ plugin to download Capital IQ data. Useful for downloading
large data sets from Capital IQ.
"""
from capiq_excel.main import (
    download_data,
    download_data_for_capiq_ids
)