# Sudoku-Solver
This is a sudoku solver I made for [Project Euler Problem 96](https://projecteuler.net/problem=96). The solver first uses contraint propagation on each square that needs to be filled in. If the grid cannot be solved using this strategy alone, a backtracking search algorithm is used in conjunction with the constraint propagation algorithm. The implementation is inspired by Peter Norvig's essay [Solving Every Sudoku Puzzle](http://norvig.com/sudoku.html).

The data file containing the 50 puzzles in the Project Euler Problem is provided. The solver can be run via 
```sh
python solve.py
```
Alternatively, the solver can be run for a single puzzle. For example
```sh
python solve.py -n 45
```
solves the 45th puzzle.

For each puzzle the script prints the initial grid and the state after constraint propagation. If still unsolved at that point, search is used to produce the final solved grid. The output for the 45th puzzle would be
```
============================== Grid 45 ==============================

Unsolved Grid
. 8 . | . . . | . 4 .
. . . | 4 6 9 | . . .
4 . . | . . . | . . 7
---------------------
. . 5 | 9 . 4 | 6 . .
. 7 . | 6 . 8 | . 3 .
. . 8 | 5 . 2 | 1 . .
---------------------
9 . . | . . . | . . 5
. . . | 7 8 1 | . . .
. 6 . | . . . | . 1 .

State After Constraint Propagation
. 8 . | 1 . 7 | . 4 .
7 . . | 4 6 9 | . 5 .
4 . . | 8 . 3 | . . 7
---------------------
1 3 5 | 9 7 4 | 6 . .
2 7 . | 6 1 8 | 5 3 .
6 . 8 | 5 3 2 | 1 7 .
---------------------
9 . . | . 4 6 | . . 5
. . . | 7 8 1 | . . .
8 6 . | . 9 5 | . 1 .

Solved After Search
5 8 6 | 1 2 7 | 9 4 3
7 2 3 | 4 6 9 | 8 5 1
4 9 1 | 8 5 3 | 2 6 7
---------------------
1 3 5 | 9 7 4 | 6 2 8
2 7 9 | 6 1 8 | 5 3 4
6 4 8 | 5 3 2 | 1 7 9
---------------------
9 1 7 | 2 4 6 | 3 8 5
3 5 2 | 7 8 1 | 4 9 6
8 6 4 | 3 9 5 | 7 1 2
```

The solver solves all 50 puzzles in just under 500ms.
