from .tile import Tile
import random
import os
class Board:
    
    def __init__(self, interface) -> None:
        self.interface  = interface
        self.screen     = interface.screen
        self.cell_size  = interface.screen.cell_size 
        self.k          = interface.k


        #self.clear = lambda: os.system('clear')
        self.board = [['_' for _ in range(self.k)] for _ in range(self.k)]
        self.generate_tiles()

        self.clear = lambda: os.system('clear')

    def __getitem__(self, index):
        row, col = index
        try:
            return self.board[row][col]
        except:
            return IndexError

    def __setitem__(self, index, value):
        row, col = index
        self.board[row][col] = value
        
    
    def check_out_of_bounds(self, position):
        r, c = position
        if not (0 <= r < self.k) or not (0 <= c < self.k):
            return True
        return False

    def generate_tiles(self):
        for r in range(self.k):
            for c in range(self.k):
                x =  c * self.cell_size
                y =  r * self.cell_size
                tile = Tile(self.interface, x, y, self.cell_size)      
                self[r, c] = tile 

    def clear(self):
        for r in self.board:
            for tile in r:
                tile.value = "_"

    def print_board(self):
        self.clear()
        for r in self.board:
            for tile in r:
                print(tile, end="")
            print()

    def draw(self):
        for r in self.board:
            for tile in r:
                tile.draw()

    
    def generate_random_position(self, x_limit = 0, y_limit = 1):
            
            def get_random():
                return random.randint(int(self.k * x_limit), int(self.k * y_limit) - 1)
            
            r = get_random()
            c = get_random()
            
            while self[r, c].value != "_": #To ensure that the spawning position of an apple and snake dont overlap
                r = get_random()
                c = get_random()

            return (r, c)

