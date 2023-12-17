from catboost import CatBoostClassifier
import pandas as pd


def model_predict(id):
    # Загрузка обученной модели
    model = CatBoostClassifier()
    model.load_model('model/catboost_model.cbm')

    # Подготовка данных для предсказания
    data = f'all_users_data/{id}_matrix.csv'
    data_1 = pd.read_csv(data)

    # Предсказание значений
    predictions = model.predict(data_1)
    return predictions