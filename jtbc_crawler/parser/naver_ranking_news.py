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

        self.browser.get(self.url)
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
            self._load_rankingnews_list()
            time.sleep(2)

            self._publisher = {}

    def _load_rankingnews_list(self):
        ranking_news_em = self.browser.find_element(By.XPATH, "/html/body/div/div[4]/div[2]/div[2]/ul")

        # <a href="/main/ranking/read.naver?mode=LSD&amp;mid=shm&amp;sid1=001&amp;oid=437&amp;aid=0000280578&amp;rankingType=RANKING" class="list_img nclicks('RBP.drnknws')">
        #                                    <img src="https://mimgnews.pstatic.net/image/origin/437/2021/11/11/280578.jpg?type=nf74_74" width="74" height="74" alt="" onerror="this.src='https://ssl.pstatic.net/static.news/image/news/errorimage/noimage_74x74_1.png';">
        #
        #                                </a>
        # /html/body/div/div[4]/div[2]/div[2]/ul/li[1]/div/a
        # /html/body/div/div[4]/div[2]/div[2]/ul/li[2]/div/a
        ranking_news_list_em = ranking_news_em.find_element(By.XPATH, "/html/body/div/div[4]/div[2]/div[2]/ul")

        ranking_news_size = len(ranking_news_list_em)
        for index in range(1, ranking_news_size+1):

            a_href = ranking_news_list_em.find_element(By.XPATH, f"/html/body/div/div[4]/div[2]/div[2]/ul/li["
                                                            f"{str(index)}]/div/a")
            print(a_href.text)
            a_href.click()
            # articleTitle_em = self.browser.find_element(By.XPATH, "/html/body/div[2]/table/tbody/tr/td[1]/div/div["
            #                                                       "1]/div[""3]/h3")
            # print("\trticleTitle_em.text")
            self.browser.back()

            ranking_news_list_em = self.browser.find_element(By.XPATH, "/html/body/div/div[4]/div[2]/div[2]/ul")





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
    print(p.naver_news_ranking_url)
    print(p.publishers)
    NaverRankingNews(url=p.naver_news_ranking_url, publishers=p.publishers)


