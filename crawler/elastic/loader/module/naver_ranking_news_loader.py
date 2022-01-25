from crawler.elastic.ElasticGenerator import ElasticGenerator
from crawler.elastic.analyzer.nori_analyzer import NoriAnalyzer
from crawler.util.conf_parser import Parser


class NaverRankingNewsElasticLoader(ElasticGenerator):
	def __init__(self, hosts:str, username:str, password:str):
		super(NaverRankingNewsElasticLoader, self).__init__(hosts, username, password)
		self.p=Parser()
		self.nori = NoriAnalyzer(hosts, username, password)

	def _search_query_string(self):
		query = {
		  "query": {
			"bool": {
			  "must": [
				{
				  "query_string": {
					"default_field": "news_nm",
					"query": "lg"
				  }
				}
			  ],
			  "filter": [
				{
				  "range": {
					"reg_date": {
					  "gte": "2022-01-20T00:00:00+09:00",
					  "lte": "2022-01-20T23:59:59+09:00"
					}
				  }
				}
			  ]
			}
		  }
		}

	def run(self, the_date):
		"""
			the_date로 지정한 날짜에 대해서 prefix_index (naver-ranking-news-hour-YYYY)에 해당하는 데이터를
			scroll해서 가져와서 nori_analyzer를 적용해서 upsert 수행
		"""
		flag = True
		start_date = the_date.strftime("%Y-%m-%dT%H:%M:%S+09:00")
		end_date = the_date.strftime("%Y-%m-%dT%23:59:59+09:00")
		prefix_index = self.p.index_naver_ranking_news+f"-{the_date.year}"
		self.logger.info(f"{start_date} ~ {end_date} -> {prefix_index}")

		try:
			# body = {
			#   "query": {
			# 	"bool": {
			# 	  "filter": [
			# 		{
			# 		  "range": {
			# 			"reg_date": {
			# 			  "gte": start_date,
			# 			  "lte": end_date
			# 			}
			# 		  }
			# 		}
			# 	  ]
			# 	}
			#   }
			# }
			# res = self.es_client.indices.get(index=prefix_index,
			# 						   			body = body)

			body = {
				"size": 100,
				"query": {
					"range": {
						"reg_date": {
							"gte": start_date,
							"lte": end_date
						}
					}
				},
				"sort": [
					{
						"reg_date": {
							"order": "asc"
						}
					}
				]
			}
			# body2 = {
			# 	"query": {
			# 		"bool": {
			# 			"must": [
			# 				{
			# 					"term": {
			# 						"news_id": {
			# 							"value": "NB12035813"
			# 						}
			# 					}
			# 				}
			# 			],
			# 			"filter": [
			# 				{
			# 					"range": {
			# 						"reg_date": date_range
			# 					}
			# 				}
			# 			]
			# 		}
			# 	}
			# }
			# # access search context for 5 seconds before moving on to the next step, .
			scroll = '30s'
			response = self.es_client.search(index=prefix_index, body=body, scroll=scroll)

			scroll_id = response['_scroll_id']
			scroll_size = response['hits']['total']['value']

			while scroll_size > 0:
				new_mapping_jtbc_map = {}
				self.logger.info(f"<<< THE_DATE = {start_date} >>>")
				self.logger.info(f"scroll_size: {scroll_size}")
				# 해당 시간동안 수집한 news_id(list)
				analyzed_data = self.nori.scroll_update(response['hits']['hits'])
				for doc in analyzed_data:
					# 추가 메시지 update
					self.es_client.update(
						index=prefix_index,
						id=doc['_id'],
						body={
							"doc": doc.get('_source')
						}
					)

				response = self.es_client.scroll(scroll_id=scroll_id, scroll=scroll)

				scroll_id = response['_scroll_id']
				scroll_size = len(response['hits']['hits'])
				self.logger.info('\n\n\n')
		except Exception as es:
			self.logger.error(f"es = {es}")
			flag = False
		return flag

