from jtbc_crawler.driver.chrome_driver import ChromeDriver
from jtbc_crawler.parser.conf_parser import Parser

class Crawler:
    def __init__(self):
        driver = ChromeDriver()
        self.parser = Parser()
        self.browser = driver.browser if driver else None

    def run(self):
        self.browser.get(self.parser.news_ranking_url)

        self.browser.find_elements_by_class_name("rankingnews_box")




if __name__ == '__main__':
    c = Crawler()
    c.run()