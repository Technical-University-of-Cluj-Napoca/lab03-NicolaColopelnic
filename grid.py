from utils import *
from spot import Spot
import pygame

class Grid:
    def __init__(self, win, rows, cols, width, height, offset_x=0):
        self.win = win
        self.rows = rows
        self.cols = cols
        self.width = width
        self.height = height
        self.offset_x = offset_x
        self.grid = self._make_grid()

    def _make_grid(self) -> list[list[Spot]]:
        """
        Create a grid of Spot objects.
        Returns:
            list[list[Spot]]: A 2D list (matrix) representing the grid of Spot objects.
        """
        grid = []
        spot_width = self.width // self.cols
        spot_height = self.height // self.rows
        for i in range(self.rows):
            grid.append([])
            for j in range(self.cols):
                spot = Spot(i, j, spot_width, spot_height, self.rows)
                grid[i].append(spot)
        return grid

    def draw_grid_lines(self) -> None:
        """
        Draw the grid lines on the Pygame window.
        Returns:
            None
        """
        spot_width = self.width // self.cols
        spot_height = self.height // self.rows

        for i in range(self.rows):
            pygame.draw.line(
                self.win,
                COLORS['GREY'],
                (self.offset_x, i * spot_height),
                (self.offset_x + self.width, i * spot_height)
            )

        for j in range(self.cols):
            pygame.draw.line(
                self.win,
                COLORS['GREY'],
                (self.offset_x + j * spot_width, 0),
                (self.offset_x + j * spot_width, self.height)
            )

    def draw(self):
        """
        Draw the grid spots and the grid lines.
        """
        for row in self.grid:
            for spot in row:
                spot.draw(self.win, self.offset_x)
        self.draw_grid_lines()
        pygame.display.update()

    def get_clicked_pos(self, pos: tuple[int, int]) -> tuple[int, int] | None:
        """
        Get the (row, col) of the grid based on mouse click position.
        Returns None if click is outside the grid.
        """
        x, y = pos
        x -= self.offset_x

        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return None

        spot_width = self.width // self.cols
        spot_height = self.height // self.rows

        col = y // spot_width
        row = x // spot_height
        return row, col

    def reset(self) -> None:
        """
        Reset the grid to its initial state.
        """
        for row in self.grid:
            for spot in row:
                spot.reset()
