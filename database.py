class Table():
    '''A class to represent a SQuEaL table'''

    def __init__(self, table={}):
        self.table = table
        # sets the numebr of rows to 0.
        self.num_row = 0

    def set_dict(self, new_dict):
        '''(Table, dict of {str: list of str}) -> NoneType

        Populate this table with the data in new_dict.
        The input dictionary must be of the form:
            column_name: list_of_values
        '''
        # Creates a new table.
        self.table = {}
        # Updates the table with the dictionary.
        self.table.update(new_dict)

    def get_dict(self):
        '''(Table) -> dict of {str: list of str}

        Return the dictionary representation of this table. The dictionary keys
        will be the column names, and the list will contain the values
        for that column.
        '''
        # Returns the table.
        return self.table

    def print_csv(self):
        '''(Table) -> NoneType
        Print a representation of table in csv format.
        '''
        # no need to edit this one, but you may find it useful (you're welcome)
        dict_rep = self.get_dict()
        columns = list(dict_rep.keys())
        print(','.join(columns))
        rows = self.num_rows()
        for i in range(rows):
            cur_column = []
            for column in columns:
                cur_column.append(dict_rep[column][i])
            print(','.join(cur_column))

    def num_rows(self):
        '''(Table) -> int
        Given a table, the function will return the number of rows in the
        table.
        '''
        self.num_row = 0
        # Gets the number of rows in a table.
        for counter in self.table:
            # Resets the number of rows back to 0 after the numeber of rows in
            # one index has been calculated.
            self.num_row = 0
            for count in self.table[counter]:
                self.num_row += 1

        # Returns the number of rows in the table.
        return self.num_row

    def get_cartesian(self, table2):
        '''(Table, Table) -> Table
        Given 2 tables, the function will calculate the cartesian product and
        return it.
        '''
        # Creates a new table.
        table = {}
        # Gets the number of rows in each table.
        table1_rows = self.num_rows()
        table2_rows = table2.num_rows()

        if (table1_rows != 0 and table2_rows != 0):
            # Creates a new list to store the keys of the first table.
            table1_keys = []

            # Appends the headers of the first table to the list.
            for element in self.table:
                table1_keys.append(element)

            # Multiplies the second table by the number of rows in it.
            for element in table2.table:
                table2.table[element] *= table2_rows

            # Creates a new dictionary used to store the new table1.
            new_table1 = {}
            for element in table1_keys:
                # initializes the new table with only a key mapped to a empty
                # list.
                new_table1[element] = []
                for counter in range(table1_rows):
                    for count in range(table2_rows):
                        # Appends a certain element based on the number of rows
                        # in the second table.
                        new_table1[element].append(self.table[element]
                                                   [counter])

            # Updates the table with the new table1 and the modified table2.
            table.update(new_table1)
            table.update(table2.table)

        # Empty's the first second table
        elif table1_rows == 0:
            for element in table2.table:
                table2.table[element] = []
            # Updates the table with table1 and the modified table2.
            table.update(table2.table)
            table.update(self.table)

        # Empty's the second second table
        elif table2_rows == 0:
            for element in self.table:
                self.table[element] = []
            # Updates the table with the modified table1 and table2.
            table.update(self.table)
            table.update(table2.table)

        # Creates a table object with the "cartesian product".
        object_table = Table(table)
        # Returns the table object.
        return object_table

    def get_read_table(self, table_handle):
        '''(Table, io.textWrapper) -> int
        Given a table and a file open for reading, the function will read the
        table, map the headers to their content and return the table.
        '''
        # Places the first line of the file into a string.
        headers = table_handle.readline()
        # Places every line after the first line into a list.
        columns = table_handle.readlines()

        # Spits all the words in the headers list.
        headers = headers.strip()
        headers = headers.split(',')
        # Creates a new list that contains all the words of the column list.
        new_columns = []
        for counter in range(len(columns)):
            new_columns += columns[counter].split(',')

        # Strips all spaces form the list.
        for counter in range(len(new_columns)):
            new_columns[counter] = new_columns[counter].strip()

        # Creates a new dictionary.
        self.table = {}
        header_values = []
        start = 0
        all_header_values = []

        for counter in range(len(headers)):

            # Loop goes up by the number of headers.
            for count in range(start, len(new_columns), len(headers)):

                # Places all the contents of a specific column in a temp list.
                header_values.append(new_columns[count])

            # Increases the starting index by one.
            start += 1
            # PLaces the temp list within another list.
            all_header_values.append(header_values)
            # Resets the temp list
            header_values = []

        for counter in range(len(headers)):
            # Maps the headers to their contents.
            self.table[headers[counter]] = all_header_values[counter]

        # Returns the table.
        return self

    def matching_headers(self, headers):
        '''(Table, list of str) -> Table
        Given a table and a list of headers, the function will reset that table
        and populate it with only the headers and the contents in the headers
        that are in the list.
        '''
        # Creates a new dictionary.
        matched_headers = {}

        for element in headers:
            # If the element is *, then the entire table is
            if (element == '*'):
                matched_headers = self.table

            # If the header is in the list, the header will be mapped to
            # the table inside it.
            elif (element in self.table):
                matched_headers[element] = self.table[element]

        # The table equals the dictionary that contains only the desired
        # headers and their contents
        self.table = matched_headers

    def equal_constraints(self, first_condition, second_condition):
        '''(Table, str, str) -> Table
        Given a table, and conditions, the function will return the table with
        the appropriate conditons applied to it.
        '''
        counter = 0
        while (counter < self.num_rows()):
            try:
                # Checks if the second condition is a header.
                if ('.' in second_condition and not(isinstance(
                        second_condition, float))):
                    # If the second condition contains a period, then all the
                    # other headers that arent the same as the one in the
                    # condition are removed from the table.
                    if (self.table[first_condition][counter] !=
                            self.table[second_condition][counter]):
                        self.remove_row(counter)
                        counter -= 1

                # Checks if the second condition is a string.
                elif ('.' not in second_condition and not(isinstance
                                                          (second_condition,
                                                           float))):
                    # If the second condition doesnt contain a period, then all
                    # the other rows that arent the same as the one in the
                    # condition are removed from the table.
                    if (self.table[first_condition][counter] !=
                            second_condition):
                        self.remove_row(counter)
                        counter -= 1
            except:
                # Checks if the second condition is a string.
                if not(isinstance(second_condition, float)):
                    # If the second condition isn't a float, than all the
                    # rows that aren't the same as the ones in the in condition
                    # are removed.
                    if (self.table[first_condition][counter] !=
                            self.table[second_condition][counter]):
                        self.remove_row(counter)

                        counter -= 1
                # If the second condition is a float:
                else:
                    # Removes all the rows that arent the same a the second
                    # condition.
                    if (float(self.table[first_condition][counter]) !=
                            second_condition):
                        self.remove_row(counter)
                        counter -= 1
            counter += 1

        # Returns the new table with the condition met.
        return self

    def greater_constraints(self, first_condition, second_condition):
        '''(Table, str, str) -> Table
        Given a table, and conditions, the function will return the table with
        the appropriate conditons applied to it.
        '''
        counter = 0
        while (counter < self.num_rows()):
            try:
                # Checks if the second condition is a header.
                if ("." in second_condition and not(isinstance(
                        second_condition, float))):
                    # If the second condition contains a period, then all
                    # the rows that have a value less or equal than the value
                    # in the first condition are removed from the table.
                    if (self.table[first_condition][counter] <=
                            self.table[second_condition][counter]):
                        self.remove_row(counter)
                        counter -= 1

                # Checks if the second condition is a float.
                elif ("." in second_condition and (isinstance
                                                   (float
                                                    (self.table
                                                     [first_condition][counter]
                                                     ), float))):
                    # If the second condition contains a period and is a float,
                    # then all the rows that have a value less or equal
                    # than the value in the second condition are removed from
                    # the table.
                    if (float(self.table[first_condition][counter]) <=
                            float(self.table[second_condition][counter])):
                        self.remove_row(counter)
                        counter -= 1

            except:

                # Checks if the second condition is a string.
                if not(isinstance(second_condition, float)):
                    if (self.table[first_condition][counter] <=
                            self.table[second_condition][counter]):
                        self.remove_row(counter)
                        counter -= 1
                # If the second condition is a float:
                else:
                    if (float(self.table[first_condition][counter]) <=
                            second_condition):
                        # Removes all the rows that arent greater than the
                        # second condition.
                        self.remove_row(counter)
                        counter -= 1
            counter += 1

        # Returns the new table with the condition met.
        return self

    def remove_row(self, counter):
        '''(Table, int) -> NoneType
        Given a table and a int, the function removes a row and the int.
        REQ: counter must be an int.
        '''
        for count in self.table.keys():
            # Uses the counter to remove the row form the list.
            self.table[count].pop(-(len(self.table[count])) + counter)


class Database():
    '''A class to represent a SQuEaL database'''

    def __init__(self, database={}):
            self.database = database

    def set_dict(self, new_dict):
        '''(Database, dict of {str: Table}) -> NoneType

        Populate this database with the data in new_dict.
        new_dict must have the format:
            table_name: table
        '''
        # Creates a new database.
        self.database = {}
        # Updates the database with the dictionary.
        self.database.update(new_dict)

    def get_dict(self):
        '''(Database) -> dict of {str: Table}

        Return the dictionary representation of this database.
        The database keys will be the name of the table, and the value
        with be the table itself.
        '''
        # Returns the database.
        return self.database

    def get_read_database(self, database_headers, file_data):
        '''(Table, list of str, list of dict) -> int
        Given a list of file names and a list of tables in the file, the
        function will return a dictionary with the file names mapped to the
        table within it.
        '''
        # Creates a new dictionary.
        self.database = {}

        for counter in range(len(database_headers)):
            # Removes the file extension from the file name.
            database_headers[counter] = (database_headers[counter].
                                         replace('.csv', ''))
            # Maps the file name with the table within the file.
            self.database[database_headers[counter]] = file_data[counter]

        # Returns the database.
        return self
