# Foodgram project

##  Информация для ревьювера
IP сервера - 158.160.35.92
Доменое имя - foodgramservice.ddns.net
Почта суперпользователя - test357@gmail.com
Логин - test
Пароль - Triumvirat357!

##  Статусы обновления ветки через Git Actions
![example branch parameter](https://github.com/msk357/foodgram-project-react/actions/workflows/main.yml/badge.svg?branch=master)


## Описание проекта:
Проект основан на базе общедоступных и безопасных фреймворков "django-rest-framework" и "Django".
Основная задача проекта, это публикация рецептов разных блюд на площадке Foodgram, с возможностью подписки на любимых авторов и рецепты. Проект использует формат SPA, для функционирования проекта backend часть разработана на базе фреймворка Django. В backend описаны API для запросов от frontend-части, написанной на базе React и JavaScript.

Проект основан на технологиях:
- Django rest framework 3.12.4
- Django 2.2.16
- GitActions
- Nginx
- Python 3.10
- PostgreSQL
- Docker

Сервис API описан для следующих приложений:
- Users - модель c пользователями и подписками на авторов.
- Recipe - модель с рецептами блюд и возможность добавления рецептов в корзину или избранное.


## Запуск проекта:
Клонировать репозиторий и перейти в него в командной строке:
```
git clone https://github.com/yandex-praktikum/foodgram-project-react.git
```
Провести установку Docker:
```
sudo apt install docker.io
```
Перейти в папку infra и подготовить среду для запуска контейнера:
```
cd infra
```
```
sudo nano .env
```
Внести имзенения в файл .env:
```
DEBUG=False
SECRET_KEY=<Your_key>
ALLOWED_HOSTS=<Your_host>
CSRF_TRUSTED_ORIGINS=https://<Your_host>
DB_ENGINE='django.db.backends.postgresql'
DB_NAME='postgres'
POSTGRES_USER='postgres'
POSTGRES_PASSWORD=<Your_password>
DB_HOST='db'
DB_PORT=5432
```
Запустить контейнер Docker:
```
docker-compose up -d --build
```