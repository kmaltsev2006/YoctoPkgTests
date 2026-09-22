#!/bin/bash

docker run --rm -d -p 8080:80 \
  -v "$(pwd)/allure-results":/app/allure-results \
  --name allure-viewer \
  allure-report-viewer