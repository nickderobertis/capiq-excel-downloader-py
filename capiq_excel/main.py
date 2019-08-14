from typing import List, Dict
from capiq_excel.workbook.create import (
    create_all_xlsx_with_financials_commands,
    create_all_xlsx_with_holdings_commands,
    create_all_xlsx_with_id_commands
)
from capiq_excel.downloader.tools import populate_all_files_in_folder
from capiq_excel.ids import populate_all_ids_in_folder, combine_all_capiq_ids_xlsx
from capiq_excel.combine import combine_all_capiq_xlsx


def download_financials(folder: str, company_ids: List[str], data_items: Dict[str, str],
                        outpath: str = 'combined.csv',
                        restart: bool = True, timeout: int = 240, run_failed: bool = False,
                        **financial_command_kwargs):
    """
    Downloads financial data from Capital IQ given the capital IQ ids and chosen variables

    :param folder: Location for in-process files
    :param company_ids: Capital IQ ids for companies, e.g. ['IQ4564656', 'IQ45643215']
    :param data_items: Data items to pull for companies. keys are variable names in capital iq, values are what the
        names should be in the output data. e.g. {'IQ_TOTAL_REVENUE': 'Sales'}
    :param outpath: Path to csv where final data should be outputted
    :param restart: If not the first run, start over from the beginning. Set to False to start from where left off
    :param timeout: Time to wait for file to be populated before considering it failed
    :param run_failed: Should only be set to True on a second or later run. Will target the failed files instead
        of the main files if True is passed.
    :param financial_command_kwargs: kwargs for financial_data_command
    :return:
    """
    print('Creating XLSX files with commands')
    create_all_xlsx_with_financials_commands(
        folder,
        company_id_list=company_ids,
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