import os
import shutil
from pathlib import Path

import pytest

GENERATED_DIR = Path(__file__).parent / 'generated'
ID_DIR = GENERATED_DIR / 'ids'
DATA_FOLDER = GENERATED_DIR / 'process_data'
OUT_DATA_PATH = GENERATED_DIR / 'full data.csv'
IDS_OUT_PATH = GENERATED_DIR / 'full ids.csv'


@pytest.fixture(scope='session', autouse=True)
def set_up_folders_clean_up_at_end():
    for dir in (ID_DIR, DATA_FOLDER):
        if not os.path.exists(dir):
            os.makedirs(dir)

    yield

    shutil.rmtree(GENERATED_DIR)