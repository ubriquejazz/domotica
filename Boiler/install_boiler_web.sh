#!/bin/bash

# Define workspace target directories
WEB_ROOT="/var/www/html"

# Compile both separate configurations into a single window.APP_CONFIG object map
echo "window.APP_CONFIG = {" > config.js
echo "  infra: $(cat config.json)," >> config.js
echo "  runtime: $(cat boiler.json)" >> config.js
echo "};" >> config.js

# Move the file into your local project development directory
mv config.js ./html/

# Deploy dependencies to your active web server workspace directory
sudo cp -r ./html/ "$WEB_ROOT/"

# Apply safe permissions assignments for your web daemon
sudo chown -R www-data:www-data "$WEB_ROOT"
sudo find "$WEB_ROOT" -type f -exec chmod 644 {} +

echo "Web compilation successful! Infrastructure and Runtime profiles deployed."