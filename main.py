import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QLabel, QVBoxLayout
import random
from PyQt5.QtWidgets import QComboBox
class TicTacToe(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tic Tac Toe - PyQt5 AI")
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.buttons = [[QPushButton() for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.scores = {'X': 0, 'O': 0}

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.grid_layout = QGridLayout()
        self.difficulty_box = QComboBox()
        self.difficulty_box.addItems(["Easy", "Medium", "Hard"])
        self.difficulty_box.setCurrentText("Hard")
        layout.addWidget(QLabel("AI Difficulty:"))
        layout.addWidget(self.difficulty_box)
        # Create buttons
        for row in range(3):
            for col in range(3):
                button = self.buttons[row][col]
                button.setFixedSize(100, 100)
                button.setStyleSheet("font-size: 24px;")
                self.grid_layout.addWidget(button, row, col)
                button.clicked.connect(lambda _, r=row, c=col: self.handle_click(r, c))

        self.label = QLabel("Player: X")
        self.score_label = QLabel("Score - X: 0 | O: 0")
        self.restart_button = QPushButton("Restart")
        self.restart_button.clicked.connect(self.restart_game)

        layout.addWidget(self.label)
        layout.addLayout(self.grid_layout)
        layout.addWidget(self.score_label)
        layout.addWidget(self.restart_button)
        self.setLayout(layout)

    def handle_click(self, row, col):
        if self.board[row][col] == '':
            self.make_move(row, col, 'X')
            if not self.check_winner('X') and not self.is_full():
                self.ai_move()

    def make_move(self, row, col, player):
        self.board[row][col] = player
        self.buttons[row][col].setText(player)
        self.buttons[row][col].setEnabled(False)

        if self.check_winner(player):
            self.label.setText(f"{player} wins!")
            self.scores[player] += 1
            self.update_score()
            self.disable_all()
        elif self.is_full():
            self.label.setText("It's a draw!")
        else:
            self.label.setText(f"Player: {'O' if player == 'X' else 'X'}")

    def ai_move(self):
        difficulty = self.difficulty_box.currentText()

        if difficulty == "Easy":
            move = random.choice(self.get_empty_cells(self.board))
        elif difficulty == "Medium":
            # 50% chance random, 50% minimax
            if random.random() < 0.5:
                move = random.choice(self.get_empty_cells(self.board))
            else:
                _, move = self.minimax(self.board, True)
        else:  # Hard
            _, move = self.minimax(self.board, True)

        if move:
            self.make_move(move[0], move[1], 'O')

    def get_empty_cells(self, board):
        return [(r, c) for r in range(3) for c in range(3) if board[r][c] == '']

    def minimax(self, board, is_maximizing):
        winner = self.check_winner_static(board)
        if winner == 'O':
            return 1, None
        elif winner == 'X':
            return -1, None
        elif self.is_full_static(board):
            return 0, None

        best_move = None

        if is_maximizing:
            best_score = -float('inf')
            for (r, c) in self.get_empty_cells(board):
                board[r][c] = 'O'
                score, _ = self.minimax(board, False)
                board[r][c] = ''
                if score > best_score:
                    best_score = score
                    best_move = (r, c)
        else:
            best_score = float('inf')
            for (r, c) in self.get_empty_cells(board):
                board[r][c] = 'X'
                score, _ = self.minimax(board, True)
                board[r][c] = ''
                if score < best_score:
                    best_score = score
                    best_move = (r, c)

        return best_score, best_move

    def check_winner(self, player):
        # Current board check
        return self.check_winner_static(self.board) == player

    def check_winner_static(self, board):
        # Rows, cols, diags
        for i in range(3):
            if board[i][0] == board[i][1] == board[i][2] != '':
                return board[i][0]
            if board[0][i] == board[1][i] == board[2][i] != '':
                return board[0][i]
        if board[0][0] == board[1][1] == board[2][2] != '':
            return board[0][0]
        if board[0][2] == board[1][1] == board[2][0] != '':
            return board[0][2]
        return None

    def is_full(self):
        return all(cell != '' for row in self.board for cell in row)

    def is_full_static(self, board):
        return all(cell != '' for row in board for cell in row)

    def update_score(self):
        self.score_label.setText(f"Score - X: {self.scores['X']} | O: {self.scores['O']}")

    def disable_all(self):
        for row in self.buttons:
            for btn in row:
                btn.setEnabled(False)

    def restart_game(self):
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.label.setText("Player: X")
        for row in range(3):
            for col in range(3):
                btn = self.buttons[row][col]
                btn.setText('')
                btn.setEnabled(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = TicTacToe()
    game.show()
    sys.exit(app.exec_())