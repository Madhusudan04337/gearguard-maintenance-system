Setup and run instructions (PostgreSQL + Tailwind)

1) Python deps (create a virtualenv first):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2) Node / Tailwind (from project root):

```powershell
npm install
npm run build:css
```

3) Create Postgres DB (example):

```powershell
# using psql:
createdb -U postgres gearguard_db
```

4) Migrate and create superuser:

```powershell
python manage.py migrate
python manage.py create_initial_superuser
```

5) Run server:

```powershell
python manage.py runserver
```

Notes:
- If your Postgres user/password/host differ, edit `gearguard/settings.py` DATABASES.
- For development you can run `npm run watch:css` to auto-build Tailwind while editing.
