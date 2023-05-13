class User(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password


class Table(object):
    def __init__(self, name, author, coauthors, table_type, size, columns_name):
        self.name = name
        self.author = author
        self.coauthors = coauthors
        self.table_type = table_type
        self.size = size
        self.columns_name = columns_name
