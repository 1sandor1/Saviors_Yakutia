import csv
import os
import time

import requests

from auth_data import access_token, secure_token


def write_in(id:int,file_name:str): # Записываем id пользователя в csv файл
    with open(f"{file_name}.csv",'a', newline="", encoding='utf-8') as f:
        writer = csv.writer(f)
        url = f"https://vk.com/id{id}"
        writer.writerow([url])


def check_uniq(id:int,file_name:str) -> bool: # Проверяем наличие id пользователя в csv файле
    with open(f"{file_name}.csv",'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if str(id) in row[0]:
                return False
        write_in(id,file_name)
        return True


def get_user_params(user_id:int) -> dict: # Получаем параметры запроса для пользователей
    parameters={
           "user_id": {user_id},
           'access_token': access_token,
           'v': "5.131"
            }
    return parameters


def get_params(group_id:str,offset:int) -> dict: # Получаем параметры запроса для групп
    parameters={
           "group_id": group_id,
           "count": "1000",
            "offset": offset,
           'access_token': secure_token,
           'v': "5.131"
            }
    return parameters


def get_url(method:str) -> str: # Создаем ссылку с указанным методом
    url = f"https://api.vk.com/method/{method}"
    return url


def get_csv(lst:list,file_name:str): # Проверка на существование файла и на наличие в нем id пользователя
    if not os.path.exists(f"{file_name}.csv"):
        open(f"{file_name}.csv", 'w', newline="", encoding='utf-8')
    for id in lst:
        if validate_user(id):
            check_uniq(id,file_name)


def validate_user(id) -> bool: # Проверяем страницы на доступность к парсингу данных
    while True:
        response = requests.get(get_url("users.get"), params=get_user_params(id))
        print(response.text)
        if "error" not in response.text:
            if not response.json()["response"][0]["is_closed"] and "deactivated" not in response.text and "удален" not in response.text.lower():
                return True
            else:
                return False
        time.sleep(1.5)

if __name__ == "__main__":
    for i in range(1,5002,100): # Находим пересечение пользователей в указанных группах

        group_list = ["143581667", "111859812", "180219808"] # id групп, пересечение которых нужно найти
        response_1 = requests.get(get_url("groups.getMembers"),params=get_params(group_list[0],i))
        response_2 = requests.get(get_url("groups.getMembers"),params=get_params(group_list[1],i))
        response_3 = requests.get(get_url("groups.getMembers"),params=get_params(group_list[2],i))

        users_ids_1 = response_1.json()["response"]["items"]
        users_ids_2 = response_2.json()["response"]["items"]
        users_ids_3 = response_3.json()["response"]["items"]

        final_users = list(set(users_ids_3) & set(users_ids_1) & set(users_ids_2))

        print(final_users)
        print(f"Количество подходящих людей: {len(final_users)}")
        get_csv(final_users[:],"tech_engineers")

        time.sleep(2)