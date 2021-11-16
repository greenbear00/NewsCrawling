from crawler.connector.ElasticGenerator import ElasticGenerator
from datetime import datetime

from crawler.parser.module.naver_ranking_news import NaverRankingNews
from crawler.schema.SchemaGenerator import SchemaGenerator
from elasticsearch.helpers import bulk


class NaverRankingElasticGenerator(ElasticGenerator):
	def __init__(self, hosts:str, username:str, password:str, shard:int):
		super().__init__(hosts, username, password)

		self.sg = SchemaGenerator(obj=self, shard=shard)

	def _get_index(self, the_date):
		return 'ranking-news-hour-naver-test-'+the_date.strftime('%Y')


	def write(self, the_date:datetime, data:dict):
		index = self._get_index(the_date=the_date)
		template_name = 'ranking-news-hour-naver-template'
		template = self.sg.get_template(template_name=template_name)
		self.make_index_and_template(index_name=index, template_name=template_name, template=template)

		new_data = self.reformat_data(data=data)
		bulk(self.es, new_data, index=index, refresh="wait_for")

	def reformat_data(self, data:dict):
		elk_doc = []


		# 나중에 collecting_time 체크
		for k, v in data.items():
			elk_doc.extend(a_data for a_data in v.get('value'))

		return elk_doc





