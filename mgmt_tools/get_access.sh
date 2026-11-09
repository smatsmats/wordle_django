#!/bin/bash

APP=wordle

ret=`gcloud run services get-iam-policy $APP`
if [[ $ret == *"allUsers"* ]]; then
  echo $ret
  echo "Access enabled"
else
  echo "No access"
fi

