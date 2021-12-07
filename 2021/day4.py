import collections

from common import problem_data

class BingoBoard:
    def __init__(self, lines):
        self.idxs = {}
        for i, line in enumerate(lines):
            for j, num_str in enumerate(line.split()):
                num = int(num_str, base=10)

                self.idxs[num] = (j, i)

        self.row_len = j + 1
        self.col_len = i + 1
        self.row_marks = collections.Counter({0: 0})
        self.col_marks = collections.Counter({0: 0})

    def mark(self, num):
        try:
            row, col = self.idxs.pop(num)

            self.row_marks[row] += 1
            self.col_marks[col] += 1
        except KeyError:
            pass

    def win(self):
        row, count =  self.row_marks.most_common(1)[0]
        if count == self.row_len:
            return True

        col, count = self.col_marks.most_common(1)[0]
        if count == self.col_len:
            return True

        return False

    def unmarked_sum(self):
        return sum(self.idxs.keys())


def make_boards(input_lines):
    boards = []
    board_input = []
    for line in input_lines:
        if line == "":
            boards.append(BingoBoard(board_input))
            board_input = []
        else:
            board_input.append(line)

    return boards


def read_bingo_data(data):
    numbers = [int(n, base=10) for n in next(data).split(",")]
    newline = next(data)
    boards = make_boards(data)

    return (numbers, boards)


def run_bingo_win(data):
    numbers, boards = read_bingo_data(data)

    for num in numbers:
        winner = None
        for board in boards:
            board.mark(num)

            if board.win():
                winner = board

        if winner is not None:
            return num * winner.unmarked_sum()


print(run_bingo_win(problem_data("day4_sample.txt")))
print(run_bingo_win(problem_data("day4_problem.txt")))


def run_bingo_win_last(data):
    numbers, boards = read_bingo_data(data)

    for num in numbers:
        next_boards = []
        last_winner = None
        for board in boards:
            board.mark(num)

            if board.win():
                if len(boards) == 1:
                    last_winner = board
            else:
                next_boards.append(board)
        boards = next_boards

        if last_winner is not None:
            return num * last_winner.unmarked_sum()

print(run_bingo_win_last(problem_data("day4_sample.txt")))
print(run_bingo_win_last(problem_data("day4_problem.txt")))


def bingo_game(numbers):
    boards = yield
    for num in numbers:
        continues = []
        winners = []
        for board in boards:
            board.mark(num)

            if board.win():
                winners.append(board)
            else:
                continues.append(board)

        boards = yield (winners, continues)
        if len(boards) == 0:
            assert len(winners) == 1
            return num * winners[0].unmarked_sum()


def run_bingo2(data, win_comp):
    numbers, boards = read_bingo_data(data)

    game = bingo_game(numbers)
    next(game)
    try:
        while True:
            winners, continues = game.send(boards)
            boards = win_comp(winners, continues)
    except StopIteration as e:
        return e.value


def win_last_comp(winners, continues):
    if len(continues) == 0:
        return []
    else:
        return continues


def win_comp(winners, continues):
    if len(winners) == 1:
        return []
    else:
        return continues


print(run_bingo2(problem_data("day4_sample.txt"), win_comp))
print(run_bingo2(problem_data("day4_problem.txt"), win_comp))
print(run_bingo2(problem_data("day4_sample.txt"), win_last_comp))
print(run_bingo2(problem_data("day4_problem.txt"), win_last_comp))
