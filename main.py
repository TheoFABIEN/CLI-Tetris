import keyboard
import os
import time
import numpy as np
import random
from tetris_objects import l_shape, j_shape, t_shape, \
        o_shape, i_shape, s_shape, z_shape


# Grid size
G_WIDTH = 10
G_HEIGHT = 20

# Initial speed
INIT_SPEED = .5

SHAPES_LIST = [
    l_shape, j_shape,
    t_shape, o_shape,
    i_shape, s_shape, z_shape
]


class Grid:

    def __init__(self, width = 10, height = 20, speed = .5):

        self.game_over = False
        self.width = width
        self.height = height
        self.speed = speed
        self.grid_list = [
            [0 for _ in range(self.width)]
            for _ in range(self.height)
        ]
        self.current_shape = None
        self.current_shape_location = (0, 0) # row, column


    def update_cells(self, row, col, value = 1):
        """
        Updates cells value in self.grid_list
        """
        if self.width > col >= 0 and self.height > row >= 0:
            self.grid_list[row][col] = value


    def draw_shape(self, shape, row, col, value = 1):
        """
        Draws a shape at a given location on the grid
        """
        shape_coords = [
            (i + row, j + col)
            for i, shape_row in enumerate(shape)
            for j, value in enumerate(shape_row)
            if value
        ]
        for coord in shape_coords:
            self.update_cells(coord[0], coord[1], value = value)

    
    def can_move(self, shape, new_pos):
        """
        Checks if a shape can be moved to a given position.
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
        if not self.current_shape:
            return
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


    def move_side(self, side = 1):
        """
        Moves the current shape to the right (side=1) or to the left (side=-1)
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
        Rotates the current shape
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
        self.current_shape = shape
        self.current_shape_location = (
            0,
            self.width // 2 - len(shape[0]) // 2
        )
        if not self.can_move(self.current_shape, self.current_shape_location):
            print("\nGame Over")
            self.game_over = True
            self.current_shape = None


    def row_is_complete(self):
        """
        Checks for completed rows after locking the current object
        """
        for i, row in enumerate(self.grid_list):
            if sum(row) == self.width*2:
                del self.grid_list[i]
                self.grid_list.insert(0, [0 for _ in range(self.width)])


    def lock_shape(self):
        """
        If the shape cannot move, it is locked in the grid
        """
        self.draw_shape(
            self.current_shape,
            self.current_shape_location[0],
            self.current_shape_location[1],
            value = 2
        )
        self.row_is_complete()
        self.current_shape = None
        new_shape = random.choice(SHAPES_LIST)
        self.new_shape(new_shape)
        self.speed *= .95


    def print(self):
        """
        Print the grid for each iteration
        """
        os.system('cls' if os.name == "nt" else "clear")
        print("+" + "-"*self.width + "+")
        for row in self.grid_list:
            print("|" + ''.join(["." if x == 0 else "#" for x in row]) + "|")
        print("+" + "-"*self.width + "+", end='\r')





def main():
    grid = Grid(G_WIDTH, G_HEIGHT, INIT_SPEED)
    grid.new_shape(random.choice(SHAPES_LIST))

    while True:

        if grid.game_over:
            break
        if keyboard.is_pressed('h'):
            grid.move_side(side = -1)
        if keyboard.is_pressed('l'):
            grid.move_side(side = 1)
        if keyboard.is_pressed('k'):
            grid.rotate()
        #if keyboard.read_key() == 'j'
        #if keyboard.read_key() == 'k'

        grid.print()
        grid.move_down()
        time.sleep(grid.speed)


if __name__ == "__main__":
    main()
