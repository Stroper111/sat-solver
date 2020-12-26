# Sat-solver

With the increase in [SAT][sat-wiki] solvers speed I tried my hand at experimenting with them.

The experiments have been run with:

- Microsoft Z3 solver, for the documentation and tutorials, check out [Z3Py][z3py-docs].
- Pycosat, for the documentation and examples, check out [Pycosat][pycosat-docs].

[sat-wiki]: https://en.wikipedia.org/wiki/Boolean_satisfiability_problem

[z3py-docs]: https://ericpony.github.io/z3py-tutorial/guide-examples.htm

[pycosat-docs]: https://github.com/ContinuumIO/pycosat

## Sudoku

For the Sudoku solver I used the basic Sudoku rules but expanded them with some common rules used on
the [Cracking The Cryptic][ctc] channel. These extra constraints are the Kings move, Knight move and non-consecutive
constraints. This make it possible to solve the following Sudoku (in real life and using the SAT solver <sup>1</sup>):


[ctc]: https://www.youtube.com/channel/UCC-UOdK8-mIjxBQm_ot1T-Q
[1]: [youtube solve](https://www.youtube.com/watch?v=yKf9aUIxdb4)

```
Begin state and solved state of the Sudoku (valid=True)

 .  .  .  |  .  .  .  |  .  .  . 		 4  8  3  |  7  2  6  |  1  5  9 
 .  .  .  |  .  .  .  |  .  .  . 		 7  2  6  |  1  5  9  |  4  8  3 
 .  .  .  |  .  .  .  |  .  .  . 		 1  5  9  |  4  8  3  |  7  2  6 
 -  -  -  +  -  -  -  +  -  -  - 		 -  -  -  +  -  -  -  +  -  -  - 
 .  .  .  |  .  .  .  |  .  .  . 		 8  3  7  |  2  6  1  |  5  9  4 
 .  .  1  |  .  .  .  |  .  .  . 		 2  6  1  |  5  9  4  |  8  3  7 
 .  .  .  |  .  .  .  |  2  .  . 		 5  9  4  |  8  3  7  |  2  6  1 
 -  -  -  +  -  -  -  +  -  -  - 		 -  -  -  +  -  -  -  +  -  -  - 
 .  .  .  |  .  .  .  |  .  .  . 		 3  7  2  |  6  1  5  |  9  4  8 
 .  .  .  |  .  .  .  |  .  .  . 		 6  1  5  |  9  4  8  |  3  7  2 
 .  .  .  |  .  .  .  |  .  .  . 		 9  4  8  |  3  7  2  |  6  1  5
```

The normal sudplu solution has also been verified using a backtracking algorithm. The backtracking for the special
sudoku cases, takes a long times and is better avoided.

For more Sudoku examples see the [examples](/sudoku/sudoku_examples.py)

## Use cases

- [Efficient SAT Approach to Multi-Agent Path Finding under the Sum of Costs Objective](https://www.andrew.cmu.edu/user/gswagner/workshop/IJCAI_2016_WOMPF_paper_5.pdf)
