import pygame
from constants import *
from circleshapes.player import Player
from asteroidfield import AsteroidField
from circleshapes.projectileplasma import ProjectilePlasma
from gamestatemanager import GameStateManager
from circleshapes.explosion import Explosion
from starfield import StarField
from circleshapes.asteroids.asteroidbasic import AsteroidBasic
from circleshapes.asteroids.asteroidgolden import AsteroidGolden
from circleshapes.asteroids.asteroidexplosive import AsteroidExplosive


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Asteroids")
    clock = pygame.time.Clock()
    dt = 0
    player_is_alive = True

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    projectiles = pygame.sprite.Group()
    moving_objects = pygame.sprite.Group()

    StarField.containers = (drawable)
    Player.containers = (updatable, drawable)
    AsteroidBasic.containers = (asteroids, updatable, drawable, moving_objects)
    AsteroidGolden.containers = (asteroids, updatable, drawable, moving_objects)
    AsteroidExplosive.containers = (asteroids, updatable, drawable, moving_objects)
    AsteroidField.containers = (updatable)
    ProjectilePlasma.containers = (projectiles, updatable, drawable, moving_objects)
    Explosion.containers = (updatable, drawable)

    starfield = StarField()
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    gameinfo = GameStateManager(player)
    asteroidfield = AsteroidField()

    while player_is_alive:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        

        screen.fill("black")
        gameinfo.draw(screen)

        for object in updatable:
            object.update(dt)

        for object in moving_objects:
            if object.is_off_screen():
                object.kill()

        for object in drawable:
            object.draw(screen)

        for asteroid in asteroids:
            if asteroid.check_colision(player) and not player.is_invul:
                player_is_alive = player.got_shot(gameinfo)
                if player_is_alive:
                    asteroid.kill()
                    explosion = Explosion(asteroid.position.x, asteroid.position.y, asteroid.radius)
                else:
                    return
                
            for shot in projectiles:
                if shot.check_colision(asteroid) and not asteroid.has_been_hit:
                    shot.kill()
                    asteroid.split()
                    explosion = Explosion(asteroid.position.x, asteroid.position.y, asteroid.radius)
                    gameinfo.score += asteroid.reward


        pygame.display.flip()
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
