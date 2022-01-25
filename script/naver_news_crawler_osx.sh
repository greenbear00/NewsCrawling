#!/bin/bash

path=$(pwd)
echo -e "\n\ncheck current path=$path"
export PYTHONPATH=$path:$PYTHONPATH
echo "check PYTHONPATH=$PYTHONPATH"


echo "job start"
python3 -m venv venv
source $path/venv/bin/activate
pip3 install -r requirements.txt
python3 crawler/scheduler/naver_ranking_news_job.py > /dev/null 2>&1 &
deactivate

#function run_unittest()
#{
#  filename=$1
#  echo -e "\n\n$path/test/$filename -v"
#  python3 $path/test/$filename -v
#}
#
#function check_fun_exit()
#{
#  filename=$1
#  result=$2
##  echo "filename $filename"
##  echo "result $result"
#  if [ $result -eq 0 ]
#  then
#    echo "$filename unittest is normal exit ($result)"
#  else
#      echo "$filename is abnormal exit ($result)"
#      exit 1
#  fi
#}
#
#run_unittest main/job/test_TimebasedRunnerTest.py
#check_fun_exit main/job/test_TimebasedRunnerTest.py $?
#run_unittest main/job/test_PlatformNewsSummary.py
#check_fun_exit main/job/test_PlatformNewsSummary.py $?