if __name__ == "__main__":
	from crawler.util.conf_parser import Parser
	p = Parser()

	data = {'JTBC': {'collecting_time': '오전 6시~7시까지 집계한 결과입니다.',
          'value': [{'_op_type': 'update',
                     '_id': 'article.aspx?news_id=NB12033702',
                     'doc_as_upsert': True,
                     'news_nm': "[단독] 모텔 복도 '음란행위', 본 사람 없어 무혐의? 판례는 달랐다",
                     'url': 'https://news.jtbc.joins.com/article/article.aspx?news_id=NB12033702',
                     'created_time': '2021-11-15T20:29:00+09:00',
                     'modified_time': None,
                     'view': 25192,
                     'reaction': 557,
                     'comment': None,
                     'platform': 'naver',
                     'reg_date': '2021-11-16T07:56:33+09:00',
                     'publisher': 'JTBC'},
                    {'_op_type': 'update',
                     '_id': 'article.aspx?news_id=NB12033706',
                     'doc_as_upsert': True,
                     'news_nm': '20년 넘게 찾던 엄마, 노숙인 시설서 발견…"형제복지원 판박이"',
                     'url': 'https://news.jtbc.joins.com/article/article.aspx?news_id=NB12033706',
                     'created_time': '2021-11-15T20:12:00+09:00',
                     'modified_time': None,
                     'view': 14786,
                     'reaction': 1720,
                     'comment': 268,
                     'platform': 'naver',
                     'reg_date': '2021-11-16T07:56:33+09:00',
                     'publisher': 'JTBC'},
                    {'_op_type': 'update',
                     '_id': 'article.aspx?news_id=NB12033713',
                     'doc_as_upsert': True,
                     'news_nm': "'껑충 뛴' 종부세 고지서 온다…다주택자 '두세배' 오를수도",
                     'url': 'https://news.jtbc.joins.com/article/article.aspx?news_id=NB12033713',
                     'created_time': '2021-11-15T19:45:00+09:00',
                     'modified_time': None,
                     'view': 13318,
                     'reaction': 1179,
                     'comment': None,
                     'platform': 'naver',
                     'reg_date': '2021-11-16T07:56:33+09:00',
                     'publisher': 'JTBC'}]
                    },
	        '중앙일보': {'collecting_time': '오전 6시~7시까지 집계한 결과입니다.',
          'value': [{'_op_type': 'update',
                     '_id': '25023899',
                     'doc_as_upsert': True,
                     'news_nm': '회사 판 돈 70억 카카오엔터 넣은 유희열···유재석은 거절, 왜',
                     'url': 'https://www.joongang.co.kr/article/25023899',
                     'created_time': '2021-11-15T18:10:00+09:00',
                     'modified_time': '2021-11-15T19:14:00+09:00',
                     'view': 62553,
                     'reaction': 1572,
                     'comment': 470,
                     'platform': 'naver',
                     'reg_date': '2021-11-16T07:56:33+09:00',
                     'publisher': '중앙일보'},
                    {'_op_type': 'update',
                     '_id': '25024000',
                     'doc_as_upsert': True,
                     'news_nm': '"눈 멀고 손가락 잘렸다"…\'야인시대\' 시라소니 근황',
                     'url': 'https://www.joongang.co.kr/article/25024000',
                     'created_time': '2021-11-16T00:11:00+09:00',
                     'modified_time': '2021-11-16T06:34:00+09:00',
                     'view': 43742,
                     'reaction': 773,
                     'comment': 112,
                     'platform': 'naver',
                     'reg_date': '2021-11-16T07:56:33+09:00',
                     'publisher': '중앙일보'},
                    {'_op_type': 'update',
                     '_id': '25024030',
                     'doc_as_upsert': True,
                     'news_nm': "'죽음의 땅' 체르노빌 반전...강남역보다 방사능 수치 낮았다 [영상]",
                     'url': 'https://www.joongang.co.kr/article/25024030',
                     'created_time': '2021-11-16T05:02:00+09:00',
                     'modified_time': '2021-11-16T06:29:00+09:00',
                     'view': 37791,
                     'reaction': 275,
                     'comment': 140,
                     'platform': 'naver',
                     'reg_date': '2021-11-16T07:56:33+09:00',
                     'publisher': '중앙일보'},
                    {'_op_type': 'update',
                     '_id': '25023931',
                     'doc_as_upsert': True,
                     'news_nm': '"아빠가 절 끌어안았어요" 추락 비행기서 홀로 생존한 소녀',
                     'url': 'https://www.joongang.co.kr/article/25023931',
                     'created_time': '2021-11-15T21:31:00+09:00',
                     'modified_time': None,
                     'view': 23521,
                     'reaction': 996,
                     'comment': 123,
                     'platform': 'naver',
                     'reg_date': '2021-11-16T07:56:33+09:00',
                     'publisher': '중앙일보'},
                    {'_op_type': 'update',
                     '_id': '25024021',
                     'doc_as_upsert': True,
                     'news_nm': '바닷속 6.9㎞ 달린다...11년만에 완공된 보령해저터널 가보니 [영상]',
                     'url': 'https://www.joongang.co.kr/article/25024021',
                     'created_time': '2021-11-16T05:01:00+09:00',
                     'modified_time': '2021-11-16T06:28:00+09:00',
                     'view': 21367,
                     'reaction': 69,
                     'comment': 24,
                     'platform': 'naver',
                     'reg_date': '2021-11-16T07:56:33+09:00',
                     'publisher': '중앙일보'},
                    {'_op_type': 'update',
                     '_id': '25024011',
                     'doc_as_upsert': True,
                     'news_nm': "[단독]취준생 죽음 몬 '김민수 검사', 中공안 체포됐다 풀려나[강주안 논설위원이 "
                                '간다]',
                     'url': 'https://www.joongang.co.kr/article/25024011',
                     'created_time': '2021-11-16T00:33:00+09:00',
                     'modified_time': '2021-11-16T06:31:00+09:00',
                     'view': 13007,
                     'reaction': 124,
                     'comment': 40,
                     'platform': 'naver',
                     'reg_date': '2021-11-16T07:56:33+09:00',
                     'publisher': '중앙일보'}]
	                 }
	        }
	print(p.naver_news_ranking_url)
	print(p.publishers)
	n1 = NaverRankingNews(url=p.naver_news_ranking_url, publishers=p.publishers, the_date=datetime.now())
	# n2 = NaverRankingNews(url=p.naver_news_ranking_url, publishers=p.publishers, the_date=datetime.now())
	#
	# print(id(n1))
	# print(id(n2))

	data = n1.run()
	# the_date = datetime.now().replace(year=2021, month=11, day=15, hour=15, minute=21)
	the_date = datetime.now()
	ne = NaverRankingElasticGenerator(**p.elastic_conf, shard=p.elastic_shard)
	ne.write(the_date=the_date, data=data)
	# ne.reformat_data(data)
