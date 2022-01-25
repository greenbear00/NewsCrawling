import os
from crawler.util.Logger import Logger
from pathlib import Path
import psutil  # 실행중인 프로세스 및 시스템 활용 라이브러리
import re


root_path = Path(__file__).parent.parent.parent
logger = Logger(path=os.path.join(root_path, "logs"),
				file_name="Common").logger

def is_hangul(word):
	reg = re.compile('[가-힣]+').findall(word)
	if len(reg) == 0:
		# self.logger.info(reg)
		# self.logger.info(f"company name({word}) is english")
		return False
	else:
		# self.logger.info(f"company name({word}) is 한글명 회사")
		return True

def _delete_process(pid:int):
	if pid is not None:
		current_process = [proc for proc in psutil.process_iter() if proc.pid == pid]
		if current_process:
			try:
				for proc in current_process:
					processName = proc.name()
					processID = proc.pid
					logger.info(f"{processName} - {processID} is running..")
					parent_pid = processID  # PID
					parent = psutil.Process(parent_pid)  # PID 찾기
					for child in parent.children(recursive=True):  # 자식-부모 종료
						child.kill()
						logger.info(f"{processName}({processID}) kill child pid")
					parent.kill()
					logger.info(f"{processName}({processID}) kill parent pid")
			except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):  # 예외처리
				pass
		else:
			logger.warning(f"process_id = {pid} is not running or already killed.")
	else:
		logger.warning(f"process_id = {pid} (process_id is None)")

def delete_pid_file(pid_file_path:str=None):
	# check before pid and delete CRAWER_PID
	with open(pid_file_path, "r+") as f:
		before_pid = f.read()
		# logger.info(before_pid)
		before_pid = None if before_pid == '' else int(before_pid)
		logger.info(f"before process_id= {before_pid}")
		f.truncate(0)
		f.close()
		logger.info(f"delete pid_file = {pid_file_path}")
		_delete_process(pid=before_pid)

def delete_pid(pid:int):
	logger.info(f"before process_id= {pid}")
	_delete_process(pid=pid)

def create_pid(pid_file_path:str=None):
	if pid_file_path is None:
		pid_file_pat = os.path.join(root_path, "CRAWER_PID")

	if os.path.exists(pid_file_path):
		# 1. delete before process based on ${pwd}/CRAWER_PID
		logger.info(f"pid_file = {pid_file_path}")
		this_pid = os.getpid()

		delete_pid_file(pid_file_path=pid_file_path)

		with open(pid_file_path, "r+") as f:
			f.write(str(this_pid))
			logger.info(f"insert current_process_id = {this_pid} to {pid_file_path}")
			f.close()

	else:
		logger.info(f"pid_file is None in {pid_file_path}")
		# create ${pwd}/CRAWER_PID file with process_id
		this_pid = os.getpid()
		pid_file_path = os.path.join(root_path, 'CRAWER_PID')
		logger.info(f"PID = {this_pid}")
		logger.info(f"PID({this_pid}) write to {pid_file_path}")
		with open(pid_file_path, "w") as f:
			f.write(str(this_pid))
		f.close()

