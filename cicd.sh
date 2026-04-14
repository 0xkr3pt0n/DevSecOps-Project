#!/bin/bash

set -e

APP_NAME=univapp
VERSION=insecure

docker rm -f $APP_NAME 2>/dev/null || true
docker build -t $APP_NAME:$VERSION .
docker scout cves $APP_NAME:$VERSION --output ./vulnsreport
docker scout cves $APP_NAME:$VERSION --only-severity critical --exit-code
docker scout sbom --output univapp.sbom $APP_NAME:$VERSION

docker run -d -p 8000:8000 --name $APP_NAME $APP_NAME:$VERSION