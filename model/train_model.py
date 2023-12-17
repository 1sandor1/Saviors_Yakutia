import pandas as pd

data = 'key_matrix.csv'
data_1 = pd.read_csv(data)
print(data_1.head())
##

##
import os
from sklearn.model_selection import train_test_split
from catboost import CatBoostClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix


def train_and_save_model(data_path, model_save_path='catboost_model'):
    # Загрузка данных
    data_1 = pd.read_csv(data_path)


    # Разделение данных на признаки и целевую переменную
    X = data_1.drop('Профессия', axis=1)
    y = data_1['Профессия']

    # Разделение данных на обучающий и тестовый наборы
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    print(X)
    print(X_train)
    print(X_test)

    # Создание и обучение модели CatBoost
    model = CatBoostClassifier(iterations=1000000, depth=5, learning_rate=0.1, loss_function='MultiClass')
    model.fit(X_train, y_train, eval_set=(X_test, y_test), early_stopping_rounds=1500, verbose=100)

    # Сохранение модели в файл в папке проекта
    project_dir = os.path.dirname(os.path.abspath(__file__))
    model_save_path = os.path.join(project_dir, model_save_path + '.cbm')
    model.save_model(model_save_path)

    # Предсказание на тестовом наборе
    y_pred = model.predict(X_test)

    # Оценка модели
    accuracy = accuracy_score(y_test, y_pred)
    conf_matrix = confusion_matrix(y_test, y_pred)
    class_report = classification_report(y_test, y_pred)

    # Вывод результатов
    print(f'Accuracy: {accuracy:.4f}\n')
    print('Confusion Matrix:\n', conf_matrix)
    print('\nClassification Report:\n', class_report)

# Пример вызова функции с указанием пути к файлу данных
train_and_save_model('key_matrix.csv', 'catboost_model')
##
