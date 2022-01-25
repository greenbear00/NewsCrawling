
import unittest
import sys
from crawler.util.Logger import Logger
from crawler.schema.SchemaGenerator import SchemaGenerator

class TestSchemaGenerator(unittest.TestCase):
	def setUp(self) -> None:
		self.logger = Logger(file_name=self.__class__.__name__).logger


	def test_naver_rankingnews_sg(self):
		from crawler.elastic.writer.module.naver_ranking_news_elastic_writer import NaverRankingNewsElasticWriter
		from crawler.util.conf_parser import Parser
		p = Parser()
		nr = NaverRankingNewsElasticWriter(**p.elastic_conf)
		sg = SchemaGenerator(obj = nr)

		self.assertEqual(list(sg.templates.keys())[0], 'naver-ranking-news-hour-template',
								'naver-ranking-news-hour-template is None')


if __name__ == "__main__":
	suite = unittest.TestLoader().loadTestsFromTestCase(TestSchemaGenerator)
	result = unittest.TextTestRunner(verbosity=2).run(suite)
	print(f"unittest result: {result}")
	print(f"result.wasSuccessful()={result.wasSuccessful()}")
	# 정상종료는 $1 에서 0을 리턴함
	sys.exit(not result.wasSuccessful())
