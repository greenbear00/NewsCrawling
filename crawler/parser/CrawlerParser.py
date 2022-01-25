from datetime import datetime
from crawler.driver.chrome_driver import ChromeDriver
from crawler.util.Logger import Logger
import abc
import re


class CrawlerParser(metaclass=abc.ABCMeta):

	@property
	def url(self):
		# 실제 crawler 대상
		return self._url

	@property
	def the_date(self):
		# 실제 crawler를 요청한 시간
		return self._the_date

	@property
	def is_enable(self):
		return self._is_enable

	def __init__(self, url: str, the_date: datetime, proxy: str = None, is_enable: bool = True,
				 publishers: list = None):
		self.logger = Logger(file_name=self.__class__.__name__).logger

		driver = ChromeDriver(proxy)
		self.browser = driver.browser

		self._url = url
		self._the_date = the_date
		self._is_enable = is_enable

		# self.check_publishers = publishers if isinstance(publishers, list) else [publishers]
		# self.company = {
		# 	'뉴시스' : 'newsis',
		# 	'연합뉴스TV': 'yonhapnewstv',
		# 	'채널A':'ichannela',
		# 	'TV조선':'tvchosun',
		# 	'뉴스1':'news1',
		# 	'중앙일보':'joongang',
		# 	'조선일보':'chosun',
		# 	'동아일보':'donga',
		# 	'한겨레':'hani',
		# 	'한국일보':'hankookilbo',
		# 	'세계일보':'segye',
		# 	'서울신문':'seoul',
		# 	'경향신문':'khan',
		# 	'국민일보':'kmib',
		# 	'문화일보':'munhwa'
		# }

	@abc.abstractmethod
	def run(self):
		self.logger.info(f"CrawlerParser created.")
		pass

	# def __del__(self):
	# # 브라우저 화면만 닫음
	# self.browser.close()
	# self.logger.info("CrawlerParser close")

	# # 브라우저를 닫고 프로세스도 종료
	# self.browser.quit()

	# def is_hangul(self, word):
	# 	reg = re.compile('[가-힣]+').findall(word)
	# 	if len(reg)==0:
	# 		# self.logger.info(reg)
	# 		self.logger.info(f"company name({word}) is english")
	# 		return False
	# 	else:
	# 		self.logger.info(f"company name({word}) is 한글명 회사")
	# 		return True