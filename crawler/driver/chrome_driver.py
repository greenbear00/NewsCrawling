from pathlib import Path
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from crawler.util.Logger import Logger
import sys


# class ChromeDriver(metaclass=Singleton):
class ChromeDriver:

    @property
    def browser(self):
        return self._browser

    def __init__(self, proxy:str=None):
        self.logger = Logger(file_name=self.__class__.__name__).logger
        try:

            options = Options()
            # chrome://version/ 을 통해서 확인 가능하며, 버전이 60이상일 경우, headless(창 없는) 모드 적용 가능

            # to solve below: append user_agnet, window-size in headless
            # Message: element not interactable (Session info: headless chrome=80.0.3987.106)
            user_agent = "Mozilla/5.0 (Linux; Android 9; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.83 Mobile Safari/537.36"
            options.add_argument('user-agent=' + user_agent)
            options.add_argument('--window-size=1920,1080')

            options.add_argument("disable-gpu")
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            # options.add_argument('ignore-certificate-errors')
            options.add_experimental_option("excludeSwitches", ["enable-logging"])

            self.logger.info(f"chrome set proxy = {proxy}")
            if proxy is not None:
                options.add_argument(f'----proxy-server=http://{proxy}')

            if sys.platform == "linux":
                # linux에서는 터미널 기반이기 때문에 무조건 False로 해야 함
                options.add_argument('headless')
            # else:
            #     options.add_argument('headless')

            # webdriver.Chrome의 excutable_path가 deprecated가 됨.
            # self._browser = webdriver.Chrome(executable_path=chrome_path, options=options)
            # 아래와 같이 하면, 자동으로 업데이트 버전으로 설치하면서 chrome 을 이용할 수 있음.
            self._browser = webdriver.Chrome(ChromeDriverManager().install(),
                                             options=options)

        except Exception as es:
            self.logger.error(f"Error = {es}")
            self._browser = None
        self.logger.info(f"ChromeDriver created.")

    def __del__(self):
        # # 브라우저 화면만 닫음
        # self._browser.close()
        self.logger.info("ChromeDriver close")

        # # 브라우저를 닫고 프로세스도 종료
        # self._browser.quit()


