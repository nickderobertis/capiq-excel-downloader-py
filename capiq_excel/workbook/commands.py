import datetime
from typing import Optional, Union
from capiq_excel.tools.dates import freq_and_periods_to_begin_date_str, today_as_str, validate_date_input, date_to_excel_str


ALLOWED_FREQ = ('Q','H', 'Y', 'LTM', 'NTM')

def financial_data_command(
    company_id: str,
    data_item: str,
    freq: str='Q',
    as_of_date: Optional[Union[str, datetime.date]] = None, 
    num_periods: int=80,
    data_item_label: Optional[str]=None,
    **kwargs,
) -> str:
    """
    Lower-level utility to create an Excel function from inputs for getting financial and estimates data
    For historical data lookup, 

    
    :param company_id: Capital IQ id, e.g. IQ21835
    :param data_item: Capital IQ item, e.g. IQ_TOTAL_REV. Look them up in Data -> Formula Builder in the Capital IQ
        Excel plugin tab
    :param freq: One character to represent frequency, Q or Y
    :param as_of_date: return latest available data as of this data
    :param num_periods: 
        When >= 0 - Returns a single value in the future time period
        When negative - Number of periods to go back in time pulling data
    :param data_item_label: Column name to use instead of data_item name
    :return: Excel command
    """
    _validate_financial_data_inputs(company_id, data_item, freq=freq, num_periods=num_periods, data_item_label=data_item_label)

    # Use variable name as label if none specified
    if data_item_label is None:
        data_item_label = data_item
    
    # set as of date to today if none supplied
    if as_of_date is None:
        as_of_date = datetime.date.today()
    else:
        validate_date_input(as_of_date)
        
        
    as_of_date = date_to_excel_str(as_of_date)
    
    match(freq):
        case 'Y' | 'Q' | 'H':
            freq_str = 'IQ_F' + freq + ('+' if num_periods > 0 else '') + (str(num_periods) if num_periods != 0 else '')
        case 'NTM':
            assert num_periods == 0, 'NTM only works when num_periods = 0'
            freq_str = 'IQ_F' + freq
        case 'LTM':
            assert num_periods <= 0, 'LTM only works when num_periods < 0'
            freq_str = 'IQ_F' + freq
        case _:
            pass
    
    out: str =  f'=CIQRANGE("{company_id}", "{data_item}", {freq_str},"{as_of_date}" , , , , , "{data_item_label}")'
    return out 


def market_data_command(
    company_id: str,
    data_item: str,
    freq: str='Q',
    begin_date: Optional[Union[str, datetime.date]]=None,
    end_date: Optional[Union[str, datetime.date]]=None,
    num_periods: int=80,
    data_item_label: Optional[str]=None,
    **kwargs,
) -> str:
    """
    Lower-level utility to reate an Excel function from inputs for getting market data

    For market data, Capital IQ is expecting begin and end date to be passed rather than relative date. This function
    converts the relative date to absolute dates then creates the Excel command.

    :param company_id: Capital IQ id, e.g. IQ21835
    :param data_item: Capital IQ item, e.g. IQ_FLOAT_PERCENT. Look them up in Data -> Formula Builder in the Capital IQ
        Excel plugin tab
    :param freq: One character to represent frequency, Q or Y
    :param num_periods: Number of periods to go back in time pulling data
    :param data_item_label: Column name to use instead of data_item name
    :return: Excel command
    """
    if begin_date == None:
        begin_date = freq_and_periods_to_begin_date_str(freq, num_periods)
    else:
        begin_date = validate_date_input(begin_date)
    
    if end_date == None:
        end_date = today_as_str()
    else:
        end_date = validate_date_input(end_date)
    
    # Use variable name as label if none specified
    if data_item_label is None:
        data_item_label = data_item

    return f'=CIQRANGE("{company_id}", "{data_item}", "{begin_date}", "{end_date}", , , , , "{data_item_label}")'

# TODO: put command to create multiples data

# TODO: put command to create economic data


def holdings_command(
    company_id,
    data_item,
    date_str,
    data_item_label=None,
):
    # Use variable name as label if none specified
    if data_item_label is None:
        data_item_label = data_item

    return f'=CIQRANGE("{company_id}", "{data_item}", 1, 50000, "{date_str}", , , , "{data_item_label}")'

def id_command(search_str: str) -> str:
    return f'=CIQ("{search_str}","IQ_COMPANY_ID")'

def name_command(search_str: str) -> str:
    return f'=CIQ("{search_str}","IQ_COMPANY_NAME")'

def _validate_financial_data_inputs(*args, **kwargs) -> None:
    assert kwargs['freq'] in ALLOWED_FREQ
    assert isinstance(args[0], str)
    assert isinstance(args[1], str)
    assert isinstance(kwargs["num_periods"], int)
    
def from_excel_ordinal(
    ordinal: float,
    _epoch0=datetime.datetime(1899, 12, 31),
) -> datetime.datetime:
    if ordinal >= 60:
        ordinal -= 1  # Excel leap year bug, 1900 is not a leap year!
    return (_epoch0 + datetime.timedelta(days=ordinal)).replace(microsecond=0)

def to_excel_ordinal(
    date: datetime.datetime,
    _epoch0=datetime.datetime(1899, 12, 31),
) -> int:
    diff = date - _epoch0
    if date >= datetime.datetime(1900, 3, 1):
        diff += 1  # Excel leap year bug, 1900 is not a leap year!
    return diff