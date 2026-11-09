#!/bin/bash
#
gcloud run services add-iam-policy-binding wordle --region=$REGION --member=allUsers --role=roles/run.invoker
