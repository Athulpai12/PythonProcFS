from CustomExceptions import constants


class ProcFsException(Exception):

    def __init__(self, process_id: int =None,
                 procfs_path:str=None,
                 platform:str=None, msg:str=""):
        """
        
        :param process_id:
        :param procfs_path:
        :param platform:
        :param msg:
        """
        self.msg = msg
        self.platform = platform
        self.procfs_path = procfs_path
        self.process_id = process_id

    def __str__(self):
        return constants.procFsExceptionMsg.format(self.msg, self.platform, self.procfs_path, self.process_id)


class AccessDenied(ProcFsException):
    """
    Raise this error if insufficient permission to get file
    """
    def __init__(self, process_id=None,
                 procfs_path=None,
                 platform=None, msg=""):
        """

        :param process_id:
        :param procfs_path:
        :param platform:
        :param msg:
        """
        super().__init__(process_id, procfs_path, platform, msg)


class CorruptFileException(ProcFsException):
    """
    Raise this error if the data read from file is corrupt
    """

    def __init__(self, process_id=None,
                 procfs_path=None,
                 platform=None, msg=""):
        """

        :param process_id:
        :param procfs_path:
        :param platform:
        :param msg:
        """
        super().__init__(process_id, procfs_path, platform, msg)


class InvalidLocation(ProcFsException):
    """
        Raise this error if file is not found
        """

    def __init__(self, process_id=None,
                 procfs_path=None,
                 platform=None, msg=""):
        """

        :param process_id:
        :param procfs_path:
        :param platform:
        :param msg:
        """
        super().__init__(process_id, procfs_path, platform, msg)
