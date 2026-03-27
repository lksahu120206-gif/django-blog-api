# Django Blog API & Web App

Full-stack blog application with REST API and web interface.

Live Demo: https://django-blog-api-q037.onrender.com/api/posts/

## Features

* Blog CRUD with authentication
* Comments with moderation
* REST API (posts, comments)
* JWT token auth
* Like/dislike voting
* Pagination and tagging
* Render deployment

## Tech Stack

* Django 6.0
* Django REST Framework
* PostgreSQL (prod) / SQLite (dev)
* JWT Authentication

## API Endpoints

* `GET/POST /api/posts/` - List/create posts
* `GET/PUT/DELETE /api/posts/<id>/` - Post detail
* `POST /api/token/` - Get JWT token

## Installation

```
git clone https://github.com/your-username/django-blog-api.git
cd django-blog-api
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Author

Lalit Kishor Sahu  
[GitHub](https://github.com/lksahu120206-gif)

