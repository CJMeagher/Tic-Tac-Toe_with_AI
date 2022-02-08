import random


class TicTacToe:
    def __init__(self):
        self.cells = dict()
        self.play_method = dict()
        self.winning_cell_sets = [
            {(1, 1), (1, 2), (1, 3)},
            {(2, 1), (2, 2), (2, 3)},
            {(3, 1), (3, 2), (3, 3)},
            {(1, 1), (2, 1), (3, 1)},
            {(1, 2), (2, 2), (3, 2)},
            {(1, 3), (2, 3), (3, 3)},
            {(1, 1), (2, 2), (3, 3)},
            {(3, 1), (2, 2), (1, 3)},
        ]
        self.current_player = "X"

    def play(self):
        while True:
            if self.set_up_new_game() == "exit":
                quit()
            winner = self.game_loop()  # returns X, O or None
            if winner:
                print(f"{winner} wins")
            else:
                print("Draw")
            print()

    def set_up_new_game(self):

        # create empty board as dictionary with cell coordinates as keys and blanks as values.
        # i.e. {(1,1): " ",(1,2): " ",(1,3): " ", ...(3,3): " "}
        all_cells = ((row, column) for row in [1, 2, 3] for column in [1, 2, 3])
        self.cells = dict.fromkeys(all_cells, " ")

        while True:
            user_input = input("Input command: ").lower().split()
            action, x_player, o_player = "   "
            if len(user_input) == 1:
                action = user_input[0]
            elif len(user_input) == 3:
                action, x_player, o_player = user_input
            try:
                if (action not in {"start", "exit"}) or (
                    action == "start"
                    and (
                        x_player
                        not in (play_suffix := {"user", "easy", "medium", "hard"})
                        or o_player not in play_suffix
                    )
                ):
                    raise Exception("Bad parameters!")
                break
            except Exception as e:
                print(e)

        if action == "start":
            # store the play method for a player in a dictionary,
            # so if O is playing as 'easy' then play_method{"O"] = self.play_easy
            self.play_method["X"] = eval(f"self.play_{x_player}")
            self.play_method["O"] = eval(f"self.play_{o_player}")
        return action

    def game_loop(self):
        self.draw_board()
        for player in "XOXOXOXOX":
            self.current_player = player
            player_choice = self.play_method[player](player)  # e.g. self.play_easy("O")
            self.cells[player_choice] = player
            self.draw_board()
            if self.do_we_have_a_winner(player):
                return player

    def play_user(self, _):
        while True:
            user_input = input("Enter the coordinates: ")
            try:
                user_cell_choice = tuple(int(i) for i in user_input.split())  # ValueError
                if self.cells[user_cell_choice] != " ":  # KeyError if not a valid cell
                    raise Exception("This cell is occupied! Choose another one!")
                break
            except ValueError:
                print("You should enter numbers!")
            except KeyError:
                print("Coordinates should be from 1 to 3!")
            except Exception as e:
                print(e)
        return user_cell_choice

    def play_easy(self, _):
        print(f'Making move level "easy"')
        available_cells = self.get_cells_by_occupant(" ")
        return random.choice(available_cells)

    def play_medium(self, player):
        print(f'Making move level "medium"')
        available_cells = self.get_cells_by_occupant(" ")
        other_player = "O" if player == "X" else "X"
        for a_player in [player, other_player]:
            for cell in available_cells:
                self.cells[cell] = a_player
                if self.do_we_have_a_winner(a_player):
                    self.cells[cell] = " "
                    return cell
                self.cells[cell] = " "
        return random.choice(available_cells)

    def play_hard(self, player):
        print(f'Making move level "hard"')
        # shortcut - recursion gives equal value to all cells on
        # first move.  So just select randomly to save processing.
        available_cells = self.get_cells_by_occupant(" ")
        if len(available_cells) == 9:
            return random.choice(available_cells)
        cell, _ = self.play_hard_recursion(player)
        return cell

    def play_hard_recursion(self, player):
        # create dictionary to hold scores for available cells initialized to 0s
        # e.g. then after scoring complete -> {(1, 1): 0, (1, 3): 1, (2, 1): -1}
        available_cells = self.get_cells_by_occupant(" ")
        scores_by_cell = dict.fromkeys(available_cells, 0)

        for cell in available_cells:
            self.cells[cell] = player
            if self.do_we_have_a_winner(player):
                if player == self.current_player:
                    scores_by_cell[cell] = 1
                else:
                    scores_by_cell[cell] = -1
            else:
                more_available_cells = self.get_cells_by_occupant(" ")
                if more_available_cells:
                    other_player = "O" if player == "X" else "X"
                    _, score = self.play_hard_recursion(other_player)
                    scores_by_cell[cell] = score
            self.cells[cell] = " "

        # sometimes a caller wants a cell, sometimes a score.
        # So return a tuple with both.  e.g. ((3,1), -1)
        scores = scores_by_cell.values()
        target_score = max(scores) if player == self.current_player else min(scores)
        best_cells_and_scores = [
            (cell, score)
            for cell, score in scores_by_cell.items()
            if score == target_score
        ]
        return random.choice(best_cells_and_scores)

    def do_we_have_a_winner(self, player):
        player_cell_set = set(self.get_cells_by_occupant(player))
        for winning_cell_set in self.winning_cell_sets:
            if winning_cell_set.issubset(player_cell_set):
                return True

    def get_cells_by_occupant(self, player):
        cells = [cell for cell, value in self.cells.items() if value == player]
        return cells

    def draw_board(self):
        print("---------")
        print(
            f"| {self.cells.get((1, 1))} {self.cells.get((1, 2))} {self.cells.get((1, 3))} |\n"
            f"| {self.cells.get((2, 1))} {self.cells.get((2, 2))} {self.cells.get((2, 3))} |\n"
            f"| {self.cells.get((3, 1))} {self.cells.get((3, 2))} {self.cells.get((3, 3))} |"
        )
        print("---------")


def main():
    ttt = TicTacToe()
    ttt.play()


if __name__ == "__main__":
    main()
