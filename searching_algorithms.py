from utils import *
from collections import deque
from queue import PriorityQueue
from grid import Grid
from spot import Spot
from typing import Callable, Optional, Tuple

pygame.mixer.init()
path_found_sound = pygame.mixer.Sound("path_found.wav")

def bfs(draw: callable, grid: Grid, start: Spot, end: Spot) -> bool:
    """
    Breadth-First Search (BFS) Algorithm.
    Args:
        draw (callable): A function to call to update the Pygame window.
        grid (Grid): The Grid object containing the spots.
        start (Spot): The starting spot.
        end (Spot): The ending spot.
    Returns:
        bool: True if a path is found, False otherwise.
    """
    if start == None or end == None:
        return False
    queue = deque()
    queue.append(start)
    visited = {start}
    came_from = {}

    while queue:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

        current = queue.popleft()
        if current == end:
            while current in came_from:
                current = came_from[current]
                current.make_path()
                draw()
            end.make_end()
            start.make_start()
            pygame.mixer.Sound.play(path_found_sound)
            return True

        for neighbor in current.neighbors:
            if neighbor not in visited and not neighbor.is_barrier():
                visited.add(neighbor)
                came_from[neighbor] = current
                queue.append(neighbor)
                neighbor.make_open()

        draw()
        if current != start:
            current.make_closed()

    return False

def dfs(draw: callable, grid: Grid, start: Spot, end: Spot) -> bool:
    """
    Depdth-First Search (DFS) Algorithm.
    Args:
        draw (callable): A function to call to update the Pygame window.
        grid (Grid): The Grid object containing the spots.
        start (Spot): The starting spot.
        end (Spot): The ending spot.
    Returns:
        bool: True if a path is found, False otherwise.
    """
    if start == None or end == None:
        return False

    stack = [start]
    visited = {start}
    came_from = {}

    while stack:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = stack.pop()

        if current == end:
            while current in came_from:
                current = came_from[current]
                current.make_path()
                draw()
            end.make_end()
            start.make_start()
            pygame.mixer.Sound.play(path_found_sound)
            return True

        for neighbor in current.neighbors:
            if neighbor not in visited and not neighbor.is_barrier():
                visited.add(neighbor)
                came_from[neighbor] = current
                stack.append(neighbor)
                neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False

def h_manhattan_distance(p1: tuple[int, int], p2: tuple[int, int]) -> float:
    """
    Heuristic function for A* algorithm: uses the Manhattan distance between two points.
    Args:
        p1 (tuple[int, int]): The first point (x1, y1).
        p2 (tuple[int, int]): The second point (x2, y2).
    Returns:
        float: The Manhattan distance between p1 and p2.
    """
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def h_euclidian_distance(p1: tuple[int, int], p2: tuple[int, int]) -> float:
    """
    Heuristic function for A* algorithm: uses the Euclidian distance between two points.
    Args:
        p1 (tuple[int, int]): The first point (x1, y1).
        p2 (tuple[int, int]): The second point (x2, y2).
    Returns:
        float: The Manhattan distance between p1 and p2.
    """
    x1, y1 = p1
    x2, y2 = p2
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5


def astar(draw: callable, grid: Grid, start: Spot, end: Spot) -> bool:
    """
    A* Pathfinding Algorithm.
    Args:
        draw (callable): A function to call to update the Pygame window.
        grid (Grid): The Grid object containing the spots.
        start (Spot): The starting spot.
        end (Spot): The ending spot.
    Returns:
        bool: True if a path is found, False otherwise.
    """
    count = 0
    open_heap = PriorityQueue()

    def h(p1: tuple[int, int], p2: tuple[int, int]) -> float:
        """
        Heuristic function for A* algorithm: uses the Manhattan distance between two points.
        Args:
            p1 (tuple[int, int]): The first point (x1, y1).
            p2 (tuple[int, int]): The second point (x2, y2).
        Returns:
            float: The Manhattan distance between p1 and p2.
        """
        x1, y1 = p1
        x2, y2 = p2
        return abs(x1 - x2) + abs(y1 - y2)

    open_heap.put((0, count, start))
    came_from = {}

    g_score = {spot: float('inf') for row in grid.grid for spot in row}
    f_score = {spot: float('inf') for row in grid.grid for spot in row}

    g_score[start] = 0
    f_score[start] = h(start.get_position(), end.get_position())

    lookup_set = {start}

    while not open_heap.empty():
        current = open_heap.get()[2]
        lookup_set.remove(current)

        if current == end:
            while current in came_from:
                current = came_from[current]
                if current != start:
                    current.make_path()
                draw()
            end.make_end()
            start.make_start()
            pygame.mixer.Sound.play(path_found_sound)
            return True

        for neighbor in current.neighbors:
            tentative_g = g_score[current] + 1

            if tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + h(neighbor.get_position(), end.get_position())

                if neighbor not in lookup_set:
                    count += 1
                    open_heap.put((f_score[neighbor], count, neighbor))
                    lookup_set.add(neighbor)
                    if neighbor != end:
                        neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False

def reconstruct_path(came_from: dict, current: Spot, start: Spot, end: Spot, draw: Callable[[], None]) -> None:
    while current in came_from:
        current = came_from[current]
        if current != start:
            current.make_path()
        draw()
    end.make_end()
    start.make_start()

