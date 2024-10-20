import keyboard
import time
import numpy as np
import random
import curses
from tetris_objects import l_shape, j_shape, t_shape, \
        o_shape, i_shape, s_shape, z_shape


# Grid size
G_WIDTH = 10
G_HEIGHT = 20

# Initial time between frames
INIT_SPEED = .05

SHAPES_LIST = [
    l_shape, j_shape,
    t_shape, o_shape,
    i_shape, s_shape, z_shape
]



class Grid:

    """
    Class representing the Tetris game grid.

    Attributes:
        game_over (bool): Indicates whether the game is over.
        score (int): The current score of the game.
        points_granted (list): Points granted for 1/2/3/4 lines combinations.
        fall_speed_mult (int): Multiplier for object falling speed.
        frame_counter (int): Counter to manage frame-based timing for 
                             falling pieces.
        width (int): Width of the grid.
        height (int): Height of the grid.
        speed (float): Speed of the game (affects how fast pieces fall).
        grid_list (list): A 2D list representing the current state of the grid.
        current_shape (list): The current shape being manipulated by the player.
        next_shape (list): The next shape to appear.
        current_shape_location (tuple): Coordinates of the current shape
                                        (row, column).
    """


    def __init__(self, width = 10, height = 20, speed = .5):
        """
        Initialization of the gri object.

        Args:
            with (int): width of the grid.
            height (int): height of the grid.
            speed (float): initial speed of the falling shapes.
        """
        self.game_over = False
        self.score = 0
        self.points_granted = [40, 100, 300, 1200]
        self.fall_speed_mult = 1
        self.frame_counter = 0
        self.width = width
        self.height = height
        self.speed = speed
        self.grid_list = [
            [0 for _ in range(self.width)]
            for _ in range(self.height)
        ]
        self.current_shape = None
        self.next_shape = random.choice(SHAPES_LIST)
        self.current_shape_location = (0, 0)


    def update_cells(self, row, col, value = 1):
        """
        Updates the value of a specific cell in the grid.

        Args:
            row (int): Row index of the cell.
            col (int): Column index of the cell.
            value (int): The new value to set in the cell
                         (0 for empty, 1 for active shape, 2 for locked shape).
        """
        if self.width > col >= 0 and self.height > row >= 0:
            self.grid_list[row][col] = value


    def draw_shape(self, shape, row, col, value = 1):
        """
        Draws a shape at a given location on the grid.

        Args:
            shape (list): 2D list representing the shape.
            row (int): Row index to start drawing the shape.
            col (int): Column index to start drawing the shape.
            value (int): Value to assign to the grid cells 
                         (1 for active shape, 0 for clearing the shape).
        """
        shape_coords = [
            (i + row, j + col)
            for i, shape_row in enumerate(shape)
            for j, value in enumerate(shape_row)
            if value
        ]
        for coord in shape_coords:
            self.update_cells(
                coord[0], coord[1], 
                value = value
            )


    def can_move(self, shape, new_pos):
        """
        Checks if a shape can be moved to a given position without collisions.

        Args:
            shape (list): 2D list representing the shape.
            new_pos (tuple): The new row and column position (row, col).
        
        Returns:
            bool: True if the shape can move, False otherwise.
        """
        new_row, new_col = new_pos 
        shape_coords = [
            (i + new_row, j + new_col)
            for i, shape_row in enumerate(shape)
            for j, value in enumerate(shape_row)
            if value
        ]
        for row, col in shape_coords:
            if col < 0 or col >= self.width \
                    or row < 0 or row >= self.height:
                return False
            if  self.grid_list[row][col] == 2:
                return False
        return True
        
        
    def move_down(self):
        """
        Moves the current shape down the grid if possible
        """
        self.frame_counter += 1

        if not self.current_shape:
            return

        new_position = (
            self.current_shape_location[0] + self.fall_speed_mult,
            self.current_shape_location[1]
        )

        if self.frame_counter % 16 == 0:    # number of frames per down move

            if self.can_move(self.current_shape, new_position):
                self.draw_shape(
                    self.current_shape,
                    self.current_shape_location[0],
                    self.current_shape_location[1],
                    value = 0          # Erasing the previous position
                )
                self.current_shape_location = new_position
                self.draw_shape(
                    self.current_shape, 
                    self.current_shape_location[0],
                    self.current_shape_location[1],
                )
            else:
                new_position = (
                    self.current_shape_location[0] + 1, # Adding 1 row
                    self.current_shape_location[1]
                )
                if self.can_move(self.current_shape, new_position):
                    self.draw_shape(
                        self.current_shape,
                        self.current_shape_location[0],
                        self.current_shape_location[1],
                        value = 0          # Erasing the previous position
                    )
                    self.current_shape_location = new_position
                    self.draw_shape(
                        self.current_shape, 
                        self.current_shape_location[0],
                        self.current_shape_location[1],
                    )

                else:
                    self.lock_shape()


        else:
            
            self.draw_shape(
                self.current_shape,
                self.current_shape_location[0],
                self.current_shape_location[1]
            )

    def move_down_on_key(self):
        """
        Moves the object down when calling key.
        This adds to the natural movement, making the object move faster.
        """
        if not self.current_shape:
            return 
        new_position = (
            self.current_shape_location[0] + 1,
            self.current_shape_location[1]
        )
        if self.can_move(self.current_shape, new_position):
            self.draw_shape(
                self.current_shape,
                self.current_shape_location[0],
                self.current_shape_location[1],
                value = 0          # Erasing the previous position
            )
            self.current_shape_location = new_position
            self.draw_shape(
                self.current_shape, 
                self.current_shape_location[0],
                self.current_shape_location[1],
            )


    def move_side(self, side = 1):
        """
        Moves the current shape to the right (side=1) or to the left (side=-1).

        Args:
            side (int): Direction to move the shape.
                        Use 1 for right, -1 for left.
        """
        if not self.current_shape:
            return 
        new_position = (
            self.current_shape_location[0],
            self.current_shape_location[1] + side 
        )
        if self.can_move(self.current_shape, new_position):
            self.draw_shape(
                self.current_shape,
                self.current_shape_location[0],
                self.current_shape_location[1],
                value = 0          # Erasing the previous position
            )
            self.current_shape_location = new_position
            self.draw_shape(
                self.current_shape, 
                self.current_shape_location[0],
                self.current_shape_location[1],
            )


    def rotate(self):
        """
        Rotates the current shape by 90 degrees if enough space.
        """
        if not self.current_shape:
            return
        rotated_shape = np.rot90(self.current_shape)
        if self.can_move(rotated_shape, self.current_shape_location):
            self.draw_shape(
                self.current_shape,
                self.current_shape_location[0],
                self.current_shape_location[1],
                value = 0          # Erasing the previous position
            )
            self.current_shape = rotated_shape.tolist()
            self.draw_shape(
                self.current_shape, 
                self.current_shape_location[0],
                self.current_shape_location[1],
            )


    def new_shape(self, shape):
        """
        Introduces a new shape at the top of the grid.

        Args:
            shape (list): The new shape to introduce.
        """
        self.current_shape = shape
        self.current_shape_location = (
            0,
            self.width // 2 - len(shape[0]) // 2
        )
        if not self.can_move(self.current_shape, self.current_shape_location):
            self.game_over = True
            self.current_shape = None


    def row_is_complete(self):
        """
        Checks for completed rows and clears them, updating the score
        and increasing speed.
        """
        num_completed = 0
        for i, row in enumerate(self.grid_list):
            if sum(row) == self.width*2:
                num_completed += 1
                del self.grid_list[i]
                self.grid_list.insert(0, [0 for _ in range(self.width)])
        if num_completed != 0:
            self.score += self.points_granted[num_completed - 1] # Give points
            self.speed *= .95 # Increase speed


    def lock_shape(self):
        """
        If the shape cannot move, locks it in place and checks
        for full rows.
        """
        self.draw_shape(
            self.current_shape,
            self.current_shape_location[0],
            self.current_shape_location[1],
            value = 2,
        )
        self.row_is_complete()
        self.current_shape = None
        #new_shape = random.choice(SHAPES_LIST)
        new_shape = self.next_shape
        self.next_shape = random.choice(SHAPES_LIST)
        self.new_shape(new_shape)


    def print(self, stdscr):
        """
        Prints the grid, score and next shape for each iteration.

        Args:
            stdscr (curses.window): The window object provided by the curses
                                    library.
        """
        stdscr.clear()
        for y, row in enumerate(self.grid_list):
            for x, cell in enumerate(row):
                char = " . " if cell == 0 else " # "
                stdscr.addstr(y, x * 2, char)  # Doubling x for better spacing
        # Printing next shape
        for i, shape_row in enumerate(self.next_shape):
            for j, value in enumerate(shape_row):
                if value:
                    stdscr.addstr(
                        i + int(self.height*.7), 
                        self.width * 2 + 5 + j * 2, 
                        " # "
                    )
        #Printing score
        stdscr.addstr(
            self.height - 1, 
            self.width*2 + 2, 
            f"Your score: {self.score}"
        )
        stdscr.refresh()


    def print_game_over(self, stdscr):
        """
        Displays a game over screen.

        Args:
            stdscr (curses.window): The window object provided by the curses
                                    library.
        """
        stdscr.clear()
        game_over_msg = "GAME OVER"
        actions_msg = "Retry (r)    Quit (q)"
        #quit_msg = "Quit (q)"
        final_score_msg = f"Final score: {self.score}"
        stdscr.addstr(
            self.height // 2,
            self.width - len(game_over_msg) // 2,
            game_over_msg,
            curses.A_BOLD
        )
        stdscr.addstr(
            self.height // 2 + 2,
            self.width - len(final_score_msg) // 2,
            final_score_msg,
            curses.A_BOLD
        )
        stdscr.addstr(
            self.height // 2 + 7,
            self.width - len(actions_msg) // 2,
            actions_msg,
            curses.A_BOLD
        )

        stdscr.refresh()
        while True:
            if keyboard.is_pressed("q"):
                return "q"
            elif keyboard.is_pressed("r"):
                return "r"




