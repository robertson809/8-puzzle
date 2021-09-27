import random
import copy
from heapq import heappush, heappop


"""Helper function outside of the class definition that takes a board and prints it out.
Outside of the class definition"""
def pretty_print_2(size, board):
    for row in range(0, size):
        for col in range(0, size):
            print(board[row][col]),
        print " "
    print ""


"""Creates a tuple out of a board represented as a list of lists.
This is helpful as a tuple is hashable.
Outside of the class definition"""
def linearize(board):
    a = tuple(board[0])
    for row in range(1, len(board)):
        a = a + tuple(board[row])
    return a


class Puzzle:
    def __init__(self, size, num_moves):
        #create instances variables
        self.size = size  #size of the board
        self.squares = []  #board state
        self.my_goal = []  #solved state
        self.g = 0  #length of path
        #Create the starting state and the goal state
        count = 1
        for i in range(0, size):
            my_row = []
            my_row_s = []
            for j in range(0, size):
                if (i == size - 1 and j == size - 1):
                    my_row.append(-1)
                    my_row_s.append(-1)
                else:
                    my_row.append(count)
                    my_row_s.append(count)
                count += 1
            self.my_goal.append(my_row)
            self.squares.append(my_row)
        # Randomly mvoe the blank num_moves times to create a pseudo-random
        # starting state.  Checks to make sure that the puzzle doesn't back-track
        past_states = []
        move = self.down()
        past_states.append(self.squares)
        for i in range(0, num_moves):
            cur = random.randint(0, 4)
            if cur == 0:
                move = self.down()
            if cur == 1:
                move = self.up()
            if cur == 2:
                move = self.right()
            if cur == 3:
                move = self.left()
            if not move[0]:
                i -= 1
                continue
            self.squares = move[1].squares
            if self.squares in past_states:
                i -= 1
                if cur == 0:
                    self.squares = self.up()[1].squares
                if cur == 1:
                    self.squares = self.down()[1].squares
                if cur == 2:
                    self.squares = self.left()[1].squares
                if cur == 3:
                    self.squares = self.right()[1].squares
            past_states.append(self.squares)

    # movement methods return a touple of the boolean sucess of the move
    # and a new puzzle *object*, if the move is impossible
    # Up is defined as moving the blank up one square, down is the reverse, etc.
    # Definitions don't matter too much so long as they are consistent.
    def down(self):
        for row in range(0, self.size - 1):
            for col in range(0, self.size):
                if self.squares[row][col] == -1:
                    ans = copy.deepcopy(self)
                    ans.squares[row][col] = ans.squares[row + 1][col]
                    ans.squares[row + 1][col] = -1
                    return (True, ans)
        return (False, self)

    def up(self):
        for row in range(1, self.size):
            for col in range(0, self.size):
                if self.squares[row][col] == -1:
                    ans = copy.deepcopy(self)
                    ans.squares[row][col] = ans.squares[row - 1][col]
                    ans.squares[row - 1][col] = -1
                    return (True, ans)
        return (False, self)

    def left(self):
        for row in range(0, self.size):
            for col in range(1, self.size):
                if self.squares[row][col] == -1:
                    ans = copy.deepcopy(self)
                    ans.squares[row][col] = ans.squares[row][col - 1]
                    ans.squares[row][col - 1] = -1
                    return (True, ans)
        return (False, self)

    def right(self):
        for row in range(0, self.size):
            for col in range(0, self.size - 1):
                if self.squares[row][col] == -1:
                    ans = copy.deepcopy(self)
                    ans.squares[row][col] = ans.squares[row][col + 1]
                    ans.squares[row][col + 1] = -1
                    return (True, ans)
        return (False, self)

    # helper function that prints the state of the board.
    def pretty_print(self):
        for row in range(0, self.size):
            for col in range(0, self.size):
                print(self.squares[row][col]),
            print (" ")
        print ("")

    # returns a list of legal square states, full puzzle object is passed
    def get_moves(self):
        # returns a list of possible moves, in the form of puzzle objects

        legal_moves = []
        move = self.right()

        # tests the boolean return
        if move[0]:
            # adds the changed board
            legal_moves.append(move[1])
        move = self.left()
        if move[0]:
            legal_moves.append(move[1])
        move = self.up()
        if move[0]:
            legal_moves.append(move[1])
        move = self.down()
        if move[0]:
            legal_moves.append(move[1])

        return legal_moves

    # A heuristic for determining how far the board state is from the goal state.
    # It returns the number of misplaced tiles, not counting the blank square.
    def h1(self):
        count = 0
        cur = -1
        for row in range(0, self.size):
            for col in range(0, self.size):
                cur = self.squares[row][col]
                if (cur != -1 and cur != row * self.size + col + 1):
                    count += 1
        return count

    # A heuristic for determining how far the board state is from the goal state.
    # Returns the sum of the manhattan distances, defined as far how a square is
    # from its goal state.
    def h2(self):
        count = 0
        proper_row = 0
        proper_col = 0
        cur = -1
        for row in range(0, self.size):
            for col in range(0, self.size):
                cur = self.squares[row][col]
                if cur != -1:
                    proper_row = (cur - 1) / self.size
                    proper_col = (cur - 1) % self.size
                    count += abs(proper_row - row)
                    count += abs(proper_col - col)
        return count

    # A heuristic for determining how far the board state is from the
    # Goal state.  Returns the number of swaps between the blank square and any
    # square needed to get to the goal state - a "relaxed" version of the 8-puzzle
    def h3(self):
        board = copy.deepcopy(self.squares)
        count = 0
        row_b = 0
        col_b = 0
        # print 'here'
        while (True):
            if board == self.my_goal:
                # print self.squares
                # print count
                return count
            for row in range(self.size):
                for col in range(self.size):
                    if board[row][col] == -1:
                        row_b = row
                        col_b = col
            has_swapped = False
            if row_b == self.size - 1 and col_b == self.size - 1:
                for row in range(self.size):
                    for col in range(self.size):
                        if board[row][col] != self.size * row + col + 1:
                            if not has_swapped:
                                board[row_b][col_b] = board[row][col]
                                board[row][col] = -1
                                has_swapped = True
            else:
                to_find = row_b * self.size + col + 1
                for row in range(self.size):
                    for col in range(self.size):
                        if board[row][col] == self.size * row_b + col_b + 1:
                            if not has_swapped:
                                board[row_b][col_b] = board[row][col]
                                board[row][col] = -1
                                has_swapped = True
            count += 1
        return count

    # A* algorithm, takes a starting point and integer 1,2, or 3
    # that defines the heuristic to use
    def search(self, num_h):
        # use to ensure we don't enter an infinte loop
        # set
        past_states = {linearize(self.squares)}
        # priorityQueue, made g an instance varaible of the board
        heap = []  #f(n), puzzle object

        # inialize
        h = 0
        if num_h == 1:
            h = self.h1()
        if num_h == 2:
            h = self.h2()
        if num_h == 3:
            h = self.h3()

        init_heap_tuple = (h, self)
        heappush(heap, init_heap_tuple)
        # while there's stuff in the heap
        count = 1
        while heap:

            best_move = heappop(heap)
            if best_move[1].squares == self.my_goal:
                return (True, best_move[1].g, count)
            else:
                sucessors = best_move[1].get_moves()
                for s in sucessors:
                    if linearize(s.squares) not in past_states:
                        count += 1
                        past_states.add(linearize(s.squares))

                        s.g = best_move[1].g + 1

                        if num_h == 1:
                            heappush(heap, (s.g + s.h1(), s))
                        if num_h == 2:
                            heappush(heap, (s.g + s.h2(), s))
                        if num_h == 3:
                            heappush(heap, (s.g + s.h3(), s))
            if not heap:
                best_move[1].pretty_print()
        #if heap empties, then we have failed

        return (False, [[]], -1)


# testing
# constants
target_depth = 18
num_moves_init = 26
num_heuristic = 1
size_puzzle = 3
puzzles_to_solve = 100
# initialize the dictionary of results
results = {}
results[target_depth] = (0, 0)

while (True):
    puzzle = Puzzle(size_puzzle, num_moves_init)
    result = puzzle.search(num_heuristic)
    depth = result[1]
    if depth != target_depth:
        continue
    node = result[2]
    times_solved = results[depth][0]
    print (times_solved)
    if times_solved < puzzles_to_solve:
        total_node_count = results[depth][1]
        entry = {depth: (times_solved + 1, total_node_count + node)}
        results.update(entry)
        continue
    break
print results
