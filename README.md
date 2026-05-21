# SPA Salon API

<p align="center">
  <img src="assets/SPA.png" alt="SPA Salon API" width="120">
</p>

<h3 align="center">REST API для SPA-салона на FastAPI</h3>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-blue?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/Swagger-OpenAPI-85EA2D?logo=swagger&logoColor=black" alt="Swagger">
  <img src="https://img.shields.io/badge/Yandex-OAuth-red" alt="Yandex OAuth">
</p>

---

## Описание

**SPA Salon API** — учебный проект по веб-программированию.
Проект представляет собой backend API для SPA-салона.

В лабораторной работе реализованы:

* регистрация пользователя;
* вход пользователя;
* выход из системы;
* получение текущего пользователя;
* просмотр списка пользователей;
* авторизация через Яндекс ID;
* Swagger-документация;
* проверка API через браузер.

Проект не является обычным сайтом с визуальным интерфейсом.
Это серверная часть приложения, которую можно тестировать через Swagger UI.

---

## Содержание

* [Технологии](#технологии)
* [Функциональность](#функциональность)
* [Структура проекта](#структура-проекта)
* [Установка и запуск](#установка-и-запуск)
* [Настройка .env](#настройка-env)
* [Swagger](#swagger)
* [Эндпоинты API](#эндпоинты-api)
* [Авторизация через Яндекс](#авторизация-через-яндекс)
* [Повторный запуск](#повторный-запуск)
* [Возможные ошибки](#возможные-ошибки)

---

## Технологии

В проекте используются:

* **Python** — язык программирования;
* **FastAPI** — backend-фреймворк;
* **Uvicorn** — ASGI-сервер для запуска приложения;
* **Swagger / OpenAPI** — автоматическая документация API;
* **Pydantic** — проверка входных данных;
* **httpx** — HTTP-клиент для обращения к Яндекс OAuth;
* **JSON** — формат обмена данными;
* **Yandex OAuth** — вход через аккаунт Яндекса.

---

## Функциональность

В текущей версии доступны следующие возможности:

| Возможность                     | Статус |
| ------------------------------- | ------ |
| Проверка работы сервера         | Готово |
| Регистрация пользователя        | Готово |
| Вход по email и паролю          | Готово |
| Выход из системы                | Готово |
| Получение текущего пользователя | Готово |
| Получение списка пользователей  | Готово |
| Вход через Яндекс ID            | Готово |
| Swagger-документация            | Готово |

---

## Структура проекта

```text
lab3/
│
├── app/
│   ├── main.py              # основной файл приложения
│   ├── core/
│   │   └── config.py        # настройки проекта
│   ├── models/              # модели данных
│   ├── schemas/             # схемы Pydantic
│   ├── services/            # сервисная логика
│   └── database/            # файлы для работы с БД
│
├── assets/
│   └── icon.png             # иконка проекта
│
├── requirements.txt         # зависимости проекта
├── .env                     # локальные переменные окружения
├── .env.example             # пример переменных окружения
├── .gitignore               # исключения для Git
├── docker-compose.yml       # конфигурация Docker/PostgreSQL
└── README.md                # описание проекта
```

---

## Установка и запуск

### 1. Перейти в папку проекта

```bash
cd lab3
```

### 2. Создать виртуальное окружение

```bash
python -m venv venv
```

### 3. Активировать виртуальное окружение

Для Windows:

```bash
venv\Scripts\activate
```

После активации в терминале должно появиться:

```text
(venv)
```

### 4. Обновить pip

```bash
python.exe -m pip install --upgrade pip setuptools wheel
```

### 5. Установить зависимости

```bash
pip install -r requirements.txt
```

### 6. Запустить сервер

```bash
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

После запуска сервер будет доступен по адресу:

```text
http://127.0.0.1:8000
```

---

## Настройка `.env`

Файл `.env` хранит настройки проекта.

Пример:

```env
DB_USER=postgres
DB_PASSWORD=postgres
DB_NAME=spa_db
DB_HOST=localhost
DB_PORT=5432

ENVIRONMENT=development

JWT_ACCESS_SECRET=super_secret_access_key_change_in_prod
JWT_REFRESH_SECRET=super_secret_refresh_key_change_in_prod
JWT_ACCESS_EXPIRATION=15
JWT_REFRESH_EXPIRATION=10080

SESSION_SECRET=your_session_secret_key_here

YANDEX_CLIENT_ID=your_yandex_client_id
YANDEX_CLIENT_SECRET=your_yandex_client_secret
YANDEX_REDIRECT_URI=http://localhost:8000/api/v1/auth/oauth/yandex/callback
```

Файл `.env` нельзя загружать на GitHub, потому что в нём находятся секретные данные.

В `.gitignore` должна быть строка:

```gitignore
.env
```

---

## Swagger

Swagger UI доступен по адресу:

```text
http://127.0.0.1:8000/api/docs
```

Swagger нужен для тестирования API прямо из браузера.

Через Swagger можно:

* посмотреть список всех эндпоинтов;
* увидеть формат запроса;
* отправить JSON-данные;
* получить ответ сервера;
* проверить регистрацию, вход и выход.

---

## Эндпоинты API

| Метод  | URL                                  | Описание                        |
| ------ | ------------------------------------ | ------------------------------- |
| `GET`  | `/`                                  | Главная информация о приложении |
| `GET`  | `/health`                            | Проверка работы сервера         |
| `POST` | `/api/v1/auth/register`              | Регистрация пользователя        |
| `POST` | `/api/v1/auth/login`                 | Вход пользователя               |
| `POST` | `/api/v1/auth/logout`                | Выход пользователя              |
| `GET`  | `/api/v1/auth/me`                    | Получение текущего пользователя |
| `GET`  | `/api/v1/users/`                     | Список пользователей            |
| `GET`  | `/api/v1/auth/oauth/yandex`          | Начало входа через Яндекс       |
| `GET`  | `/api/v1/auth/oauth/yandex/callback` | Callback от Яндекса             |

---

## Примеры запросов

### Проверка сервера

```http
GET /health
```

Пример ответа:

```json
{
  "status": "ok"
}
```

---

### Регистрация пользователя

```http
POST /api/v1/auth/register
```

Тело запроса:

```json
{
  "email": "user@example.com",
  "password": "password123",
  "full_name": "Иван Петров"
}
```

Пример ответа:

```json
{
  "message": "User user@example.com registered successfully"
}
```

---

### Вход пользователя

```http
POST /api/v1/auth/login
```

Тело запроса:

```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

Пример ответа:

```json
{
  "message": "Login successful"
}
```

---

### Получение текущего пользователя

```http
GET /api/v1/auth/me
```

Пример ответа:

```json
{
  "email": "user@example.com",
  "full_name": "Иван Петров",
  "auth_provider": "local"
}
```

---

### Получение списка пользователей

```http
GET /api/v1/users/
```

Пример ответа:

```json
[
  {
    "email": "user@example.com",
    "full_name": "Иван Петров",
    "auth_provider": "local",
    "yandex_id": null
  }
]
```

---

### Выход из системы

```http
POST /api/v1/auth/logout
```

Пример ответа:

```json
{
  "message": "Logout successful"
}
```

---

## Авторизация через Яндекс

Для входа через Яндекс используется OAuth.

Порядок работы:

1. Пользователь открывает адрес входа через Яндекс.
2. Приложение перенаправляет пользователя на страницу Яндекса.
3. Пользователь входит в аккаунт Яндекса.
4. Яндекс возвращает пользователя обратно в приложение.
5. Приложение получает данные пользователя.
6. Пользователь добавляется во временное хранилище.
7. Пользователь считается авторизованным.

Адрес для запуска входа через Яндекс:

```text
http://localhost:8000/api/v1/auth/oauth/yandex
```

Важно: вход через Яндекс лучше запускать именно из адресной строки браузера, а не через кнопку `Execute` в Swagger.
Swagger может показать ошибку `Failed to fetch`, потому что OAuth использует перенаправление на внешний сайт.

После успешного входа через Яндекс можно проверить список пользователей:

```http
GET /api/v1/users/
```

В списке должен появиться пользователь с полем:

```json
"auth_provider": "yandex"
```

---

## Повторный запуск

Если компьютер был выключен, заново устанавливать зависимости не нужно.

Достаточно выполнить:

```bash
cd lab3
venv\Scripts\activate
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Затем открыть:

```text
http://127.0.0.1:8000/api/docs
```

---

## Запуск на другом компьютере

Для запуска проекта на другом компьютере:

1. Скачать или скопировать проект.
2. Установить Python.
3. Перейти в папку проекта.
4. Создать виртуальное окружение.
5. Установить зависимости.
6. Создать `.env`.
7. Запустить сервер.

Команды:

```bash
cd lab3
python -m venv venv
venv\Scripts\activate
python.exe -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

---

## Возможные ошибки

### `uvicorn` не найден

Ошибка:

```text
uvicorn is not recognized
```

Решение:

```bash
venv\Scripts\activate
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

---

### Ошибка кодировки `.env`

Ошибка:

```text
UnicodeDecodeError: 'utf-8' codec can't decode byte
```

Причина: файл `.env` сохранён не в UTF-8.

Решение:

1. Открыть `.env` в Notepad++.
2. Выбрать `Кодировки`.
3. Нажать `Преобразовать в UTF-8`.
4. Сохранить файл.
5. Перезапустить сервер.

---

### Ошибка `YANDEX_CLIENT_ID is not configured`

Причина: в `.env` не указан `YANDEX_CLIENT_ID`.

Решение: заполнить данные приложения Яндекса:

```env
YANDEX_CLIENT_ID=your_yandex_client_id
YANDEX_CLIENT_SECRET=your_yandex_client_secret
YANDEX_REDIRECT_URI=http://localhost:8000/api/v1/auth/oauth/yandex/callback
```

---

### Ошибка `redirect_uri mismatch`

Причина: callback URL в настройках Яндекса не совпадает с `.env`.

В Яндексе и в `.env` должно быть одинаково:

```text
http://localhost:8000/api/v1/auth/oauth/yandex/callback
```

---

### Ошибка с `psycopg2`

Если при установке зависимостей появляется ошибка:

```text
Error: pg_config executable not found
```

или:

```text
Failed to build psycopg2-binary
```

Для текущей демонстрационной версии можно удалить из `requirements.txt` строку:

```txt
psycopg2
```

или:

```txt
psycopg2-binary
```

После этого повторить установку:

```bash
pip install -r requirements.txt
```

---

## Особенности текущей версии

Текущая версия является учебной.

Особенности:

* пользователи хранятся во временной памяти приложения;
* после перезапуска сервера пользователи очищаются;
* PostgreSQL подготовлен в структуре проекта, но в текущей версии напрямую не используется;
* авторизация реализована в демонстрационном виде;
* Swagger используется как основной способ проверки API.

В полноценном приложении нужно доработать:

* хранение пользователей в базе данных;
* хеширование паролей;
* скрытие паролей из ответов API;
* полноценную JWT-авторизацию;
* защиту приватных эндпоинтов;
* хранение токенов в HttpOnly cookies.

https://habr.com/ru/articles/649363/ "Оформляем README-файл профиля на GitHub / Хабр"
