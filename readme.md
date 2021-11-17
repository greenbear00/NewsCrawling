# 뉴스 크롤링

## 개발 준비사항 
### 1. install for selenium
#### for osx
osx 환경에서 cask, chrome driver를 install 해야 함
참고: homebrew만 설치해서는 일반적으로 쓰는 GUI기반의 어플리케이션을 설치할 수 없으므로 cask를 설치해야 함
```
brew install cask
brew install --cask chromedriver

# osx에서 chromedriver 설치 위치 확인 (예: /usr/local/Caskroom/chromedriver/95.0.4638.54/chromedriver)
brew info chromedriver
cp /usr/local/Caskroom/chromedriver/95.0.4638.54/chromedriver driver

# 또한 osx 상 브라우저 신뢰가 필요하므로
# brew info chromedriver를 통해서 chromedriver가 설치된 /usr/local/bin의 위치에서 아래 명령어 수행
xattr -d com.apple.quarantine chromedriver
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
   (수정해야할 샇아: 언론사별 뉴스에 대한 id 값이 일부 수정되어야 함)

### 3. 실행
```
python3 test/test_ranking_news_update_time.py
```


#### 참고: elastic field type text or keyword
text에 대해서 anlayzer를 적용하여 분할 분석을 하기 위해서는 filed_data가 text로 되어 있어야 함

다만, 쿼리시 데이터 분석에 따른 메모리 소비가 많기 때문에 CircuitBreakingException이 발생
-> 해결 방법: 클러스터에 노  추가

https://wonyong-jang.github.io/elk/2021/07/06/ELK-Elastic-Search-fielddata.html