def dls(draw: callable, grid: Grid, start: Spot, end: Spot, limit: int) -> bool:
    """
    Depth-Limited Search (recursive).
    limit: maximum depth to search (0 means only start)
    """
    if start is None or end is None:
        return False

    def dfs_limit(node: Spot, depth: int, visited_path: set) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

        if node == end:
            return True

        if depth == 0:
            return False

        for neighbor in node.neighbors:
            if neighbor in visited_path or neighbor.is_barrier():
                continue
            visited_path.add(neighbor)
            neighbor.make_open()
            draw()
            found = dfs_limit(neighbor, depth - 1, visited_path)
            if found:
                return True
            visited_path.remove(neighbor)
            if neighbor != end:
                neighbor.make_closed()
            draw()
        return False

    visited_path = {start}
    start.make_open()
    found = dfs_limit(start, limit, visited_path)
    if found:
        came_from = {}

        def dfs_parent(node: Spot, target: Spot, visited_p: set) -> bool:
            if node == target:
                return True
            for neighbor in node.neighbors:
                if neighbor in visited_p or neighbor.is_barrier():
                    continue
                visited_p.add(neighbor)
                came_from[neighbor] = node
                if dfs_parent(neighbor, target, visited_p):
                    return True
            return False

        visited_p = {start}
        dfs_parent(start, end, visited_p)
        reconstruct_path(came_from, end, start, end, draw)
        pygame.mixer.Sound.play(path_found_sound)
        return True

    return False

def ucs(draw: callable, grid: Grid, start: Spot, end: Spot) -> bool:
    if start is None or end is None:
        return False

    count = 0
    pq = PriorityQueue()
    pq.put((0, count, start))
    came_from = {}
    g_score = {spot: float('inf') for row in grid.grid for spot in row}
    g_score[start] = 0
    visited = set()

    while not pq.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

        current = pq.get()[2]

        if current == end:
            reconstruct_path(came_from, end, start, end, draw)
            pygame.mixer.Sound.play(path_found_sound)
            return True

        if current in visited:
            continue
        visited.add(current)

        for neighbor in current.neighbors:
            if neighbor.is_barrier():
                continue
            tentative_g = g_score[current] + 1
            if tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                count += 1
                pq.put((g_score[neighbor], count, neighbor))
                if neighbor != end:
                    neighbor.make_open()

        draw()
        if current != start:
            current.make_closed()

    return False

def greedy_best_first(draw: callable, grid: Grid, start: Spot, end: Spot,
                      heuristic: Callable[[Tuple[int, int], Tuple[int, int]], float] = h_manhattan_distance) -> bool:
    if start is None or end is None:
        return False

    count = 0
    pq = PriorityQueue()
    pq.put((heuristic(start.get_position(), end.get_position()), count, start))
    came_from = {}
    visited = set([start])

    while not pq.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

        current = pq.get()[2]

        if current == end:
            reconstruct_path(came_from, end, start, end, draw)
            pygame.mixer.Sound.play(path_found_sound)
            return True

        for neighbor in current.neighbors:
            if neighbor in visited or neighbor.is_barrier():
                continue
            visited.add(neighbor)
            came_from[neighbor] = current
            count += 1
            pq.put((heuristic(neighbor.get_position(), end.get_position()), count, neighbor))
            if neighbor != end:
                neighbor.make_open()

        draw()
        if current != start:
            current.make_closed()

    return False

def iddfs(draw: callable, grid: Grid, start: Spot, end: Spot, max_depth: Optional[int] = None) -> bool:
    if start is None or end is None:
        return False

    if max_depth is None:
        rows = len(grid.grid)
        cols = len(grid.grid[0]) if rows > 0 else 0
        max_depth = rows * cols

    for depth in range(max_depth + 1):
        found = dls(draw, grid, start, end, depth)
        if found:
            pygame.mixer.Sound.play(path_found_sound)
            return True
    return False

def ida(draw: callable, grid: Grid, start: Spot, end: Spot,
        heuristic: Callable[[Tuple[int, int], Tuple[int, int]], float] = h_manhattan_distance) -> bool:
    if start is None or end is None:
        return False

    start_pos = start.get_position()
    end_pos = end.get_position()
    bound = heuristic(start_pos, end_pos)

    def search(node: Spot, g: float, bound: float, path_set: set, came_from: dict) -> (bool, float):

        f = g + heuristic(node.get_position(), end_pos)
        if f > bound:
            return False, f
        if node == end:
            return True, f

        min_exceeded = float('inf')
        for neighbor in node.neighbors:
            if neighbor.is_barrier() or neighbor in path_set:
                continue
            path_set.add(neighbor)
            came_from[neighbor] = node
            if neighbor != end:
                neighbor.make_open()
            draw()
            found, temp = search(neighbor, g + 1, bound, path_set, came_from)
            if found:
                return True, temp
            if temp < min_exceeded:
                min_exceeded = temp
            if neighbor != end:
                neighbor.make_closed()
            path_set.remove(neighbor)
            came_from.pop(neighbor, None)
            draw()
        return False, min_exceeded

    while True:
        came_from = {}
        path_set = {start}
        found, next_bound = search(start, 0, bound, path_set, came_from)
        if found:
            reconstruct_path(came_from, end, start, end, draw)
            pygame.mixer.Sound.play(path_found_sound)
            return True
        if next_bound == float('inf'):
            return False
        bound = next_bound
