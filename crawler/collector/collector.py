from crawler.util.Logger import Logger
from datetime import datetime
import abc

from crawler.util.conf_parser import Parser


class Collector(metaclass=abc.ABCMeta):

	def __init__(self, logger_name: str):
		self.logger = Logger(file_name=logger_name).logger

		self.p = Parser()
		self.proxy = self.p.proxy if self.p.build_level == 'prod' else None

	@abc.abstractmethod
	def run(self, the_date:datetime):
		self.logger.info(f"Collector created.")
		pass
