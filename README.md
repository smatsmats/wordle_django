# Wordle Helper (Django)

Django port of the `wordle.py` CLI solver from `sm_scripts`. Filter candidate
words by green/yellow/gray letters, rank by letter frequency. Stateless (no DB).

## Run locally
    python -m venv .venv && .venv/bin/pip install -r requirements.txt
    DJANGO_DEBUG=1 .venv/bin/python manage.py runserver

JSON API: `GET /api/solve?p1=c&include=ra&exclude=xyz&not2=a&dict=ww|all&no_repeats=1&regex=...`
Health: `GET /healthz`.

## Docker
    docker build -t wordle .
    docker run -p 8080:8080 -e DJANGO_SECRET_KEY=change-me wordle

## Google Cloud Run
    gcloud run deploy wordle --source . --region us-central1 --allow-unauthenticated \
      --set-env-vars DJANGO_SECRET_KEY=$(openssl rand -hex 32)

(Or build with Cloud Build / Artifact Registry and `gcloud run deploy --image`.
Use Secret Manager for the key in real deployments.)

## Env vars
`DJANGO_SECRET_KEY` (required unless `DJANGO_DEBUG=1`), `DJANGO_ALLOWED_HOSTS`,
`DJANGO_CSRF_TRUSTED_ORIGINS` (comma separated), `PORT`.
