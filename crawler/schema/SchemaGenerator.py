from pathlib import Path
import os

from crawler.util.Logger import Logger
import json


class SchemaGenerator:

	def __init__(self, obj:object, shard:int):
		root_path = Path(__file__).parent.parent
		self._schema_path = os.path.join(root_path, *["schema", obj.__class__.__name__])
		self._shard = shard

		self.logger = Logger(path=os.path.join(root_path, "logs"), file_name=type(self).__name__).logger

		self._templates = None

		if obj is None:
			self.logger.warning(ValueError('obj is None'))
			raise ValueError('obj is None')

		self._load_templates()
		if self.templates is None:
			self.logger.info(f"{obj.__class__.__name__} does not have index_patterns.")
		else:
			self.logger.info(f"loaded {obj.__class__.__name__}'s index_patterns")



	@property
	def templates(self):
		# 실제 등록된 templates의 key name을 리턴
		return self._templates

	def _load_templates(self) -> None:
		"""
		Class에 맞춰서 templates를 load하고, 이때 BUILD_LEVEL에 맞춰서
			- index_patterns의 template/settings/number_of_shards를 수정
		:return:
		"""
		import glob

		templates = {}

		json_files = glob.glob(f"{self._schema_path}/*.json")
		try:
			for file in json_files:
				with open(file) as json_file:
					self.logger.info(f"load index_pattern file path = {file}")
					json_data = json.load(json_file)
					filename = Path(file).stem

					self.logger.info(f"load index_pattern : {filename} ")

					template = json_data.get('template')
					if template:
						# update settings
						settings = template.get('settings')
						settings.update({'number_of_shards': self._shard})
						template.update({'settings': settings})
						self.logger.info(f"\tupdate {settings} in template.settings")

					json_data.update({'template': template})

				templates.update({filename: json_data})
		except Exception:
			# self.logger.error(f"Error: {traceback.format_exc()}")
			raise

		self._templates = templates

	def get_all_template_names(self):
		return list(self.templates.keys()) if self.templates else []

	def get_template(self, template_name):
		template = {}
		if template_name:
			template = self.templates.get(template_name) if self.templates else {}

		return template


if __name__ == "__main__":
	from crawler.util.conf_parser import Parser
	from crawler.connector.module.NaverRankingElasticGenerator import NaverRankingElasticGenerator
	p = Parser()
	sg = SchemaGenerator(NaverRankingElasticGenerator(**p.elastic_conf), shard=p.elastic_shard)
	print(sg.get_all_template_names())
	print(sg.get_template(template_name='ranking-news-hour-naver-template'))


