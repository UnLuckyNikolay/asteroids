import pygame
from constants import *
from player.player import Player
from player.weapons.projectiles.projectileplasma import ProjectilePlasma
from player.weapons.projectiles.bomb import Bomb
from player.weapons.projectiles.bombexplosion import BombExplosion
from gamestatemanager import GameStateManager
from vfx.explosion import Explosion
from world.starfield import StarField
from world.asteroidfield import AsteroidField
from asteroids.asteroid import Asteroid
from userinterface import UserInterface


# Move player_is_alive to player.is_alive


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Asteroids")
    clock = pygame.time.Clock()
    dt = 0
    player_is_alive = True

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()            # Used for colision detection
    projectiles = pygame.sprite.Group()          # ^
    explosion_hitboxes = pygame.sprite.Group()   # ^
    moving_objects = pygame.sprite.Group()        # Used to destroy objects that are off-screen

    UserInterface.containers = (drawable)

    StarField.containers = (drawable)
    Explosion.containers = (updatable, drawable)

    Player.containers = (updatable, drawable)
    ProjectilePlasma.containers = (projectiles, updatable, drawable, moving_objects)
    Bomb.containers = (drawable, updatable)
    BombExplosion.containers = (explosion_hitboxes)

    AsteroidField.containers = (updatable)
    Asteroid.containers = (asteroids, updatable, drawable, moving_objects)

    # Layers for drawable
    # 0 - StarField
    # 10 - Explosion
    # 20 - Bomb
    # 30 - Asteroid(and children)
    # 50 - Player
    # 60 - ProjectilePlasma
    # 100 - UserInterface


    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    game = GameStateManager(player)
    ui = UserInterface(game, player)
    starfield = StarField()
    asteroidfield = AsteroidField(player)

    while player_is_alive:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        

        screen.fill("black")

        for object in updatable:
            object.update(dt)

        for object in moving_objects:
            if object.is_off_screen():
                object.kill()

        for object in sorted(list(drawable), key = lambda object: object.layer):
            object.draw(screen)

        for asteroid in asteroids:
            if asteroid.check_colision(player) and not player.is_invul:
                player_is_alive = player.take_damage_and_check_if_alive(game)
                if player_is_alive:
                    asteroid.kill()
                    explosion = Explosion(asteroid.position.x, asteroid.position.y, asteroid.radius)
                else:
                    return
                
            for projectile in projectiles:
                if projectile.check_colision(asteroid) and not asteroid.has_been_hit:
                    projectile.kill()
                    asteroid.split()
                    explosion = Explosion(asteroid.position.x, asteroid.position.y, asteroid.radius)
                    game.score += asteroid.reward
            
        for hitbox in explosion_hitboxes:
            for asteroid in asteroids:
                if hitbox.check_colision(asteroid) and not asteroid.has_been_hit:
                    asteroid.split()
                    game.score += asteroid.reward
            hitbox.kill()


        pygame.display.flip()
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
