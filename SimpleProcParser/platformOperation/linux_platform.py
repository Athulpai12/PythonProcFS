import os
import pwd
import re
import typing

from models import base_model
import utils
import constants

PROCFS_PATH = "/proc"
OPERATING_SYSTEM = constants.OperatingSystem.LINUX


def _pids(procfs_path: str) -> typing.List:
    """ 
    A protected function that is used to return all the pids in the procfs path
    :return: A list of processes ids  in the system in sorted order
    """""
    return sorted([int(x) for x in os.listdir(procfs_path) if x.isdigit()])


@utils.func_exception_decorator
def get_all_processes(procfs_path: str = PROCFS_PATH) -> typing.List:
    """
    A function that return a list of process objects with the pids present

    :param procfs_path: the location of procfs
    :return: A list of procfs object
    """

    pids = _pids(procfs_path)
    process = []
    for pid in pids:
        process.append(Process(pid, procfs_path))
    return process


def _real_uids(procfs_path: str, process_id: int, uids_re: typing.Pattern = re.compile(br'Uid:\t(\d+)\t(\d+)\t(\d+)'))\
        ->int:
    """
    This function get the real uid and then return it
    :param procfs_path: The path of the procfs file [str]
    :param process_id: The process id [int]
    :param uids_re:
    :return:
    """
    with open("%s/%s/status" % (procfs_path, process_id), "rb") as f:
        data = f.read()
    try:
        real, effective, saved = uids_re.findall(data)[0]
    except IndexError as exc:
        raise IOError
    return int(real)


def _parse_stat_file(procfs_path: str, process_id: int) -> dict:
    """
    Parse /proc/{pid}/stat file and return a dict with various
            process info.
    :param procfs_path:
    :param process_id:
    :return:
    """
    with open("%s/%s/stat" % (procfs_path, process_id), "rb") as f:
        data = f.read()

    # process name is between parenthesis and it can contain spaces hence using this
    rpar = data.rfind(b')')
    epar = data.find(b'(')
    if rpar == -1 or epar == -1:
        raise IOError
    name = data[epar + 1:rpar]
    fields = data[rpar + 2:].split()
    try:
        ret = {'process_name': name, 'status': fields[0], 'ppid': fields[1], 'ttynr': fields[4], 'utime': fields[11],
               'stime': fields[12], 'children_utime': fields[13], 'children_stime': fields[14],
               'create_time': fields[19],
               "virtual_mem": fields[20], 'cpu_num': fields[36], 'blkio_ticks': fields[39]}
    except IndexError:
        raise IOError

    return ret


class ProcessStats(base_model.ProcessStat):
    """
    This model stores the stats in process
    """

    def __init__(self, process_name: bytes,
                 status: bytes,
                 ppid: bytes,
                 ttynr: bytes,
                 utime: bytes,
                 stime: bytes,
                 children_utime: bytes,
                 children_stime: bytes,
                 create_time: bytes,
                 virtual_mem: bytes,
                 cpu_num: bytes,
                 blkio_ticks:bytes
                 ):
        # import ipdb;ipdb.set_trace()
        self.process_name = process_name.decode(),
        self.status = status
        self.ppid = ppid
        self.ttynr = ttynr
        self.utime = utime
        self.stime = stime
        self.children_utime = children_utime
        self.children_stime = children_stime
        self.create_time = create_time
        self.virtual_mem = virtual_mem
        self.cpu_num = cpu_num
        self.blkio_ticks = blkio_ticks

    def to_dict(self) -> dict:
        """

        :return: A dict of the object parameters
        """
        return {
            "processName": str(self.process_name).strip()[1:-2],
            "utime": utils.get_human_format(int(self.utime)),
            "stime": utils.get_human_format(int(self.stime)),
            "parentProcessId": int(self.ppid),
            "virtualMemory": utils.convert_size(int(self.virtual_mem))
        }


class Process(base_model.ProcessFactory):
    """
    This model stores data about process and  its stats
    """

    def __init__(self, processId : int,
                 procfsPath: str=PROCFS_PATH):
        """

        :param processId: The process id
        :param procfsPath: The path of procfs in the system
        """
        self.processId = processId
        self.procfsPath = procfsPath
        self.processStats = None
        self.processCreator = None
        self.platform = OPERATING_SYSTEM

    @utils.exception_decorator
    def get_process_stat(self) -> dict:
        """

        :return: The process statistics in a dictionary
        """
        data = _parse_stat_file(self.procfsPath, self.processId)
        self.processStats = ProcessStats(**data)
        return self.processStats.to_dict()

    @utils.exception_decorator
    def get_process_creator(self)-> str:
        """

        :return: The user name who created the process
        """
        real_uid = _real_uids(self.procfsPath, self.processId)

        try:
            self.processCreator = pwd.getpwuid(real_uid).pw_name
        except KeyError:
            # if real uid is not resolved by system
            self.processCreator = str(real_uid)

        return self.processCreator

    def to_dict(self) -> dict:
        """

        :return:  A dictionary of process parameters
        """
        ret = {}
        ret["processID"] = self.processId
        if self.processStats:
            ret.update(self.processStats.to_dict())

        if self.processCreator:
            ret["processCreator"] = self.processCreator

        return ret
