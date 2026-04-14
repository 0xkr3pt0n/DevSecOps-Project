#!/bin/bash

set -e 

#enviroment variables
APP_NAME=univ_app
VERSION=insecure

#building docker image
echo "----------------- removing old image -----------------"
docker rm -f $APP_NAME 2>/dev/null || true
echo "----------------- Building new image -----------------"
docker build -t $APP_NAME:$VERSION .
echo "----------------- checking for vulnerabilites (cves) -----------------"
docker scout cves $APP_NAME:$VERSION --output ./CVEs_Report
#check with owasp dependency
dependency-check --project $APP_NAME --scan . --format "HTML" --out "reports"
#docker scout cves $APP_NAME:$VERSION --only-severity critical --exit-code
echo "----------------- checking for depandancies (SBOM) -----------------"
docker scout cves $APP_NAME:$VERSION --output ./SBOM_Report 

#run container
echo "----------------- running the container -----------------"
docker run -d -p 8000:8000 --name $APP_NAME $APP_NAME:$VERSION