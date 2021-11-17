
from apscheduler.schedulers.background import BackgroundScheduler

from crawler.connector.module.NaverRankingElasticGenerator import NaverRankingElasticGenerator
from crawler.util.conf_parser import Parser
from crawler.util.Logger import Logger
from crawler.parser.module.naver_ranking_news import NaverRankingNews

from datetime import datetime, timedelta
import time
from pathlib import Path

sched = BackgroundScheduler(timezone="Asia/Seoul")
root_path = Path(__file__).parent.parent
logger = logger_factory = Logger(path=root_path, file_name="RankingNews_check_update_time").logger

p = Parser()
logger.info(f"start...{datetime.now().strftime('%Y-%m-%d %H:%M:%S.%s')}")


@sched.scheduled_job('cron', minute=10, second=0, id="update_news_time")
def run():
	the_date = datetime.now()
	ranking_news = NaverRankingNews(url=p.naver_news_ranking_url, publishers=p.publishers,
	                           the_date=the_date)
	ne = NaverRankingElasticGenerator(**p.elastic_conf, shard=p.elastic_shard)

	data = ranking_news.run()
	ne.write(the_date=the_date, data = data)

	print_joblist()


def print_joblist():
	for a_job in sched.get_jobs():
		logger.info(f"[job] {a_job.id} -> {a_job.next_run_time}\n\n")

def backgroundScheduler():

	end_time = datetime.now()+timedelta(days=3, hours=10, minutes=10)

	sched.start()
	run()
	print_joblist()


	while datetime.now()<end_time:
		time.sleep(1)

	sched.shutdown()

if __name__ == "__main__":

	backgroundScheduler()
