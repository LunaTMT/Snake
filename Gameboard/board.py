from .tile import Tile

class Board:
    
    def __init__(self, interface, k=5) -> None:
        self.interface = interface
        self.grid_size = k

        self.cell_size = interface.screen.width // self.grid_size
        
        # Calculate the width and height of the grid
        self.grid_width = self.grid_size * self.cell_size
        self.grid_height = self.grid_size * self.cell_size

        self.board = [[0 for _ in range(k)] for _ in range(k)]
        self.generate_tiles()

        self.print_board()
        
    def print_board(self):
        for r in self.board:
            for tile in r:
                print(tile, end="")
            print()

    def generate_tiles(self):
        """
        This function initialises the board with all the tile objects in their respective location
        """ 
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                x =  c * self.cell_size
                y =  r * self.cell_size
                tile = Tile(self.interface, x, y, self.cell_size)      
                self.interface.all_sprites.add(tile)   
                self.board[r][c] = tile 
