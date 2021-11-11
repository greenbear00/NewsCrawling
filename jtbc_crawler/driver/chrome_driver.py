
from pathlib import Path
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from jtbc_crawler.util.Singleton import Singleton

class ChromeDriver(metaclass=Singleton):

    @property
    def browser(self):
        return self._browser

    def __init__(self):
        path = Path(__file__).parent.parent.parent
        chrome_path = os.path.join(path, *["driver", "osx_chromedriver"])
        print(f"chrome path = {chrome_path}")
        try:
            options = Options()
            # chrome://version/ 을 통해서 확인 가능하며, 버전이 60이상일 경우, headless(창 없는) 모드 적용 가능
            options.headless = False
            options.add_argument("window-size=1920x1080")
            options.add_argument("disable-gpu")
            options.add_experimental_option("excludeSwitches", ["enable-logging"])


            # 현재 excutable_path는 deprecated됨
            # self._browser = webdriver.Chrome(executable_path=chrome_path, options=options)
            self._browser = webdriver.Chrome(options=options)
        except Exception as es:
            print(f"Error = {es}")
            self._browser = None

if __name__ == "__main__":
    d1 = ChromeDriver()
    d2 = ChromeDriver()

    print(id(d1.browser))
    print(id(d2.browser))