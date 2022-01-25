import unittest
from datetime import datetime, timedelta

from crawler.util.Logger import Logger
from crawler.util.conf_parser import Parser
from crawler.elastic.analyzer.nori_analyzer import NoriAnalyzer


class TestNoriAnalyzer(unittest.TestCase):
	def setUp(self) -> None:
		self.logger = Logger(file_name=self.__class__.__name__).logger

		self.p = Parser()

		self.nori = NoriAnalyzer(**self.p.elastic_conf)

	def _get_ranking_news_li(self):
		ranking_news_li = [
			{'news_nm': '김건희 "바보같은 보수" 폄훼에…원팀·지지층 실망 우려', 'url': 'https://n.news.naver.com/article/003/0010948194',
			 'service_date': '2022-01-17T10:48:00+09:00', 'company': 'newsis', 'ranking_num': 1, 'platform': 'naver',
			 'reg_date': '2022-01-17T00:00:00+09:00'}]

		return ranking_news_li

	def test_run(self):
		the_date = datetime.now()
		data = self._get_ranking_news_li()
		result = self.nori.run(the_date, data)
		self.logger.info(result)

		self.assertEqual(list(result[0].keys()), ["news_nm", "url", "service_date", "company", "ranking_num",
												  "platform",
											"reg_date", "news_nm_analyzer"], "nori_analyzer not passed")



if __name__ == "__main__":
	suite = unittest.TestLoader().loadTestsFromTestCase(TestNoriAnalyzer)
	result = unittest.TextTestRunner(verbosity=2).run(suite)

	import sys

	print(f"unittest result: {result}")
	print(f"result.wasSuccessful()={result.wasSuccessful()}")
	# 정상종료는 $1 에서 0을 리턴함
	sys.exit(not result.wasSuccessful())