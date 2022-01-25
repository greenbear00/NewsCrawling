#!/bin/bash

path=$PWD
echo -e "\n\ncheck current path=$PWD"
export PYTHONPATH=$path:$PYTHONPATH
echo "check PYTHONPATH=$PYTHONPATH"


echo "crawler unittest"
python3 -m venv venv
source $path/venv/bin/activate
pip3 install --upgrade pip
pip3 install -r requirements.txt --proxy http://192.168.1.139:3128


function run_unittest()
{
  filename=$1
  echo -e "\n\n$path/test/$filename -v"
  python3 $path/test/$filename -v
}

function check_fun_exit()
{
  filename=$1
  result=$2
  echo "filename $filename"
  echo "result $result"

  if [ $result -eq 0 ]
  then
    echo "$filename unittest is normal exit ($result)"
  else
      echo "$filename is abnormal exit ($result)"
      exit 1
  fi
}


#echo "unittest"
##source $path/venv/bin/activate
#echo -e "$path/test/main/job/test_TimebasedRunnerTest.py -v"
#python3 $path/test/main/job/test_TimebasedRunnerTest.py -v
#echo -e "\n\n$path/test/test_helper.py -v"
#python3 $path/test/test_helper.py -v
#deactivate

## check conf/build.ini
run_unittest crawler/util/test_conf_parser.py
check_fun_exit crawler/util/test_conf_parser.py $?

# nori-analyzer가 잘 동작하는지 체크
run_unittest crawler/elastic/analyzer/test_nori_analyzer.py
check_fun_exit crawler/elastic/analyzer/test_nori_analyzer.py $?

# naver ranking news가 잘 파싱되는지 체크
run_unittest crawler/parser/module/test_naver_rankingnews_parser.py
check_fun_exit crawler/parser/module/test_naver_rankingnews_parser.py $?