#!/bin/bash

# 1. Generate the config.js file locally
echo "window.APP_CONFIG = $(cat config.json);" > config.js

# 2. Move the file into your local project development directory
mv config.js ./rpi4/

# 3. Copy the entire contents of your project folder to the lighttpd directory
# Change /var/www/html if your lighttpd is serving from a different folder
sudo cp -r ./rpi4/. /var/www/html/

# 4. Set the owner and group to www-data so lighttpd can read them
sudo chown -R www-data:www-data /var/www/html/

# 5. Fix permissions (644 for files so they are readable by the browser)
sudo find /var/www/html/ -type f -exec chmod 644 {} +
