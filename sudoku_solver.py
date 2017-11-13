import copy

'''
Sudoku puzzle format:
     XX: cell_id
    XXX: cell_tag
         fields: r, c, b
         r: row
         c: column
         b: block

[      0   1   2   3   4   5   6   7   8
      --- --- --- --- --- --- --- --- ---
     | 00| 01| 02| 03| 04| 05| 06| 07| 08|
   0 |000|010|020|031|041|051|062|072|082|
      --- --- --- --- --- --- --- --- ---
     | 09| 10| 11| 12| 13| 14| 15| 16| 17|
   1 |100|110|120|131|141|151|162|172|182|
      --- --- --- --- --- --- --- --- ---
     | 18| 19| 20| 21| 22| 23| 24| 25| 26|
   2 |200|210|220|231|241|251|262|272|282|
      --- --- --- --- --- --- --- --- ---
     | 27| 28| 29| 30| 31| 32| 33| 34| 35|
   3 |303|313|323|334|344|354|365|375|385|
      --- --- --- --- --- --- --- --- ---
     | 36| 37| 38| 39| 40| 41| 42| 43| 44|
   4 |403|413|423|434|444|454|465|475|485|
      --- --- --- --- --- --- --- --- ---
     | 45| 46| 47| 48| 49| 50| 51| 52| 53|
   5 |503|513|523|534|544|554|565|575|585|
      --- --- --- --- --- --- --- --- ---
     | 54| 55| 56| 57| 58| 59| 60| 61| 62|
   6 |606|616|626|637|647|657|668|678|688|
      --- --- --- --- --- --- --- --- ---
     | 63| 64| 65| 66| 67| 68| 69| 70| 71|
   7 |706|716|726|737|747|757|768|778|788|
      --- --- --- --- --- --- --- --- ---
     | 72| 73| 74| 75| 76| 77| 78| 79| 80|
   8 |806|816|826|837|847|857|868|878|888|
      --- --- --- --- --- --- --- --- ---
]
'''

class SudokuCell(object):
    def __init__ (self, id_num, tag):
        self.id = id_num
        self.tag = tag
        self.value = None
        self.possible_values = [1,2,3,4,5,6,7,8,9]
        self.value_given = None
            # True if value is prepopulated.
            # False is value is solved.

    def __str__ (self):
        return str(self.value) if self.value != None else "-"

    def summary(self):
        print ("Sudoku Cell at (" + str(self.tag[0]) + ", " + str(self.tag[1]) + ") is in block " + str(self.tag[2]) + ". It has a value of " + str(self.value) + ".")
        return None

