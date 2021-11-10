from jtbc_crawler.util.Singleton import Singleton
from jtbc_crawler.driver.chrome_driver import ChromeDriver
from selenium.webdriver.common.by import By

class NaverRankingNews(ChromeDriver, metaclass=Singleton):

    def __init__(self, url:str):

        super().__init__()
        print(f"naver ranking news url = {url}")
        self.browser.get(url)

        self._publisher = {}
        self._click_more_publisher()
        self._find_publisher()
        self._go_publisher(publisher_name="JTBC")

    # def _load_ranking_news(self):
    #     rank_box = self.browser.find_elements(By.CLASS_NAME, "rankingnews_box")
    #     for a_box in rank_box:
    #         print(a_box)

    @property
    def publisher(self):
        return self._publisher

    def _find_publisher(self):
        news_name = self.browser.find_elements(By.CLASS_NAME, "rankingnews_name")
        self._publisher = {news.text:news for news in news_name}


    def _go_publisher(self, publisher_name:str):
        jtbc_publisher = self.publisher.get(publisher_name)
        jtbc_publisher.click()



    def _click_more_publisher(self):
        # 아래 button에 대한 xpath
        # <button type="button" class="button_rankingnews_more _moreButton nclicks('RBP.more')">다른 언론사 랭킹 더보기</button>
        # xpath: /html/body/div/div[4]/button
        # WebElement(button)
        while True:
            button = self.browser.find_element(By.XPATH, '/html/body/div/div[4]/button')
            if button.aria_role == "button" and button.tag_name == "button":
                button.click()
            else:
                break



        print("done")



if __name__ == "__main__":
    from jtbc_crawler.parser.conf_parser import Parser
    p = Parser()
    NaverRankingNews(url=p.naver_news_ranking_url)

