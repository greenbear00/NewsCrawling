from configparser import ConfigParser
from pathlib import Path
import os
from jtbc_crawler.util.Singleton import Singleton

class Parser(metaclass=Singleton):
    def __init__(self):
        conf_path = os.path.join(Path(__file__).parent.parent.parent, *["conf", "build.ini"])

        self._conf_parser = ConfigParser()

        self._news_ranking_url = None
        if os.path.isfile(conf_path):
            self._conf_parser.read(conf_path)
            self._naver_news_ranking_url = self._conf_parser.get("crawling", "naver_news_ranking_url") if \
                self._conf_parser.get("crawling", "naver_news_ranking_url") else None
            self._publishers = self._conf_parser.get("crawling", "publishers").replace(" ", "").split(",")
            # print(self._news_ranking_url)

    @property
    def publishers(self):
        return self._publishers

    @property
    def naver_news_ranking_url(self):
        return self._naver_news_ranking_url

if __name__ == "__main__":
    p = Parser()
    print("naver news ranking_url: ", p.naver_news_ranking_url)
    print("publishers: ", p.publishers)
