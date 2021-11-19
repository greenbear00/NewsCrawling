from selenium.webdriver.common.by import By
import time
from datetime import datetime
from crawler.parser.CrawlerParser import CrawlerParser


class NaverRankingNews(CrawlerParser):
	"""
		우선 확인한 바로는 대략 매시 08분 사이에 처리가 됨. (08분 사이에 처리 되는듯)
		2021-11-15 11:07:52,971 [INFO] - naver_ranking_news.py:_click_more_publisher - line:119 - 2021-11-15 11:07:52.1636942072: 오전 9시~10시까지 집계한 결과입니다.
		2021-11-15 11:08:53,007 [INFO] - naver_ranking_news.py:_click_more_publisher - line:119 - 2021-11-15 11:08:53.1636942133: 오전 10시~11시까지 집계한 결과입니다.
	"""

	def __del__(self):
		print("NaverRnakingNews deleted")

	def __init__(self, url: str, publishers: list, the_date: datetime, is_enable: bool = True):

		super().__init__(url=url, publishers=publishers, the_date=the_date, is_enable=is_enable)

		self.logger.info(f"naver ranking news url = {self.url}")

		self._publisher = {}

	def run(self) -> dict:
		"""

		:return:
			예) {'JTBC': {
						'collecting_time': '오후 1시~2시까지 집계한 결과입니다.',
                        'value': [
                                    {
                                    'id': 'JTBC_20211115T14_1',
                                    'title': '"화이자 맞은 고3 동생, 수능 대신 항암치료 받게 됐다"',
                                    ....
                                    },
                                    ...
                                 ]
                        }
                }

		"""
		result = self._get_all_publishers_info(url=self.url, publishers=self.check_publishers)

		self.logger.info(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S.%s')} was done.")
		return result

	@property
	def publisher(self):
		return self._publisher

	def _find_publisher(self):
		publishers = self.browser.find_elements(By.CLASS_NAME, "rankingnews_box_head")
		for a_publisher in publishers:
			self._publisher[a_publisher.text] = a_publisher

	def _get_all_publishers_info(self, url: str, publishers: list) -> dict:

		# elastic에 보낼 데이터
		# '_op_type': "update",
		# '_id' : 언론사key_YYYYMMDD_HH_{ranking},
		# "doc_as_upsert": True,
		# "doc": {
		#   news_nm
		#   create_time, modified_time
		#   view, reaction, comment
		# }
		publishers_set = {}

		start_time = time.time()

		for publisher_name in publishers:
			self.logger.info(f"================ [{publisher_name}] ================")
			if not self.publisher:
				self.browser.get(url)
				collecting_time_str = self._click_more_publisher()
				self._find_publisher()
			a_publisher = self.publisher.get(publisher_name)
			a_publisher.click()
			a_publisher_result = self._load_rankingnews_list(publichser_name=publisher_name)
			publishers_set[publisher_name] = {
				'collecting_time': collecting_time_str,
				'value': a_publisher_result
			}
			time.sleep(2)

			self._publisher = {}
			print()

		self.logger.info(f"taken time: {time.time() - start_time}")

		self.browser.close()

		return publishers_set

	def _load_rankingnews_list(self, publichser_name: str) -> list:

		a_publisher_info = []

		ranking_news_em = self.browser.find_element(By.XPATH, "/html/body/div/div[4]/div[2]/div[2]/ul")

		# 많이 본 뉴스 <ul> 밑에 있는 <li></li>에 해당하는 부
		list_content = ranking_news_em.find_elements(By.CLASS_NAME, "list_content")
		ranking_news_size = len(list_content)
		for index in range(1, ranking_news_size + 1):
			# id = f"{publisher_key}_{self.the_date.strftime('%Y%m%dT%H')}_{index}"
			# self.logger.info(f"[{index}] id = {id}")

			# ranking index에 해당하는 a href이며, text가 뉴스 title
			a_href = self.browser.find_element(By.XPATH,
			                                   f"/html/body/div/div[4]/div[2]/div[2]/ul/li[{str(index)}]/div/a")
			title = a_href.text

			# ranking index에 해당하는 span이며, view 정보를 집계
			a_span = self.browser.find_element(By.XPATH,
			                                   f'//*[@id="wrap"]/div[4]/div[2]/div[2]/ul/li[{str(index)}]/div/span[2]')
			view = int(a_span.text.replace(',','')) if a_span.text else None
			a_href.click()

			# <a href="https://news.jtbc.joins.com/article/article.aspx?news_id=NB12033568" target="_blank"
			# class="btn_artialoriginal nclicks(are.ori,'437', 'nilGParam', '437_59b7528403f0247c')">기사원문</a>
			a_news_href = self.browser.find_element(By.XPATH, '//*[@id="main_content"]/div[1]/div[3]/div/a[1]')
			a_news_ori_href = a_news_href.get_property('href')
			id = a_news_ori_href.split("/")[-1]
			self.logger.info(f"[{index}] id = {id}")
			self.logger.info(f"\t- news_nm: {title}")
			self.logger.info(f"\t- view: {view}")
			self.logger.info(f"\t- url: {a_news_ori_href}")
			a_news_timestamp = self.browser.find_elements(By.CLASS_NAME, "t11")

			a_news_created_time = datetime.strptime(a_news_timestamp[0].text.replace('오전', 'AM').replace('오후', 'PM'), '%Y.%m.%d. %p %I:%M').strftime('%Y-%m-%dT%H:%M:%S+09:00')
			a_news_modified_time = datetime.strptime(a_news_timestamp[1].text.replace('오전', 'AM').replace('오후', 'PM'), '%Y.%m.%d. %p %I:%M').strftime(
				'%Y-%m-%dT%H:%M:%S+09:00') if len(a_news_timestamp) > 1 else None
			self.logger.info(f"\t- created time: {a_news_created_time}")
			self.logger.info(f"\t- modified time: {a_news_modified_time}")
			a_news_reaction = self.browser.find_element(By.XPATH,
			                                   '//*[@id="main_content"]/div[1]/div[3]/div/div[3]/div[1]/div/a/span[3]')
			a_news_comment = self.browser.find_element(By.CLASS_NAME, "lo_txt")
			a_news_reaction_cnt = None if not a_news_reaction.text else 0 if a_news_reaction.text=="공감" else int(a_news_reaction.text.replace(',',''))
			a_news_comment_cnt = None if not a_news_comment.text else 0 if a_news_comment.text=="댓글" else int(
				a_news_comment.text.replace(',',''))
			self.logger.info(f"\t- reaction: {a_news_reaction_cnt}")
			self.logger.info(f"\t- comment: {a_news_comment_cnt}")

			a_publisher_info.append({
				'_op_type': "update",
				'_id': id,
				"doc_as_upsert": True,
				"doc": {
					"news_nm": title,
					"url": a_news_ori_href,
					"created_time": a_news_created_time,
					"modified_time": a_news_modified_time,
					"view": view,
					"reaction": a_news_reaction_cnt,
					"comment": a_news_comment_cnt,
					"platform": "naver",
					"reg_date": self.the_date.strftime('%Y-%m-%dT%H:%M:%S+09:00'),
					"publisher": publichser_name
				}
			})

			self.browser.back()
		return a_publisher_info

	def _click_more_publisher(self, is_enable=True) -> str:

		self.browser.find_element(By.XPATH, '//*[@id="wrap"]/div[4]/div[1]/button').click()
		ranking_news_time = self.browser.find_element(By.XPATH, '//*[@id="wrap"]/div[4]/div[1]/div').text
		ranking_news_time_str = ranking_news_time[:ranking_news_time.find('.') + 1]
		self.logger.info(
			f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S.%s')}: {ranking_news_time_str}")

		# 아래 button에 대한 xpath
		# <button type="button" class="button_rankingnews_more _moreButton nclicks(RBP.more)">다른 언론사 랭킹 더보기</button>
		# xpath: /html/body/div/div[4]/button
		# WebElement(button)
		while is_enable:
			button = self.browser.find_element(By.XPATH, "/html/body/div/div[4]/button")
			if button.aria_role == "button" and button.tag_name == "button":
				button.click()
			else:
				break

		return ranking_news_time_str


if __name__ == "__main__":
	from crawler.util.conf_parser import Parser
	import pprint

	p = Parser()
	print(p.naver_news_ranking_url)
	print(p.publishers)
	n1 = NaverRankingNews(url=p.naver_news_ranking_url, publishers=p.publishers, the_date=datetime.now())
	# n2 = NaverRankingNews(url=p.naver_news_ranking_url, publishers=p.publishers, the_date=datetime.now())
	#
	# print(id(n1))
	# print(id(n2))

	result = n1.run()
	pprint.pp(result)
