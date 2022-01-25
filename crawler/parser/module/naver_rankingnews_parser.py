from crawler.parser.CrawlerParser import CrawlerParser
from selenium.webdriver.common.by import By
from datetime import datetime, timedelta
import time


class NaverRankingNewsParser(CrawlerParser):
	def __init__(self, url: str, the_date: datetime, proxy: str = None, is_enable: bool = True):
		super().__init__(url=url, the_date=the_date, proxy=proxy, is_enable=is_enable, publishers=None)

	# self.logger.info(f"naver ranking news url = {self.url}")
	# self.logger.info(f"crawler publishers = {self.check_publishers}")

	# def __del__(self):
	# 	self.logger.info(f"deleted NaverRankingNewsParser instance (url={self.url})")

	# 브라우저를 닫고 프로세스도 종료
	# self.browser.quit()
	# self.logger.info(f"deleted NaverRankingNewsParser browser instance (url={self.url})")

	def run(self)-> list:
		ranking_info = []
		try:

			now_time = self.the_date.strftime("%Y-%m-%dT%H:00:00+09:00")
			self.logger.info(f"now_time = {now_time}")
			self.logger.info(f"crawling url = {self.url}")

			self.browser.get(self.url)
			self.browser.implicitly_wait(10)
			ranking_news = self.browser.find_element(By.XPATH,
													 "/html/body/div[2]/div/section[1]/header/div[4]/div/div[2]/div[1]/div[1]/h3/a")
			ranking_company = ranking_news.text
			self.logger.info(f"name = {ranking_company}")
			# hangule_flag = self.is_hangul(ranking_company)
			# if hangule_flag:
			# 	# self.logger.info(f"company name is hangule : {ranking_company}")
			# 	ranking_company = self.company.get(ranking_company)


			# 네이버에서 랭킹뉴스 집계한 시간에 대한 text 정보가 있음 '//*[@id="ct"]/div[2]/div[1]'
			collect_time_info = self.browser.find_element(By.XPATH, '//*[@id="ct"]/div[2]/div[1]')
			naver_collect_time_info = collect_time_info.text
			self.logger.info(naver_collect_time_info)

			# todo ranking_news를 가져오는데 아래와 같은 이슈가 있으면 retry 시키기
			#  Message: stale element reference: element is not attached to the page document
			#   (Session info: chrome=97.0.4692.71)
			# 네이버에서 랭킹 뉴스 집계한 1-10 순위의 데이터
			result = []
			count = 0
			while len(result)!=10 and count<3:
				result = self._get_ranking_news(ranking_company=ranking_company, xpath='//*[@id="ct"]/div[2]/div['
																			 '2]/ul/li')
				count+=1
			ranking_info.extend(result)

			result = []
			count = 0
			while len(result) != 10 and count < 3:
				result = self._get_ranking_news(ranking_company=ranking_company, xpath='//*[@id="ct"]/div[2]/div['
																					   '3]/ul/li')
				count += 1
			ranking_info.extend(result)


			# ranking_info = self._get_ranking_news(ranking_company=ranking_company, xpath='//*[@id="ct"]/div[2]/div['
			# 																			 '2]/ul/li')

			# 네이버에서 랭킹뉴스 집계한 11-20 순위의 데이터 '//*[@id="ct"]/div[2]/div[3]/ul'
			# ranking_info.extend(self._get_ranking_news(ranking_company=ranking_company, xpath='//*[@id="ct"]/div[2]/div['
			# 																		   '3]/ul/li'))

		except Exception as es:
			self.logger.error(f"Error = {es}")
		finally:
			self.browser.close()
			self.browser.quit()

		return ranking_info

	def _go_a_href_link(self, xpath:str)-> dict:
		try:
			self.browser.implicitly_wait(10)
			a_rank_news_href_el = self.browser.find_element(By.XPATH, xpath)
			a_href = a_rank_news_href_el.get_attribute('href')
			if "?" in a_href:
				a_href_li = a_href.split("?")
				a_href = a_href_li[0]

			a_rank_news_href_el.click()
			# to solve: Message: stale element reference: element is not attached to the page document"
			time.sleep(1)

			self.browser.implicitly_wait(10)
			title_el = self.browser.find_element(By.XPATH, '//*[@id="ct"]/div[1]/div[2]/h2')
			title = title_el.text

			self.browser.implicitly_wait(10)
			create_time_el = self.browser.find_element(By.XPATH, '//*[@id="ct"]/div[1]/div[3]/div[1]/div[1]/span')
			create_time_str = create_time_el.text
			create_time_str2 = create_time_str.replace('오후', 'PM') if '오후' in create_time_str else \
				create_time_str.replace('오전', 'AM')
			create_dt = datetime.strptime(create_time_str2, '%Y.%m.%d. %p %I:%M')
			create_time = create_dt.strftime('%Y-%m-%dT%H:%M:%S+09:00')

			self.browser.back()

			a_href_link_info = {
				'news_nm': title,
				'url': a_href,
				'service_date': create_time	# 네이버 측에서 서비스 노출 시간
			}
		except Exception as es:
			raise

		return a_href_link_info

	def _get_ranking_news(self, ranking_company:str, xpath:str):
		ranking_info = []
		# 집계는 the_date 기준
		# 2022-01-13 15:42:56,518 ...... 오후 2시 ~ 3시까지 집계한 결과입니다. 총 누적수와 다를 수 있습니다.
		reg_date = (self.the_date - timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
		reg_date = reg_date.strftime('%Y-%m-%dT%H:%M:%S+09:00')
		# update_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S+09:00')
		try:
			if xpath.split("/")[-1] == "li":
				self.browser.implicitly_wait(10)
				ranking = self.browser.find_elements(By.XPATH, xpath+'[position()<=20]')
				# ul>li는 index가 1부터 시작함
				for index in range(1, len(ranking)+1):
					self.browser.implicitly_wait(10)
					# //*[@id="ct"]/div[2]/div[2]/ul/li[1]/a/em
					ranking_index_el = self.browser.find_element(By.XPATH, xpath+f"[{index}]/a/em")
					self.logger.info(f"{ranking_company} : {ranking_index_el.text}")
					ranking_num = int(float(ranking_index_el.text)) if ranking_index_el.text != '' else None

					a_href_info = self._go_a_href_link(xpath=xpath + f"[{index}]/a")

					# dict data:
					# - company
					# - ranking_num, news_nm, url, service_date
					# - reg_date, platform

					a_href_info.update({'company': ranking_company,
										'ranking_num': ranking_num,
										'platform':'naver',
										'reg_date':reg_date,
										# 'update_date': update_time
										})
					ranking_info.append(a_href_info)
		except Exception as es:
			self.logger.error(f"ERROR={es}")

		return ranking_info






if __name__ == "__main__":
	url = "https://media.naver.com/press/437/ranking" # jtbc
	url = 'https://media.naver.com/press/028/ranking' # 한글 테스트 (한겨례)
	url = 'https://media.naver.com/press/422/ranking'
	crawler = NaverRankingNewsParser(url=url, the_date=datetime.now(), proxy=None)
	crawler.run()
