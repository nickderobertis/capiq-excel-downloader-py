import pandas as pd

def _date_strs_from_date_range(start_date, end_date, freq='Q'):
    return pd.date_range(start=start_date, end=end_date, freq=freq).to_series().dt.strftime('%m/%d/%Y').tolist()