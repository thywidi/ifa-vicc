#!/bin/bash
# this script is used to boot a Docker container
source venv/bin/activate
for i in {1..6}; do
    flask db upgrade
    if [[ "$?" == "0" ]]; then
        break
    fi
    echo Deploy command failed, retrying in 5 secs...
    sleep 5
done
exec gunicorn -w 4 --bind 0.0.0.0:5000 --access-logfile - --error-logfile - parking:app
