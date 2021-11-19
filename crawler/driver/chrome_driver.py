
from pathlib import Path
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from crawler.util.Logger import Logger
import sys

# TODO conf/build.ini에 있는 proxy를 기반하여 상용에서는 proxy로 데이터 가져오게금 해야 함
# PROXY = "IP:Port"
#
# webdriver.DesiredCapabilities.CHROME['proxy'] = {
#     "httpProxy": PROXY,
#     "ftpProxy": PROXY,
#     "sslProxy": PROXY,
#     "proxyType": "MANUAL"
# }

# class ChromeDriver(metaclass=Singleton):
class ChromeDriver:

    @property
    def browser(self):
        return self._browser

    def __init__(self):
        path = Path(__file__).parent.parent.parent
        self.logger = Logger(file_name=self.__class__.__name__).logger
        try:
            options = Options()
            # chrome://version/ 을 통해서 확인 가능하며, 버전이 60이상일 경우, headless(창 없는) 모드 적용 가능
            options.headless = True
            options.add_argument("window-size=1920x1080")
            options.add_argument("disable-gpu")
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_experimental_option("excludeSwitches", ["enable-logging"])


            if sys.platform == "linux":
                chrome_path = os.path.join(path, *["driver", "linux_chromedriver_96"])
                self.logger.info(f"chrome path = {chrome_path}")
                self._browser = webdriver.Chrome(executable_path=chrome_path, options=options)
            else:
                # osx's platform: darwin
                # 현재 excutable_path는 deprecated됨
                # self._browser = webdriver.Chrome(executable_path=chrome_path, options=options)
                self._browser = webdriver.Chrome(options=options)


        except Exception as es:
            self.logger.error(f"Error = {es}")
            self._browser = None

    def __del__(self):
        print("ChromeDriver deleted")



if __name__ == "__main__":
    d1 = ChromeDriver()
    d2 = ChromeDriver()

    print(id(d1.browser))
    print(id(d2.browser))