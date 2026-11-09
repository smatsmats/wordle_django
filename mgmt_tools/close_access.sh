#!/bin/sh

gcloud run services remove-iam-policy-binding wordle --region=$REGION --member=allUsers --role=roles/run.invoker
