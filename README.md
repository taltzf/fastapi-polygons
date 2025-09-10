# FastAPI Polygon Manager

A FastAPI application for creating, listing, and deleting polygons. Includes a web UI for drawing polygons on a canvas and automated API/UI tests.

---

## Features

- **API Endpoints**:
  - Create polygon: `POST /api/polygon/`
  - List polygons: `GET /api/polygons/`
  - Delete polygon: `DELETE /api/polygon/{id}`

- **Web UI**:
  - Draw polygons on a canvas over an image
  - List and delete existing polygons
  - Uses [https://picsum.photos/1920/1080](https://picsum.photos/1920/1080) as background

- **Database**:
  - SQLite (default)
  - Alembic migrations supported

- **Testing**:
  - API tests with `pytest`
  - UI tests using Playwright

- **Dockerized**:
  - Full containerized setup for both app and tests
  - Optional `--test` flag to run tests during deploy

---

## Project Structure

```commandline
    app/
        ├── main.py # FastAPI application entry point
        ├── models.py # SQLAlchemy models
        ├── schemas.py # Pydantic schemas
        ├── crud.py # CRUD operations
        ├── database.py # DB engine & session
        ├── routers/
        │   └── polygon.py # Polygon API routes
        ├── static/ # Web UI static files (HTML, JS, CSS)
    tests/
        ├── test_api_polygon.py # API tests
        ├── test_ui_polygon.py # UI tests
    run_ui_tests.py # Script to run Playwright UI tests
    Dockerfile
    docker-compose.yml
    requirements.txt
    requirements-dev.txt
    deploy.sh
    README.md
```
## Setup

### 1. Create virtual environment
```bash
    python -m venv .venv
    source .venv/bin/activate
```
### 2. Install dependencies
```bash
    pip install -r requirements.txt
    pip install -r requirements-dev.txt  # For tests
```
### 3. Run migrations
```bash
    alembic upgrade head
```

## Running the Application
### Locally
```bash
  uvicorn app.main:app --reload
```
* API base: http://127.0.0.1:8000/api
* UI: http://127.0.0.1:8000/
### With Docker
```bash
    ./deploy.sh
```

## Testing
### API Tests
```bash
    pytest -m api
```
### UI Tests (Playwright)
```bash
    python run_ui_tests.py
```
#### * Make sure Chromium is installed:
```bash
    playwright install chromium
```

## Alembic Migrations
1. Initialize Alembic (if not done):
```bash
    alembic init alembic
```
2. Generate migration:
```bash
  alembic revision --autogenerate -m "Create polygons table"
```
3. Apply migrations:
```bash
    alembic upgrade head
```
## Notes
* SQLite database file is stored locally by default (polygons.db), or in-memory during tests.
* UI uses HTML5 canvas and vanilla JS (no frameworks required).
* Docker container uses internal SQLite by default, no external DB needed.

## License
MIT License