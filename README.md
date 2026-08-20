# 🎬 Movie Watchlist (Django + PostgreSQL)

A server-rendered web application for keeping a personal movie watchlist, built
for **Full Stack Application Development (AST02.04 · FSAD 2026), Assignment 1**.

It demonstrates the core Django concepts covered in class: project/app structure,
the **MTV** pattern, models & the ORM, migrations, function-based views, URL
routing, `ModelForm`s, templates, the Django Admin, and a **PostgreSQL** backend.

---

## Features

| Requirement | Implemented |
|---|---|
| Homepage listing all movies | ✅ `movie_list` view |
| Movies ordered **newest first** | ✅ `Meta.ordering = ["-date_added"]` |
| Add a new movie | ✅ `movie_create` |
| Edit an existing movie | ✅ `movie_update` |
| Delete a movie (with confirmation) | ✅ `movie_delete` |
| Mark Watched / Unwatched | ✅ `movie_toggle_watched` |
| Search by title | ✅ `?q=` filter (`title__icontains`) |
| Registered in Django Admin | ✅ `MovieAdmin` |
| PostgreSQL + Django ORM | ✅ |
| CRUD functionality | ✅ |
| Bootstrap UI | ✅ (via CDN) |

### Movie model fields
- **Title** — required (`CharField`)
- **Genre** — optional
- **Release Year** — optional, validated 1888–2100
- **Personal Rating** — optional, validated 1–5
- **Watched** — Boolean (default `False`)
- **Date Added** — automatic (`auto_now_add`)

---

## Tech stack
- Python 3.13
- Django 6.0
- PostgreSQL 18 (via `psycopg` 3)
- Bootstrap 5 (CDN)
- `python-dotenv` for environment configuration

---

## Project structure
```
Assignment_1/
├── config/            # Project configuration package
│   ├── settings.py    # Installed apps, DATABASES, templates
│   └── urls.py        # Root URL routing
├── movies/            # The "movies" app (functional module)
│   ├── models.py      # Movie model
│   ├── views.py       # CRUD + search + toggle views
│   ├── urls.py        # App-level routes
│   ├── forms.py       # MovieForm (ModelForm)
│   ├── admin.py       # Django Admin registration
│   ├── tests.py       # Model + view tests
│   └── migrations/    # 0001_initial.py
├── templates/         # HTML templates (base + movie pages)
├── requirements.txt
├── setup_db.sql       # One-time PostgreSQL setup
├── .env.example       # Template for environment variables
└── manage.py
```

---

## Setup instructions

### 1. Prerequisites
- Python 3.12+ installed
- PostgreSQL 18 installed and running

### 2. Clone and install dependencies
```bash
git clone <your-repo-url>
cd Assignment_1

python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Create the PostgreSQL database and user
Run the provided script as the `postgres` superuser (it creates the
`movie_watchlist` database and a dedicated `movie_user`):

```bash
# Windows (adjust the path to your PostgreSQL install if needed)
& "C:\Program Files\PostgreSQL\18\bin\psql.exe" -U postgres -f setup_db.sql

# macOS/Linux
psql -U postgres -f setup_db.sql
```

### 4. Configure environment variables
Copy the example env file and adjust values if needed:
```bash
cp .env.example .env      # Windows: copy .env.example .env
```
Make sure `DB_PASSWORD` in `.env` matches the password in `setup_db.sql`.

### 5. Run migrations
```bash
python manage.py migrate
```

### 6. Create an admin user (for Django Admin)
```bash
python manage.py createsuperuser
```

### 7. Run the development server
```bash
python manage.py runserver
```

Then open:
- App: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/

---

## Running tests
```bash
python manage.py test
```
Covers the model (`__str__`, default `watched`, newest-first ordering) and the
views (list, create, update, delete, toggle watched, search).

---

## URL routes
| URL | View | Purpose |
|---|---|---|
| `/` | `movie_list` | Homepage list + search |
| `/add/` | `movie_create` | Add a movie |
| `/<pk>/edit/` | `movie_update` | Edit a movie |
| `/<pk>/delete/` | `movie_delete` | Delete (with confirmation) |
| `/<pk>/toggle/` | `movie_toggle_watched` | Toggle Watched/Unwatched |
| `/admin/` | Django Admin | Manage movies |

---

## Security notes
- Secrets (`SECRET_KEY`, DB password) live in `.env`, which is **git-ignored**.
- `.env.example` documents the required variables without real values.
- All state-changing actions (add, edit, delete, toggle) use `POST` with Django's
  CSRF protection.

---

## AI usage disclosure
In line with the course academic-integrity policy, I acknowledge that I used an AI
assistant (Claude) to support my work on this assignment. I used it as a helper for
explanations of Django concepts, speeding up repetitive boilerplate, and help with
debugging. I made the design decisions, reviewed and adapted the code, set up and
tested the application myself, and I understand the code and can explain any part of
it on request.

## Author
- **Student:** st126005@ait.asia
- **Course:** AST02.04 Full Stack Application Development · FSAD 2026
