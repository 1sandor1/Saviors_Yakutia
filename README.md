# Прототип веб-сервиса для профориентации молодежи от команды SAVIORS
## Описание проекта:
Сайт, на котором пользователь регистрируется и указывает ссылку на интересующую его **страницу в VK** \
                                                        (она должна быть **открытой**) \
С неё собираются данные о всех подписках, сообществах, посещенных мероприятиях. \
Вслед за этим они анализуруются: формируется матрица ключевых слова в формате csv (path: /all_users_data/{user_id}_matrix.csv).\
Матрица загружается в обученную модель, которая предсказывает пользователю рекомендуемую профессию
В зависимости от профессии, подгружается траектория обучения пользователя:
1. ВУЗ
2. Колледж ( при наличии)
3. Образовательный курс номер 1 
4. Образовательный курс номер 2\

Курсы подбирались с возможностью бесплатного прохождения или ознокомления.

## Как запустить проект?

Вам необходимо открыть файл **saviors_site.py** и перейти по ссылке, указанной в консоли

## Какие файлы содержатся в проекте? 

**Директории:**
1. all_users_data  - хранилище матриц ключевых слов по каждому пользователю
2. data_parse - инструменты для парсинга данных с исползование API VK
3. each_profession_data - обучающая выборка пользователей по каждой профессии 
4. groups_data - перечень репрезентативных групп по каждой из представленных профессий
5. instance - база данных пользователей (логины, пароли, информация о себе и т.д.)
6. model - модель и её обучение
7. static и templates - css и html файлы

## Особенности создания и обучения модели

Обучающая выборка - пользователи 3х и более групп, соответствующей тематики\
Ключевые слова - часто встречающиеся слова из названий групп, название приложений и профильные термины\
Модель создана с использованием библиотеки CatBoost, является мультирегрессионной моделью классификаци\
с использованием градиентного бустинга на деревьях решений

## Возможности для роста

1. Добавление входа через социальные сети
2. Увеличение количества ключевых слова благодаря токенизации названий сообществ по частям и отслеживание наиболее репрезентативных
3. Расширение датасета
4. Добавление статистики пользователей сайта ( % пользователей, которым рекомендована та же профессия)