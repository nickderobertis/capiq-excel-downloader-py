import pandas as pd
import shutil
import os
import time
import re
import datetime
from functools import partial

def append_csvs_to_csv(csv_filepath_list, outpath=None):
    """
    Appends csvs into a single csv. Is memory efficient by only keeping the current
    processed file in memory. However still keeps track of changing columns to ensure
    data is correctly aligned.

    :param csv_filepath_list:
    :param outpath:
    :return:
    """

    outpath, df_of_headers = _get_outpath_and_df_of_headers(outpath)

    all_columns = [col for col in df_of_headers.columns]

    for file in csv_filepath_list:
        df_for_append = pd.read_csv(file) #load new data
        df_of_headers, all_columns = _append_df_to_csv(df_for_append, df_of_headers, outpath, all_columns)

def append_csv_to_csv(inpath, outpath):
    return append_csvs_to_csv([inpath], outpath)

def append_csvs_to_monthly_csv_of_first_date(csv_filepath_list, rootname):
    [append_csv_to_monthly_csv_of_first_date(inpath, rootname) for inpath in csv_filepath_list]

def append_csv_to_monthly_csv_of_first_date(inpath, rootname):
    df_for_append = pd.read_csv(inpath)  # load new data
    return append_df_to_monthly_csv_of_first_date(df_for_append, rootname)

def append_df_to_monthly_csv_of_first_date(df_for_append, rootname):
    year_month_str = first_year_month_in_df(df_for_append)

    outpath = rootname + year_month_str + '.csv'
    append_df_to_csv(df_for_append, outpath)

def append_df_to_csv(df, outpath):
    outpath, df_of_headers = _get_outpath_and_df_of_headers(outpath)
    all_columns = [col for col in df_of_headers.columns]
    _append_df_to_csv(df, df_of_headers, outpath, all_columns)

def _get_outpath_and_df_of_headers(outpath):
    # Output to a new csv if outpath not supplied
    if outpath is None:
        outpath = 'combined.csv'
    # If outpath doesn't exists, must create df from scratch
    if (outpath is None) or (not os.path.exists(outpath)):
        df_of_headers = pd.DataFrame()
    # If exists, load headers
    else:
        df_of_headers = pd.read_csv(outpath, nrows=0)

    return outpath, df_of_headers

def _append_df_to_csv(df_for_append, df_of_headers, outpath, all_columns):

    # Set mode to append or write
    # If there are any columns from loaded csv, then don't write headers. If there are none, write.
    if not all_columns:
        header = True
    else:
        header = False

    # Get headers for combined data
    new_columns = [col for col in df_for_append.columns if col not in df_of_headers.columns]
    all_columns += new_columns
    df_of_headers = pd.DataFrame(columns=all_columns)

    # Append new data, with or without writing headers to file
    full_df = df_of_headers.append(df_for_append)
    full_df[all_columns].to_csv(outpath, mode='a', index=False, header=header, encoding='utf8')

    # Go back to file and update the headers
    headers_csv = pd.DataFrame(columns=all_columns).to_csv(index=False)
    replace_first_line_of_file(outpath, headers_csv)

    return df_of_headers, all_columns


def replace_first_line_of_file(inpath, new_first_line, outpath=None):

    if outpath is None:
        rename = True
        outpath = inpath + '.temp' #replace existing file
    else:
        rename = False

    with open(inpath, 'r', encoding='utf8') as infile:
        infile.readline()  # and discard
        with open(outpath, 'w', encoding='utf8') as outfile:
            outfile.write(new_first_line)
            shutil.copyfileobj(infile, outfile) #bring over rest of contents to new (or replaced) file

    if rename:
        _replace(outpath, inpath)


def _replace(src, dst):
    retries = 0
    while True:
        try:
            os.replace(src, dst)
            break
        except (PermissionError, OSError) as e:
            time.sleep(.1)
            retries += 1
            if retries > 100:
                print(f'Retried removing {filepath} over 10s but still failed.')
                raise e


ymd_pattern = re.compile(r'(\d\d\d\d)-(\d\d)-(\d\d)')

def first_year_month_in_df(df, date_str_col='Date'):
    return _year_month_from_date_string(df.loc[0, date_str_col])

def _year_month_from_date_string(date_string):
    m = ymd_pattern.match(date_string)

    return f'{m.group(1)}{m.group(2)}'

def add_year_month_column_from_date_string_column(df, date_str_col='Date'):
    """
    note: inplace
    """

    df['YearMonth'] = df[date_str_col].apply(_year_month_from_date_string)


def convert_excel_date_to_pandas_date(exceldates):
    epoch = datetime.datetime(1899, 12, 30)
    convert = partial(_convert_excel_date_to_pandas_date, epoch)

    return exceldates.apply(convert)


def _convert_excel_date_to_pandas_date(epoch, date):
    if not pd.isnull(date) and isinstance(date, (int, float)):
        return epoch + datetime.timedelta(days=date)
    else:
        return date


def scale_variables(df, rescale_factor, rescale_vars):
    """
    Note: inplace
    """
    for var in rescale_vars:
        df[var] = df[var] * rescale_factor

def _how_merge_df(df: pd.DataFrame, other_df: pd.DataFrame, ids, how='left'):
    return df.merge(other_df, on=ids, how=how)

def outer_merge_df(df: pd.DataFrame, other_df: pd.DataFrame, ids):
    return _how_merge_df(df, other_df, ids, how='outer')

def left_merge_df(df: pd.DataFrame, other_df: pd.DataFrame, ids):
    return _how_merge_df(df, other_df, ids, how='left')

def right_merge_df(df: pd.DataFrame, other_df: pd.DataFrame, ids):
    return _how_merge_df(df, other_df, ids, how='right')

def get_full_date_df_from_date_series(date_series, new_date_name=None):

    if new_date_name is None:
        new_date_name = date_series.name

    start_date = date_series.min()
    end_date = date_series.max()

    dates = pd.date_range(
        start=start_date,
        end=end_date,
        freq='D'
    )

    date_df = pd.DataFrame(dates, columns=[new_date_name])

    return date_df


def date_from_year_month(df: pd.DataFrame, day: int = 15, month_col: str = 'Month',
                         year_col: str = 'Year', date_col: str = 'Date') -> None:
    """
    Note: inplace
    """

    _date_str = partial(
        _date_str_from_year_month,
        day=day,
        month_col=month_col,
        year_col=year_col
    )

    df[date_col] = df.apply(_date_str, axis=1)
    df[date_col] = pd.to_datetime(df[date_col])


def _date_str_from_year_month(row_series: pd.Series, day: int = 15, month_col: str = 'Month',
                              year_col: str = 'Year'):
    return f'{int(row_series[month_col])}/{day}/{int(row_series[year_col])}'