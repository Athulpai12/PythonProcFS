import os
import unittest


from platformOperation import linux_platform
import CustomExceptions


class TestProcessIdRetrival(unittest.TestCase):

    def setUp(self) -> None:
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.fixtures_path = os.path.join(dir_path, "fixtures")
        self.exception_raising_path = os.path.join(self.fixtures_path, "fake_path")
        self.result = [163718]

    def test_pids(self):
        process_ids = [process.processId for process in linux_platform.get_all_processes(self.fixtures_path)]
        self.assertEqual(process_ids, self.result)

    def test_exception(self):
        with self.assertRaises(CustomExceptions.InvalidLocation):
            linux_platform.get_all_processes(self.exception_raising_path)


if __name__ == '__main__':
    unittest.main()