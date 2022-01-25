import unittest
from pathlib import Path
from crawler.util.Logger import Logger
from crawler.util.conf_parser import Parser

class TestConfParser(unittest.TestCase):
	def setUp(self) -> None:
		self.root_path = Path(__file__).parent.parent.parent.parent
		self.logger = Logger(file_name=self.__class__.__name__).logger
		self.parser = Parser()

	def test_naver_ranking_news(self):
		self.logger.info(f"broadcaster_urls = {self.parser.broadcaster_urls_li}")
		self.logger.info(f"press_urls = {self.parser.press_urls_li}")

		flag = True if len(self.parser.broadcaster_urls_li) > 0 and len(self.parser.press_urls_li) > 0 else False
		self.assertEqual(flag, True, "not load naver ranking news urls")

if __name__ == "__main__":
	suite = unittest.TestLoader().loadTestsFromTestCase(TestConfParser)
	result = unittest.TextTestRunner(verbosity=2).run(suite)

	import sys

	print(f"unittest result: {result}")
	print(f"result.wasSuccessful()={result.wasSuccessful()}")
	# 정상종료는 $1 에서 0을 리턴함
	sys.exit(not result.wasSuccessful())
