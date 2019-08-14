import pandas as pd

from exceldriver.tools import _start_excel_with_addins_and_attach
from processfiles.files import FileProcessTracker
from .workbook.populate import populate_capiq_ids_for_file


def populate_all_ids_in_folder(folder, restart=True):
    excel = _start_excel_with_addins_and_attach()
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
