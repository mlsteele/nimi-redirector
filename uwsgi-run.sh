#!/usr/bin/env bash

# Run as the www-data user.
# Start uwsgi on the specified socket.
sudo -H -u www-data sh -c "uwsgi \
  -s /tmp/uwsgi-nimi.sock \
  -w nimi:app \
  --master \
  --uid www-data \
  --gid www-data"
