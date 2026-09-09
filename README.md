# Sparsh Inclusive Education — Public Website

Production-ready public site for **Sparsh Inclusive Education**, built with Django (MVC), HTML/CSS/JS, and PostgreSQL.

**Tagline:** Different Abilities. Limitless Possibilities.

## Project structure

```
Sparsh/
├── frontend/                 # Public UI assets
│   ├── templates/            # Django HTML templates
│   └── static/               # CSS, JS, images
│       ├── css/
│       ├── js/
│       └── img/
├── backend/                  # Django application
│   ├── manage.py
│   ├── config/               # Settings, URLs, WSGI/ASGI
│   ├── apps/
│   │   ├── core/             # Home, about, contact, legal pages
│   │   ├── programs/         # Programs & feature pillars
│   │   ├── admissions/       # Enquiry form & storage
│   │   ├── people/           # Team & advisors
│   │   └── content/          # Testimonials, FAQs, stats, gallery
│   ├── media/                # User uploads (local)
│   └── db.sqlite3            # Local SQLite (when DB_NAME unset)
├── manage.py                 # Convenience wrapper → backend/
├── requirements.txt
├── .env.example
├── Procfile
└── README.md
```

## Stack

| Layer | Technology |
|-------|------------|
| Frontend | HTML templates, modular CSS, accessible JS |
| Backend | Python Django 5 (views, forms, CSRF, admin) |
| Database | PostgreSQL in production; SQLite for local demo |

## Quick start (local)

```bash
cd c:\Users\satheesh\Desktop\Sparsh
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt

# Optional: copy .env.example .env  (not required for local SQLite)

python manage.py migrate
python manage.py seed_data
python manage.py runserver
```

Or from the backend folder:

```bash
cd backend
python manage.py runserver
```

Open http://127.0.0.1:8000/

Admin: http://127.0.0.1:8000/admin/

## PostgreSQL (production)

Set in project-root `.env` (copy from `.env.example`):

```
DJANGO_DEBUG=False
DJANGO_SECRET_KEY=<long-random-string>
DJANGO_ALLOWED_HOSTS=sparshinclusive.edu,www.sparshinclusive.edu
DJANGO_CSRF_TRUSTED_ORIGINS=https://sparshinclusive.edu,https://www.sparshinclusive.edu
SITE_URL=https://sparshinclusive.edu
DB_NAME=sparsh
DB_USER=sparsh
DB_PASSWORD=<secure>
DB_HOST=localhost
DB_PORT=5432
```

Then:

```bash
python manage.py migrate
python manage.py seed_data
python manage.py collectstatic --noinput
cd backend && gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

## Site map

- `/` — Home (hero, philosophy, pillars, gallery, stats, testimonials, admissions, FAQ)
- `/about/` `/inclusive-education/` `/our-approach/` `/parents-corner/` `/contact/`
- `/programs/` + detail + pillar detail pages
- `/admissions/` — secure enquiry form → database
- `/team/` `/advisors/`
- `/accessibility/` `/privacy/` `/terms/`

## Brand

Logo colours: forest green `#5E8D45`, moss `#8DA760`, sunny yellow `#F9D61E`, soft off-white ground.
