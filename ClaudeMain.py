import math
from typing import List, Dict

class TranspositionTable:
    def __init__(self, size: int = 256):
        self.table: Dict[int, int] = {}
        self.max_size = size

    def put(self, key: int, value: int) -> None:
        if len(self.table) >= self.max_size:
            self.table.pop(next(iter(self.table)))
        self.table[key] = value

    def get(self, key: int) -> int:
        return self.table.get(key, 0)

class BoardState:
    def __init__(self, state: str, width: int, height: int, win_length: int = 4):
        self.state = state
        self.width = width
        self.height = height
        self.win_length = win_length
        self.min_score = -((width * height) // 2) + 3
        self.max_score = ((width * height + 1) // 2) - 3
        self.board = self._translate_to_board()

    def col_full(self, column: int) -> bool:
        return self.state.count(str(column + 1)) >= self.height

    def board_full(self) -> bool:
        return len(self.state) >= self.width * self.height

    def move_number(self) -> int:
        return len(self.state)

    def _translate_to_board(self) -> List[List[int]]:
        board = [[0 for _ in range(self.width)] for _ in range(self.height)]
        for n, move in enumerate(self.state):
            col = int(move) - 1
            for y in range(self.height - 1, -1, -1):
                if board[y][col] == 0:
                    board[y][col] = 1 if n % 2 == 0 else 2
                    break
        return board

    def is_winning_move(self, move: int) -> bool:
        move += 1
        new_state = self.state + str(move)
        move_pos = (move - 1, self.height - self.state.count(str(move)) - 1, 1 if len(self.state) % 2 == 0 else 2)
        
        # Check vertical
        if new_state.count(str(move)) > 3:
            if all(self.board[move_pos[1] + i][move_pos[0]] == move_pos[2] for i in range(1, 4)):
                return True

        # Check horizontal, diagonal1, and diagonal2
        for direction in [(1, 0), (1, 1), (1, -1)]:
            count = 1
            for sign in [-1, 1]:
                for i in range(1, 4):
                    x = move_pos[0] + sign * i * direction[0]
                    y = move_pos[1] + sign * i * direction[1]
                    if 0 <= x < self.width and 0 <= y < self.height and self.board[y][x] == move_pos[2]:
                        count += 1
                    else:
                        break
            if count >= self.win_length:
                return True

        return False

    def render(self) -> None:
        pieces = {0: "  ", 1: "🔴", 2: "🟡"}
        output = []
        for row in self.board:
            output.append("|".join(pieces[cell] for cell in row))
        print(f"\n{('--+'*self.width)[:-1]}\n".join(output))

class NegMaxSolver:
    move_order: List[int] = []

    @staticmethod
    def init_move_order(width: int) -> None:
        NegMaxSolver.move_order = [width // 2 + (-x // 2 if x % 2 == 0 else math.ceil(x / 2)) for x in range(width)]

    @staticmethod
    def neg_max(board: BoardState, alpha: int, beta: int, trans_table: TranspositionTable) -> int:
        if board.board_full():
            return 0

        for col in NegMaxSolver.move_order:
            if not board.col_full(col) and board.is_winning_move(col):
                return (board.width * board.height + 1 - board.move_number()) // 2

        max_score = (board.width * board.height - 1 - board.move_number()) // 2
        if beta > max_score:
            beta = max_score
            if alpha >= beta:
                return beta

        for col in NegMaxSolver.move_order:
            if not board.col_full(col):
                new_board = BoardState(f"{board.state}{col+1}", board.width, board.height, board.win_length)
                score = -NegMaxSolver.neg_max(new_board, -beta, -alpha, trans_table)
                if score >= beta:
                    return score
                if score > alpha:
                    alpha = score

        return alpha

    @staticmethod
    def solve(board: BoardState, weak: bool = False, table_size: int = 81) -> int:
        trans_table = TranspositionTable(table_size)
        min_score = -(board.width * board.height - board.move_number()) // 2
        max_score = (board.width * board.height + 1 - board.move_number()) // 2
        if weak:
            min_score, max_score = -1, 1

        while min_score < max_score:
            med = min_score + (max_score - min_score) // 2
            if med <= 0 and min_score // 2 < med:
                med = min_score // 2
            elif med >= 0 and max_score // 2 > med:
                med = max_score // 2
            score = NegMaxSolver.neg_max(board, med, med + 1, trans_table)
            if score <= med:
                max_score = score
            else:
                min_score = score

        return min_score
import time
# Usage
NegMaxSolver.init_move_order(7)

Failed=[]
Tested=0
TotalTime=0
StartTime=time.time()
for X in open("Test_L2_R1","r").readlines():
    #solver = NegMaxSolver.solve()
    XSplit=X.split(" ")
    #if abs(int(XSplit[1])) < 6:
    B=BoardState(XSplit[0],7,6)
    State=NegMaxSolver.solve(B,False)#NegMax(B,-1,1)#-(6*7)//2,(6*7)//2)
    Tested+=1
    if State != int(XSplit[1]):
        Failed.append([B,State,int(XSplit[1])])
    print("Done",Tested,State,int(XSplit[1]))
print("Tested:",Tested)
print("Failed:",len(Failed))
print("Average Time:",(time.time() - StartTime)/Tested)