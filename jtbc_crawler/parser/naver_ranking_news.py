from jtbc_crawler.util.Singleton import Singleton
from jtbc_crawler.driver.chrome_driver import ChromeDriver
from selenium.webdriver.common.by import By

class NaverRankingNews(ChromeDriver, metaclass=Singleton):

    def __init__(self, url:str):

        super().__init__()
        print(f"naver ranking news url = {url}")
        self.browser.get(url)

        self._load_ranking_news()

    def _load_ranking_news(self):
        rank_box = self.browser.find_elements(By.CLASS_NAME, "rankingnews_box")
        for a_box in rank_box:
            print(a_box)


if __name__ == "__main__":
    from jtbc_crawler.parser.conf_parser import Parser
    p = Parser()
    NaverRankingNews(url=p.naver_news_ranking_url)

