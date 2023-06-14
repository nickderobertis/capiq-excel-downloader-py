import math
from typing import Sequence, List
import pandas as pd

from exceldriver.tools import _start_excel_with_addins_and_attach
from processfiles.files import FileProcessTracker
from capiq_excel.workbook.populate.main import populate_capiq_ids_for_file
from capiq_excel.workbook.create import create_all_xlsx_with_id_commands


def download_capiq_ids(ids: Sequence[str], outpath: str = 'capiq ids.csv', folder: str = 'in_process_ids') -> List[str]:
    """
    Downloads Capital IQ identifiers when passed other identifiers such as CUSIP,
    ISIN, ticker, name, etc.

    Stores in a CSV with matched names included and also returns capiq ids as a list

    :param ids: identifiers such as CUSIP, ISIN, ticker, name. Can be a mixture.
    :param folder: folder which will hold in process files
    :param outpath: filepath to output csv, including file extension
    :return: capiq ids
    """
    print('Creating XLSX files with commands to get ids')
    num_files = math.ceil(len(ids) / 100)
    create_all_xlsx_with_id_commands(ids, folder, num_files=num_files)

    print('Populating XLSX files for ids')
    populate_all_ids_in_folder(folder)

    print('Combining all ids into a single CSV file')
    combine_all_capiq_ids_xlsx(folder, outpath)

    return _get_ids_from_csv_path(outpath)


def populate_all_ids_in_folder(folder, restart=True):
    excel = _start_excel_with_addins_and_attach()
    file_tracker = FileProcessTracker(folder=folder, restart=restart, file_types=('xlsx',))

    for file in file_tracker.file_generator():
        populate_capiq_ids_for_file(file, excel)


def combine_all_capiq_ids_xlsx(infolder, outpath, restart=True):

    df = pd.DataFrame()
    df_list = []

    file_tracker = FileProcessTracker(folder=infolder, restart=restart, file_types=('xlsx',))

    for file in file_tracker.file_generator():
        df_list.append(pd.read_excel(file))
    
    df = pd.concat(df_list, sort = False)
    
    _remove_useless_cols(df)
    df.to_csv(outpath, index=False)

    return df


def _remove_useless_cols(df):
    """
    NOTE: inplace
    """
    blank_cols = [col for col in df.columns if 'blank' in col.lower()]
    useless_cols = ['ID'] + blank_cols
    df.drop(useless_cols, axis=1, inplace=True)


def _get_ids_from_csv_path(csv_path: str) -> List[str]:
    df = pd.read_csv(csv_path)
    return df['IQID'].tolist()
