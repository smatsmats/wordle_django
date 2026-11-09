#!/bin/bash

gcloud run services describe wordle --region=$REGION --format='value(status.url)'
