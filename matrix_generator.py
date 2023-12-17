import pandas as pd
import requests
import time

import csv

from auth_data import secure_token, access_token
from prediction import model_predict

def get_user_params(user_id) -> dict: # Получаем параметры запроса для пользователей
    parameters={
           "user_id": {user_id},
           'access_token': access_token,
           'v': "5.131"
            }
    return parameters


def get_user_id(short_name:str) -> str:
    while True:
        response = requests.get(get_url("users.get"), params=get_user_params(short_name))
        if "error" not in response.text:
            if not response.json()["response"][0]["is_closed"] and "deactivated" not in response.text and "удален" not in response.text.lower():
                return str(response.json()["response"][0]["id"])
            else:
                return "Страница закрыта или удалена!"
        time.sleep(1.5)


def get_group_params(group_ids:str) -> dict: # Получаем параметры запроса для групп
    parameters={
           "group_ids": {group_ids},
           'access_token': access_token,
           'v': "5.131"
            }
    return parameters


def get_url(method:str) -> str: # Создаем ссылку с указанным методом
    url = f"https://api.vk.com/method/{method}"
    return url


def get_keywords() -> list: # Получаем список с ключевыми словами пользователей
    lst = []
    for i in open('data_parse/keywords.txt', encoding='utf-8'):
        lst.append(i[:-1])
    return lst


def list_convert_int_to_str(lst:list) -> list: # Трансформируем id пользователей из целочисленного типа в строковый
    str_list = []
    for el in lst:
        str_list.append(str(el))
    return str_list[:499]


def times_keyword_in_lst(key:str,lst:list) -> bool: # Находим частоту появления ключевого слова
    cnt = 0
    for sub_name in lst:
        if key.lower() in sub_name.lower():
            cnt += 1
    return cnt


def get_subscriptions_ids_in_str(id:int) -> str: # Формируем одну строку, состоящую из id подписок пользователя
    while True:
        response = requests.get(get_url("groups.get"), params=get_user_params(id))
        if "Too many requests per second" not in response.text and "User was deleted or banned" not in response.text:
            subscriptions_ids = list_convert_int_to_str(response.json()["response"]['items'])
            subscriptions_in_str = ",".join(subscriptions_ids)
            return subscriptions_in_str
        if "User was deleted or banned" in response.text:
            print(f"Пользователь удален! {id}")
        time.sleep(2)


def get_user_subscriptions_names(id:int) -> list: # Получение списка имен подписок пользователя
    while True:
        response = requests.get(get_url("groups.getById"), params=get_group_params(get_subscriptions_ids_in_str(id)))
        if "Too many requests per second" not in response.text:
            if "response" in response.text:
                subscriptions = response.json()["response"]
                subscriptions_names = []
                for el in subscriptions:
                    subscriptions_names.append(el['name'])
                return subscriptions_names
        time.sleep(2)


def prof_predict(id): # Получение предсказанной профессии пользователя
    keywords = get_keywords()
    user_subscriptions_names = get_user_subscriptions_names(id=id)
    final_lst = []
    for keyword in keywords:
            final_lst.append(times_keyword_in_lst(keyword, user_subscriptions_names))
    with open(f'all_users_data/{id}_matrix.csv', mode='w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(keywords)
        writer.writerow(final_lst)
    time.sleep(1)
    return model_predict(id)

if __name__ == "__main__":
    db_professions = pd.read_excel('profession_data.xlsx', sheet_name='Список пользователей')
    keywords = get_keywords()
    for user_lnk in db_professions['Разработчики ИИ'][:]: # Парсинг пользователей по заданной профессии
        user_subscriptions_names = get_user_subscriptions_names(user_lnk[17:])
        start_time = time.time()
        final_lst = ['ML_engineer']
        for keyword in keywords:
                final_lst.append(times_keyword_in_lst(keyword, user_subscriptions_names))

        print(f"Id пользователя: {user_lnk[17:]}")
        with open('data_parse/key_matrix.csv', mode='a', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(final_lst)

    print('Данные собраны!')