"""
    A list of example sudoku, that can be solved using the Z3 Solver.

"""

SIMPLE_SUDOKU = [
    # Examples taken from US PYcon December 2019
    # https://rhettinger.github.io/einstein.html
    '53  7    6  195    98    6 8   6   34  8 3  17   2   6 6    28    419  5    8  79',
    '       75  4  5   8 17 6   36  2 7 1   5 1   1 5 8  96   1 82 3   4  9  48       ',
    ' 9 7 4  1    6 2 8    1 43  6     59   1 3   97     8  52 7    6 8 4    7  5 8 2 ',
    '67 38      921   85    736 1 8  4 7  5 1 8 4  2 6  8 5 175    24   321      61 84',
    '27  15  8   3  7 4    7     5 1   7   9   2   6   2 5     8    6 5  4   8  59  41',
    '8 64 3    5     7     2    32  8  5   8 5 4  1   7  93    4     9     4    6 72 8',
]

HARD_SUDOKU = [
    # hardest Sudoku: https://www.conceptispuzzles.com/index.aspx?uri=info/article/424
    '8          36      7  9 2   5   7       457     1   3   1    68  85   1  9    4  ',

    # Cracking the cryptic
    # https: // cracking-the-cryptic.web.app / sudoku / nn468RjnbB
    '2 1 7 8   4     3 8  2    547  65 936 5                  34 6    47   1 79  5   8',
]

KNIGHT_CONSTRAINT = [
    # https: // cracking-the-cryptic.web.app / sudoku / n9mq3gTF4J
    '     5   1      7         26 4  7      8   6             2        39             ',
]

KINGS_MOVE_CONSTRAINT = [
    # Cracking the cryptic: https://www.youtube.com/watch?v=N41yZsxIsK8&t=684s
    '   431     8   4   3     1 2       53   6   99       2 7     6   9   5     853   ',
]

NON_CONSECUTIVE_CONSTRAINT = [
    # https://app.crackingthecryptic.com/webapp/HFQNbqqB4n
    ' ' * 5 * 9 + '3 9 4 1 6 9 4 5 3 8 7 6 5 4' + ' ' * 9,
]

MIRACLE = [
    # Cracking the cryptic: https://www.youtube.com/watch?v=yKf9aUIxdb4&t=271s
    # Knight move, Kings move and non consecutive constraint
    ' ' * 4 * 9 + '  1' + ' ' * 4 * 3 + '2  ' + ' ' * 3 * 9
]
