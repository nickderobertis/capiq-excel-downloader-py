import pandas as pd

from capiq_excel import download_data

import test.conftest as conf

def _check_for_correct_ids(df: pd.DataFrame):
    id_values = df['CQID'].unique().tolist()
    assert len(id_values) == 2
    assert 'IQ21835' in id_values
    assert 'IQ24937' in id_values


def _check_for_correct_columns(df: pd.DataFrame):
    assert (df.columns == ['Date', 'Fiscal Quarter', 'IQ_TOTAL_REV', 'IQ_COST_REV',
       'IQ_FLOAT_PERCENT', 'CQID']).all()


def _check_for_data_in_columns(df: pd.DataFrame):
    for col in ('Date', 'IQ_TOTAL_REV', 'IQ_COST_REV', 'IQ_FLOAT_PERCENT'):
        assert len(df[col].dropna()) > 0


def _check_that_dates_are_valid(df: pd.DataFrame):
    pd.to_datetime(df['Date'])  # will raise error if invalid date


def test_download_data():
    download_data(
        ['MSFT', 'AAPL'], # Any id type. Ticker, name, CUSIP, ISIN, etc.
        financial_data_items=['IQ_TOTAL_REV', 'IQ_COST_REV'], # Financial data variable names from Capital IQ
        market_data_items=['IQ_FLOAT_PERCENT'], # Market data variable names from Capital IQ
        freq='Q',
        num_periods=6,
        ids_folder=str(conf.ID_DIR),
        data_folder=str(conf.DATA_FOLDER),
        data_outpath=str(conf.OUT_DATA_PATH),
        ids_outpath=str(conf.IDS_OUT_PATH),
    )
    df = pd.read_csv(conf.OUT_DATA_PATH)
    _check_for_correct_ids(df)
    _check_for_correct_columns(df)
    _check_for_data_in_columns(df)
    _check_that_dates_are_valid(df)