import xlsxwriter
import os
from pathlib import Path

from psd_tools import PSDImage

from src.psdtools import list_of_psd_layers, list_of_modules, get_mobile_artboard
from src.helpers import (
    psd_filename
)

modules_dict = {
    "1COL_A_Scale_850_M": "1",
    "1COL_C_Scale_780_M": "1",
    "1COL_E_Scale_780_M": "1",
    "1COL_G_Scale_670_M": "1",
    "1COL_B_Swap_850_M": "1",
    "1COL_D_Swap_780_M": "1",
    "1COL_F_Swap_780_M": "1",
    "1COL_H_Swap_670_M": "1",
    "2COL_OFFSET_A_Scale_850_M": "2",
    "2COL_OFFSET_B_Scale_850_M": "2",
    "2COL_OFFSET_C_Scale_780_M": "2",
    "2COL_OFFSET_D_Scale_780_M": "2",
    "2COL_OFFSET_E_Scale_670_M": "2",
    "2COL_OFFSET_F_Scale_670_M": "2",
    "2COL_OFFSET_G_Scale_850_M": "2",
    "2COL_OFFSET_H_Scale_850_M": "2",
    "2COL_A_Scale_425_M": "2",
    "2COL_D_Scale_380_M": "2",
    "2COL_E_Scale_415_M": "2",
    "2COL_G_Scale_380_M": "2",
    "2COL_H_Scale_415_M": "2",
    "2COL_K_Scale_380_M": "2",
    "2COL_L_Scale_415_M": "2",
    "2COL_N_Scale_325_M": "2",
    "TEXT_2COL_A_780_M": "4",
    "TEXT_2COL_B_780_M": "4",
    "TEXT_2COL_C_780_M": "4",
    "TEXT_2COL_D_Offset_M": "4",
    "TEXT_2COL_E_Offset_M": "4",
    "TEXT_2COL_F_Scale_380_M": "4",
    "2COL_B_Wrap_850_M": "2",
    "2COL_C_Wrap_Switch_850_M": "2",
    "2COL_F_Wrap_780_M": "2",
    "2COL_I_Wrap_780_M": "2",
    "2COL_J_Wrap_670_M": "2",
    "2COL_M_Wrap_670_M": "2",
    "2COL_WRAP_SWAP": "2",
    "3COL_A_Scale_246_M": "3",
    "3COL_Wrap_A_780_M": "3",
    "BUTTONS_01_M": "1",
    "BUTTONS_01_M_VML": "1",
    "BUTTONS_02_Long_M": "2",
    "BUTTONS_02_Long_M_VML": "2",
    "BUTTONS_02_Short_M": "2",
    "BUTTONS_02_Short_M_VML": "2",
    "BUTTONS_03_M": "3",
    "BUTTONS_03_M_VML": "3",
    "BUTTONS_04_M": "4",
    "BUTTONS_04_M_VML": "4",
    "BUTTON_01": "1",
    "BUTTON_02": "2",
    "BUTTON_03": "3",
    "BUTTON_04": "4",
    "COMPONENT_01": "1",
    "COMPONENT_02": "1",
    "HERO_K_2COL_850_M": "2",
    "HERO_L_2COL_780_M": "2",
    "HERO_C_Bottom_SCALE_850_M": "1",
    "HERO_F_SCALE_Bottom_780_M": "1",
    "HERO_A_Top_850_M": "1",
    "HERO_B_Middle_850_M": "1",
    "HERO_C_Bottom_850_M": "1",
    "HERO_D_Top_780_M": "1",
    "HERO_E_Middle_780_M": "1",
    "HERO_F_Bottom_780_M": "1",
    "HERO_G_BUTTONS_850_M": "2",
    "HERO_H_BUTTONS_780_M": "2",
    "HERO_I_BUTTONS_850_M": "4",
    "HERO_J_BUTTONS_780_M": "4",
    "SPLIT_Scale_A_380_M": "3",
    "SPLIT_Scale_C_380_M": "3",
    "SPLIT_Scale_E_380_M": "3",
    "SPLIT_Scale_G_380_M": "3",
    "doesnotmatchpsd_TEXT_SPLIT_E_780_M": "3",
    "TEXT_SPLIT_A_850_M": "3",
    "TEXT_SPLIT_B_850_M": "3",
    "TEXT_SPLIT_C_850_M": "3",
    "TEXT_SPLIT_D_850_M": "3",
    "TEXT_SPLIT_F_780_M": "3",
    "TEXT_SPLIT_G_780_M": "3",
    "TEXT_SPLIT_H_780_M": "3",
    "SPLIT_Wrap_B_780_M": "3",
    "SPLIT_Wrap_D_780_M": "3",
    "SPLIT_Wrap_F_780_M": "3",
    "SPLIT_Wrap_H_780_M": "3",
    "TEXT_01": "1",
    "TEXT_02": "1",
    "TEXT_03": "1",
    "TEXT_04": "1",
    "TEXT_05": "1",
    "TEXT_06": "1",
    "TEXT_07": "1",
    "TEXT_08": "1",
}

def create_xlsx(modules):
    loc = Path(user_directory).joinpath(WORKBOOK)
    wb = xlsxwriter.Workbook(loc)
    ws = wb.add_worksheet()

    merge_format = wb.add_format({
        'bold':     True,
        'border':   6,
        'align':    'center',
        'valign':   'vcenter',
        'fg_color': '#D7E4BC',
    })
    blank_format = wb.add_format({'bg_color': '#404040'})
    cell_width = wb.add_format()
    cell_width.set_shrink()

    ws.set_column(0, 0, 25)
    ws.set_column(1, 1, 40)
    ws.set_column(2, 2, 40)
    ws.set_column(3, 3, 40)
    ws.set_column(4, 4, 40)

    ws.write('A1', 'Module')
    ws.write('B1', 'URL 1')
    ws.write('C1', 'URL 2')
    ws.write('D1', 'URL 3')
    ws.write('E1', 'URL 4')

    counter = 0
    for name in modules:
        counter += 1
        row = counter
        links = match_module_value(name, modules_dict)
        line = row + 1
        if links == '1':
            ws.merge_range(f'C{line}:E{line}', '', blank_format)
        if links == '2':
            ws.merge_range(f'D{line}:E{line}', '', blank_format)
        if links == '3':
            ws.write(f'E{line}', None, blank_format)
        ws.write(row, 0, name)
    wb.close()

def match_module_value(name, modules_dict):
    for key, value in modules_dict.items():
        if name.strip() == key.strip():
            return value

def modules_names(layers):
    lst = []
    for i in layers:
        lst.append(i.name)
    return lst

if __name__ == "__main__":
    WORKBOOK = 'modules.xlsx'

    # user_directory = Path("C:\\Users\\Rory.Ferguson\\test")
    user_directory = input('PSD path:')

    psd = psd_filename(
        user_directory, message="PSD name (can be blank or without file extension):"
    )

    print(f"\nLoading {psd}")
    psd_load = PSDImage.open(Path(user_directory).joinpath(psd))
    print(f"Finished loading {psd}\n")
    print(f"The file {psd} is being parsed.\n")

    artboard = get_mobile_artboard(psd_load)

    layers = list_of_psd_layers(artboard)

    if artboard:
        modules = modules_names(layers)

    create_xlsx(modules)
