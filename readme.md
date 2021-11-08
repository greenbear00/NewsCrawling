# ...

## install for selenium
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
python 가상환경에서 selenium 설치
```
pip install selenium
```

