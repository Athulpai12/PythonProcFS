import collections
import os
import unittest
from unittest.mock import MagicMock

from platformOperation import linux_platform
import CustomExceptions


class TestProcssNameRetrival(unittest.TestCase):

    def setUp(self) -> None:
        user_login = collections.namedtuple('user_login', 'pw_name')
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.fixtures_path = os.path.join(dir_path, "fixtures")
        self.exception_raising_path = os.path.join(self.fixtures_path, "fake_path")
        linux_platform.pwd.getpwuid = MagicMock(return_value = user_login('testuser') )
        self.result = ['testuser']


    def get_process(self):
        processes = linux_platform.get_all_processes(self.fixtures_path)
        for process in processes:
            process.get_process_creator()
        return processes

    def test_pids(self):
        process_ids = [process.processCreator for process in self.get_process()]
        self.assertEqual(process_ids, self.result)

    def test_exception(self):
        with self.assertRaises(CustomExceptions.InvalidLocation):
            linux_platform.get_all_processes(self.exception_raising_path)



if __name__ == '__main__':
    unittest.main()