"""

Quick reimplementation of UTTT_cpp for speed comparison without comments
For original repo, see:
    https://github.com/internetvandingen/UTTT_cpp.git

"""

import random
import time

random.seed(0)

class Board:
    ind_field = ((0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6))
    ind_coords = tuple(tuple((field//3*3+square//3, field%3*3+square%3) for square in range(9)) for field in range(9))
    whos_turn = 1
    
    def __init__(self):
        self.board = [[0 for col in range(9)] for row in range(9)]
        self.legal = [[1 for col in range(9)] for row in range(9)]
        
    def get_winner(self):
        field_winners = tuple(self.get_winner_field(i) for i in range(9))
        return self.get_winner_arr(field_winners)
    
    def get_winner_field(self, fieldnr):
        field = tuple(self.board[self.ind_coords[fieldnr][i][0]][self.ind_coords[fieldnr][i][1]] for i in range(9))
        return self.get_winner_arr(field)
    
    def get_winner_arr(self, arr):
        for line in self.ind_field:
            if (arr[line[0]] != 0 and 
                arr[line[0]] == arr[line[1]] and 
                arr[line[1]] == arr[line[2]]):
                return arr[line[0]]
        return 0
    
    def is_field_full(self, fieldnr):
        total = 0
        for i in range(9):
            total += self.board[self.ind_coords[fieldnr][i][0]][self.ind_coords[fieldnr][i][1]] != 0
        return 1 if total==9 else 0
    
    def print_board(self, game_nr = None):
        if game_nr is None:
            game_nr = " "
        board_symbols = ('o', ' ', 'x', 'd')
        "-"*31
        string = "{0:2d}: 0  1  2   3  4  5   6  7  8".format(game_nr)
        for row in range(9):
            if row%3 == 0:
                string += "\n  "+"-"*31
            string += "\n"+str(row)+" |"
            for col in range(9):
                string += " "+board_symbols[self.board[row][col]+1]+" "
                if col%3==2:
                    string += "|"
        print(string+"\n  "+"-"*31+"\n")
    
    def get_board(self):
        return self.board
    def get_legal(self):
        return self.legal
    def get_turn(self):
        return self.whos_turn
    def parse_move(self, row, col):
        assert (self.legal[row][col] == 1), "Illegal move "+str(row)+","+str(col)
#        if self.legal[row][col] == 0:
#            print('illegal move, stop game')
#            return 0
        self.board[row][col] = self.whos_turn
        self.last_move = (row, col)
        
        move_field_nr = row//3*3+col//3
        temp_winner = self.get_winner_field(move_field_nr)
        if temp_winner != 0:
            for r in range(3):
                for c in range(3):
                    self.board[row//3*3+r][col//3*3+c] = temp_winner
            winner = self.get_winner()
            if winner:
                return winner
        
        fieldnr = row%3*3+col%3
        total_available_moves = 0
        replacement = 0 if self.is_field_full(fieldnr) else 1
        for r in range(9):
            for c in range(9):
                if self.board[r][c] == 0:
                    if r//3 == fieldnr//3 and c//3 == fieldnr%3:
                        self.legal[r][c] = replacement
                        total_available_moves += replacement
                    else:
                        self.legal[r][c] = 1-replacement
                        total_available_moves += 1-replacement
                else:
                    self.legal[r][c] = 0
        
        if total_available_moves == 0:
            return 0
        
        self.whos_turn *= -1
        
        return 9

class Player:
    def decide_move(self, board, legal):
        return self.random_legal_move(board, legal)
    def random_legal_move(self, board, legal):
        counter = 0
        row = random.randint(0,8)
        col = random.randint(0,8)
        while(legal[row][col] == 0 and counter <1000):
            row = random.randint(0,8)
            col = random.randint(0,8)
            counter += 1
        if (legal[row][col] != 1):
            print("No legal moves found in 1000 tries!")
        
        return (row, col)

class Engine:
    def __init__(self, pone, ptwo):
        self.players = [ptwo, pone]

    def game(self, verbose=False):
        self.board = Board()
        self.status = 9
        for i in range(81):
            player_turn = (self.board.whos_turn+1)//2
            zet = self.players[player_turn].decide_move(self.board.board, self.board.legal)
            self.status = self.board.parse_move(zet[0], zet[1])
            
            if verbose:
                self.board.print_board(i)
            
            if self.status != 9:
                if verbose:
                    print("Game status code: "+str(self.status))
                break
        
        return self.status
    
    def get_result(self):
        return self.status
    
if __name__ == "__main__":
    pone = Player()
    ptwo = Player()

    start_time = time.time()
    for i in range(10000):
        e = Engine(pone, ptwo)
        e.game(False)
    print("--- %s seconds ---" % (time.time() - start_time))
    
    