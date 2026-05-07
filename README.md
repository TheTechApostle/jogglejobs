# Joggle Jobs — Full-Stack Job Board

## Quick Start

```bash
pip install -r requirements.txt
python app.py
```

Open http://localhost:5050

## Admin Panel
URL: http://localhost:5050/admin
Password: admin1234

## Features
- Nigeria + International job listings
- Job scraping endpoint (POST /api/scrape)  
- Admin panel: add / delete / feature jobs
- Filters: region, type, category, search
- Fully responsive purple design

## Structure
joggle-jobs/
├── app.py              # Flask backend
├── templates/          # Jinja2 HTML templates
├── static/css/         # Stylesheet
├── static/js/          # Frontend JS
├── data/jobs.json      # Job data store
└── requirements.txt
