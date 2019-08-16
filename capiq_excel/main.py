from typing import List, Dict, Union, Sequence
import os
from capiq_excel.workbook.create import create_all_xlsx_with_financials_commands
from capiq_excel.downloader.tools import populate_all_files_in_folder
from capiq_excel.ids import download_capiq_ids, _get_ids_from_csv_path
from capiq_excel.combine import combine_all_capiq_xlsx


def download_data(company_ids: List[str], data_items: Union[Dict[str, str], Sequence[str]],
                  ids_folder: str = 'in_process_ids', data_folder: str = 'in_process_data',
                  data_outpath: str = 'capiq data.csv', ids_outpath: str = 'capiq ids.csv',
                  restart: bool = True, timeout: int = 240, run_failed: bool = False,
                  **financial_command_kwargs):
    """
    Downloads data from Capital IQ given arbitrary ids such as name, ticker, CUSIP, ISIN, etc.

    :param company_ids:
    :param data_items: Data items to pull for companies. keys are variable names in capital iq, values are what the
        names should be in the output data. e.g. {'IQ_TOTAL_REVENUE': 'Sales'}. If wanting to use the original names
        from Capital IQ, simply a list may be passed, e.g. ['IQ_TOTAL_REVENUE']
    :param ids_folder: Location for in-process files for getting ids
    :param data_folder: Location for in-process files for getting data
    :param data_outpath: Path to csv where final data should be outputted
    :param ids_outpath: Path to csv where Capital IQ ids should be outputted
    :param restart: If not the first run, start over from the beginning. Set to False to start from where left off
    :param timeout: Time to wait for file to be populated before considering it failed
    :param run_failed: Should only be set to True on a second or later run. Will target the failed files instead
        of the main files if True is passed.
    :param financial_command_kwargs: kwargs for financial_data_command
    :return:
    """

    if restart or not os.path.exists(ids_outpath):
        capiq_ids = download_capiq_ids(
            company_ids,
            outpath=ids_outpath,
            folder=ids_folder
        )
    else:
        capiq_ids = _get_ids_from_csv_path(ids_outpath)

    download_data_for_capiq_ids(
        capiq_ids,
        data_items,
        folder=data_folder,
        outpath=data_outpath,
        restart=restart,
        timeout=timeout,
        run_failed=run_failed,
        **financial_command_kwargs
    )


def download_data_for_capiq_ids(capiq_company_ids: List[str], data_items: Union[Dict[str, str], Sequence[str]],
                                folder: str = 'in_process_data',
                                outpath: str = 'capiq data.csv',
                                restart: bool = True, timeout: int = 240, run_failed: bool = False,
                                **financial_command_kwargs):
    """
    Downloads data from Capital IQ given the capital IQ ids and chosen variables

    :param capiq_company_ids: Capital IQ ids for companies, e.g. ['IQ4564656', 'IQ45643215']
    :param data_items: Data items to pull for companies. keys are variable names in capital iq, values are what the
        names should be in the output data. e.g. {'IQ_TOTAL_REVENUE': 'Sales'}. If wanting to use the original names
        from Capital IQ, simply a list may be passed, e.g. ['IQ_TOTAL_REVENUE']
    :param folder: Location for in-process files
    :param outpath: Path to csv where final data should be outputted
    :param restart: If not the first run, start over from the beginning. Set to False to start from where left off
    :param timeout: Time to wait for file to be populated before considering it failed
    :param run_failed: Should only be set to True on a second or later run. Will target the failed files instead
        of the main files if True is passed.
    :param financial_command_kwargs: kwargs for financial_data_command
    :return:
    """
    if not isinstance(data_items, dict):
        data_items = {var_name: var_name for var_name in data_items}

    if restart or not os.path.exists(folder):
        print('Creating XLSX files with commands')
        create_all_xlsx_with_financials_commands(
            folder,
            company_id_list=capiq_company_ids,
            data_items_dict=data_items,
            **financial_command_kwargs
        )

    print('Populating XLSX files with Capital IQ data')
    populate_all_files_in_folder(
        folder,
        restart=restart,
        timeout=timeout,
        run_failed=run_failed
    )

    print('Combining individual XLSX files into a single CSV file')
    combine_all_capiq_xlsx(
        folder,
        outpath,
        restart=restart
    )


# TODO: download_ids, download_holdings, or combine those into the above function