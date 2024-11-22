import copy
from typing import List, Any, Tuple
from stack_and_queue import Stack, Queue

def remove_if_present(lst: Any, elem: Any) -> None:
    if isinstance(lst, list) and elem in lst:
        lst.remove(elem)

class Board:
    def __init__(self):
        self.size: int = 9
        self.num_nums_placed: int = 0
        self.rows: List[List[Any]] = (
            [[list(range(1, 10)) for _ in range(self.size)] for _ in range(self.size)]
        )

    def __str__(self) -> str:
        row_str = ""
        row_num = 0 
        for r in self.rows:
            row_str += f"Row {row_num}: {r}\n"
        return f"num_nums_placed: {self.num_nums_placed}\nboard (rows): \n{row_str}"

    def print_pretty(self):
        row_str = ""
        for i, r in enumerate(self.rows):
            if not i % 3:
                row_str += " -------------------------\n"
            for j, x in enumerate(r):
                row_str += " | " if not j % 3 else " "
                row_str += "*" if isinstance(x, list) else f"{x}"
            row_str += " |\n"
        row_str += " -------------------------\n"
        print(f"num_nums_placed: {self.num_nums_placed}\nboard (rows): \n{row_str}")

    def subgrid_coordinates(self, row: int, col: int) -> List[Tuple[int, int]]:
        subgrids = [(0, 1, 2), (3, 4, 5), (6, 7, 8)]
        return [(r, c) for c in subgrids[col // 3] for r in subgrids[row // 3]]

    def find_most_constrained_cell(self) -> Tuple[int, int]:
        min_size = 9
        min_row = 0
        min_col = 0
        for i in range(self.size):
            for j in range(self.size):
                cell = self.rows[i][j]
                if isinstance(cell, list) and len(cell) < min_size:
                    min_size = len(cell)
                    min_row = i 
                    min_col = j 
        return (min_row, min_col)

    def failure_test(self) -> bool:
        for r in range(self.size):
            for c in range(self.size):
                cell = self.rows[r][c]
                if isinstance(cell, list) and not cell: 
                    return True 
        return False 

    def goal_test(self) -> bool:
        return self.num_nums_placed == self.size * self.size  

    def update(self, row: int, column: int, assignment: int) -> None:
        self.rows[row][column] = assignment 
        self.num_nums_placed += 1 
        for i in range(self.size):
            remove_if_present(self.rows[row][i], assignment)
            remove_if_present(self.rows[i][column], assignment)
        for i, j in self.subgrid_coordinates(row, column):
            remove_if_present(self.rows[i][j], assignment)

def DFS(state: Board) -> Board:
    s = Stack([state])
    while not s.is_empty():
        b: Board = s.pop()
        if b.goal_test():
            return b 
        mcc = b.find_most_constrained_cell()
        row = mcc[0]
        col = mcc[1]
        for sel in b.rows[row][col]:
            cpy = copy.deepcopy(b)
            cpy.update(row, col, sel)
            s.push(cpy)

def BFS(state: Board) -> Board:
    q = Queue([state])
    while not q.is_empty():
        b: Board = q.pop()
        if b.goal_test():
            return b 
        mcc = b.find_most_constrained_cell()
        row = mcc[0]
        col = mcc[1]
        for sel in b.rows[row][col]:
            cpy = copy.deepcopy(b)
            cpy.update(row, col, sel)
            q.push(cpy)

if __name__ == "__main__":
    b = Board()
    b.print_pretty()
    b.update(0, 0, 1)
    b.print_pretty()
    b.update(0, 2, 2)
    b.update(1, 0, 9)
    b.update(1, 1, 8)
    b.update(0, 4, 3)
    b.update(1, 6, 4)
    b.update(1, 3, 2)
    b.update(1, 8, 3)
    b.print_pretty()
    print("<<<<<<<<<<<<<< Solving Sudoku >>>>>>>>>>>>>>")

    def test_dfs_or_bfs(use_dfs: bool, moves: List[Tuple[int, int, int]]) -> None:
        b = Board()
        for move in moves:
            b.update(*move)
        print("<<<<< Initial Board >>>>>")
        b.print_pretty()
        solution = (DFS if use_dfs else BFS)(b)
        print("<<<<< Solved Board >>>>>")
        solution.print_pretty()

    first_moves = [
        (0, 1, 7),
        (0, 7, 1),
        (1, 2, 9),
        (1, 3, 7),
        (1, 5, 4),
        (1, 6, 2),
        (2, 2, 8),
        (2, 3, 9),
        (2, 6, 3),
        (3, 1, 4),
        (3, 2, 3),
        (3, 4, 6),
        (4, 1, 9),
        (4, 3, 1),
        (4, 5, 8),
        (4, 7, 7),
        (5, 4, 2),
        (5, 6, 1),
        (5, 7, 5),
        (6, 2, 4),
        (6, 5, 5),
        (6, 6, 7),
        (7, 2, 7),
        (7, 3, 4),
        (7, 5, 1),
        (7, 6, 9),
        (8, 1, 3),
        (8, 7, 8),
    ]

    second_moves = [
        (0, 1, 2),
        (0, 3, 3),
        (0, 5, 5),
        (0, 7, 4),
        (1, 6, 9),
        (2, 1, 7),
        (2, 4, 4),
        (2, 7, 8),
        (3, 0, 1),
        (3, 2, 7),
        (3, 5, 9),
        (3, 8, 2),
        (4, 1, 9),
        (4, 4, 3),
        (4, 7, 6),
        (5, 0, 6),
        (5, 3, 7),
        (5, 6, 5),
        (5, 8, 8),
        (6, 1, 1),
        (6, 4, 9),
        (6, 7, 2),
        (7, 2, 6),
        (8, 1, 4),
        (8, 3, 8),
        (8, 5, 7),
        (8, 7, 5),
    ]
    
    b = Board()
    for trip in first_moves:
        b.rows[trip[0]][trip[1]] = trip[2]
    b.print_pretty()
    
    remove_if_present(b.rows[0][0], 8)
    remove_if_present(b.rows[0][0], 7)
    remove_if_present(b.rows[0][0], 3)
    remove_if_present(b.rows[0][0], 2)
    remove_if_present(b.rows[4][8], 8)
    remove_if_present(b.rows[4][8], 1)
    remove_if_present(b.rows[4][8], 2)
    remove_if_present(b.rows[4][8], 3)
    remove_if_present(b.rows[4][8], 4)
    remove_if_present(b.rows[6][7], 2)
    remove_if_present(b.rows[6][7], 3)
    remove_if_present(b.rows[6][7], 5)
    remove_if_present(b.rows[6][7], 6)

    assert b.find_most_constrained_cell() == (4, 8), "find most constrained cell test 1"
    assert b.failure_test() == False, "failure test test 1"
    assert b.goal_test() == False, "goal test test 1"

    b.rows[4][3] = []
    assert b.find_most_constrained_cell() == (4, 3), "find most constrained cell test 2"
    assert b.failure_test() == True, "failure test test 2"
    print("All part 1 tests passed!")

    g = Board()
    for trip in first_moves:
        g.update(trip[0], trip[1], trip[2])
    print("<<<<<< DFS Test >>>>>>")
    test_dfs_or_bfs(True, first_moves)
    print("<<<<<< BFS Test >>>>>>")
    test_dfs_or_bfs(False, first_moves)

    print("<<<<<< DFS Test >>>>>>")
    test_dfs_or_bfs(True, second_moves)
    print("<<<<<< BFS Test >>>>>>")
    test_dfs_or_bfs(False, second_moves)
    pass     
