import os
import unittest
from pathlib import Path
import sys

from crawler.driver.chrome_driver import ChromeDriver
from crawler.util.Logger import Logger
from crawler.util.conf_parser import Parser

class TestChromeDriver(unittest.TestCase):
	def setUp(self) -> None:
		self.root_path = Path(__file__).parent.parent.parent.parent
		self.logger = Logger(path=os.path.join(self.root_path, "logs"), file_name=self.__class__.__name__).logger
		self.parser = Parser()
		# self.driver = ChromeDriver()

	def test_chrome_test(self):
		import time

		if self.parser.build_level == 'prod':
			d1 = ChromeDriver(proxy=self.parser.proxy)
		else:
			# for local
			d1 = ChromeDriver()
		print("chrome driver create")
		d1.browser.get(url="http://www.daum.net")
		from selenium.webdriver.common.by import By
		print(d1.browser.find_element(By.XPATH, '/html/head/meta[10]'))
		for n in range(0, 3):
			print("....")
			time.sleep(1)
		print(id(d1.browser))
		print("chrome driver test done")

if __name__ == "__main__":
	import sys
	suite = unittest.TestLoader().loadTestsFromTestCase(TestChromeDriver)
	result = unittest.TextTestRunner(verbosity=2).run(suite)

	print(f"unittest result: {result}")
	print(f"result.wasSuccessful()={result.wasSuccessful()}")
	# 정상종료는 $1 에서 0을 리턴함
	sys.exit(not result.wasSuccessful())
