# Alexander Bake
import sys

# A board is defined by the number of nodes, n, and a list of winning paths
class Board:
    def __init__(self, n, winning_paths):
        self.free, self.player_x, self.player_o = '-', 'x', 'o'
        self.node_key = {0 : self.free, 1 : self.player_x, 2: self.player_o}
        self.player_map = {1 : 'Player X', 2: 'Player O', None : None}
        self.n = n
        self.winning_paths = winning_paths
        self.spaces = [0] * n
        self.moves = range(1, n+1)

    def show(self):
        print '\n* * * * * * *\n* The Board *\n* * * * * * *\n'
        if self.n != 9:
            for i, key in enumerate(self.spaces):
                print i+1, self.node_key[key]
        else:
            # Added for funsies. 
            # (Just shows the board in an intuitive way for 3x3 games)
            for line in [self.spaces[0:3], self.spaces[3:6], self.spaces[6:9]]:
                print ' '.join([self.node_key[key] for key in line])

    def winner(self):
        for path in self.winning_paths:
            current_state = [self.spaces[i-1] for i in path]
            if current_state.count(current_state[0]) == len(current_state) and 0 not in current_state:
                return current_state[0], path
        return None, None

    def allowed_moves(self):
        return [node for i, node in enumerate(self.moves) if self.spaces[i] == 0]

    def game_over(self):
        return self.winner()[0] or not self.allowed_moves()

    def make_move(self, move, player):
        self.spaces[move-1] = player

    def undo_move(self, move):
        self.spaces[move-1] = 0

# Player function
def human(board, player):
    board.show()
    allowed_moves = board.allowed_moves()
    print 'Allowed moves', allowed_moves
    move = int(raw_input('Make a move: '))
    while move not in allowed_moves:
        print "Oops! Someone already placed a token at '%s'!" % move
        move = int(raw_input('Choose another move: '))
    board.make_move(move, player)

# A.I. Function
def ai(board, player):
    other_player = {1 : 2, 2: 1}
    def score(winner):
        if winner == player:
            return 1
        if winner == None:
            return 0
        return -1
    def minimax_ab(move, p=player):
        try:
            board.make_move(move, p)
            if board.game_over():
                return score(board.winner()[0])
            # Fancy python generator! (Reduces runtime...)
            outcomes = (minimax_ab(next_move, other_player[p]) for next_move in board.allowed_moves())
            if p == player:
                # Alpha pruning
                _min = 1
                for option in outcomes:
                    if option == -1:
                        return option
                    _min = min(option, _min)
                return _min
            else:
                # Beta pruning
                _max = -1
                for option in outcomes:
                    if option == 1:
                        return option
                    _max = max(option, _max)
                return _max
        finally:
            board.undo_move(move)
    board.show()
    allowed_moves = board.allowed_moves()
    for move in allowed_moves:
        board.make_move(move, player)
        if board.game_over():
            print 'Computer made move:', move
            return None
        else:
            board.undo_move(move)
    moves = [(move, minimax_ab(move)) for move in allowed_moves]
    move = max(moves, key=lambda x: x[1])[0]
    print 'Computer made move:', move
    board.make_move(move, player)

def main():
    if len(sys.argv) < 2:
        print 'Usage: python ttt.py [game file]'
    
    try:
        game_file = sys.argv[1]
    except IndexError:    
        game_file = 'nine.txt'
    
    (n, winning_paths) = parse_file(game_file)
    game = Board(n, winning_paths)
    
    print 'Welcome to Generalized Tic-Tac-Toe!'
    print 'You are %s' % game.player_map[1]
    play_game(game)

def play_game(board):
    while 1:
        print "It is %s's turn..." % board.player_map[1]
        human(board, 1)
        print '-' * 50
        if board.game_over():
            break
        print "It is %s's turn..." % board.player_map[2]
        ai(board, 2)
        print '-' * 50
        if board.game_over():
            break
    board.show()
    winner = board.winner()
    if winner[0]:
        print '%s has won the game! Hip, hip, Hooray!!' % board.player_map[winner[0]]
        print 'Using the path:', winner[1]
        sys.exit()
    else:
        print "Game Over. It's a Cat's game!"
        sys.exit()

def parse_file(file_path):
    f = open(file_path, 'rU')
    num_nodes = 0
    winning_paths = []
    for i, line in enumerate(f):
        if i == 0:
            num_nodes = int(line)
        else:
            winning_paths.append([int(i) for i in line.split(' ')])
    return num_nodes, winning_paths

if __name__ == '__main__':
    main()