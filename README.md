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
    PROJECT=wordle-pup REGION=us-west1
    gcloud config set run/region $REGION
    gcloud artifacts repositories create wordle --repository-format=docker --location=$REGION
    gcloud builds submit --tag $REGION-docker.pkg.dev/$PROJECT/wordle/wordle:latest .
    gcloud container clusters create-auto wordle --region=$REGION
    gcloud container clusters get-credentials wordle --region=$REGION

    kubectl create secret generic wordle-secret --from-literal=secret-key=$(openssl rand -hex 32)
    sed "s#REGION-docker.pkg.dev/PROJECT_ID#$REGION-docker.pkg.dev/$PROJECT#" k8s/deployment.yaml | kubectl apply -f -
    kubectl apply -f k8s/service.yaml
    kubectl get service wordle   # wait for EXTERNAL-IP, then browse to http://<ip>/

Set `DJANGO_ALLOWED_HOSTS` in `k8s/deployment.yaml` to your IP/domain instead of `*`.

## Google Cloud Run
    PROJECT=wordle-pup REGION=us-west1
    gcloud config set project $PROJECT
    gcloud services enable run.googleapis.com artifactregistry.googleapis.com cloudbuild.googleapis.com secretmanager.googleapis.com

    # Store the Django secret key in Secret Manager
    openssl rand -hex 32 | gcloud secrets create wordle-secret-key --data-file=-
    gcloud secrets add-iam-policy-binding wordle-secret-key \
      --member=serviceAccount:$(gcloud projects describe $PROJECT --format='value(projectNumber)')-compute@developer.gserviceaccount.com \
      --role=roles/secretmanager.secretAccessor

    # Build from the Dockerfile and deploy (Cloud Run sets $PORT; the image honors it)
    gcloud run deploy wordle --source . --region=$REGION --allow-unauthenticated \
      --set-secrets=DJANGO_SECRET_KEY=wordle-secret-key:latest

    curl $(gcloud run services describe wordle --region=$REGION --format='value(status.url)')/healthz

`*.run.app` hosts are already allowed. For a custom domain, add
`--set-env-vars=DJANGO_ALLOWED_HOSTS=example.com,DJANGO_CSRF_TRUSTED_ORIGINS=https://example.com`
(use `^@^` delimiter syntax if values contain commas). Redeploy by re-running `gcloud run deploy`.

### Stop / tear down
Cloud Run scales to zero when idle, so an idle service costs nothing. To stop serving traffic:

    # Block public access (service stays deployed; requests get 403)
    gcloud run services remove-iam-policy-binding wordle --region=$REGION --member=allUsers --role=roles/run.invoker

    # Or delete the service entirely
    gcloud run services delete wordle --region=$REGION

To restore public access after blocking it:

    gcloud run services add-iam-policy-binding wordle --region=$REGION --member=allUsers --role=roles/run.invoker

Optional cleanup of remaining resources:

    gcloud secrets delete wordle-secret-key
    gcloud artifacts repositories delete cloud-run-source-deploy --location=$REGION   # repo created by --source deploys

## Env vars
`DJANGO_SECRET_KEY` (required unless `DJANGO_DEBUG=1`), `DJANGO_ALLOWED_HOSTS`,
`DJANGO_CSRF_TRUSTED_ORIGINS` (comma separated), `PORT`.
