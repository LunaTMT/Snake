class Apple:

    def __init__(self, interface) -> None:
            self.interface  = interface
            self.board      = interface.board
            self.screen     = interface.screen
            self.k          = interface.k
            
            self.value = "Apple"

            self.generate()

    def generate(self):
        self.position = r, c = self.board.generate_random_position()
        self.board[r, c].value = self.value