import abc


class ProcessFactory(abc.ABC):

    """
    The Interface for the Concrete implementation of the Process object in each platform
    """

    def __init__(self):
        pass

    @abc.abstractmethod
    def get_process_stat(self)  -> dict:
        """

        :return: The statistics of the process
        """
        pass

    @abc.abstractmethod
    def get_process_creator(self) -> str:
        """

        :return: The user who created the process
        """
        pass

    @abc.abstractmethod
    def to_dict(self) ->dict:
        """

        :return: A dict object of all the parameters of the object
        """
        pass


class ProcessStat(abc.ABC):

    """
    The Interface for the Concrete implementation of the ProcessStat object in each platform
    """

    def __init__(self):
        pass

    @abc.abstractmethod
    def to_dict(self) -> dict:
        pass

