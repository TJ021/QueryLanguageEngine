from reading import *
from database import *


def cartesian_product(table1, table2):
    '''(Table, Table) -> Table
    Given 2 tables, the function will return a new table contianing the
    cartesian product of the 2 given tables.

    >>> table1 = {'t1.greeting' : ['hi', 'hello'], 't2.thing' :\
    ['earth', 'world']}
    >>> table2 = {'t2.first' : ['1', '2'], 't2.second' : ['3', '4']}
    >>> t1 = Table(table1)
    >>> t2 = Table(table2)
    >>> result = cartesian_product(t1, t2)
    >>> result = result.table
    >>> expected = {'t1.greeting' : ['hi', 'hi', 'hello', 'hello'], 't2.thing'\
    : ['earth', 'earth', 'world', 'world'], 't2.first' : ['1', '2', '1', '2'],\
    't2.second' : ['3', '4', '3', '4']}
    >>> result == expected
    True

    >>> table1 = {'t1.greeting' : ['hi', 'hello'], 't2.thing' :\
    ['earth', 'world']}
    >>> table2 = {'t2.first' : ['1', '2']}
    >>> t1 = Table(table1)
    >>> t2 = Table(table2)
    >>> result = cartesian_product(t1, t2)
    >>> result = result.table
    >>> expected = {'t1.greeting' : ['hi', 'hi', 'hello', 'hello'], 't2.thing'\
    : ['earth', 'earth', 'world', 'world'], 't2.first' : ['1', '2', '1', '2']}
    >>> result == expected
    True

    >>> table1 = {'t1.greeting' : ['hi', 'hello']}
    >>> table2 = {'t2.first' : ['1', '2'], 't2.second' : ['3', '4']}
    >>> t1 = Table(table1)
    >>> t2 = Table(table2)
    >>> result = cartesian_product(t1, t2)
    >>> result = result.table
    >>> expected = {'t1.greeting' : ['hi', 'hi', 'hello', 'hello'], 't2.first'\
    : ['1', '2', '1', '2'], 't2.second' : ['3', '4', '3', '4']}
    >>> result == expected
    True

    >>> table1 = {'t1.greeting' : ['hi', 'hello']}
    >>> table2 = {'t2.first' : ['hi', 'hello']}
    >>> t1 = Table(table1)
    >>> t2 = Table(table2)
    >>> result = cartesian_product(t1, t2)
    >>> result = result.table
    >>> expected = {'t1.greeting' : ['hi', 'hi', 'hello', 'hello'], 't2.first'\
    : ['hi', 'hello', 'hi', 'hello']}
    >>> result == expected
    True

    >>> table1 = {'t1.greeting' : []}
    >>> table2 = {'t2.first' : []}
    >>> t1 = Table(table1)
    >>> t2 = Table(table2)
    >>> result = cartesian_product(t1, t2)
    >>> result = result.table
    >>> expected = {'t1.greeting' : [], 't2.first' : []}
    >>> result == expected
    True

    >>> table1 = {'t1.greeting' : ['1', '2']}
    >>> table2 = {'t2.first' : []}
    >>> t1 = Table(table1)
    >>> t2 = Table(table2)
    >>> result = cartesian_product(t1, t2)
    >>> result = result.table
    >>> expected = {'t1.greeting' : [], 't2.first' : []}
    >>> result == expected
    True

    >>> table1 = {'t1.greeting' : ['1', '2']}
    >>> table2 = {'t2.first' : ['1', '2']}
    >>> t1 = Table(table1)
    >>> t2 = Table(table2)
    >>> result = cartesian_product(t1, t2)
    >>> result = result.table
    >>> expected = {'t1.greeting' : ['1', '1', '2', '2'], 't2.first' :\
    ['1', '2', '1', '2']}
    >>> result == expected
    True
    '''
    # Calls the get_cartesian function in database.py to get the cartesian
    # product fo the 2 tables.
    object_table = table1.get_cartesian(table2)

    # Returns the cartesian product.
    return object_table


def run_query(database, query):
    '''(, str) -> Table
    Given a ___ and a string command, the function will return the
    appropriate contents of a table(s).
    REQ: query must have proper syntax.
    '''
    # Makes a list filel with the contents of the user input.
    token = query.split(' ', 5)

    # Creates a list that contains the header(s) that the user wants to output.
    headers = token[1].split(',')
    # Creates a list that contains name of the file(s) the user wants to get
    # a table from.
    table_file = token[3].split(',')

    # Gets the first table in the database.
    table = database.database[table_file[0]]

    if len(table_file) > 1:
        for counter in range(1, len(table_file)):
            # Gets the second table from the database and so on.
            table2 = database.database[table_file[counter]]
            # Creates a cartesian product of the 2 existing tables.
            table = cartesian_product(table, table2)

    # Finds out whether theres a where constraint in the user input.
    where_conditions = []
    operator = ''
    final_where_conditions = []
    if 'where' in token:
        # Creates a list with all the constraints.
        where_conditions = token[5].split(',')

        # Sends each conditiona into another function to get appropriate
        # table.
        for element in where_conditions:
            table = where_constraints(table, element)

    # Checks if the headers that the user wants are in the database.
    table.matching_headers(headers)

    # Returns the table.
    return table


def where_constraints(table, conditions):
    '''(Table, list of str) -> Dict of str
    Given a table and conditions, the function returns a table with the
    appropriate conditions met.
    REQ: conditions must include '=' or '>'.

    >>> table = {'t1.greeting' : ['hi', 'hello'], 't2.thing' :['1', '2']}
    >>> t = Table(table)
    >>> conditions = ['t1.greeting=hi']
    >>> result = where_constraints(t, conditions)
    >>> expected = {'t1.greeting' : ['hi'], 't2.thing' : ['1']}
    >>> result == expected
    True

    >>> table = {'t1.greeting' : ['hi', 'hello'], 't2.thing' :['1', '2']}
    >>> t = Table(table)
    >>> conditions = ['t2.thing>1']
    >>> result = where_constraints(t, conditions)
    >>> expected = {'t1.greeting' : ['hello'], 't2.thing' : ['2']}
    >>> result == expected
    True
    '''
    # Creates a new dictionary.
    new_table = {}

    # If the operator of the condtion is '=', then the header and value will be
    # split from the operator and stripped of any quotations.
    if ('=' in conditions):
        conditions = conditions.split('=')
        header = conditions[0]
        value = conditions[1].strip('"').strip("'")
        try:
            # Changes the value to a float if it can.
            value = float(value)
        except:
            pass
        # Calls another function in to get the new_table with the appropriate
        # conditions in place.
        new_table = table.equal_constraints(header, value)

    # If the operator of the condtion is '>', then the header and value will be
    # split from the operator and stripped of any quotations.
    elif ('>' in conditions):
        conditions = conditions.split('>')
        header = conditions[0]
        value = conditions[1].strip('"').strip("'")
        try:
            # Changes the value to a float if it can.
            value = float(value)
        except:
            pass
        # Calls another function in to get the new_table with the appropriate
        # conditions in place.
        new_table = table.greater_constraints(header, value)

    # Returns the new table.
    return new_table


if(__name__ == "__main__"):
    # Initializes the query input.
    query = ' '
    # If the user doesnt input a blank, the program continues to ask the user
    # to input a query input until the user enters a blank to exit.
    while (query != ''):
            query = input("Enter a SQuEaL query, or a blank line to exit:")
            try:
                # Prints the table.
                run_query(read_database(), query).print_csv()
            except:
                pass
