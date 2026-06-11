#!/bin/bash

# 1. Generate the config.js file locally by wrapping config.json
echo "window.APP_CONFIG = $(cat config.json);" > config.js

# 2. Copy the entire workspace to your web directory (Apache or Lighttpd)
# Adjust /var/www/html if your server configuration hosts from a different folder
sudo cp config.js index.html functions.js style.css /var/www/html/

# 3. Secure file assignments for the web server daemon
sudo chown -R www-data:www-data /var/www/html/
sudo find /var/www/html/ -type f -exec chmod 644 {} +

echo "Web deployment complete! Configuration synced."