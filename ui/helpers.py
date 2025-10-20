import pygame, pygame.gfxdraw

def get_points(
        position : tuple[int, int],
        size : tuple[int, int],
        corners : tuple[int, int, int, int]
    ) -> list:
    """Returns a list of 4 to 8 points for drawing a quadrangular polygon with cut corners."""

    points = []
    if corners[0] == 0:
        points.append(position)
    else:
        points.extend([
            (position[0], position[1] + corners[0]), 
            (position[0] + corners[0], position[1])
        ])
    if corners[1] == 0:
        points.append(((position[0] + size[0], position[1])))
    else:
        points.extend([
            (position[0] + size[0] - corners[1], position[1]), 
            (position[0] + size[0], position[1] + corners[1])
        ])
    if corners[2] == 0:
        points.append((position[0] + size[0], position[1] + size[1]))
    else:
        points.extend([
            (position[0] + size[0], position[1] + size[1] - corners[2]), 
            (position[0] + size[0] - corners[2], position[1] + size[1]
        )])
    if corners[3] == 0:
        points.append((position[0], position[1] + size[1]))
    else:
        points.extend([
            (position[0] + corners[3], position[1] + size[1]), 
            (position[0], position[1] + size[1] - corners[3])
        ])
    return points

def draw_polygon(
        screen,
        position : tuple[int, int],
        size : tuple[int, int],
        corners : tuple[int, int, int, int],
        color : tuple[int, int, int, int]
    ):
    """Draws a filled quadrangular polygon with cut corners."""

    points = get_points(position, size, corners)
    pygame.gfxdraw.filled_polygon(screen, points, color)
