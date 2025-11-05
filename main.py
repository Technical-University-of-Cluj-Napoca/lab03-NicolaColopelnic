from utils import *
from grid import Grid
from searching_algorithms import *

import pygame

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, text_color=(255, 255, 255)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.font = pygame.font.SysFont("times new roman", 20)
        self.click_sound = pygame.mixer.Sound("button.wav")

    def draw(self, win):
        mouse_pos = pygame.mouse.get_pos()
        color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
        pygame.draw.rect(win, color, self.rect, border_radius=8)
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        win.blit(text_surf, text_rect)

    def is_clicked(self, event):
        if (
                event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
                and self.rect.collidepoint(event.pos)
        ):
            pygame.mixer.Sound.play(self.click_sound)
            return True
        return False


if __name__ == "__main__":
    pygame.init()

    SIDEBAR_WIDTH = 200
    GRID_WIDTH = WIDTH
    GRID_HEIGHT = HEIGHT
    WIN_WIDTH = GRID_WIDTH + SIDEBAR_WIDTH
    WIN_HEIGHT = GRID_HEIGHT

    WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption("Searching Algorithms Visualization!")

    DARK_GRAY = (50, 50, 50)
    BLUE = (70, 130, 180)
    LIGHT_BLUE = (150, 190, 255)
    GREEN = (46, 204, 113)
    LIGHT_GREEN = (88, 214, 141)
    WHITE = (255, 255, 255)
    PASTEL_PINK = (255, 192, 192)
    BACKGROUND = (100, 30, 30)

    ROWS = 50
    COLS = 50
    grid = Grid(WIN, ROWS, COLS, GRID_WIDTH, GRID_HEIGHT, offset_x=SIDEBAR_WIDTH)

    buttons = [
        Button(20, 20, 160, 35, "1. BFS", LIGHT_BLUE, WHITE),
        Button(20, 65, 160, 35, "2. DFS", LIGHT_BLUE, WHITE),
        Button(20, 110, 160, 35, "3. DLS", LIGHT_BLUE, WHITE),
        Button(20, 155, 160, 35, "4. UCS", LIGHT_BLUE, WHITE),
        Button(20, 200, 160, 35, "5. Greedy", LIGHT_BLUE, WHITE),
        Button(20, 245, 160, 35, "6. A*", LIGHT_BLUE, WHITE),
        Button(20, 290, 160, 35, "7. IDDFS", LIGHT_BLUE, WHITE),
        Button(20, 335, 160, 35, "8. IDA*", LIGHT_BLUE, WHITE),

    ]
    start_button = Button(20, 650, 160, 40, "Start", LIGHT_BLUE, WHITE)
    reset_button = Button(20, 700, 160, 40, "Reset", LIGHT_BLUE, WHITE)

    selected_algorithm = None
    start = None
    end = None
    run = True
    started = False

    while run:
        WIN.fill(BACKGROUND)

        pygame.draw.rect(WIN, PASTEL_PINK, (0, 0, SIDEBAR_WIDTH, WIN_HEIGHT))
        for b in buttons:
            b.draw(WIN)
        start_button.draw(WIN)
        reset_button.draw(WIN)

        if selected_algorithm is not None:
            pygame.draw.rect(WIN, (70, 130, 180), buttons[selected_algorithm].rect, 3, border_radius=8)

        grid.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if started:
                continue

            if reset_button.is_clicked(event):
                start = None
                end = None
                grid.reset()

            for i, b in enumerate(buttons):
                if b.is_clicked(event):
                    selected_algorithm = i

            if start_button.is_clicked(event) and not started and start and end and selected_algorithm is not None:
                for row in grid.grid:
                    for spot in row:
                        spot.update_neighbors(grid.grid)
                started = True

                if selected_algorithm == 0:
                    bfs(lambda: grid.draw(), grid, start, end)
                elif selected_algorithm == 1:
                    dfs(lambda: grid.draw(), grid, start, end)
                elif selected_algorithm == 2:
                    dls(lambda: grid.draw(), grid, start, end, limit=15)
                elif selected_algorithm == 3:
                    ucs(lambda: grid.draw(), grid, start, end)
                elif selected_algorithm == 4:
                    greedy_best_first(lambda: grid.draw(), grid, start, end)
                elif selected_algorithm == 5:
                    astar(lambda: grid.draw(), grid, start, end)
                elif selected_algorithm == 6:
                    iddfs(lambda: grid.draw(), grid, start, end, max_depth=20)
                elif selected_algorithm == 7:
                    ida(lambda: grid.draw(), grid, start, end)

                started = False

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                if pos[0] > SIDEBAR_WIDTH:
                    clicked = grid.get_clicked_pos(pos)
                    if clicked:
                        row, col = clicked
                        spot = grid.grid[row][col]
                        if not start and spot != end:
                            start = spot
                            start.make_start()
                        elif not end and spot != start:
                            end = spot
                            end.make_end()
                        elif spot != end and spot != start:
                            spot.make_barrier()

            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                if pos[0] > SIDEBAR_WIDTH:
                    clicked = grid.get_clicked_pos(pos)
                    if clicked:
                        row, col = clicked
                        spot = grid.grid[row][col]
                        spot.reset()
                        if spot == start:
                            start = None
                        elif spot == end:
                            end = None

            if event.type == pygame.KEYDOWN and event.key == pygame.K_c:
                start = None
                end = None
                grid.reset()

        pygame.display.update()

    pygame.quit()
