import pandas as pd
import warnings

from capiq_excel.downloader.timeout import TimeoutWrapper
from capiq_excel.fileops import get_path_of_failed_folder_add_if_necessary, move_file_to_failed_folder, get_path_of_additional_failed_folder_add_if_necessary
from capiq_excel.workbook.populate import populate_capiq_for_file
from exceldriver.tools import _start_excel_with_addins_and_attach, _get_excel_running_workbook, _restart_excel_with_addins_and_attach, NoExcelWorkbookException
from processfiles.files import FileProcessTracker



def populate_all_files_in_folder(folder, restart=True, timeout=240, run_failed=False):
    """

    """
    _validate_populate_inputs(folder, restart, run_failed)

    excel = _start_excel_with_addins_and_attach()
    failed_folder = get_path_of_failed_folder_add_if_necessary(folder)

    if run_failed:
        # Set main folder as 'failed', then set failed folder as another failed folder inside the original
        folder = failed_folder
        failed_folder = get_path_of_additional_failed_folder_add_if_necessary(folder)

    file_tracker = FileProcessTracker(folder=folder, restart=restart, file_types=('xlsx',))


    populate_all_files_in_folder_with_timeout = TimeoutWrapper(timeout, _populate_capiq_for_multiprocess, timeout_callback=_return_false)


    for i, file in enumerate(file_tracker.file_generator()):
        successful = populate_all_files_in_folder_with_timeout(file, index=i + 1)
        if not successful:
            move_file_to_failed_folder(file, failed_folder)


def _get_company_id_list(id_filepath, id_col='IQID'):
    df = pd.read_csv(id_filepath, usecols=[id_col])
    unique = df[id_col].unique().tolist()

    # Drop nans
    return [i for i in unique if not pd.isnull(i)]

def _validate_populate_inputs(folder, restart, run_failed):
    assert not (restart and run_failed)

    if run_failed:
        warnings.warn(f'run_failed flag passed. Folder {folder}, will not be run, instead the failed folder will')

### Functions below to assist with multiprocessing/timeout handling


def _populate_capiq_for_multiprocess(file, **kwargs):
    try:
        excel = _get_excel_running_workbook('Book1.xlsx')
    except NoExcelWorkbookException:
        excel = _restart_excel_with_addins_and_attach()
    excel, successful = populate_capiq_for_file(file, excel, **kwargs)
    return successful

def _restart_excel_and_return_false():
    excel = _restart_excel_with_addins_and_attach(max_retries=10)

    return False

def _return_false():
    return False

## END TEMP