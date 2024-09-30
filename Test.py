import math
import time
from collections import deque

class TranspositionTable:
    def __init__(self, size=1024):
        self.size = size
        self.table = {}
        self.order = deque()

    def put(self, key, value):
        if key in self.table:
            # Move the key to the end to mark it as recently used
            self.order.remove(key)
        elif len(self.table) >= self.size:
            # Remove the oldest entry
            oldest = self.order.popleft()
            del self.table[oldest]
        self.table[key] = value
        self.order.append(key)

    def get(self, key):
        if key in self.table:
            # Move the key to the end to mark it as recently used
            self.order.remove(key)
            self.order.append(key)
            return self.table[key]
        return None

class BoardState:
    def __init__(self, state="", width=7, height=6, win_length=4):
        self.width = width
        self.height = height
        self.win_length = win_length

        self.min_score = -((self.width * self.height) // 2) + 3
        self.max_score = ((self.width * self.height + 1) // 2) - 3

        self.moves = len(state)
        # Initialize bitboards for both players
        self.board = [0, 0]

        # Initialize column heights
        self.heights = [0] * self.width

        # Precompute bit shifts for win detection
        self.bit_shifts = [1, self.height + 1, self.height, self.height + 2]

        # Translate the initial state into bitboards
        self._translate_to_board(state)

    def _translate_to_board(self, state):
        for move_char in state:
            move = int(move_char) - 1  # Convert to 0-based index
            if not (0 <= move < self.width):
                raise ValueError(f"Invalid move: {move_char}")
            player = self.moves % 2
            bit_position = self.heights[move] + move * (self.height + 1)
            self.board[player] |= 1 << bit_position
            self.heights[move] += 1
            self.moves += 1

    def make_move(self, column):
        bit_position = self.heights[column] + column * (self.height + 1)
        bit = 1 << bit_position
        current_player = self.moves % 2
        self.board[current_player] |= bit  # Set the bit using OR
        self.heights[column] += 1
        self.moves += 1

    def undo_move(self, column):
        self.moves -= 1
        self.heights[column] -= 1
        bit_position = self.heights[column] + column * (self.height + 1)
        bit = 1 << bit_position
        current_player = self.moves % 2
        self.board[current_player] &= ~bit  # Clear the bit using AND NOT

    def is_column_full(self, column):
        return self.heights[column] >= self.height

    def is_board_full(self):
        return self.moves >= self.width * self.height

    def get_key(self):
        # Combine both bitboards into a single unique key
        return self.board[0] | (self.board[1] << (self.width * (self.height + 1)))

    def is_winning_move(self, column):
        bit_position = self.heights[column] + column * (self.height + 1)
        bit = 1 << bit_position
        current_player = self.moves % 2  # Player who is about to make the move
        temp = self.board[current_player] | bit
        for shift in self.bit_shifts:
            m = temp & (temp >> shift)
            if m & (m >> (2 * shift)):
                return True
        return False

    def render(self):
        grid = [[' ' for _ in range(self.width)] for _ in range(self.height)]
        for x in range(self.width):
            for y in range(self.heights[x]):
                bit_pos = y + x * (self.height + 1)
                if self.board[0] & (1 << bit_pos):
                    grid[y][x] = "🔴"
                elif self.board[1] & (1 << bit_pos):
                    grid[y][x] = "🟡"
        output = "\n".join(["|".join(row) for row in reversed(grid)])
        separator = "\n" + "--" * self.width + "-"
        print(separator.join(output.split("\n")))

class NegMaxSolver:
    def __init__(self, width=7):
        self.move_order = self.init_move_order(width)

    @staticmethod
    def init_move_order(width):
        center = width // 2
        order = [center]
        for offset in range(1, center + 1):
            if center - offset >= 0:
                order.append(center - offset)
            if center + offset < width:
                order.append(center + offset)
        return order

    def negamax(self, board, alpha, beta, trans_table):
        key = board.get_key()
        trans_value = trans_table.get(key)
        if trans_value is not None:
            return trans_value

        if board.is_board_full():
            return 0  # Draw

        # Check for immediate win
        for move in self.move_order:
            if not board.is_column_full(move):
                if board.is_winning_move(move):
                    # The score is how soon a win can be achieved
                    return ((board.width * board.height + 1) - board.moves) // 2

        max_score = ((board.width * board.height - 1) - board.moves) // 2
        if beta > max_score:
            beta = max_score
            if alpha >= beta:
                return beta

        for move in self.move_order:
            if not board.is_column_full(move):
                board.make_move(move)
                score = -self.negamax(board, -beta, -alpha, trans_table)
                board.undo_move(move)

                if score >= beta:
                    return score
                if score > alpha:
                    alpha = score

        trans_table.put(key, alpha)  # Store the exact score
        return alpha

    def solve(self, board, weak=False, table_size=1024):
        trans_table = TranspositionTable(table_size)
        min_score = -(board.width * board.height) // 2
        max_score = (board.width * board.height + 1) // 2

        if weak:
            min_score = -1
            max_score = 1

        while min_score < max_score:
            mid = (min_score + max_score) // 2
            score = self.negamax(board, mid, mid + 1, trans_table)
            if score <= mid:
                max_score = score
            else:
                min_score = score
        return min_score

# Initialize the solver with the desired board width
solver = NegMaxSolver(width=7)

def main():
    failed = []
    tested = 0
    total_time = 0
    start_time = time.time()

    try:
        with open("Test_L2_R1", "r") as file:
            for line in file:
                parts = line.strip().split()
                if not parts:
                    continue
                state_str, expected_str = parts
                expected = int(expected_str)

                try:
                    board = BoardState(state=state_str, width=7, height=6)
                except ValueError as ve:
                    print(f"Invalid test case {tested + 1}: {ve}")
                    failed.append((state_str, 'Invalid Move', expected))
                    tested += 1
                    continue

                test_start = time.time()
                score = solver.solve(board, weak=False, table_size=8024)
                test_end = time.time()
                elapsed = test_end - test_start
                total_time += elapsed

                tested += 1

                if score != expected:
                    failed.append((state_str, score, expected))

                print(f"Done {tested}: Score={score}, Expected={expected}")
    except FileNotFoundError:
        print("Test file 'Test_L1_R1' not found.")
        return

    end_time = time.time()
    overall_elapsed = end_time - start_time
    avg_time = total_time / tested if tested else 0

    print(f"\nTested: {tested}")
    print(f"Failed: {len(failed)}")
    if failed:
        print("Failed Cases:")
        for state, score, expected in failed:
            print(f"State: {state}, Score: {score}, Expected: {expected}")
    print(f"Overall Time: {overall_elapsed:.6f} seconds")
    print(f"Average Time per Test: {avg_time:.6f} seconds")

if __name__ == "__main__":
        main()