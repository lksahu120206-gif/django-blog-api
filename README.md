# Blog API (Django REST Framework)

A backend API for a blog application built using Django and Django REST Framework.
The project supports user authentication, post management, comments, and permission-based access control.

---

## Features

* User authentication (session-based)
* Create, read, update, delete posts
* Comment system linked to posts
* Author-based permissions
* Only content owners can edit or delete their data
* Nested API structure (posts and comments)

---

## Tech Stack

* Python
* Django
* Django REST Framework
* SQLite

---

## API Endpoints

### Posts

* GET `/api/posts/` — List all posts
* POST `/api/posts/` — Create a post
* GET `/api/posts/<id>/` — Retrieve a post
* PUT `/api/posts/<id>/` — Update a post
* DELETE `/api/posts/<id>/` — Delete a post

---

### Comments

* GET `/api/posts/<post_id>/comments/` — List comments for a post
* POST `/api/posts/<post_id>/comments/` — Create a comment
* GET `/api/comments/<id>/` — Retrieve a comment
* PUT `/api/comments/<id>/` — Update a comment
* DELETE `/api/comments/<id>/` — Delete a comment

---

## Authentication

Login is required for creating, updating, and deleting content.

Login URL:

```
/api-auth/login/
```

---

## Setup Instructions

1. Clone the repository

```
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

2. Create a virtual environment

```
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies

```
pip install -r requirements.txt
```

4. Apply migrations

```
python manage.py makemigrations
python manage.py migrate
```

5. Create a superuser

```
python manage.py createsuperuser
```

6. Run the server

```
python manage.py runserver
```

---

## Testing

* Use the browser (Django REST Framework UI) or Postman
* Log in before performing POST, PUT, or DELETE operations

---

## Sample Response

```
{
  "id": 1,
  "title": "My First Post",
  "content": "Hello World",
  "author": 1,
  "comments": [
    {
      "id": 1,
      "content": "Nice post",
      "author": 1
    }
  ]
}
```

---

## Learning Outcomes

* Built REST APIs using Django REST Framework
* Implemented authentication and permissions
* Designed relational models (Post and Comment)
* Created nested API endpoints

---

## Future Improvements

* Like system
* JWT authentication
* Pagination and search
* Deployment

---

## Author

Lalit Kishor Sahu
GitHub: https://github.com/lksahu120206-gif
LinkedIn: https://linkedin.com/in/lalit-kishor-sahu-b137a0352
