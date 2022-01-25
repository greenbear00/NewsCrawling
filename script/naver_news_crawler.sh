#!/bin/bash

path=$PWD
echo -e "\n\ncheck current path=$path"
export PYTHONPATH=$path:$PYTHONPATH
echo "check PYTHONPATH=$PYTHONPATH"


echo "job start"
echo -e "install -r requirements.txt --proxy http://192.168.1.139:3128\n\n"
python3 -m venv venv
source $path/venv/bin/activate
pip3 install --upgrade pip
pip3 install -r requirements.txt --proxy http://192.168.1.139:3128

echo -e "python3 crawler/scheduler/naver_ranking_news_job.py > /dev/null 2>&1 &\n\n"
python3 crawler/scheduler/naver_ranking_news_job.py > /dev/null 2>&1 &
deactivate