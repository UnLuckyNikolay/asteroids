from shapes.circleshape import CircleShape


class BombExplosion(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        