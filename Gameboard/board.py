from .tile import Tile
import random
class Board:
    
    def __init__(self, interface) -> None:
        self.interface  = interface
        self.screen     = interface.screen
        self.cell_size  = interface.screen.cell_size 
        self.k          = interface.k

        self.board = [[0 for _ in range(self.k)] for _ in range(self.k)]
        self.generate_tiles()

    def __getitem__(self, index):
        row, col = index
        return self.board[row][col]

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

    def draw(self):
        for r in self.board:
            for tile in r:
                tile.draw()

    
    def generate_random_position(self, x_limit = 0, y_limit = 1):
            
            def get_random():
                return random.randint(int(self.k * x_limit), int(self.k * y_limit) - 1)
            
            r = get_random()
            c = get_random()
            
            while self[r, c].value != "0": #To ensure that the spawning position of an apple and snake dont overlap
                r = get_random()
                c = get_random()

            return (r, c)


    def print_board(self):
        for r in self:
            for tile in r:
                print(tile, end="")
            print()