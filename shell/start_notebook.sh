#!bin/bash
BASE_PATH=/usr/local/projects/MrDoc
nohup python3 ${BASE_PATH}/manage.py runserver 0.0.0.0:9200 &
