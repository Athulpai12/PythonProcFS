__title__ = 'SimpleProcParser'
__version__ = '1.0.0'
__author__ = 'Athul Pai'


import sys
import os
import logging


log = logging.getLogger(__name__)
sys.path.append(os.path.dirname(os.path.realpath(__file__)))


if sys.platform == 'linux':
    from platformOperation import linux_platform
    import CustomExceptions
    import prettyPrint

else:
    log.error("Currently the platoform {} is not supported".format(sys.platform))
    raise Exception("Currently module does not support any other operating system yet.")


def get_entire_process_info(pids=None):
    """

    :return: A list of dictionary with all the stats
    """
    if pids is None:
        processes_list = linux_platform.get_all_processes()
    else:
        processes_list = [linux_platform.Process(pid) for pid in pids]
    ret = []
    for process in processes_list:
        try:
            process.get_process_stat()
            process.get_process_creator()
        except (CustomExceptions.InvalidLocation,
                CustomExceptions.CorruptFileException, CustomExceptions.AccessDenied) as exc:
            log.exception("The process Id {} failed due to the following ab exception".format(process.processId))
        else:
            ret.append(process.to_dict())

    return ret


def print_process_info():
    """
    The function prints the process table data in a table
    :return: None
    """
    data = get_entire_process_info()
    table = prettyPrint.PrettyPrint(data)
    table.print_table()


def print_stats_of_given_pids(pids):
    """
    Prints the status of the given pids
    return: None
    """
    data = get_entire_process_info(pids)
    table = prettyPrint.PrettyPrint(data)
    table.print_table()


if __name__ == "__main__":
    print_stats_of_given_pids([1])

