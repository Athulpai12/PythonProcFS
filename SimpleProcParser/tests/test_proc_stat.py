import collections
import os
import unittest
from unittest.mock import MagicMock

from platformOperation import linux_platform
import CustomExceptions


class TestProcessStatRetrival(unittest.TestCase):

    def setUp(self) -> None:
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.fixtures_path = os.path.join(dir_path, "fixtures")
        self.exception_raising_path = os.path.join(self.fixtures_path, "fake_path")
        self.result = [{'processName': "'networkd-dispat'",
                         'utime': '0 H : 0 M : 0.0025 S',
                         'stime': '0 H : 0 M : 0.0010 S',
                         'parentProcessId': 1,
                         'virtualMemory': '46.84 MB'}]

    def get_process_stat(self):
        processes = linux_platform.get_all_processes(self.fixtures_path)
        data = []
        for process in processes:
            data.append(process.get_process_stat())
        return data

    def test_stats(self):
        process_stats = self.get_process_stat()
        self.assertCountEqual(process_stats, self.result)

    def test_exception(self):
        with self.assertRaises(CustomExceptions.InvalidLocation):
            linux_platform.get_all_processes(self.exception_raising_path)



if __name__ == '__main__':
    unittest.main()