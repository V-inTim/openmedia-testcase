# Тестовое задание "Сервис парсинга страниц"

Написано api трех запросов.\
Вид запросов и ответов соответствует условию.\
DRF не использовал, в условиях не прописано, да и надобности как таковой не было.

## Используемые технологии
Django, Postgres

## Запуск программы с помощью django

1. Установить виртуальное окружение
```
python -m venv venv
venv/Scripts/activate
```

2. Установить зависимости
```
pip install -r requirements.txt
```

3. Создайте .env-файл в корне проекта
- **DATABASE_URL**=postgres://myuser:mypass@localhost:5433/test_db (url подключения к базе)
- **DEBUG**=True
- **SECRET_KEY**=secret_key - секретный ключ Django, сгенерируйте (например просто secret_key)
- **ALLOWED_HOSTS**=localhost,127.0.0.1

4. Проект работает с postgres.
БД можно или создать, или запустить в docker-compose (файл в проект добавлен)
```
docker-compose up -d
```

5. Примените миграции к базе и запустите сервер
```
python manage.py migrate
python manage.py runserver
```
## API
Запрос на парсинг и сохранение страницы
GET http://localhost:8000/page/create \
**Запрос:**
```json
{
    "url": "url"
}
```
**Ответ:**
```json
// 201
{
    "id": "4"
}
```
Запрос на получение страницы
POST http://localhost:8000/page/ **int:pk** \
**Ответ:**
```json
// 200
{
    "h1": 1,
    "h2": 2,
    "h3": 3,
    "a": ["link"]
}
```
Запрос на получение страницы
POST http://localhost:8000/page/list&order=h1 \
**Ответ:**
```json
// 200
[
    {
        "h1": 1,
        "h2": 2,
        "h3": 3,
        "a": ["link"]
    }
]
```

## Дополнительно 
- Код написан с flake8 (конфигурация прописана в setup.cfg)
- Переменные перенесены в .env из соображений безопасности
- Добавлен workflow git actions для запуска тестов и проверки code style по flake8
- Добавлены тесты