from __future__ import division
from datetime import timedelta
import functools
import math
import os

import CustomExceptions


def exception_decorator(func):
    """
    This is a decorator to decorate class methods that raise exceptions
    :param func: The function which is being called
    :return: The return value of the function
    :exception: Raises CustomExceptions.AccessDenied, CustomExceptions.InvalidLocation, CustomExceptions.InvalidLocation
    """

    @functools.wraps(func)
    def wrap(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except PermissionError as exc:
            raise CustomExceptions.AccessDenied(self.pid, self.procfs_path, self.platform,
                                                msg="An exception occurred "
                                                    "in the function {}. The following arguments ar"
                                                    "e passed {}, {} ".format(func.__name__, str(args),
                                                                              str(kwargs))) from exc
        except FileNotFoundError as exc:
            raise CustomExceptions.InvalidLocation(self.processId, self.procfsPath, self.platform,
                                                   msg="An exception occurred "
                                                       "in the function {}. The following arguments ar"
                                                       "e passed {}, {} . The following could be due to"
                                                       " process getting destroyed or "
                                                       "invalid file location".format(func.__name__, str(args),
                                                                                      str(kwargs))) from exc
        except IOError as exc:
            raise CustomExceptions.CorruptFileException(self.pid, self.procfs_path, self.platform,
                                                        msg="An exception occurred "
                                                            "in the function {}. The following arguments ar"
                                                            "e passed {}, {} . The following could be due to"
                                                            "invalid file file read".format(func.__name__, str(args),
                                                                                           str(kwargs))) from exc

    return wrap


def get_human_format(ticks):
    """
    The function converts ticks into human readable format ie H:M:S
    :param ticks: An integer value ticks
    :return: A string in the H:M:S format
    """
    freq = os.sysconf_names['SC_CLK_TCK']
    duration = timedelta(milliseconds=ticks / freq)
    days, seconds = duration.days, duration.total_seconds()
    hours = int(days * 24 + seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = (seconds % 60)
    return "{} H : {} M : {:.4f} S".format(hours, minutes, seconds)


def convert_size(size_bytes):
    """
    This function converts bytes to human readable for format ie in KB,MB and so on
    :param size_bytes: An Integer that is the total bytes
    :return:
    """
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])


def func_exception_decorator(func):
    """
    This is a decorator to decorate  methods that raise exceptions
    :param func: The function which is being called
    :return: The return value of the function
    :exception: Raises CustomExceptions.AccessDenied, CustomExceptions.InvalidLocation, CustomExceptions.InvalidLocation
    """
    @functools.wraps(func)
    def wrap(*args, **kwargs):
        try:

            return func(*args, **kwargs)
        except PermissionError as exc:
            raise CustomExceptions.AccessDenied(
                msg="An exception occurred "
                    "in the function {}. The following arguments ar"
                    "e passed {}, {} ".format(func.__name__, str(args),
                                              str(kwargs))) from exc
        except FileNotFoundError as exc:
            raise CustomExceptions.InvalidLocation(
                msg="An exception occurred "
                    "in the function {}. The following arguments ar"
                    "e passed {}, {} . The following could be due to"
                    " process getting destroyed or "
                    "invalid file location".format(func.__name__, str(args),
                                                   str(kwargs))) from exc

    return wrap
