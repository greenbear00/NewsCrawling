import unittest
from datetime import datetime, timedelta

from crawler.util.Logger import Logger
from crawler.util.conf_parser import Parser
from crawler.elastic.loader.module.naver_ranking_news_loader import NaverRankingNewsElasticLoader


class TestNaverRankingNewsElasticLoader(unittest.TestCase):
	def setUp(self) -> None:
		self.logger = Logger(file_name=self.__class__.__name__).logger

		self.p = Parser()

		self.loader = NaverRankingNewsElasticLoader(**self.p.elastic_conf)

	def test_run(self):
		# the_date로 지정한 날짜에 대해서 prefix_index (naver-ranking-news-hour-YYYY)에 해당하는 데이터를
		# 			scroll해서 가져와서 nori_analyzer를 적용해서 upsert 수행
		start_date = datetime.now().replace(year=2022, month=1, day=19, hour=0, minute=0, second=0, microsecond=0)
		end_date = datetime.now()

		flag = True
		while start_date <= end_date:
			flag = self.loader.run(start_date)
			if not flag:
				break
			start_date = start_date + timedelta(days=1)
		self.assertEqual(flag, True, f"{start_date} upsert error")


if __name__ == "__main__":
	suite = unittest.TestLoader().loadTestsFromTestCase(TestNaverRankingNewsElasticLoader)
	result = unittest.TextTestRunner(verbosity=2).run(suite)

	import sys

	print(f"unittest result: {result}")
	print(f"result.wasSuccessful()={result.wasSuccessful()}")
	# 정상종료는 $1 에서 0을 리턴함
	sys.exit(not result.wasSuccessful())