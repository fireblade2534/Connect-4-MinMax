import sys

class Connect4:
    ROWS = 6
    COLS = 7

    def __init__(self):
        # Initialize an empty board
        self.board = [[0 for _ in range(self.COLS)] for _ in range(self.ROWS)]

    def copy(self):
        new_board = Connect4()
        new_board.board = [row.copy() for row in self.board]
        return new_board

    def make_move(self, col, player):
        """
        Apply the move to the board.
        :param col: Column to drop the piece (0-indexed)
        :param player: 1 or -1
        :return: True if move is successful, False otherwise
        """
        for row in reversed(range(self.ROWS)):
            if self.board[row][col] == 0:
                self.board[row][col] = player
                return True
        return False  # Column is full

    def get_valid_moves(self):
        """
        Return a list of columns that are not full.
        """
        return [c for c in range(self.COLS) if self.board[0][c] == 0]

    def is_full(self):
        """
        Check if the board is full.
        """
        return all(self.board[0][c] != 0 for c in range(self.COLS))

    def check_winner(self):
        """
        Check if there's a winner.
        :return: 1 if Player 1 wins, -1 if Player 2 wins, 0 otherwise
        """
        # Check horizontal, vertical, and both diagonals
        for row in range(self.ROWS):
            for col in range(self.COLS):
                if self.board[row][col] == 0:
                    continue
                player = self.board[row][col]
                # Check horizontal
                if col + 3 < self.COLS and all(self.board[row][col+i] == player for i in range(4)):
                    return player
                # Check vertical
                if row + 3 < self.ROWS and all(self.board[row+i][col] == player for i in range(4)):
                    return player
                # Check diagonal /
                if row + 3 < self.ROWS and col + 3 < self.COLS and all(self.board[row+i][col+i] == player for i in range(4)):
                    return player
                # Check diagonal \
                if row - 3 >= 0 and col + 3 < self.COLS and all(self.board[row-i][col+i] == player for i in range(4)):
                    return player
        return 0  # No winner

    def evaluate_window(self, window, player):
        """
        Evaluate a window of four cells.
        """
        score = 0
        opponent = -player

        if window.count(player) == 4:
            score += 100
        elif window.count(player) == 3 and window.count(0) == 1:
            score += 5
        elif window.count(player) == 2 and window.count(0) == 2:
            score += 2

        if window.count(opponent) == 3 and window.count(0) == 1:
            score -= 4

        return score

    def score_position(self, player):
        """
        Score the board from the perspective of the given player.
        """
        score = 0

        # Score horizontal
        for row in range(self.ROWS):
            row_array = self.board[row]
            for col in range(self.COLS - 3):
                window = row_array[col:col+4]
                score += self.evaluate_window(window, player)

        # Score vertical
        for col in range(self.COLS):
            col_array = [self.board[row][col] for row in range(self.ROWS)]
            for row in range(self.ROWS - 3):
                window = col_array[row:row+4]
                score += self.evaluate_window(window, player)

        # Score positive diagonal
        for row in range(self.ROWS - 3):
            for col in range(self.COLS - 3):
                window = [self.board[row+i][col+i] for i in range(4)]
                score += self.evaluate_window(window, player)

        # Score negative diagonal
        for row in range(3, self.ROWS):
            for col in range(self.COLS - 3):
                window = [self.board[row-i][col+i] for i in range(4)]
                score += self.evaluate_window(window, player)

        return score

    def is_terminal_node(self):
        return self.check_winner() != 0 or self.is_full()

    def print_board(self):
        for row in self.board:
            print(' '.join(['.' if cell == 0 else ('X' if cell == 1 else 'O') for cell in row]))
        print()

def negamax(board, depth, alpha, beta, player):
    """
    NegaMax implementation with Alpha-Beta pruning.
    :param board: Current board state
    :param depth: Depth limit
    :param alpha: Alpha value for pruning
    :param beta: Beta value for pruning
    :param player: Current player (1 or -1)
    :return: Tuple (score, column)
    """
    valid_moves = board.get_valid_moves()
    is_terminal = board.is_terminal_node()
    if depth == 0 or is_terminal:
        if is_terminal:
            winner = board.check_winner()
            if winner == player:
                return (float('inf'), None)
            elif winner == -player:
                return (float('-inf'), None)
            else:  # Game is over, no more valid moves
                return (0, None)
        else:
            return (board.score_position(player), None)

    max_score = float('-inf')
    best_col = None
    for col in valid_moves:
        temp_board = board.copy()
        temp_board.make_move(col, player)
        score, _ = negamax(temp_board, depth-1, -beta, -alpha, -player)
        score = -score
        if score > max_score:
            max_score = score
            best_col = col
        alpha = max(alpha, score)
        if alpha >= beta:
            break  # Alpha-Beta pruning
    return (max_score, best_col)

def parse_move_sequence(sequence):
    """
    Parse a sequence of digits into a list of column moves (0-indexed).
    Assuming the digits represent columns 1 to 7.
    """
    return [int(c)-1 for c in sequence if c.isdigit() and 1 <= int(c) <= 7]

def main():
    import os

    filename = "Test_L2_R1"
    if not os.path.exists(filename):
        print(f"Test file '{filename}' not found.")
        sys.exit(1)

    game = Connect4()

    with open(filename, 'r') as file:
        for line_num, line in enumerate(file, 1):
            line = line.strip()
            if not line:
                continue
            try:
                move_sequence, expected = line.split()
                expected = float(expected)
                moves = parse_move_sequence(move_sequence)
            except ValueError:
                print(f"Invalid format in line {line_num}: {line}")
                continue

            # Reset the board for each test case
            game = Connect4()
            current_player = 1  # Player 1 starts

            # Apply the move sequence
            valid = True
            for move in moves:
                if not game.make_move(move, current_player):
                    print(f"Invalid move {move+1} in line {line_num}")
                    valid = False
                    break
                current_player *= -1  # Switch player

            if not valid:
                continue

            # Optionally, you can print the board
            # print(f"Test case {line_num}:")
            # game.print_board()

            # Run NegaMax to evaluate the position
            search_depth = 4  # You can adjust the depth
            score, best_move = negamax(game, search_depth, float('-inf'), float('inf'), current_player)

            # Print the results
            print(f"Test case {line_num}:")
            print(f"Move sequence: {move_sequence}")
            print(f"Expected evaluation: {expected}")
            print(f"NegaMax evaluation: {score}")
            if best_move is not None:
                print(f"Recommended move: Column {best_move+1}")
            else:
                print("No possible moves.")
            print("-" * 30)

if __name__ == "__main__":
    main()