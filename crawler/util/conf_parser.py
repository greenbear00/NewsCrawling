from configparser import ConfigParser
from pathlib import Path
import os

from crawler.util.Logger import Logger
from crawler.util.Singleton import Singleton
import json

class Parser(metaclass=Singleton):
    def __init__(self):
        root_path = Path(__file__).parent.parent.parent

        self._conf_parser = ConfigParser()
        self.logger = Logger(path=os.path.join(root_path, "logs"), file_name=type(self).__name__).logger

        self._news_ranking_url = None
        self._config = None
        self._load_conf(conf_path=root_path)
        self._load_build_conf(conf_path=root_path)

    def _load_conf(self, conf_path:Path):
        build_path = os.path.join(conf_path, *["conf", "build.ini"])
        if os.path.isfile(build_path):
            self.logger.info(f"load build.ini: {build_path} ")
            self._conf_parser.read(build_path)
            self._naver_news_ranking_url = self._conf_parser.get("crawling", "naver_news_ranking_url") if \
                self._conf_parser.get("crawling", "naver_news_ranking_url") else None
            self._publishers = self._conf_parser.get("crawling", "publishers").replace(" ", "").split(",")


            self._build_level = self._conf_parser.get("build", "BUILD_LEVEL")
            self._elastic_shard = self._conf_parser.get("elastic", "ELASTIC_DEV_SHARD") if self._build_level == 'dev' \
                else self._conf_parser.get("elastic", "ELASTIC_PROD_SHARD")


    def _load_build_conf(self, conf_path:Path):
        conf_file_name = "dev-config.json" if self.build_level == "dev" else "prod-config.json" if self.build_level == "prod" else "qa-config.json"
        config_file = os.path.join(conf_path, *["conf", conf_file_name])
        if os.path.isfile(config_file):
            self.logger.info(f"load BUILD_LEVEL({self.build_level}) config: {config_file} ")

            with open(config_file, 'r') as f:
                self._config = json.load(f)

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
    def publishers(self):
        return self._publishers

    @property
    def naver_news_ranking_url(self):
        return self._naver_news_ranking_url

if __name__ == "__main__":
    p = Parser()
    print("naver news ranking_url: ", p.naver_news_ranking_url)
    print("publishers: ", p.publishers)
    print("build_level: ", p.build_level)

    print(p.config)