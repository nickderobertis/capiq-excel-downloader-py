import re
import pandas as pd
import numpy as np
from exceldriver.columns import excel_cols


CIQ_MARKET_ITEM_FORMULA_PATTERN = re.compile(r'=CIQ\("[\w]+", "[\w]+", "([\w\/]+)"\)')


def extract_capiq_df_from_sheet(ws, market_data_items):
    col_gen = excel_cols()

    all_series = []
    while True:
        col = next(col_gen)
        if col == 'A':
            continue  # A is date column, don't need to extract
        cell_range = f'{col}1'
        value = ws.Range(cell_range).Value
        if value is None:
            # Blank column label, data is finished
            break
        if value in market_data_items.values():
            # Market data item, need to extract data
            all_series.append(get_series_from_ciq_market_item_col(ws, col))
        else:
            # Financial data item, need to extract data
            all_series.append(get_series_from_ciq_financial_col(ws, col))

    df = pd.concat(all_series, axis=1)
    df.index.name = 'Date'
    return df


def get_series_from_ciq_market_item_col(ws, col: str):
    series = pd.Series()
    row = 2
    while True:
        cell_range = f'{col}{row}'
        value = ws.Range(cell_range).Value
        if value is None:
            break
        formula = ws.Range(cell_range).Formula
        date = get_date_from_ciq_market_item_formula(formula)
        series[date] = value
        row += 1
    series.name = ws.Range(f'{col}1').Value
    series.index = pd.to_datetime(series.index)
    return series


def get_series_from_ciq_financial_col(ws, col: str):
    series = pd.Series()
    row = 2
    while True:
        cell_range = f'{col}{row}'
        value = ws.Range(cell_range).Value
        if value is None:
            break
        # Column A has dates
        date = ws.Range(f'A{row}').Value
        if isinstance(date, str):
            # Handle CapIQ missing representation
            if date == 'NA':
                date = np.nan
            # Allow other strs to pass through
        else:
            # TODO: add check for pycom datetime object type
            # Extract date str from pycom datetime object
            date = str(date.date())
        series[date] = value
        row += 1
    series.name = ws.Range(f'{col}1').Value
    series.index = pd.to_datetime(series.index)
    return series


def get_date_from_ciq_market_item_formula(formula: str) -> str:
    match = CIQ_MARKET_ITEM_FORMULA_PATTERN.match(formula)
    if not match:
        return None
    return match.group(1)