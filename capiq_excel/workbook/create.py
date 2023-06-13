from typing import Sequence, Dict, Iterable, Callable
import os
import string
import itertools
import math
import pandas as pd
from openpyxl.utils.dataframe import dataframe_to_rows
from typing import Optional, Union

from exceldriver.workbook.create import get_workbook_and_worksheet
from exceldriver.columns import excel_cols
from .commands import financial_data_command, id_command, name_command, holdings_command, market_data_command


def create_all_xlsx_with_commands(
    folder: str, company_id_list: Sequence[str],
    financial_data_items_dict: Dict[str, str],
    market_data_items_dict: Dict[str, str],
    **financials_kwargs,
) -> None:
    [
        create_xlsx_with_commands(
            folder,
            company_id,
            financial_data_items_dict,
            market_data_items_dict,
            **financials_kwargs
        )
        for company_id in company_id_list
    ]


def create_xlsx_with_commands(
    folder: str,
    company_id: str,
    financial_data_items_dict: Dict[str, str],
    market_data_items_dict: Dict[str, str],
    **financials_kwargs
) -> os.PathLike:
    wb, ws = get_workbook_and_worksheet()
    
    _fill_with_commands(
        ws,
        company_id,
        financial_data_items_dict,
        market_data_items_dict,
        **financials_kwargs
    )

    if not os.path.exists(folder):
        os.makedirs(folder)

    filepath: os.PathLike = os.path.join(folder, f'{company_id}.xlsx')
    wb.save(filepath)

    return os.path.abspath(filepath)

def create_all_xlsx_with_holdings_commands(folder, company_id_list, date_str_list, data_items_dict):
    [
        create_xlsx_with_holdings_commands(folder, company_id, date_str, data_items_dict)
        for company_id, date_str in itertools.product(company_id_list, date_str_list)
    ]


def create_xlsx_with_holdings_commands(folder, company_id: str, date_str: str, data_items_dict):
    wb, ws = get_workbook_and_worksheet()
    _fill_with_holdings_commands(ws, company_id, date_str, data_items_dict)

    filepath = os.path.join(folder, f'{company_id} {_date_str_to_file_format(date_str)}.xlsx')
    wb.save(filepath)

    return os.path.abspath(filepath)

def create_all_xlsx_with_id_commands(ids: Sequence[str], folder: Union[str, os.PathLike], num_files: int = 100) -> None:
    wb, ws = get_workbook_and_worksheet()

    if not os.path.exists(folder):
        os.makedirs(folder)

    df = pd.DataFrame()
    _fill_id_column(df, ids)
    _fill_capiq_id_column(df)
    _fill_capiq_name_column(df)

    rows_per_ws = math.ceil(len(df)/num_files) + 1  # one additional row for headers

    count_per_wb = 0
    count_of_wb = 0
    for index, r in enumerate(dataframe_to_rows(df, index=False, header=True)):
        if index == 0:
            headers = r
        count_per_wb += 1
        ws.append(r)
        if count_per_wb >= rows_per_ws:
            count_per_wb = 0
            count_of_wb += 1
            wb, ws = _save_wb_by_index_get_new_wb(count_of_wb, folder, wb)
            ws.append(headers)

##### Helper functions ####

def _save_wb_by_index_get_new_wb(index, folder, wb):
    filename = f'ids {index}.xlsx'
    filepath = os.path.join(folder, filename)
    wb.save(filepath)
    wb, ws = get_workbook_and_worksheet()
    return wb, ws

def _fill_id_column(df: pd.DataFrame, ids: Sequence[str]) -> None:
    """
    NOTE: inplace
    """
    df['ID'] = ids

def _fill_capiq_id_column(df) -> None:
    """
    NOTE: inplace
    """
    df['IQID'] = df['ID'].apply(id_command)

    # # Blank needed because ids will populate to the right by one column
    # df['IQID'] = ''


def _fill_capiq_name_column(df):
    """
    NOTE: inplace
    """
    df['IQ Name'] = df['ID'].apply(name_command)
    

def _fill_with_commands(
    ws,
    company_id: str,
    financial_data_items_dict: Dict[str, str],
    market_data_items_dict: Dict[str, str],
    **financials_kwargs,
):
    """
    Note: inplace
    """

    # Set default freq
    try:
        freq = financials_kwargs['freq']
    except KeyError:
        freq = 'Q'

    date_dict = _get_date_var_dict_from_freq(freq)

    column_generator = excel_cols()

    common_args = (
        column_generator,
        ws,
        company_id,
    )

    _fill_ws_by_data_item_dict(date_dict, financial_data_command, *common_args, **financials_kwargs)
    _fill_ws_by_data_item_dict(financial_data_items_dict, financial_data_command, *common_args, **financials_kwargs)
    _fill_ws_by_data_item_dict(market_data_items_dict, market_data_command, *common_args, **financials_kwargs)



def _fill_ws_by_data_item_dict(
    data_items_dict: Dict[str, str],
    command_func: Callable,
    column_generator: Iterable,
    ws,
    company_id: str,
    **financials_kwargs,
):
    for item in data_items_dict:
        current_column = next(column_generator)
        ws[f'{current_column}1'] = command_func(
            company_id,
            item,
            **financials_kwargs,
            data_item_label=data_items_dict[item]
        )


def _fill_with_holdings_commands(ws, company_id, date_str, data_items_dict):
    column_generator = excel_cols()

    for item in data_items_dict:
        current_column = next(column_generator)
        ws[f'{current_column}1'] = holdings_command(
            company_id, item, date_str,
            data_item_label=data_items_dict[item]
        )

def _get_date_var_dict_from_freq(freq) -> Dict[str, str]:
    date_dict = {
        'IQ_PERIODDATE_BS': 'Date'
    }
    if freq == 'Y':
        date_dict.update(dict(
            IQ_FISCAL_Y='Fiscal Year'
        ))
    elif freq == 'Q':
        date_dict.update(dict(
            IQ_ABS_PERIOD='Fiscal Quarter'
        ))
    else:
        raise ValueError('Must pass Y or Q for freq')

    return date_dict

def _date_str_to_file_format(date_str):
    return date_str.replace('/','-')


