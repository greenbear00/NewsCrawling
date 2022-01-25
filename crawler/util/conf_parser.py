from configparser import ConfigParser
from pathlib import Path
import os

from crawler.util.Logger import Logger
from crawler.util.Singleton import Singleton
import json

class Parser(metaclass=Singleton):
    def __init__(self):
        self.root_path = Path(__file__).parent.parent.parent

        self._conf_parser = ConfigParser()
        self.logger = Logger(file_name=type(self).__name__).logger

        self._news_ranking_url = None
        self._config = None
        self._load_conf(conf_path=self.root_path)
        self._load_build_conf(conf_path=self.root_path)

    def _load_naver_ranking_conf(self):
        broadcaster_urls = self._conf_parser.get("naver_ranking_news", "broadcaster_urls") if \
            self._conf_parser.get("naver_ranking_news", "broadcaster_urls") else None
        self._broadcaster_urls_li = broadcaster_urls.split('\n')
        self.logger.info(f"naver broadcast_urls = {self.broadcaster_urls_li}")

        press_urls = self._conf_parser.get("naver_ranking_news", "press_urls") if \
            self._conf_parser.get("naver_ranking_news", "press_urls") else None
        self._press_urls_li = press_urls.split('\n')
        self.logger.info(f"naver press_urls = {self.press_urls_li}")

    def _load_elastic_conf(self):
        self._elastic_shard = self._conf_parser.getint("elastic", "ELASTIC_DEV_SHARD") if self._build_level == 'dev' \
            else self._conf_parser.getint("elastic", "ELASTIC_PROD_SHARD")

        self._index_naver_ranking_news = self._conf_parser.get("elastic", "INDEX_NAVER_RANKING_NEWS") if \
            self._conf_parser.get("elastic", "INDEX_NAVER_RANKING_NEWS") else None

    def _load_conf(self, conf_path:Path):
        build_path = os.path.join(conf_path, *["conf", "build.ini"])
        if os.path.isfile(build_path):
            self.logger.info(f"load build.ini: {build_path} ")

            self._conf_parser.read(build_path)
            self._build_level = self._conf_parser.get("build", "BUILD_LEVEL")
            self._proxy = self._conf_parser.get("proxy", "proxy") if self._conf_parser.get("proxy", "proxy") else None

            self._load_naver_ranking_conf()
            self._load_elastic_conf()


    def _load_build_conf(self, conf_path:Path):
        conf_file_name = "dev-config.json" if self.build_level == "dev" else "prod-config.json" if self.build_level == "prod" else "qa-config.json"
        config_file = os.path.join(conf_path, *["conf", conf_file_name])
        if os.path.isfile(config_file):
            self.logger.info(f"load BUILD_LEVEL({self.build_level}) config: {config_file} ")

            with open(config_file, 'r') as f:
                self._config = json.load(f)


    @property
    def proxy(self):
        return self._proxy

    @property
    def broadcaster_urls_li(self):
        return self._broadcaster_urls_li

    @property
    def press_urls_li(self):
        return self._press_urls_li

    @property
    def elastic_shard(self):
        return self._elastic_shard

    @property
    def elastic_conf(self):
        if self._config:
            result = self._config.get('elastic')
            if result:
                return result

        return None, None, None

    @property
    def build_level(self):
        return self._build_level

    @property
    def index_naver_ranking_news(self):
        return self._index_naver_ranking_news
