import unittest
from datetime import datetime
from crawler.collector.module.naver_ranking_news_collector import NaverRankingNewsCollector
from crawler.util.Logger import Logger
from crawler.util.conf_parser import Parser


class TestNaverRankingNewsController(unittest.TestCase):
	def setUp(self) -> None:
		self.logger = Logger(file_name=self.__class__.__name__).logger

		self.p = Parser()
		self.controller = NaverRankingNewsCollector()

	def test_run(self):
		self.controller.run(the_date=datetime.now())

if __name__ == "__main__":

	suite = unittest.TestLoader().loadTestsFromTestCase(TestNaverRankingNewsController)
	result = unittest.TextTestRunner(verbosity=2).run(suite)
	import sys
	print(f"unittest result: {result}")
	print(f"result.wasSuccessful()={result.wasSuccessful()}")
	# 정상종료는 $1 에서 0을 리턴함
	sys.exit(not result.wasSuccessful())