def main(stdscr):
    """
    The main game loop controlling the flow of the game.

    Args:
        stdscr (curses.window): The window object provided by the curses
                                library.
    """
    grid = Grid(G_WIDTH, G_HEIGHT, INIT_SPEED)
    grid.new_shape(random.choice(SHAPES_LIST))

    last_k_time = 0
    last_h_time = 0
    last_l_time = 0
    freeze_time_rotation = .12   # minimum time between rotation actions
    freeze_time_side_mov = .05    # minimum time between side movement actions

    curses.curs_set(0)  # Hide cursor

    while not grid.game_over:

        grid.print(stdscr)

        current_time = time.time()

        if keyboard.is_pressed('h'):
            #grid.move_side(side = -1)
            if current_time - last_h_time > freeze_time_side_mov:
                grid.move_side(side = -1)
                last_h_time = current_time
        if keyboard.is_pressed('l'):
            #grid.move_side(side = 1)
            if current_time - last_l_time > freeze_time_side_mov:
                grid.move_side(side = 1)
                last_l_time = current_time
        if keyboard.is_pressed('k'):
            if current_time - last_k_time > freeze_time_rotation:
                grid.rotate()
                last_k_time = current_time
        #if keyboard.is_pressed('j'):
        #    grid.fall_speed_mult = 2
        #else:
        #    grid.fall_speed_mult = 1
        if keyboard.is_pressed('j'):
            grid.move_down_on_key()

        grid.move_down()
        time.sleep(grid.speed)


    choice = grid.print_game_over(stdscr)

    if choice == 'r':
        main(stdscr)
    elif choice == 'q':
        time.sleep(1)


# Execution of the main function inside terminal using the curses wrapper.
curses.wrapper(main)
