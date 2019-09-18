import time
from ..exceptions import WorkbookClosedException, CapitalIQInactiveException

def _wait_for_capiq_result(excel):
    finished = False
    while not finished:
        time.sleep(1)
        finished = _capiq_is_done(excel)

    return True

def _capiq_is_done(excel):
    if _ciq_not_working(excel):
        raise CapitalIQInactiveException('CapitalIQ Plugin did not properly pull values.')

    return _data_in_a2(excel)

def _ciq_not_working(excel):
    a1 = _get_cell_value_by_index(excel, 1, 1)
    if a1 is None:
        return True  # should always have something in A1
    error_values = ('refresh', 'ciqinactive', 'error')
    return any([value in a1.lower() for value in error_values])


def _data_in_a2(excel):
    a2 = _get_cell_value_by_index(excel, 1, 2)
    return a2 is not None

def _get_cell_value_by_index(excel, x, y):
    try:
        result = excel.ActiveSheet.Cells(1, 2).Value
        return result
    except AttributeError:
        raise WorkbookClosedException('Workbook was not open when trying to populate values.')