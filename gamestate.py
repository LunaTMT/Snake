class GameState:

    dead = False
    play_game = True
    end_game = False

    @classmethod
    def reset_states(self):
        GameState.dead = False
        GameState.play_game = True
        GameState.end_game = False