import os
import re
import tempfile
import math

import pandas as pd

from capiq_excel.tools.ext_pandas import _get_outpath_and_df_of_headers, _append_df_to_csv, append_csv_to_csv
from processfiles.files import FileProcessTracker


def combine_all_capiq_xlsx(infolder, outpath, restart=True, num_parts=100):

    file_tracker = FileProcessTracker(folder=infolder, restart=restart, file_types=('xlsx',))
    outpath, df_of_headers = _get_outpath_and_df_of_headers(outpath)
    all_columns = [col for col in df_of_headers.columns]

    # TODO: cleanup
    # Set up appending to many files to speed up process. Then the part files will be combined at the end
    num_files_per_part = math.ceil(len(file_tracker.process_list) / num_parts)
    file_num = 0
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f'Creating temporary directory {temp_dir}')
        print(f'Running first pass of append. Will create {num_parts} files to be used in the final append.')
        for i, file in enumerate(file_tracker.file_generator()):
            # Every time we process num_files_per_part number of files, increment the output file
            if i % num_files_per_part == 0:
                file_num += 1
            temp_outpath = os.path.join(temp_dir, f'{file_num}.csv')
            # TODO: better error handling
            try:
                df_of_headers, all_columns = _append_capiq_xlsx_to_csv(file, temp_outpath, df_of_headers, all_columns)
            except Exception:
                print(f'ERROR: Could not load or append {file}. Skipping.')

        # Now append created parts to output file
        print('Running second pass of append. Using in part files to create output file.')
        file_tracker = FileProcessTracker(folder=temp_dir, restart=True, file_types=('csv',))
        outpath, df_of_headers = _get_outpath_and_df_of_headers(outpath)
        all_columns = [col for col in df_of_headers.columns]
        for file in file_tracker.file_generator():
            df_for_append = pd.read_csv(file)  # load new data
            # TODO: better error handling
            try:
                df_of_headers, all_columns = _append_df_to_csv(df_for_append, df_of_headers, outpath, all_columns)
            except Exception:
                print(f'ERROR: Could not load or append {file}. Skipping.')

def _append_capiq_xlsx_to_csv(file, outpath, df_of_headers, all_columns):
    df_for_append = pd.read_excel(file)  # load new data
    if _filepath_has_date(file):
        id_, date = _capiq_filepath_to_iq_id_and_date(file)
        df_for_append['CQID'] = id_
        df_for_append['Date'] = date
    else:
        df_for_append['CQID'] = _capiq_filepath_to_iq_id(file)
    df_of_headers, all_columns = _append_df_to_csv(df_for_append, df_of_headers, outpath, all_columns)

    return df_of_headers, all_columns

def _filepath_has_date(filepath):
    filename = os.path.basename(filepath)  # strips folders, etc.
    pattern = re.compile(r'(IQ\d+) ([\d-]+)([.]xlsx)')
    return True if pattern.match(filename) else False

def _capiq_filepath_to_iq_id(filepath):
    filename = os.path.basename(filepath) #strips folders, etc.
    pattern = re.compile(r'(IQ\d+)([.]xlsx)')
    return pattern.match(filename).group(1)

def _capiq_filepath_to_iq_id_and_date(filepath):
    filename = os.path.basename(filepath)  # strips folders, etc.
    pattern = re.compile(r'(IQ\d+) ([\d-]+)([.]xlsx)')
    match = pattern.match(filename)
    return match.group(1), match.group(2)
