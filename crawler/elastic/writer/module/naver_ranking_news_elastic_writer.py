from crawler.util.conf_parser import Parser
from crawler.elastic.ElasticGenerator import ElasticGenerator
from datetime import datetime, timedelta
from crawler.schema.SchemaGenerator import SchemaGenerator
from elasticsearch.helpers import bulk
from crawler.util.common import is_hangul


class NaverRankingNewsElasticWriter(ElasticGenerator):
	def __init__(self, hosts:str, username:str, password:str):
		super(NaverRankingNewsElasticWriter, self).__init__(hosts, username, password)
		self.p=Parser()

		self.sg = SchemaGenerator(obj=self)

	def run(self, the_date:datetime, data:list):
		# template_name: 'naver-ranking-news-hour-template'
		# index_name: 'origin-naver-ranking-news-hour-2022'
		# alias_name: 'naver-ranking-news-hour-2022'
		template_name, template, index_name, alias_name, aliases = \
			self.sg.get_template(the_date=the_date, template_name='naver-ranking-news-hour-template',
								 index_name=self.p.index_naver_ranking_news)

		self.logger.info(f"template_name: {template_name}")
		self.logger.info(f"index_name: {index_name}")
		self.logger.info(f"alias_name: {alias_name}")

		self.make_index_and_template(index_name=index_name,
									 template_name=template_name,
									 template=template,
									 alias_name=alias_name,
									 aliases=aliases)

		new_data = self.reformat_data(data=data, the_date=the_date)
		bulk(self.es_client, new_data, index=index_name, refresh="wait_for")

	def reformat_data(self, the_date:datetime, data:list):
		update_time = datetime.now().strftime('%Y-%m-%dT%H:%M:%S+09:00')
		# doc_id = reg_date.split("T")[0].replace("-", "") +"_"+ a_news.get('news_id')
		# 					elk_docs.append(
		# 						{
		# 							'_op_type': "update",
		# 							'_id': doc_id,
		# 							"doc_as_upsert": True,
		# 							"doc": a_news
		# 						}
		# 					)
		elk_doc = []


		# 회사 명은 모두 한글 또는 영문으로 하고, _id 값만 회사 명을 영문으로 변환하여 처리
		for a_data in data:
			a_data.update({'update_date': update_time})
			ranking_company = a_data.get('company')
			hangule_flag = is_hangul(ranking_company)
			if hangule_flag:
				# self.logger.info(f"company name is hangule : {ranking_company}")
				ranking_company = self.company.get(ranking_company)
				# a_data.update({'company': ranking_company})
			elk_doc.append(
				{
					'_op_type': "update",
					'_id': f"{ranking_company}_{the_date.strftime('%Y%m%d')}_"
						   f"{(the_date-timedelta(hours=1)).strftime('%H')}"
						   f"_{a_data.get('ranking_num')}",
					"doc_as_upsert": True,
					"doc": a_data
				}
			)
			# print({
			# 		'_op_type': "update",
			# 		'_id': f"{a_data.get('company')}_{str(the_date.hour).zfill(2)}_{a_data.get('ranking_num')}",
			# 		"doc_as_upsert": True,
			# 		"doc": a_data
			# 	})

		return elk_doc





