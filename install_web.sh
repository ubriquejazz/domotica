#!/bin/bash

WEB_ROOT="/var/www/html"

# 1. Generate the config.js file locally
echo "window.APP_CONFIG = $(cat config.json);" > config.js

# 2. Move the file into your local project development directory
mv config.js ./html/

# 3. Copy the entire contents of your project folder to the lighttpd directory
# Change /var/www/html if your lighttpd is serving from a different folder
sudo cp -r ./html/* "$WEB_ROOT"

# Apply safe permissions assignments for your web daemon
sudo chown -R www-data:www-data "$WEB_ROOT"
sudo find "$WEB_ROOT" -type f -exec chmod 644 {} +

echo "Web compilation successful! Infrastructure and Runtime profiles deployed."