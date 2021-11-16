from pathlib import Path
from datetime import datetime

from crawler.driver.chrome_driver import ChromeDriver
from crawler.util.Logger import Logger
import abc


class CrawlerParser(metaclass=abc.ABCMeta):

	@property
	def url(self):
		return self._url

	@property
	def the_date(self):
		return self._the_date

	@property
	def is_enable(self):
		return self._is_enable

	def __init__(self, url: str, publishers: list, the_date:datetime, is_enable: bool = True):
		path = Path(__file__).parent.parent.parent
		self.logger = Logger(file_name=self.__class__.__name__).logger

		driver = ChromeDriver()
		self.browser = driver.browser

		self._url = url
		self._the_date = the_date
		self._is_enable = is_enable

		self.check_publishers = publishers if isinstance(publishers, list) else [publishers]

	@abc.abstractmethod
	def run(self):
		pass