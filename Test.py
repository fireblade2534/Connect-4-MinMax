import math
from collections import OrderedDict

class TranspositionTable:
    def __init__(self, size: int = 256):
        self.size = size
        self.table = OrderedDict()

    def put(self, key: str, value: int):
        if key in self.table:
            self.table.move_to_end(key)
        self.table[key] = value
        if len(self.table) > self.size:
            self.table.popitem(last=False)

    def get(self, key: str):
        if key in self.table:
            self.table.move_to_end(key)
            return self.table[key]
        return 0

class BoardState:
    def __init__(self, state: str, width: int, height: int, win_length: int = 4):
        self.state = state  # String representing the sequence of moves
        self.width = width
        self.height = height
        self.win_length = win_length
        self.min_score = -((width * height) // 2) + 3
        self.max_score = ((width * height + 1) // 2) - 3
        self.board = self._translate_to_board()

    def is_column_full(self, column: int) -> bool:
        # Since state is a string of moves, count the occurrences of the column
        return self.state.count(str(column + 1)) >= self.height

    def is_board_full(self) -> bool:
        return len(self.state) >= self.width * self.height

    def move_number(self) -> int:
        return len(self.state)

    def _translate_to_board(self):
        # Initialize an empty board
        board = [[0 for _ in range(self.width)] for _ in range(self.height)]
        # Track the next available row in each column
        next_row = [self.height - 1] * self.width

        for move_number, move in enumerate(self.state):
            col = int(move) - 1
            if 0 <= col < self.width and next_row[col] >= 0:
                board[next_row[col]][col] = 1 if move_number % 2 == 0 else 2
                next_row[col] -= 1
        return board

    def is_winning_move(self, move: int) -> bool:
        # Adjust move to 0-based index
        col = move
        if self.is_column_full(move):
            return False  # Cannot make a move in a full column

        # Determine the row where the piece will land
        row = self.height - self.state.count(str(move + 1)) - 1
        player = 1 if len(self.state) % 2 == 0 else 2

        # Temporarily place the piece
        self.board[row][col] = player

        # Check all directions for a win
        directions = [
            (0, 1),  # Vertical
            (1, 0),  # Horizontal
            (1, 1),  # Diagonal /
            (1, -1)  # Diagonal \
        ]

        for dx, dy in directions:
            count = 1
            # Check in the positive direction
            x, y = col + dx, row + dy
            while 0 <= x < self.width and 0 <= y < self.height and self.board[y][x] == player:
                count += 1
                x += dx
                y += dy

            # Check in the negative direction
            x, y = col - dx, row - dy
            while 0 <= x < self.width and 0 <= y < self.height and self.board[y][x] == player:
                count += 1
                x -= dx
                y -= dy

            if count >= self.win_length:
                # Remove the temporarily placed piece
                self.board[row][col] = 0
                return True

        # Remove the temporarily placed piece
        self.board[row][col] = 0
        return False

    @staticmethod
    def _format_piece(piece: int) -> str:
        if piece == 1:
            return "🔴"
        if piece == 2:
            return "🟡"
        return "  "

    def render(self):
        board_str = []
        for row in self.board:
            board_str.append("|".join([self._format_piece(cell) for cell in row]))
        separator = "\n" + ("--+" * self.width)[:-1] + "\n"
        print(separator.join(board_str))

    def get_hash(self) -> str:
        # Create a unique hash for the current board state
        return ''.join([''.join(map(str, row)) for row in self.board])

class NegMaxSolver:
    move_order = []

    @staticmethod
    def init_move_order(width: int):
        # Order moves starting from the center column for better pruning
        center = width // 2
        NegMaxSolver.move_order = [center]
        for offset in range(1, center + 1):
            if center - offset >= 0:
                NegMaxSolver.move_order.append(center - offset)
            if center + offset < width:
                NegMaxSolver.move_order.append(center + offset)

    @staticmethod
    def neg_max(board: BoardState, alpha: int, beta: int, trans_table: TranspositionTable) -> int:
        # Generate a unique key for the current board state
        key = board.get_hash()
        # Check transposition table
        trans_value = trans_table.get(key)
        if trans_value != 0:
            return trans_value + board.min_score - 1

        column_states = [board.is_column_full(x) for x in range(board.width)]
        if all(column_states):
            return 0  # Draw

        max_score = ((board.width * board.height - 1) - board.move_number()) // 2

        if beta > max_score:
            beta = max_score
            if alpha >= beta:
                return beta

        # Order moves to improve pruning
        for x in NegMaxSolver.move_order:
            if not column_states[x]:
                if board.is_winning_move(x):
                    return (((board.width * board.height) + 1) - board.move_number()) // 2

        # After checking immediate wins, proceed with recursive search
        for x in NegMaxSolver.move_order:
            if not column_states[x]:
                new_state = board.state + str(x + 1)
                new_board = BoardState(new_state, board.width, board.height, board.win_length)
                score = -NegMaxSolver.neg_max(new_board, -beta, -alpha, trans_table)
                if score >= beta:
                    return score
                if score > alpha:
                    alpha = score

        # Store the result in the transposition table
        trans_table.put(key, alpha - board.min_score + 1)
        return alpha

    @staticmethod
    def solve(board: BoardState, weak: bool = False, table_size: int = 512) -> int:
        trans_table = TranspositionTable(table_size)
        min_score = -((board.width * board.height) - board.move_number()) // 2
        max_score = ((board.width * board.height + 1) - board.move_number()) // 2

        if weak:
            min_score = -1
            max_score = 1

        alpha = min_score
        beta = max_score

        return NegMaxSolver.neg_max(board, alpha, beta, trans_table)

# Initialize move order for a standard Connect Four board
NEG_MAX_WIDTH = 7
NegMaxSolver.init_move_order(NEG_MAX_WIDTH)

import time
Failed=[]
Tested=0
TotalTime=0
StartTime=time.time()
for X in open("Test_L2_R1","r").readlines():
    
    XSplit=X.split(" ")

    #if abs(int(XSplit[1])) < 6:
    B=BoardState(XSplit[0],7,6)
    State=NegMaxSolver.solve(B,False,1024)#NegMax(B,-1,1)#-(6*7)//2,(6*7)//2)
    Tested+=1
    if State != int(XSplit[1]):
        Failed.append([B,State,int(XSplit[1])])
    print("Done",Tested,State,int(XSplit[1]))
print("Tested:",Tested)
print("Failed:",len(Failed))
print("Average Time:",(time.time() - StartTime)/Tested)