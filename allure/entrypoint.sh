#!/bin/sh

set -e

echo "Generating Allure report..."
allure generate /app/allure-results -o /var/www/html --clean

echo "HTML mode enabled. Starting server in foreground..."
nginx -g 'daemon off;'