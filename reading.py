import glob
from database import *


def read_table(table_file):
    '''(str) -> Table
    Given a file name without the extension, the function will read the table
    and return it.
    REQ: table_file must have proper format.
    '''
    if (".csv" not in table_file):
        table_file = table_file + ".csv"
    # Opens the file for reading.
    table_handle = open(table_file, 'r')
    # Ceates a table object.
    object_table = Table()
    # Calls a function withing database.py to create a table.
    object_table = object_table.get_read_table(table_handle)

    # Returns a table
    return object_table


def read_database():
    '''() -> Database
    The function returns a database with the keys being the file name and
    they're mapped to the table within them.
    '''
    # Reads all the file names in the directory.
    database_headers = glob.glob('*.csv')
    # Creates a new dictionary.
    file_data = []

    # Creates a list filled with tables from each file in the directory.
    for counter in range(len(database_headers)):
        file_data.append(read_table(database_headers[counter]))

    # Creates a new database object.
    object_database = Database()
    # Calls a function within database.py to create a database.
    object_database = object_database.get_read_database(database_headers,
                                                        file_data)

    # Returns a database.
    return object_database
