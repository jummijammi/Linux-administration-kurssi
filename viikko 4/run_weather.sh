#!/bin/bash
# Aja säädatan päivitys

cd /home/ubuntu/myapp

# Aktivoi virtuaaliympäristö
source venv/bin/activate

# Suorita varsinainen sääskripti
python3 fetch_weather.py >> weather_cron.log 2>&1
