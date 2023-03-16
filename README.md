# praktikum_new_diplom

##  Статусы обновления ветки через Git Actions
![example branch parameter](https://github.com/msk357/foodgram-project-react/actions/workflows/foodgram-project-react.yml/badge.svg?branch=master)


## Описание проекта:
Проект основан на базе общедоступных и безопасных фреймворков "django-rest-framework" и "Django".
Основной задачей проекта является настройка работы сервиса API для моделей прототипа социальной сети. В приложении 'API' описана структура API для 4-рех моделей, ниже добавлено их краткое описание. Для безопасного функционирования проекта проведена настройка аутентификации пользователя по средствам JWT-токена. Данный проект позволит вам оперативно развернуть работу сервисов API для своего проекта.

Проект основан на технологиях:
- Django rest framework 3.12.4
- Django 2.2.16
- Djangorestframework-simplejwt 4.7.2
- Docker Hub

Сервис API описан для следующих моделей:
- Reviews - модель c отзывами пользователей сети.
- Users - модель с зарегистрированными пользователями.


## Запуск проекта:
Клонировать репозиторий и перейти в него в командной строке:
```
git clone https://github.com/yandex-praktikum/kittygram2plus.git
```
```
cd yatube_api
```

Cоздать и активировать виртуальное окружение:
```
python3 -m venv venv
```
```
source venv/bin/activate
```
```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:
```
pip install -r requirements.txt
```

Выполнить миграции:
```
python3 manage.py migrate
```

Запустить проект:
```
python3 manage.py runserver
```

Запуск проекта в облачном сервере:
```
После развертывания рабочего простанства и отправки push на ветку master в GitHub, проект будет запушен на облачном сервере Yandex Cloud (IP 158.160.35.92). Дополнительно будет обновлена версия репозитория на DockerHub (пользователь "msk357", проект "infra").
```

## Примеры API запросов:
Get - получить список всех публикаций `/api/v1/posts/`
<pre><code>Response
{
  "count": 123,
  "next": "http://api.example.org/accounts/?offset=400&limit=100",
  "previous": "http://api.example.org/accounts/?offset=200&limit=100",
  "results": [
    {
      "id": 0,
      "author": "string",
      "text": "string",
      "pub_date": "2021-10-14T20:41:29.648Z",
      "image": "string",
      "group": 0
    }
  ]
}</code></pre>


Get - получение всех комментариев к публикации. `/api/v1/posts/{post_id}/comments/`
<pre><code>Response
[
  {
    "id": 0,
    "author": "string",
    "text": "string",
    "created": "2019-08-24T14:15:22Z",
    "post": 0
  }
]</code></pre>


Get - Получение списка доступных сообществ. `/api/v1/groups/`
<pre><code>Response
[
  {
    "id": 0,
    "title": "string",
    "slug": "string",
    "description": "string"
  }
]</code></pre>


Post - добавление новой публикации. `api/v1/posts/`
<pre><code>Request
{
  "text": "string",
  "image": "string",
  "group": 0
}

Response
{
  "id": 0,
  "author": "string",
  "text": "string",
  "pub_date": "2019-08-24T14:15:22Z",
  "image": "string",
  "group": 0
}
</code></pre>