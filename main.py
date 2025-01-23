import pygame
from constants import *
from circleshapes.player import Player
from circleshapes.asteroid import Asteroid
from asteroidfield import AsteroidField
from circleshapes.shot import Shot
from gameinfo import GameInfo
from circleshapes.explosion import Explosion


# To fix:

# --- Asteroids can be split multiple times


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Asteroids")
    clock = pygame.time.Clock()
    dt = 0
    score = 0
    player_is_alive = True

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    Shot.containers = (shots, updatable, drawable)
    Explosion.containers = (updatable, drawable)

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    gameinfo = GameInfo(player)
    asteroidfield = AsteroidField()

    while player_is_alive:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        

        screen.fill("black")
        gameinfo.draw(screen)

        for object in updatable:
            object.update(dt)
        print(f"The amount of objects: {len(drawable)}")

        for object in drawable:
            if object.is_off_screen():
                object.kill()
            else:
                object.draw(screen)

        for asteroid in asteroids:
            if asteroid.check_colision(player) and not player.is_invul:
                player_is_alive = player.got_shot(gameinfo)
                if player_is_alive:
                    asteroid.kill()
                    explosion = Explosion(asteroid.position.x, asteroid.position.y, asteroid.radius)
                else:
                    return
                
            for shot in shots:
                if shot.check_colision(asteroid):
                    shot.kill()
                    asteroid.split()
                    explosion = Explosion(asteroid.position.x, asteroid.position.y, asteroid.radius)
                    gameinfo.score += 1


        pygame.display.flip()
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