class SudokuGrid(object):

    TAG_MAP = [
        "000", "010", "020", "031", "041", "051", "062", "072", "082",
        "100", "110", "120", "131", "141", "151", "162", "172", "182",
        "200", "210", "220", "231", "241", "251", "262", "272", "282",
        "303", "313", "323", "334", "344", "354", "365", "375", "385",
        "403", "413", "423", "434", "444", "454", "465", "475", "485",
        "503", "513", "523", "534", "544", "554", "565", "575", "585",
        "606", "616", "626", "637", "647", "657", "668", "678", "688",
        "706", "716", "726", "737", "747", "757", "768", "778", "788",
        "806", "816", "826", "837", "847", "857", "868", "878", "888"
    ]

    FIELD_MAP = [
        # Cell.ids organized by field-types.
        # Each individual list in the field-types is a field.
        # E.g., there are 9 fields of field-type "row".

        # First array: cell.id by row
        [
            [ 0,  1,  2,  3,  4,  5,  6,  7,  8],
            [ 9, 10, 11, 12, 13, 14, 15, 16, 17],
            [18, 19, 20, 21, 22, 23, 24, 25, 26],
            [27, 28, 29, 30, 31, 32, 33, 34, 35],
            [36, 37, 38, 39, 40, 41, 42, 43, 44],
            [45, 46, 47, 48, 49, 50, 51, 52, 53],
            [54, 55, 56, 57, 58, 59, 60, 61, 62],
            [63, 64, 65, 66, 67, 68, 69, 70, 71],
            [72, 73, 74, 75, 76, 77, 78, 79, 80]
        ],
        # Second array: cell.id by column
        [
            [ 0,  9, 18, 27, 36, 45, 54, 63, 72],
            [ 1, 10, 19, 28, 37, 46, 55, 64, 73],
            [ 2, 11, 20, 29, 38, 47, 56, 65, 74],
            [ 3, 12, 21, 30, 39, 48, 57, 66, 75],
            [ 4, 13, 22, 31, 40, 49, 58, 67, 76],
            [ 5, 14, 23, 32, 41, 50, 59, 68, 77],
            [ 6, 15, 24, 33, 42, 51, 60, 69, 78],
            [ 7, 16, 25, 34, 43, 52, 61, 70, 79],
            [ 8, 17, 26, 35, 44, 53, 62, 71, 80]
        ],
        # Third array: cell.id by block
        [
            [ 0,  1,  2,  9, 10, 11, 18, 19, 20],
            [ 3,  4,  5, 12, 13, 14, 21, 22, 23],
            [ 6,  7,  8, 15, 16, 17, 24, 25, 26],
            [27, 28, 29, 36, 37, 38, 45, 46, 47],
            [30, 31, 32, 39, 40, 41, 48, 49, 50],
            [33, 34, 35, 42, 43, 44, 51, 52, 53],
            [54, 55, 56, 63, 64, 65, 72, 73, 74],
            [57, 58, 59, 66, 67, 68, 75, 76, 77],
            [60, 61, 62, 69, 70, 71, 78, 79, 80]
        ]
    ]

    def __init__ (self):

        self.list = []
        self.solved = False
        self.solvable = True

        for i in range(81):
            self.list.append(SudokuCell(i, SudokuGrid.TAG_MAP[i]))

    def print_grid(self):
        i = 0
        for row in range(9):
            print("")
            for column in range(9):
                print self.list[i],
                i += 1
        print("")
        return None

    def summary(self):
        for i in range(81):
            self.list[i].summary()
        return None

    @staticmethod
    # To be edited for variable file name
    def parser():
        test_file_path = raw_input("Please enter the path for the file: ")
        test_file = open(test_file_path)
        proto_grid = test_file.read().splitlines()
        test_grid = []
        for row in range(9):
            test_grid.append([])
            current_row = proto_grid[row].split(" ")
            for column in range(9):
                value = None
                if (current_row[column] != "0"):
                    value = int(current_row[column])
                test_grid[row].append(value)
