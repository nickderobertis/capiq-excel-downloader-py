from win32com.client import constants
from pywintypes import com_error
import time
import traceback, sys

from .wait import _wait_for_capiq_result
from ..exceptions import WorkbookClosedException, CapitalIQInactiveException
from exceldriver.tools import _restart_excel_with_addins_and_attach

def populate_capiq_for_file(filepath, excel, retries_remaining=3, close_workbook=False, index=0):
    """

    Private function has main functionality. This is a wrapper to add retries afer com errors
    """

    # Even if things are going normally, restart every 500 worksheets as there is a memory leak
    if index % 500 == 0 and retries_remaining == 3:
        excel = _restart_excel_with_addins_and_attach()

    # Stop retries
    if retries_remaining <= 0:
        print(fr'ERROR: Could not process {filepath}. Skipping and moving to "..\failed".')
        return excel, False

    try:
        # If we are retrying, need to close the workbook before trying to populate
        if close_workbook:
            excel.CutCopyMode = False
            time.sleep(1)
            if excel.ActiveWorkbook:
                excel.ActiveWorkbook.Close(SaveChanges=False)
            time.sleep(5)

        _populate_capiq_for_file(filepath, excel)
        return excel, True
    except (com_error, WorkbookClosedException, CapitalIQInactiveException) as e:
        print(f'Error {e} populating {filepath}. Will wait 30 seconds, restart Excel, and try again.')
        traceback.print_tb(sys.exc_info()[2])
        time.sleep(30)
        excel = _restart_excel_with_addins_and_attach()
        return populate_capiq_for_file(filepath, excel, retries_remaining=retries_remaining - 1, close_workbook=True)

def _populate_capiq_for_file(filepath, excel):
    wb = excel.Workbooks.Open(filepath)
    successful = _wait_for_capiq_result(excel)
    _copy_paste_values(excel, wb)
    excel.ActiveWorkbook.Close(SaveChanges=True)
    return successful

def populate_capiq_ids_for_file(filepath, excel):
    wb = excel.Workbooks.Open(filepath)
    successful = _wait_for_capiq_result(excel)
    _copy_paste_values(excel, wb, range='A1:H3000')
    excel.ActiveWorkbook.Close(SaveChanges=True)
    return successful

def _copy_paste_values(excel, wb, range='A1:ZZ20000'):
    ws = wb.Sheets('Sheet')
    ws.Range(range).Copy()
    ws.Range(range.split(':')[0]).PasteSpecial(Paste=constants.xlPasteValues, Operation=constants.xlNone)
    excel.CutCopyMode = False