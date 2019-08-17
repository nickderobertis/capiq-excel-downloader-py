from typing import Optional
from capiq_excel.tools.dates import freq_and_periods_to_begin_date_str, today_as_str


def financial_data_command(company_id: str, data_item: str, freq: str='Q', num_periods: int=80,
                           data_item_label: Optional[str]=None) -> str:
    """
    Lower-level utility to create an Excel function from inputs for getting financial data

    :param company_id: Capital IQ id, e.g. IQ21835
    :param data_item: Capital IQ item, e.g. IQ_TOTAL_REV. Look them up in Data -> Formula Builder in the Capital IQ
        Excel plugin tab
    :param freq: One character to represent frequency, Q or Y
    :param num_periods: Number of periods to go back in time pulling data
    :param data_item_label: Column name to use instead of data_item name
    :return: Excel command
    """
    _validate_financial_data_inputs(company_id, data_item, freq=freq, num_periods=num_periods, data_item_label=data_item_label)

    # Use variable name as label if none specified
    if data_item_label is None:
        data_item_label = data_item

    return f'=CIQRANGE("{company_id}", "{data_item}", IQ_F{freq} - {num_periods}, , , , , , "{data_item_label}")'


def market_data_command(company_id: str, data_item: str, freq: str='Q', num_periods: int=80,
                        data_item_label: Optional[str]=None) -> str:
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
    begin_date = freq_and_periods_to_begin_date_str(freq, num_periods)
    end_date = today_as_str()

    # Use variable name as label if none specified
    if data_item_label is None:
        data_item_label = data_item

    return f'=CIQRANGE("{company_id}", "{data_item}", "{begin_date}", "{end_date}", , , , , "{data_item_label}")'


def holdings_command(company_id, data_item, date_str, data_item_label=None):
    # Use variable name as label if none specified
    if data_item_label is None:
        data_item_label = data_item

    return f'=CIQRANGE("{company_id}", "{data_item}", 1, 50000, "{date_str}", , , , "{data_item_label}")'

def id_command(search_str):
    return f'=CIQRANGEA("{search_str}","IQ_COMPANY_ID_QUICK_MATCH",1,1)'

def name_command(search_str):
    return f'=CIQRANGEA("{search_str}","IQ_COMPANY_NAME_QUICK_MATCH",1,1)'

def _validate_financial_data_inputs(*args, **kwargs):
    assert kwargs['freq'] in ('Q','Y')
    assert isinstance(args[0], str)
    assert isinstance(args[1], str)