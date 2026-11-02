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

## Google Kubernetes Engine (GKE)
    PROJECT=my-project REGION=us-central1
    gcloud artifacts repositories create wordle --repository-format=docker --location=$REGION
    gcloud builds submit --tag $REGION-docker.pkg.dev/$PROJECT/wordle/wordle:latest .
    gcloud container clusters create-auto wordle --region=$REGION
    gcloud container clusters get-credentials wordle --region=$REGION

    kubectl create secret generic wordle-secret --from-literal=secret-key=$(openssl rand -hex 32)
    sed "s#REGION-docker.pkg.dev/PROJECT_ID#$REGION-docker.pkg.dev/$PROJECT#" k8s/deployment.yaml | kubectl apply -f -
    kubectl apply -f k8s/service.yaml
    kubectl get service wordle   # wait for EXTERNAL-IP, then browse to http://<ip>/

Set `DJANGO_ALLOWED_HOSTS` in `k8s/deployment.yaml` to your IP/domain instead of `*`.
The image also runs unchanged on Cloud Run (`gcloud run deploy --source .`).

## Env vars
`DJANGO_SECRET_KEY` (required unless `DJANGO_DEBUG=1`), `DJANGO_ALLOWED_HOSTS`,
`DJANGO_CSRF_TRUSTED_ORIGINS` (comma separated), `PORT`.
