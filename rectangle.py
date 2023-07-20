import assets.colours as colours


class Rectangle():

    @classmethod
    def get_size(cls, rect) -> tuple[int]:
        """
        Gets the height and width of a rect object and returns it
        """
        rect = rect.get_rect()
        return  rect.width, rect.height
    
    @classmethod
    def draw_text_in_center(cls, screen, font, text, rect):
            # Calculate the center coordinates of the rectangle
            center_x = rect.x + rect.width // 2
            center_y = rect.y + rect.height // 2 + 2

            # Render the number using the font
            text = font.render(text, True, colours.BLACK)

            # Get the size of the rendered text
            text_width, text_height = text.get_size()

            # Calculate the position to center the number in the rectangle
            number_x = center_x - text_width // 2
            number_y = center_y - text_height // 2

            # Draw the number at the center position
            screen.blit(text, (number_x, number_y))