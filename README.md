# sudoku-solver
Exercise in writing a sudoku solver in Python 2.7

**Implemented - as of 2017.11**
* Recursive depth-first search for guessing and filling the grid.

**Implemented - as of 2017.04**
* Method for eliminating possible values for a particular cell by checking against values in the same row, column, or 3-by-3 block.
* Method for determining values for a particular cell by checking which values MUST be in a particular row, column, or 3-by-3 block.
* Method for filling cells, assuming that their possible values have been reduced to a single possibility.
