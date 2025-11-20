#!/bin/bash
# Aktivoi virtuaaliympäristö
source /home/ubuntu/myapp/venv/bin/activate

# Siirry sovelluskansioon
cd /home/ubuntu/myapp

# Aja datan hakuskripti
python3 fetch_neo_data.py >> cron.log 2>&1
