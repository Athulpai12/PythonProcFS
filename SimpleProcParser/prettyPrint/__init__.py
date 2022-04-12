class PrettyPrint(object):

    def __init__(self, data):
        """

        :param data: This is table in dictionary format
        """
        self.data = data

    def print_table(self, collist=None):
        """
         Pretty print a list of dictionaries (self.data) as a dynamically sized table.
        If column names (colList) aren't specified, they will show in random order.
        """
        if not collist: collist = list(self.data[0].keys() if self.data else [])
        mylist = [collist]  # 1st row = header
        for item in self.data: mylist.append([str(item[col] if item[col] is not None else '') for col in collist])
        colsize = [max(map(len, col)) for col in zip(*mylist)]
        formatStr = ' | '.join(["{{:<{}}}".format(i) for i in colsize])
        mylist.insert(1, ['-' * i for i in colsize])  # Seperating line
        for item in mylist: print(formatStr.format(*item))

