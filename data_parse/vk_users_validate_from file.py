import requests
from auth_data import access_token
import csv
import time
import os


def create_list_from_csv(name): # Читаем csv файл и добавляем построчно в лист
    lst = list()
    with open(f'{name}.csv', mode='r') as f:
        reader = csv.reader(f)
        for row in reader:
            lst.append(row[0][17:])
        return lst


def validate_user(id:int) -> bool: # Проверяем страницы на доступность к парсингу данных
    while True:
        response = requests.get(get_url("users.get"), params=get_user_params(id))
        print(response.text)
        if "error" not in response.text:
            if not response.json()["response"][0]["is_closed"] and "deactivated" not in response.text and "удален" not in response.text.lower():
                return True
            else:
                return False
        time.sleep(1.5)


def write_in(id:int,file_name:str): # Записываем id пользователя в csv файл
    with open(f"{file_name}.csv",'a', newline="", encoding='utf-8') as f:
        writer = csv.writer(f)
        url = f"https://vk.com/id{id}"
        writer.writerow([url])


def get_user_params(user_id:str) -> dict: # Получаем параметры запроса
    parameters={
           "user_id": {user_id},
           'access_token': access_token,
           'v': "5.131"
            }
    return parameters


def get_url(method:str) -> str: # Создаем ссылку с указанным методом
    url = f"https://api.vk.com/method/{method}"
    return url


def check_uniq(id:int,file_name:str) -> bool: # Проверяем наличие id пользователя в csv файле
    with open(f"{file_name}.csv",'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if str(id) in row[0]:
                return False
        write_in(id,file_name)
        return True


def get_csv(lst:list,file_name:str): # Проверка на существование файла и на наличие в нем id пользователя
    if not os.path.exists(f"{file_name}.csv"):
        open(f"{file_name}.csv", 'w', newline="", encoding='utf-8')
    for id in lst:
        check_uniq(id,file_name)


def get_validated_list(lst:list) -> list:
    users = []
    for id in lst:
        if validate_user(id):
            users.append(id)
        time.sleep(2)
    return users


ids = create_list_from_csv()
v_ids = get_validated_list(ids)
get_csv(v_ids,"validated_data_scientists")

