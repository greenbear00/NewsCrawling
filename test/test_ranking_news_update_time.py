
from apscheduler.schedulers.background import BackgroundScheduler

from crawler.connector.module.NaverRankingElasticGenerator import NaverRankingElasticGenerator
from crawler.util.conf_parser import Parser
from crawler.util.Logger import Logger
from crawler.parser.module.naver_ranking_news import NaverRankingNews

from datetime import datetime, timedelta
import time

sched = BackgroundScheduler(timezone="Asia/Seoul")
logger = logger_factory = Logger(file_name="RankingNews_check_update_time").logger

p = Parser()
logger.info(f"start...{datetime.now().strftime('%Y-%m-%d %H:%M:%S.%s')}")


@sched.scheduled_job('cron', minute=15, second=0, id="update_news_time")
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
		logger.info(f"\n\n[job] {a_job.id} -> {a_job.next_run_time}")

def backgroundScheduler():

	end_time = datetime.now()+timedelta(days=1, hours=1, minutes=10)

	sched.start()
	run()
	print_joblist()


	while datetime.now()<end_time:
		time.sleep(1)

	sched.shutdown()

if __name__ == "__main__":

	backgroundScheduler()
