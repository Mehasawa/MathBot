from webbrowser import Error

import openpyxl
from openpyxl import utils
from PIL import Image as pil_image  # Чтобы не было конфликта имен
import os

output_dir = "C:\\Users\\User\\Downloads\\OUTPUT"  # Папка для сохранения картинок
excel_file = 'C:\\Users\\User\\Downloads\\Банк.xlsx'
workbook = openpyxl.load_workbook(excel_file, data_only=True)

# def poiskImage(sheet,cell):
#     # Получаем номер строки и столбца из координат ячейки
#     col = openpyxl.utils.column_index_from_string(cell[:1])  # Преобразуем букву столбца в индекс
#     row = int(cell[1:])  # извлекаем номер строки
#     try:
#         image_name = f"{sheet.title}_{col}{row}.png"
#         image_path = os.path.join(output_dir, image_name)
#         if hasattr(sheet, '_images'):
#             for drawing in sheet._images:
#                 # Получаем координаты ячейки, к которой прикреплено изображение
#                 anchor = drawing.anchor._from
#                 if anchor.col == col - 1 and anchor.row == row - 1:  # Indexes start at 0
#                     # Получаем саму картинку
#                     image = pil_image.open(drawing.ref)
#                     # Сохраняем картинку как PNG
#                     image.save(image_path, "PNG")
#                     print(f"Изображение сохранено: {image_path}")
#                     return image_path
#     except ValueError:
#         print(ValueError)
#         return  'none'
def poiskImage(sheet,cell):
    col = openpyxl.utils.column_index_from_string(cell[:1])
    row = int(cell[1:])  # извлекаем номер строки
    str = f'{sheet.title}_{col}{row}'
    print(str)
    filepath = os.path.join(output_dir, f"{str}.png")
    if os.path.exists(filepath):
        return filepath
    else:
        return 'none'

def poiskZadachi(lvl,tema,k=1):
    spisok=[]
    sheet = workbook[str(lvl)]
    for one in sheet['E']:
        # print(one)
        if one.value:
            if tema in one.value:
                print(one.row)
                zadacha={'lvl':lvl,'topic':tema,'task':sheet[f'F{one.row}'].value,'image':sheet[f'G{one.row}'],'answer':sheet[f'I{one.row}'].value}
                zadacha['image']=poiskImage(sheet,zadacha['image'].coordinate)
                spisok.append(zadacha)
                print(zadacha)
    return spisok
poiskZadachi(4,'Движение')

def extract_data_and_images(excel_file, output_dir):

    # Создаем папку для сохранения картинок, если ее нет
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Загружаем Excel файл
    workbook = openpyxl.load_workbook(excel_file)

    # Перебираем листы (sheets)
    for sheet_name in workbook.sheetnames:
        sheet = workbook[sheet_name]

        # Перебираем рисунки на листе
        for drawing in sheet._images:
            # Получаем координаты ячейки, где находится картинка
            cell = drawing.anchor._from

            # Формируем имя файла для сохранения картинки
            image_name = f"{sheet.title}_{cell.col+1}{cell.row+1}.png"
            image_path = os.path.join(output_dir, image_name)

            # Получаем саму картинку
            image = pil_image.open(drawing.ref)
            # Сохраняем картинку как PNG
            image.save(image_path, "PNG")

            print(f"Изображение сохранено: {image_path}")

        # Вывод текстовых данных из ячеек
        for row in sheet.iter_rows():
            row_values = [cell.value for cell in row]
            print(row_values)


# Пример использования:
excel_file = "C:\\Users\\User\\Downloads\\Банк.xlsx"  # Замените на путь к вашему Excel-файлу
output_dir = "C:\\Users\\User\\Downloads\\OUTPUT"  # Папка для сохранения картинок

# extract_data_and_images(excel_file, output_dir)

