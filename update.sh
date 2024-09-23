#!/bin/sh
docker compose down
git pull origin dev
sleep 2s
docker compose up -d --force-recreate
sleep 1s
docker compose logs
