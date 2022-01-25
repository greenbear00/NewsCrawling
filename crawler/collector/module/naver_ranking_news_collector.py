from datetime import datetime
import time
from tqdm import tqdm

from crawler.parser.module.naver_rankingnews_parser import NaverRankingNewsParser
from crawler.collector.collector import Collector



class NaverRankingNewsCollector(Collector):

	def __init__(self):
		super().__init__(logger_name=self.__class__.__name__)
		self.broadcast_urls = self.p.broadcaster_urls_li
		self.press_urls = self.p.press_urls_li

	def _collect_ranking_news(self, urls:list, the_date:datetime, desc:str):
		collect_li = []
		try:
			for index in tqdm(range(len(urls)), desc=desc):
				a_url = urls[index]
			# for a_url in urls:
				crawler = NaverRankingNewsParser(url=a_url, the_date=the_date,
												 proxy=self.proxy)
				result = crawler.run()
				collect_li.extend(result)
		except Exception as es:
			self.logger.error(f"error = {es}")

		return collect_li


	def run(self, the_date: datetime)-> list:
		start_time = time.time()
		ranking_news_li = []
		try:
			ranking_news_li.extend(self._collect_ranking_news(self.broadcast_urls, the_date, "1st broadcast"))
			ranking_news_li.extend(self._collect_ranking_news(self.press_urls, the_date, "2st press"))
		except Exception as es:
			self.logger.error(f"error = {es}")

		# for f in ranking_news_li:
		# 	print(f)
		self.logger.info(f"랭킹뉴스 수집 대상 방송/통신군 수: {len(self.broadcast_urls)}")
		self.logger.info(f"랭킹뉴스 수집 대상 신문군 수 : {len(self.press_urls)}")
		self.logger.info(f"총 랭킹 뉴스 수집 건수(*20) : {len(ranking_news_li)}")

		self.logger.info(f"{self.__class__.__name__} Job Done (taken time {time.time()-start_time})")

		return ranking_news_li