#        for row in range(9):
#            print("")
#            for column in range(9):
#                print test_grid[row][column],
        return test_grid

    def puzzle_population(self, puzzle):
        i = 0
        for row in range(9):
            for column in range (9):
                if puzzle[row][column] != None:
                    self.list[i].value = puzzle[row][column]
                    self.list[i].possible_values = []
                    self.list[i].value_given = True
                i += 1
        return None

    def trim_value_by_field_type(self, id_num, field_type):
        # Determine location of cell by tag.
        # Eliminate possible values by evaluating field for cell.
        # Field type: 0=row, 1=column, 2=block.
        cell = self.list[id_num]
        cell_field = int(cell.tag[field_type])
        if cell.value == None:
            # Identify list of indexes for relevant field.
            # FIELD_MAP[field_type] -> index by field type number for row, column, or block.
            # FIELD_MAP[field_type][cell_field] -> index by cell.tag for field list.
            field = SudokuGrid.FIELD_MAP[field_type][cell_field]
            for i in range(9):
                self_index = field[i]
                if self.list[self_index].value in cell.possible_values:
                    cell.possible_values.remove(self.list[self_index].value)
        return None

    def trim_value_by_all_fields(self):
        # For grid, eliminates impossible values by running through rows, columns, and blocks.
        for id_num in range(81):
            for field_type in range(3):
                self.trim_value_by_field_type(id_num, field_type)
        return None

    def missing_numbers_by_field(self, field_type, field_list):
        # Field_type: 0=row, 1=column, 2=block
        # Field_list = index into field-type list for specific field: 0-8
        missing_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        field = SudokuGrid.FIELD_MAP[field_type][field_list]
        for i in range(9):
            self_index = field[i]
            if self.list[self_index].value in missing_numbers:
                missing_numbers.remove(self.list[self_index].value)
        return missing_numbers

    def trim_value_by_necessary_placement(self, field_type, field_list):
        # The possible values for a cell will be trimmed to a number that MUST
        #    be placed in that cell to satisfy the completion condition for that
        #    cell's field.
        # Field_type: 0=row, 1=column, 2=block
        # Field_list = index into field-type list for specific field: 0-8
        missing_numbers = self.missing_numbers_by_field(field_type, field_list)
        field = SudokuGrid.FIELD_MAP[field_type][field_list]
        for i in range(len(missing_numbers)):
            number_to_place = missing_numbers[i]
            possible_cells = []
            for j in range(9):
                self_index = field[j]
                if number_to_place in self.list[self_index].possible_values:
                    possible_cells.append(self_index)
            if len(possible_cells) == 1:
                self.list[possible_cells[0]].possible_values = [number_to_place]
        return None

    def trim_value_by_all_necessary_placements(self):
        for field_type in range(3):
            for field in range(9):
                self.trim_value_by_necessary_placement(field_type, field)
        return None

    def fill_cell(self, id_num, guess = None):
        filling_cell = False
        possible_values = self.list[id_num].possible_values

        if guess is not None:
            self.list[id_num].value = guess
            filling_cell = True
        elif len(possible_values) == 1:
            self.list[id_num].value = possible_values[0]
            filling_cell = True
        if self.list[id_num].value:
            self.list[id_num].possible_values = []
            self.list[id_num].value_given = False
        return filling_cell

    def fill_grid_naive(self):
        # Fills the grid via Constraint Propagation and Domain Reduction.
        # Attempts these strategies until the grid is stable.
        # Does not employ guess and check.
        # Returns FALSE if a cell changed value.
        # Returns TRUE if no cells changed value (i.e., if the grid is stable).
        stable_grid = True

        self.trim_value_by_all_fields()
        self.trim_value_by_all_necessary_placements()
        for i in range(81):
            if self.fill_cell(i) == True:
                stable_grid = False

        return stable_grid

    def fill_grid(self):
        stable_grid = False

        while not stable_grid:
            # Loop through Constraint Propagation and Domain Reduction until the grid no longer changes.
            stable_grid = self.fill_grid_naive()
            self.completion_check()

        if self.solved:
            return self

        self.solvable = self.solvable_check()

        while not self.solved and self.solvable:
            # Starts guessing.
            for i in range(81):
                if (self.list[i].value is None):
                    for j in range(len(self.list[i].possible_values)):
                        working_grid = self.guess(i, self.list[i].possible_values[j])
                        filled_grid = working_grid.fill_grid()
                        if filled_grid:
                            self = filled_grid
                            return self
        return None

    def guess(self, id_num, possible_value):
    # Fills the cell with a number.
    # Argument: `id_num` is the identification the cell for the guess.
    # Argument: `possible_value` is the guess of the value for that cell.
    # Returns new SudokuGrid object based on guess.
        working_grid = copy.deepcopy(self)
        working_grid.fill_cell(id_num, possible_value)
        return working_grid

    def completion_check(self):
        for i in range(81):
            if self.list[i].value is None:
                return False
        self.solved = True
        return True

    def solvable_check(self):
        for i in range(81):
            if (self.list[i].value is None and self.list[i].possible_values == []):
                return False
        return True

    def solve_grid(self):
        solution = self.fill_grid()
        if solution:
            self = solution
            print("TADA")
        else:
            print("This puzzle was unsolvable.")
        self.print_grid()

bar = SudokuGrid()
bar.print_grid()
puzzle = SudokuGrid.parser()
bar.puzzle_population(puzzle)
bar.print_grid()
# bar.fill_grid()
bar.solve_grid();
