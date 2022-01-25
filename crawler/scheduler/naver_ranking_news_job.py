from datetime import datetime, timedelta
from crawler.util.Logger import Logger

logger = Logger(file_name="JOB_NaverRankingNews").logger
logger.info(f"\n\n\n\nstart...{datetime.now().strftime('%Y-%m-%d %H:%M:%S.%s')}")

from crawler.collector.module.naver_ranking_news_collector import NaverRankingNewsCollector
from crawler.util.conf_parser import Parser
from crawler.elastic.analyzer.nori_analyzer import NoriAnalyzer
from crawler.elastic.writer.module.naver_ranking_news_elastic_writer import NaverRankingNewsElasticWriter
from apscheduler.schedulers.background import BackgroundScheduler
import time
from crawler.util.common import *

sched = BackgroundScheduler(timezone="Asia/Seoul")

# @sched.scheduled_job('cron', minute='10,25', second=0, id="update_news_time", name="update_news_time")
# @sched.scheduled_job('interval', minutes=10, id="update_news_time", name="update_news_time")
@sched.scheduled_job('cron', hour='0, 6-23', minute='10,40', second=0, id="update_news_time", name="update_news_time")
def run():
	# 참고로 해당 job은 6-24시까지 매 1시간 간격으로 수행해야 함
	# root_path = Path(__file__).parent.parent.parent
	# pid_file_path = os.path.join(root_path, "CRAWER_PID")
	# create_pid(pid_file_path=pid_file_path)

	the_date = datetime.now()

	p = Parser()
	controller = NaverRankingNewsCollector()
	collect_ranking_news = controller.run(the_date)
	nori = NoriAnalyzer(**p.elastic_conf)
	new_collect_ranking_news = nori.run(the_date, collect_ranking_news)
	writer = NaverRankingNewsElasticWriter(**p.elastic_conf)
	writer.run(the_date, new_collect_ranking_news)

	print_joblist()


def print_joblist():
	logger.info(f"=================[ job info ]============================")
	for a_job in sched.get_jobs():
		logger.info(f"[job] {a_job.id} -> {a_job.next_run_time}\n\n")


def background_scheduler():
	root_path = Path(__file__).parent.parent.parent
	pid_file_path = os.path.join(root_path, "CRAWER_PID")
	create_pid(pid_file_path=pid_file_path)
	end_time = datetime.now() + timedelta(days=50, hours=10, minutes=10)

	sched.start()
	logger.info("\n\n\n\n")
	# run()
	print_joblist()

	while datetime.now() < end_time:
		time.sleep(1)

	sched.shutdown()


if __name__ == "__main__":
	background_scheduler()
