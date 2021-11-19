import os
import unittest
from datetime import datetime
from pathlib import Path

from crawler.parser.module.naver_ranking_news import NaverRankingNews
from crawler.util.Logger import Logger
from crawler.util.conf_parser import Parser
from crawler.parser.publishers.publisher_names import PUBLISHERS


class Test_NaverRankingNews(unittest.TestCase):
	def setUp(self) -> None:
		root_path = Path(__file__).parent.parent.parent.parent.parent
		self.logger = Logger(path=os.path.join(root_path, "logs"), file_name=NaverRankingNews.__name__).logger

		p = Parser()
		print(p.naver_news_ranking_url)
		print(p.publishers)
		self.n1 = NaverRankingNews(url=p.naver_news_ranking_url,
							  publishers=['MBC', 'SBS', 'TV조선', '채널A', 'MBN', '중앙일보', '조선일보', '동아일보', '한겨레'],
							  the_date=datetime.now())
	def test_make_news_id(self):
		publisher_name = 'TV조선'
		url = "http://news.tvchosun.com/site/data/html_dir/2021/11/17/2021111790043.html"
		news_id = self.n1.make_news_id(publisher_name=publisher_name, url=url)

		check_publisher_nm = PUBLISHERS.get(publisher_name)
		if (check_publisher_nm is not None) and (check_publisher_nm !="jtbc"):
			check_publisher_nm = check_publisher_nm.lower() +"_"
		else:
			check_publisher_nm = ""


		self.assertEqual(check_publisher_nm+"2021111790043", news_id)

if __name__ == "__main__":
	suite = unittest.TestLoader().loadTestsFromTestCase(Test_NaverRankingNews)
	result = unittest.TextTestRunner(verbosity=2).run(suite)