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

        info = self.browser.find_element(By.XPATH, "/html/body/div/div[4]/div[1]/div")

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
        """
        특정 언론사 별 많이 본 뉴스(왼쪽)
        :return:
        """

        ranking_news_em = self.browser.find_element(By.XPATH, "/html/body/div/div[4]/div[2]/div[2]/ul")

        # 많이 본 뉴스 <ul> 밑에 있는 <li></li>에 해당하는 부
        list_content = ranking_news_em.find_elements(By.CLASS_NAME, "list_content")
        ranking_news_size = len(list_content)
        for index in range(1, ranking_news_size+1):

            # ranking index에 해당하는 a href이며, text가 뉴스 title
            a_href = self.browser.find_element(By.XPATH, f"/html/body/div/div[4]/div[2]/div[2]/ul/li["
                                                            f"{str(index)}]/div/a")
            print(f"[{index}] {a_href.text}")
            # ranking index에 해당하는 span이며, view 정보를 집계
            a_span = self.browser.find_element(By.XPATH, f"/html/body/div/div[4]/div[2]/div[2]/ul/li[{str(index)}]/div/span[2]")
            print(f"\t- view: {a_span.text}")
            a_href.click()

            a_news_timestamp = self.browser.find_elements(By.CLASS_NAME, "t11")
            a_news_created_time = a_news_timestamp[0].text
            a_news_modified_time = a_news_timestamp[1].text if len(a_news_timestamp)>1 else None
            print(f"\t- created time: {a_news_created_time}")
            print(f"\t- modified time: {a_news_modified_time}")
            a_news_reaction = self.browser.find_element(By.XPATH, "/html/body/div[2]/table/tbody/tr/td[1]/div/div[1]/div[3]/div/div[3]/div[1]/div/a/span[3]")
            a_news_comment = self.browser.find_element(By.CLASS_NAME, "lo_txt")
            print(f"\t- reaction: {a_news_reaction.text}")
            print(f"\t- comment: {a_news_comment.text}")

            self.browser.back()



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


