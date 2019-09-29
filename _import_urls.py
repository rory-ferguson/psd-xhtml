import xlsxwriter
import os
from pathlib import Path
import json
from pprint import pprint
import pandas as pd

from src.helpers import json_dump, load_json
from config import WORKBOOK, MODULE_DATA

def load_excel_as_dict(path):
    xlsx = pd.ExcelFile(path)
    df = pd.read_excel(xlsx)
    df = df.where(pd.notnull(df), None)
    return df.to_dict('index')

def get_workbook_urls(url_dict, index, name):
    urls = dict()
    copy = url_dict[int(index)].copy()
    copy.pop('Module', None)
    urls['URL'] = copy
    return urls

def collate(url_dict, module_data):
    for k, v in module_data.items():
        v.update(get_workbook_urls(url_dict, k, v['Module']))
    return module_data


if __name__ == "__main__":
    # user_directory = input('PSD path:')
    user_directory = 'C:\\Users\\Rory.Ferguson\\test'

    workbook_path = Path(user_directory).joinpath(WORKBOOK)
    module_path = Path(user_directory).joinpath(MODULE_DATA)

    url_dict = load_excel_as_dict(workbook_path)  

    module_data = load_json(module_path)

    data = collate(url_dict, module_data)
    json_dump(module_path, data, 'w')
