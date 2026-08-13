# Ethical Writes

A small Django application for short creative pieces and personal writing exercises. This repository contains the site source, templates and static assets used to present user-created content, plus a tiny admin for managing submissions.

## Features
- Simple Django site using SQLite for storage
- Template-based pages for multiple writings (webpage2, webpage3, webpage4)
- User-authenticated area and a user work viewer (`webpageuserwork.html`)
- Reusable header/footer template components for consistent layout

## Repository layout

- `manage.py` — Django management script
- `db.sqlite3` — SQLite database (development)
- `ethicalwrites/` — Django project settings and WSGI/ASGI
- `ethicalwritesapp/` — Django app containing views, models and URLs
- `templates/` — Jinja/Django templates used by the site
	- `header.html` and `footer.html` — shared header/footer components
	- `webpage2.html`, `webpage3.html`, `webpage4.html`, `webpageuserwork.html` — content pages
- `static/` — static assets (CSS, images)

## Quick start (development)
These instructions assume Windows and the project root is the repository root (where `manage.py` lives).

1. Create and activate a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies

```powershell
pip install -r requirements.txt
# If you don't have a requirements.txt, install Django directly:
pip install django
```

3. Run migrations and start the development server

```powershell
python manage.py migrate
python manage.py createsuperuser   # optional, to access admin
python manage.py runserver
```

Open http://127.0.0.1:8000/ in a browser.

## Templates and shared components
- The project now uses reusable header and footer components. Include them in templates with:

```django
{% include 'header.html' %}
... page content ...
{% include 'footer.html' %}
```

- The header component mirrors the styled header used in `webpageuserwork.html` and contains the branded link and action buttons (back to creations, logout). See [ethicalwrites/templates/header.html](ethicalwrites/templates/header.html) and [ethicalwrites/templates/footer.html](ethicalwrites/templates/footer.html).

## Styling and assets
- Global CSS and page-specific styles live under `static/` and inside individual templates for small pages. Fonts and icons are loaded via CDN in templates (Google Fonts, Font Awesome, Bootstrap). Adjust those links in the `<head>` sections of the page templates if you want to self-host.

## Common tasks
- Create a new page: add a template under `templates/`, then add a URL pattern in `ethicalwritesapp/urls.py` and a view in `ethicalwritesapp/views.py`.
- Update header links: edit [ethicalwrites/templates/header.html](ethicalwrites/templates/header.html).
- Change footer text: edit [ethicalwrites/templates/footer.html](ethicalwrites/templates/footer.html).

## Notes about running and deployment
- The project uses SQLite for development. For production, switch to Postgres/MySQL and update `ethicalwrites/settings.py`.
- Remember to set `DEBUG = False`, configure `ALLOWED_HOSTS`, and run `collectstatic` when deploying.

## Contributing
- Fork the repo and open a pull request for proposed changes.
- Keep changes focused and include small, testable commits.

## License
This repository does not include an explicit license file. Add a `LICENSE` if you intend to make this project open-source.

## Contact
If you want help extending the project (APIs, user profiles, rich-text editing, or deployment), open an issue or reach out in the project tracker.




