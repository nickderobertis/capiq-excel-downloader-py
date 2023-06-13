import datetime
import pandas as pd
from typing import Any, Union

CAPIQ_DATE_STR_FORMAT = '%Y-%m-%d'


def freq_and_periods_to_begin_date_str(
    freq: str,
    periods: int,
) -> str:
    ts = _freq_and_periods_to_begin_date(freq, periods)
    return ts.strftime(CAPIQ_DATE_STR_FORMAT)


def _freq_and_periods_to_begin_date(
    freq: str,
    periods: int,
) -> pd.Timestamp:
    all_dates = pd.date_range(end=datetime.datetime.today(), periods=periods, freq=freq)
    return all_dates[0]


def today_as_str() -> str:
    return datetime.datetime.today().strftime(CAPIQ_DATE_STR_FORMAT)

def validate_date_input(
    date_input: Union[str, datetime.date, datetime.datetime],
) -> datetime.date:
    """Check that a given input  is of the form datetime.date, datetime.datetime, or a string yyyy-mm-dd"""
    assert type(date_input) in [str, datetime.date, datetime.datetime], 'as_of_date not a date, datetime or a string'
    if type(date_input) == str:
        date_output = datetime.datetime.strptime(date_input, '%Y-%m-%d').date()
    elif type(date_input) in [datetime.datetime]:
        date_output = date_input.date()
    elif type(date_input) in [datetime.date]:
        date_output = date_input
    else:
        raise ValueError('Must pass a string date as yyyy-mm-dd, datetime.date or datetime.datetime object')
    
    return date_output

def date_to_excel_str(input_date: Union[str, datetime.date, datetime.datetime]) -> str:
    validated_date: datetime.date = validate_date_input(input_date)
    return validated_date.strftime(CAPIQ_DATE_STR_FORMAT)