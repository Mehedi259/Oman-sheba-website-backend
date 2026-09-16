#!/bin/bash
SSH_KEY="~/.ssh/sheba_hetzner"
SERVER="root@188.245.212.240"
REMOTE_DIR="/var/www/sheba"

FILES=(
    "classifieds/models.py"
    "classifieds/views.py"
    "classifieds/migrations/0006_job_country_property_country_service_country_and_more.py"
    "community/models.py"
    "community/views.py"
    "community/migrations/0005_classified_country_forumpost_country.py"
    "emergency/models.py"
    "emergency/views.py"
    "emergency/migrations/0002_emergencycontact_country_emergencyservice_country.py"
    "news/models.py"
    "news/views.py"
    "news/migrations/0002_article_country_news_country.py"
    "system/models.py"
    "system/views.py"
    "system/migrations/0003_advertisement_country_heroslider_country.py"
    "system/filters.py"
)

for file in "${FILES[@]}"; do
    echo "Uploading $file..."
    scp -i ~/.ssh/sheba_hetzner "$file" "$SERVER:$REMOTE_DIR/$file"
done
echo "Upload complete!"
