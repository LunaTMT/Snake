from rectangle import Rectangle

class Scoreboard:
    def __init__(self, interface) -> None:
        self.interface = interface
        self.board     = interface.board
        self.screen    = interface.screen
        self.snake     = interface.snake
        self.k         = interface.k

        self.scoreboard_font = interface.scoreboard_font

    def draw(self):
        """
        In this funciton we draw the score, I.e. the length of the snake in the top right tiles of the board
        The numbers are drawn in reverse order.
        
        E.g.
        score = 354 (length)
        we draw:
        1. 4 (k)
        2. 5 (k-1)
        3. 3 (k-2)
        """
        score = str(self.snake.length)
        n = len(score)
        for i in range(n): 
            tile = self.board[0, self.k - 1 - i] #First row 
            number_txt = score[::-1][i]
            Rectangle.draw_text_in_center(self.screen.surface, self.scoreboard_font, number_txt, tile.rect)
