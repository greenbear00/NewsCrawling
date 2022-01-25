# 뉴스 크롤링

## 개발 준비사항 
### 1. install for selenium
#### for osx
osx 환경에서 cask, chrome driver를 install 해야 함
참고: homebrew만 설치해서는 일반적으로 쓰는 GUI기반의 어플리케이션을 설치할 수 없으므로 cask를 설치해야 함
```
# 만약 버전 UPDATE이면 brew reinstall chromedriver
brew install cask
brew install --cask chromedriver

# osx에서 chromedriver 설치 위치 확인 (예: /usr/local/Caskroom/chromedriver/95.0.4638.54/chromedriver)
brew info chromedriver
cp /usr/local/Caskroom/chromedriver/95.0.4638.54/chromedriver driver

# 또한 osx 상 브라우저 신뢰가 필요하므로
# brew info chromedriver를 통해서 chromedriver가 설치된 /usr/local/bin의 위치에서 아래 명령어 수행
xattr -d com.apple.quarantine driver/chromedriver
```
#### for centos
이전에 python 및 jdk8이상 설치 필요
```
$ sudo python3 -m pip install selenium
$ sudo vi /etc/yum.repos.d/google-chrome.repo
[google-chrome]
name=google-chrome
baseurl=http://dl.google.com/linux/chrome/rpm/stable/x86_64
enabled=1
gpgcheck=1
gpgkey=https://dl-ssl.google.com/linux/linux_signing_key.pub

$ sudo yum install -y google-chrome-stable
```

### 2. python 가상환경에서 selenium 설치
```
pip install selenium
```
### 3. chrome driver downalod

crhome driver url = https://sites.google.com/a/chromium.org/chromedriver/downloads

## how to 스크랩
### 1. 스크랩 타겟
스크랩 타겟 URL: https://news.naver.com/main/ranking/popularDay.naver?mid=etc&sid1=111
- 일반적으로 매시 08분 즈음에 네이버 배치 잡이 수행해서 결과가 바뀜

| 실행시간 | 집계한 결과 | 부연설명 |
| --- | --- | --- |
| 00:15 | 오후 11시~자정 |  |
| 01:15 | 자정~오전 1시 | 무시하기(view가 깍이는 증상이 있고, 고정된 값임) |
| 02:15 | 자정~오전 1시 | 무시하기(view가 깍이는 증상이 있고, 고정된 값임) |
| 03:15 | 자정~오전 1시 | 무시하기(view가 깍이는 증상이 있고, 고정된 값임) |
| 04:15 | 자정~오전 1시 | 무시하기(view가 깍이는 증상이 있고, 고정된 값임) |
| 05:15 | 자정~오전 1시 | 무시하기(view가 깍이는 증상이 있고, 고정된 값임) |
| 06:15 | 오전1시~오전6시 |  |
| 07:15 | 오전6시~오전7시 |  |

- 하루 동안 집계 결과는 위 url 밑에 하단에서 이전 날짜를 클릭해야 하루 동안 집계된 결과를 볼 수 있음.

### 2. 구현 내용
1. 스크랩 타겟 URL을 바탕으로 지정한 언론사에 대한 랭킹 뉴스를 가져옴 (w. selenium)
2. 가져온 뉴스를 대상으로 elastic으로 write
   - conf/dev-config.json으로 정보를 넣으면 자동 동작함
   - 이때, 알아서 index template를 생성
   - 또한 news_nm(뉴스 타이틀)을 분석하기 위해서 내부에 eleastic에 nori analyzer가 설치 되어 있어야 함.
   ```
   # conf/dev-config.json
   {
      "elastic": {
         "hosts": "",
         "username": "",
         "password": ""
      }
   }



   # elastic에 nori analysis를 설치
   $ sudo bin/elasticsearch-plugin install analysis-nori

   # nori analysis 설치 확인
   $ bin/elasticsearch-plugin list
   analysis-nori

   ```
3. 실제 job은 python 내부 스케줄러로 동작 -> 스케줄러 대신 airflow 연동하면 됨
   3.1 이로 인해 process_id를 생성하고, 기존에 생성된 process_id(.CRAWER_PID)를 삭제함

### 3. 실행
```
$ chmod u+x driver/*
$ chmod u+x script/*
$ nohup ./script/naver_news_crawler.sh &
[1] 39282
$

check current path=/crawler-tmp2
check PYTHONPATH=/crawler-tmp2:
job start

$ ps -ef | grep naver
root       1275      1  0 Jun29 ?        00:21:00 /usr/bin/python2 -Es /usr/sbin/tuned -l -P
asmanag+  44900  44898  5 16:04 pts/0    00:00:01 python3 main/test_ranking_news_update_time.py
asmanag+  45054  43328  0 16:04 pts/0    00:00:00 grep --color=auto python
$ ps -ef | grep $(cat CRAWER_PID)
asmanag+  44898  43328  0 16:04 pts/0    00:00:00 /bin/bash ./script/naver_news_crawler.sh
asmanag+  45075  43328  0 16:04 pts/0    00:00:00 grep --color=auto naver
```
