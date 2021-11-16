from pathlib import Path
import os

from elasticsearch import Elasticsearch

from crawler.util.Logger import Logger
from crawler.util.Singleton import Singleton

class ElasticGenerator(metaclass=Singleton):
	def __init__(self, hosts:str, username:str, password:str):
		root_path = Path(__file__).parent.parent.parent

		self.logger = Logger(path=os.path.join(root_path, "logs"), file_name=type(self).__name__).logger
		self.logger.info(f"elastic url={hosts}, user_name={username}, password={password}")
		self.es = Elasticsearch(hosts, http_auth=(username, password), timeout=7800, max_retries=1,
		                        retry_on_timeout=True)

	def make_index_and_template(self, index_name:str, template_name:str, template:dict):
		try:
			if not self.es.indices.exists(index=index_name):
				# index_template와 index 생성

				self._create_index_pattern(template_name=template_name, template=template)
				self.logger.info(f"create index: {index_name}")
				self.es.indices.create(index=index_name)

				# alias 생성
				# (index 최초 생성시킬때 index_pattern과 index, alias를 최초로 한번 생성시킨다.)
				# self.create_alias(index_name=index_name, alias_name=alias_name)

			else:
				# index_template 생성
				self._create_index_pattern(template_name=template_name, template=template)

		# # alias 생성
		# self.create_alias(index_name=index_name, alias_name=alias_name)
		except Exception as es:
			self.logger.error(es)

	def _create_index_pattern(self, template_name, template):
		try:
			if template:
				if not self.es.indices.exists_index_template(template_name):
					# index_template 생성
					self.logger.info(f"create index_template: {template_name}")

					# put_index_template에서 create옵션이 default로 False가 되어 있어야 자동으로 index_pattern update
					self.es.indices.put_index_template(name=template_name, body=template)
			else:
				self.logger.warning(f"{template_name}'s template is None (index_template was not created.)")
		except Exception as es:
			self.logger.error(es)
