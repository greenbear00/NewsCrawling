from jtbc_crawler.util.Singleton import Singleton
from jtbc_crawler.driver.chrome_driver import ChromeDriver
from selenium.webdriver.common.by import By
import time

class NaverRankingNews(ChromeDriver, metaclass=Singleton):

    def __init__(self, url:str, publishers:list):

        super().__init__()
        self._url = url
        print(f"naver ranking news url = {url}")

        self._publisher = {}

        self.browser.get(url)
        self._click_more_publisher()
        self._find_publisher()

        self._go_publisher(url=url, publishers=publishers)


    @property
    def url(self):
        return self._url

    @property
    def publisher(self):
        return self._publisher


    def _find_publisher(self):
        news_name = self.browser.find_elements(By.CLASS_NAME, "rankingnews_name")
        self._publisher = {news.text:news for news in news_name}


    def _go_publisher(self, url:str, publishers:list):

        for publisher_name in publishers:
            if not self.publisher:
                self.browser.get(url)
                self._click_more_publisher()
                self._find_publisher()
            a_publisher = self.publisher.get(publisher_name)
            a_publisher.click()
            time.sleep(2)
            self._publisher = {}




    def _click_more_publisher(self):
        # 아래 button에 대한 xpath
        # <button type="button" class="button_rankingnews_more _moreButton nclicks(RBP.more)">다른 언론사 랭킹 더보기</button>
        # xpath: /html/body/div/div[4]/button
        # WebElement(button)
        while True:
            button = self.browser.find_element(By.XPATH, "/html/body/div/div[4]/button")
            if button.aria_role == "button" and button.tag_name == "button":
                button.click()
            else:
                break


if __name__ == "__main__":
    from jtbc_crawler.parser.conf_parser import Parser
    p = Parser()
    NaverRankingNews(url=p.naver_news_ranking_url, publishers=p.publishers)


