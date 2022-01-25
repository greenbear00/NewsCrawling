from crawler.util.Logger import Logger
import json
import os
from crawler.util.conf_parser import Parser
import traceback
from datetime import datetime
from pathlib import Path


class SchemaGenerator:
    ###################################################################################################
    #   index 관리 체계 (참고: alias 맵핑은 우선 수동으로 하기)
    #   - index 생성 규칙          : origin-hourly-summary-YYYY.MM (예: original-hourly-summary-2021.05)
    #   - alias 생성 규칙          : hourly-summary-YYYY.MM
    #   - index template 생성 규칙 : hourly-summary-template
    #                              (내부에 original-hourly-summary-*로 걸기)
    #   - (kibana) index pattern : hourly-summary-*
    #
    #  - 만약, doc 추가 작업하려면 hourly-summary-YYYY.MM.dd 이렇게 하기로...
    ##################################################################################################
    def __init__(self, obj:object):
        # super(SchemaGenerator, self).__init__()
        p = Parser()
        self.elastic_shard = p.elastic_shard
        self.root_path = p.root_path
        self._templates = None
        self.logger = Logger(file_name=type(self).__name__).logger

        if obj is None:
            self.logger.warning(ValueError('obj is None'))
            raise ValueError('obj is None')

        self.logger.info(f"loading index_patterns from {obj.__class__.__name__}")

        self._obj = obj

        self._schema_path = os.path.join(self.root_path, *['schema_json', f"{self._obj.__class__.__name__}"])

        self._templates = None

        self._load_templates()
        if not self.templates:
            self.logger.info(f"{obj.__class__.__name__} does not have index_patterns.")
        else:
            self.logger.info(f"loaded {obj.__class__.__name__}'s index_patterns")


    @property
    def templates(self):
        # 실제 등록된 templates의 key name을 리턴
        return self._templates

    def get_small_template(self, template_name:str):
        template = self.templates.get(template_name) if self.templates else None
        index_name = 'my-'+template_name.replace('-template', '')
        new_template = {'settings': template.get('settings')}
        return new_template, index_name


    def get_templates_name(self) -> str:
        return list(self.templates.keys()) if self.templates else None

    def get_template(self, the_date:datetime, template_name:str, index_name:str=None) -> (str, dict, str, str, dict):
        """
        template_name으로 생성할 index_pattern의 파일명(확장자 제외)을 넣으면,
        해당 index_pattern에 따르는 template_name과 index_pattern, 그리고 index명이 리턴됨

        주의) index명 규칙은 origin-{지표명}-YYYY.MM으로 정함
             참고: https://pri-confluence.joongang.co.kr/pages/viewpage.action?pageId=27549616
        :param the_date: datetime (index의 YYYY.MM을 생성하기 위해 필요한 인자)
        :param template_name: hourly-summary-template (json의 파일 명으로 확장자 제외)
        :param index_name: 'origin'이 붙어 있는 index_name이 있을 경우, 이를 통해 index_name을 생성
        :return:
            template_name(str), template(json), index_name(str), alias_name(str), aliases(dict)
        """
        template = {}
        if index_name:
            index_name = f"{index_name}-{the_date.strftime('%Y')}" if 'origin-' in index_name else f"origin-{index_name}-{the_date.strftime('%Y')}"
        elif template_name:
            index_name = f"origin-{template_name.replace('-template', '')}-{the_date.strftime('%Y')}"
        else:
            raise ValueError("index_name or template_name is none")

        if template_name:
            template = self.templates.get(template_name) if self.templates else None

        # setting aliases
        aliase = {
                    index_name : {
                        "aliases": {
                            f"{template_name.replace('-template', '')}-{the_date.strftime('%Y')}" : {
                                "is_write_index": True
                            }
                        }
                    }
        }
        alias_name = f"{template_name.replace('-template', '')}-{the_date.strftime('%Y')}"

        return template_name, template, index_name, alias_name, aliase


    def _load_templates(self)->None:
        """
        Class에 맞춰서 templates를 load하고, 이때 BUILD_LEVEL에 맞춰서
            - index_patterns의 template/settings/number_of_shards를 수정
        :return:
        """
        import glob
        from pathlib import Path

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
                        settings.update({'number_of_shards': self.elastic_shard})
                        # settings.update({"number_of_replicas": 1})
                        template.update({'settings':settings})
                        self.logger.info(f"\tupdate {settings} in template.settings")

                    json_data.update({'template':template})

                templates.update({filename: json_data})
        except Exception:
            # self.logger.error(f"Error: {traceback.format_exc()}")
            raise

        self._templates = templates








