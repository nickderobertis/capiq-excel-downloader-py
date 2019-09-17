from typing import List, Union
import pandas as pd
from exceldriver.columns import get_n_cols_after_col


def write_df_to_ws_values(df: pd.DataFrame, ws, begin_col: str = 'A', begin_row: int = 1):
    # TODO: multi-index
    num_cols = len(df.columns) + 1  # add 1 as index will automatically be converted to col
    end_col = get_n_cols_after_col(begin_col, num_cols - 1)  # -1 as first col goes in begin_col
    end_row = begin_row + len(df)
    cell_range = f'{begin_col}{begin_row}:{end_col}{end_row}'
    values = _df_to_values_for_insert_into_ws(df)
    ws.Range(cell_range).Value = values


def _df_to_values_for_insert_into_ws(df: pd.DataFrame) -> List[List[Union[str, float, int]]]:
    temp_df = df.reset_index()
    temp_df.fillna('', inplace=True)
    temp_df['Date'] = temp_df['Date'].apply(lambda x: x.strftime('%m/%d/%Y'))
    values_list = temp_df.values.tolist()
    values_list.insert(0, list(temp_df.columns))
    return values_list
