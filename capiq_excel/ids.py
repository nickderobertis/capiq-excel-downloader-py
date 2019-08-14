import pandas as pd

from exceldriver.tools import _get_excel_running_workbook
from tracker.files import FileProcessTracker
from .workbook.create import create_all_xlsx_with_id_commands
from .workbook.populate import populate_capiq_ids_for_file

def populate_all_ids_in_folder(folder, restart=True, open_workbook_name='Book1'):
    """
    WARNING: you must first run Excel separately, then open a new workbook, then run this function. This function will
    not start Excel on its own.
    """
    excel = _get_excel_running_workbook(open_workbook_name)
    file_tracker = FileProcessTracker(folder=folder, restart=restart, file_types=('xlsx',))

    for file in file_tracker.file_generator():
        populate_capiq_ids_for_file(file, excel)

def combine_all_capiq_ids_xlsx(infolder, outpath, restart=True):

    df = pd.DataFrame()

    file_tracker = FileProcessTracker(folder=infolder, restart=restart, file_types=('xlsx',))

    for file in file_tracker.file_generator():
        df = _append_capiq_xlsx_to_df(df, file)

    _remove_useless_cols(df)
    df.to_csv(outpath, index=False)

    return df

def _append_capiq_xlsx_to_df(df, filepath):
    temp_df = pd.read_excel(filepath)
    df = df.append(temp_df)

    return df

def _remove_useless_cols(df):
    """
    NOTE: inplace
    """
    blank_cols = [col for col in df.columns if 'blank' in col.lower()]
    useless_cols = ['ID'] + blank_cols
    df.drop(useless_cols, axis=1, inplace=True)

if __name__ == '__main__':
    inpath = r'C:\Users\derobertisna.UFAD\Dropbox (Personal)\UF\Andy\ETF Project\Data\all holdings ids.csv'
    folder = r'C:\Users\derobertisna.UFAD\Dropbox (Personal)\UF\Andy\ETF Project\Data\CapitalIQ\ids'
    outpath = r'C:\Users\derobertisna.UFAD\Dropbox (Personal)\UF\Andy\ETF Project\Data\CapitalIQ\all capiq ids.csv'

    create_all_xlsx_with_id_commands(inpath, folder, num_files=100)

    populate_all_ids_in_folder(folder)

    combine_all_capiq_ids_xlsx(folder, outpath)