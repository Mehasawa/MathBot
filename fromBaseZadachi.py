import random

import openpyxl
from openpyxl import utils
from PIL import Image as pil_image  # Чтобы не было конфликта имен
import os

output_dir = "C:\\Users\\User\\Downloads\\OUTPUT"  # Папка для сохранения картинок
excel_file = 'C:\\Users\\User\\Downloads\\Telegram Desktop\\bank4.xlsx'
workbook = openpyxl.load_workbook(excel_file, data_only=True)

def poiskImage(sheet,cell):
    col = openpyxl.utils.column_index_from_string(cell[:1])
    row = int(cell[1:])  # извлекаем номер строки
    str = f'{sheet.title}_{col}{row}'
    # print(str)
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
                # print(one.row)
                zadacha={'lvl':lvl,'topic':tema,'task':sheet[f'F{one.row}'].value,'image':sheet[f'G{one.row}'],'answer':sheet[f'I{one.row}'].value}
                zadacha['image']=poiskImage(sheet,zadacha['image'].coordinate)
                spisok.append(zadacha)
                # print(zadacha)
    return spisok

def task_level(message, user_data):#собирает инфу
    user_id=message.from_user.id
    tema = user_data[user_id]['third_choice'][1:]
    lvl =  int(user_data[user_id]['second_choice'][-1])
    rezhim = user_data[user_id]['first_choice']
    print(tema,lvl)
    return tema,lvl,rezhim


def taskcount(message,user_data):#цикл задач
    user_id = message.from_user.id
    tema,lvl,rezhim = task_level(message,user_data)#############
    spisok = poiskZadachi(lvl,tema)#список задач на тему (долго)
    sp = random.choice(spisok)
    problem, answer, image = sp['task'], sp['answer'], sp['image']
    while problem in user_data[user_id]['list']:
        sp=random.choice(spisok)
        problem, answer, image = sp['task'],sp['answer'],sp['image']
    print(problem,answer,image)
    return problem,answer, image