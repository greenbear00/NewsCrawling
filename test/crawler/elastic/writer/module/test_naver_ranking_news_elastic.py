import unittest
from datetime import datetime

from crawler.parser.module.naver_rankingnews_parser import NaverRankingNewsParser
from crawler.util.Logger import Logger
from crawler.util.conf_parser import Parser
from crawler.elastic.analyzer.nori_analyzer import NoriAnalyzer
from crawler.elastic.writer.module.naver_ranking_news_elastic_writer import NaverRankingNewsElasticWriter


class TestNaverRankingNewsElastic(unittest.TestCase):
	def setUp(self) -> None:
		self.logger = Logger(file_name=self.__class__.__name__).logger

		self.p = Parser()
		# self.controller = NaverRankingNewsCollector()

	def _get_rankingnews(self, the_date):
		"for test: collector로부터 전체를 가져와야 하나, test용으로 1개의 사이트에 대한 랭킹뉴스 데이터를 제공"
		ranking_news_li = []
		try:
			# for ranking_broadcaster_url in self.p.broadcaster_urls_li:
			# for ranking_broadcaster_url in self.p.broadcaster_urls_li[:1]:
			# 	crawler = NaverRankingNewsParser(url=ranking_broadcaster_url,
			# 									 the_date=the_date,
			# 									 proxy=self.p.proxy if self.p.build_level == 'prod' else None)
			crawler = NaverRankingNewsParser(url='https://media.naver.com/press/422/ranking', the_date=the_date,
											 proxy=self.p.proxy if self.p.build_level == 'prod' else None)
			ranking_news_li.extend(crawler.run())
		except Exception as es:
			self.logger.error(f"error = {es}")

		return ranking_news_li

	def _tmp_get_ranking(self, the_date):
		ranking_news_li = [
			{'news_nm': '김건희 "바보같은 보수" 폄훼에…원팀·지지층 실망 우려', 'url': 'https://n.news.naver.com/article/003/0010948194',
			 'service_date': '2022-01-17T10:48:00+09:00', 'company': 'newsis', 'ranking_num': 1, 'platform': 'naver',
			 'reg_date': '2022-01-17T00:00:00+09:00'},
			{'news_nm': "김건희 녹취 효과…'스트레이트' 시청률 7배 폭등 17.4%", 'url': 'https://n.news.naver.com/article/003/0010947677',
			 'service_date': '2022-01-17T08:16:00+09:00', 'company': 'newsis', 'ranking_num': 2, 'platform': 'naver',
			 'reg_date': '2022-01-17T00:00:00+09:00'},
			{'news_nm': '정부 "전국 학원·마트·영화관 등 방역패스 해제"', 'url': 'https://n.news.naver.com/article/003/0010947788',
			 'service_date': '2022-01-17T09:01:00+09:00', 'company': 'newsis', 'ranking_num': 3, 'platform': 'naver',
			 'reg_date': '2022-01-17T00:00:00+09:00'}, {'news_nm': '내일부터 전국 마트·백화점 방역패스 해제…서울 외 지역, 오늘은 적용',
														'url': 'https://n.news.naver.com/article/003/0010948261',
														'service_date': '2022-01-17T11:00:00+09:00',
														'company': 'newsis', 'ranking_num': 4, 'platform': 'naver',
														'reg_date': '2022-01-17T00:00:00+09:00'},
			{'news_nm': '서울의소리 "김건희 녹취록, 괜히 MBC에 줬나 답답"…전체 파일 공개 예고',
			 'url': 'https://n.news.naver.com/article/003/0010948157', 'service_date': '2022-01-17T10:43:00+09:00',
			 'company': 'newsis', 'ranking_num': 5, 'platform': 'naver', 'reg_date': '2022-01-17T00:00:00+09:00'},
			{'news_nm': "LG엔솔 청약 D-1…증권사 계좌개설 '러시'", 'url': 'https://n.news.naver.com/article/003/0010948307',
			 'service_date': '2022-01-17T11:07:00+09:00', 'company': 'newsis', 'ranking_num': 6, 'platform': 'naver',
			 'reg_date': '2022-01-17T00:00:00+09:00'}, {'news_nm': '통가 해저 화산 폭발에 한때 일본·미국에 쓰나미 경보 발령 [뉴시스Pic]',
														'url': 'https://n.news.naver.com/article/003/0010948105',
														'service_date': '2022-01-17T10:32:00+09:00',
														'company': 'newsis', 'ranking_num': 7, 'platform': 'naver',
														'reg_date': '2022-01-17T00:00:00+09:00'},
			{'news_nm': '정몽규 HDC현산 회장 사퇴, "광주 사건 책임 통감… 피해자·가족에 머리 숙여 사죄" [뉴시스Pic]',
			 'url': 'https://n.news.naver.com/article/003/0010948342', 'service_date': '2022-01-17T11:16:00+09:00',
			 'company': 'newsis', 'ranking_num': 8, 'platform': 'naver', 'reg_date': '2022-01-17T00:00:00+09:00'},
			{'news_nm': '추미애 "길 잃은 보수정당이 김건희에 완전 접수" 시청소감', 'url': 'https://n.news.naver.com/article/003/0010947927',
			 'service_date': '2022-01-17T09:52:00+09:00', 'company': 'newsis', 'ranking_num': 9, 'platform': 'naver',
			 'reg_date': '2022-01-17T00:00:00+09:00'},
			{'news_nm': '우상호, 김건희 녹취 보도에 "보수 능멸하며 비하…되게 특이"', 'url': 'https://n.news.naver.com/article/003/0010948036',
			 'service_date': '2022-01-17T10:14:00+09:00', 'company': 'newsis', 'ranking_num': 10, 'platform': 'naver',
			 'reg_date': '2022-01-17T00:00:00+09:00'},
			{'news_nm': "14조도 부족하다?…대선 퍼주기 경쟁에 나라 곳간 '텅텅'", 'url': 'https://n.news.naver.com/article/003/0010948215',
			 'service_date': '2022-01-17T10:53:00+09:00', 'company': 'newsis', 'ranking_num': 11, 'platform': 'naver',
			 'reg_date': '2022-01-17T00:00:00+09:00'},
			{'news_nm': '윤석열 40.6%·이재명 36.7%·안철수 12.9%[리얼미터]', 'url': 'https://n.news.naver.com/article/003/0010947789',
			 'service_date': '2022-01-17T09:01:00+09:00', 'company': 'newsis', 'ranking_num': 12, 'platform': 'naver',
			 'reg_date': '2022-01-17T00:00:00+09:00'}, {'news_nm': '[일문일답]정몽규 "광주 화정아이파크, 완전철거 및 재시공도 고려"',
														'url': 'https://n.news.naver.com/article/003/0010948182',
														'service_date': '2022-01-17T10:45:00+09:00',
														'company': 'newsis', 'ranking_num': 13, 'platform': 'naver',
														'reg_date': '2022-01-17T00:00:00+09:00'},
			{'news_nm': '대장동 재판부 "정영학 녹취록으론 혐의·결백 다 입증 안돼"', 'url': 'https://n.news.naver.com/article/003/0010948361',
			 'service_date': '2022-01-17T11:22:00+09:00', 'company': 'newsis', 'ranking_num': 14, 'platform': 'naver',
			 'reg_date': '2022-01-17T00:00:00+09:00'}, {'news_nm': '국힘, \'김건희 녹취\' 보도 MBC에 "李 형수 욕설도 방송해야"',
														'url': 'https://n.news.naver.com/article/003/0010947877',
														'service_date': '2022-01-17T09:38:00+09:00',
														'company': 'newsis', 'ranking_num': 15, 'platform': 'naver',
														'reg_date': '2022-01-17T00:00:00+09:00'},
			{'news_nm': '이준석, 北 미사일 발사에 "文정부, 북 비위만 맞추니 이러는 것"',
			 'url': 'https://n.news.naver.com/article/003/0010948003', 'service_date': '2022-01-17T10:07:00+09:00',
			 'company': 'newsis', 'ranking_num': 16, 'platform': 'naver', 'reg_date': '2022-01-17T00:00:00+09:00'},
			{'news_nm': '윤석열 지지율 급등에…이재명·尹, 엎치락뒤치락(종합)', 'url': 'https://n.news.naver.com/article/003/0010947128',
			 'service_date': '2022-01-16T15:34:00+09:00', 'company': 'newsis', 'ranking_num': 17, 'platform': 'naver',
			 'reg_date': '2022-01-17T00:00:00+09:00'},
			{'news_nm': '광주 신축아파트 붕괴 일주일째…상층부 수색 초읽기', 'url': 'https://n.news.naver.com/article/003/0010947663',
			 'service_date': '2022-01-17T07:48:00+09:00', 'company': 'newsis', 'ranking_num': 18, 'platform': 'naver',
			 'reg_date': '2022-01-17T00:00:00+09:00'}, {'news_nm': "녹유 '오늘의 운세' 2022년 1월 18일 화요일(음력 12월 16일 신미)",
														'url': 'https://n.news.naver.com/article/003/0010947952',
														'service_date': '2022-01-17T10:00:00+09:00',
														'company': 'newsis', 'ranking_num': 19, 'platform': 'naver',
														'reg_date': '2022-01-17T00:00:00+09:00'},
			{'news_nm': "프랑스, '백신패스' 강화…미접종자 공공장소 전격 금지", 'url': 'https://n.news.naver.com/article/003/0010947644',
			 'service_date': '2022-01-17T06:50:00+09:00', 'company': 'newsis', 'ranking_num': 20, 'platform': 'naver',
			 'reg_date': '2022-01-17T00:00:00+09:00'}]

		return ranking_news_li

	def test_run(self):
		the_date = datetime.now()
		ranking_news_li = self._get_rankingnews(the_date)
		# ranking_news_li = self._tmp_get_ranking(the_date)
		nr_ewriter = NaverRankingNewsElasticWriter(**self.p.elastic_conf)
		nori = NoriAnalyzer(**self.p.elastic_conf)
		new_collect_ranking_news = nori.run(the_date, ranking_news_li)
		nr_ewriter.run(the_date, new_collect_ranking_news)


if __name__ == "__main__":
	suite = unittest.TestLoader().loadTestsFromTestCase(TestNaverRankingNewsElastic)
	result = unittest.TextTestRunner(verbosity=2).run(suite)

	import sys

	print(f"unittest result: {result}")
	print(f"result.wasSuccessful()={result.wasSuccessful()}")
	# 정상종료는 $1 에서 0을 리턴함
	sys.exit(not result.wasSuccessful())