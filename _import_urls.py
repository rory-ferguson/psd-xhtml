import xlsxwriter
import os
from pathlib import Path
import json
from pprint import pprint

from config import WORKBOOK, MODULE_DATA

def open_file(path, t):
    with open(path, t) as file:
        return file

if __name__ == "__main__":
    # user_directory = input('PSD path:')
    user_directory = 'C:\\Users\\Rory.Ferguson\\test'

    workbook_path = Path(user_directory).joinpath(WORKBOOK)
    module_path = Path(user_directory).joinpath(MODULE_DATA)

    workbook = open_file(workbook_path, 'r')

    with open(module_path) as f:
        module_data = json.load(f)
    pprint(module_data)