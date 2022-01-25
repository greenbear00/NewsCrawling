from crawler.schema.SchemaGenerator import SchemaGenerator
from crawler.elastic.ElasticGenerator import ElasticGenerator
from datetime import datetime

class NoriAnalyzer(ElasticGenerator):
	def __init__(self, hosts:str, username:str, password:str):
		super(NoriAnalyzer, self).__init__(hosts, username, password)
		# self.nori_analyzer_update_flag = nori_analyzer_update_flag
		self.sg = SchemaGenerator(obj=self)

	def _update_index_setting(self):
		template_name = "nori-analyzer-template"
		# prefix index_name = "my-nori-analyzer"
		setting_template, index_name = self.sg.get_small_template(template_name)

		# 기존 my_analyzer의 filter에 "lowercase"를 지움 -> LG엔솔 -> lg 엔솔로 분석되어져 나옴
		self.create_index_with_setting(index_name=index_name, setting=setting_template)
		return index_name

	def scroll_update(self, data:list):
		index_name = self._update_index_setting()

		text = []
		text_position = []
		before_position = 0
		for a_data in data:
			source = a_data.get('_source')
			news_nm = source.get('news_nm')
			news_nm_size = len(news_nm)
			text_position.append(before_position)
			text.append(news_nm)
			before_position += (news_nm_size + 1)
		text_position.append(before_position)
		body = {
			"analyzer": "my_analyzer",
			"text": text
		}
		res2 = self.es_client.indices.analyze(index=index_name, body=body)

		tokens = []
		for index in range(1, len(text_position)):  # start 31
			# for a_token in res2.get('tokens'):
			# 	print(f"{text_position[index - 1]} <= {a_token.get('start_offset')} and"
			# 		  f" {text_position[index]} > {a_token.get('end_offset')} =====> {text_position[index - 1] <= a_token.get('start_offset') and text_position[index] > a_token.get('end_offset')}")
			filtered_tokens = list(filter(lambda x: text_position[index - 1] <= x.get('start_offset') and text_position[
				index] > x.get('end_offset'), res2.get('tokens')))
			tokens.append([a_token.get('token') for a_token in filtered_tokens])

		new_data = data.copy()
		for index in range(len(new_data)):
			source = new_data[index].get('_source')
			source.update({"news_nm_analyzer": tokens[index]})
			new_data[index].update(source)

		return new_data


	def run(self, the_date:datetime, data:list)->list:
		"""
		index_name = my-nori-analyzer
		"""

		index_name = self._update_index_setting()

		text = []
		text_position = []
		before_position = 0
		for a_data in data:
			news_nm = a_data.get('news_nm')
			news_nm_size = len(news_nm)
			text_position.append(before_position)
			text.append(news_nm)
			before_position += (news_nm_size + 1)
		text_position.append(before_position)
		body = {
			"analyzer": "my_analyzer",
			"text": text
		}
		res2 = self.es_client.indices.analyze(index=index_name, body=body)

		tokens = []
		for index in range(1, len(text_position)):  # start 31
			# for a_token in res2.get('tokens'):
			# 	print(f"{text_position[index - 1]} <= {a_token.get('start_offset')} and"
			# 		  f" {text_position[index]} > {a_token.get('end_offset')} =====> {text_position[index - 1] <= a_token.get('start_offset') and text_position[index] > a_token.get('end_offset')}")
			filtered_tokens = list(filter(lambda x: text_position[index - 1] <= x.get('start_offset') and text_position[
				index] > x.get('end_offset'), res2.get('tokens')))
			tokens.append([a_token.get('token') for a_token in filtered_tokens])

		new_data = data.copy()
		for index in range(len(new_data)):
			new_data[index].update({"news_nm_analyzer": tokens[index]})

		return new_data






