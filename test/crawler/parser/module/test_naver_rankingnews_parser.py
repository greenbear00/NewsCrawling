import os
import unittest
from datetime import datetime
from pathlib import Path
from crawler.parser.module.naver_rankingnews_parser import NaverRankingNewsParser
from crawler.util.Logger import Logger
from crawler.util.conf_parser import Parser


class TestNaverRankingParser(unittest.TestCase):
	def setUp(self) -> None:
		self.logger = Logger(file_name=NaverRankingNewsParser.__name__).logger

		self.p = Parser()

	def test_naver_ranking_news_parser(self):
		ranking_news_li = []
		try:
			for ranking_broadcaster_url in self.p.broadcaster_urls_li[:1]:
				crawler = NaverRankingNewsParser(url=ranking_broadcaster_url, the_date=datetime.now(),
													  proxy=self.p.proxy if self.p.build_level == 'prod' else None)
				ranking_news_li.extend(crawler.run())
		except Exception as es:
			self.logger.error(f"error = {es}")

		# for news in ranking_news_li:
		# 	print(news)

		self.assertEqual(len(ranking_news_li), 20, "failed the naver ranking news")


if __name__ == "__main__":
	suite = unittest.TestLoader().loadTestsFromTestCase(TestNaverRankingParser)
	result = unittest.TextTestRunner(verbosity=2).run(suite)

	import sys

	print(f"unittest result: {result}")
	print(f"result.wasSuccessful()={result.wasSuccessful()}")
	# 정상종료는 $1 에서 0을 리턴함
	sys.exit(not result.wasSuccessful())