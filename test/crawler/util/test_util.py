import os
import unittest
from pathlib import Path
import sys

from crawler.util.Logger import Logger
from crawler.util.common import *


class TestUtil(unittest.TestCase):
	def setUp(self) -> None:
		self.root_path = Path(__file__).parent.parent.parent.parent
		self.logger = Logger(file_name=self.__class__.__name__).logger

	@unittest.skip("later")
	def test_delete_pid_with_file(self):
		pid_file_path = os.path.join(self.root_path, "CRAWER_PID")
		delete_pid_file(pid_file_path=pid_file_path)

	def test_delete_pid(self):
		pids = []
		for pid in pids:
			delete_pid(pid)

	@unittest.skip("later")
	def test_create_process_id(self):
		pid_file_path = os.path.join(self.root_path, "CRAWER_PID")
		create_pid(pid_file_path=pid_file_path)

if __name__ == "__main__":
	suite = unittest.TestLoader().loadTestsFromTestCase(TestUtil)
	result = unittest.TextTestRunner(verbosity=2).run(suite)
	print(f"unittest result: {result}")
	print(f"result.wasSuccessful()={result.wasSuccessful()}")
	# 정상종료는 $1 에서 0을 리턴함
	sys.exit(not result.wasSuccessful())
