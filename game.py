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


class Game():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Asteroids")
        self.clock = pygame.time.Clock()
        self.dt = 0
            
        self.updatable = pygame.sprite.Group()
        self.drawable = pygame.sprite.Group()
        self.asteroids = pygame.sprite.Group()            # Used for colision detection
        self.projectiles = pygame.sprite.Group()          # ^
        self.explosion_hitboxes = pygame.sprite.Group()   # ^
        self.moving_objects = pygame.sprite.Group()        # Used to destroy objects that are off-screen

        UserInterface.containers = (self.drawable)

        StarField.containers = (self.drawable)
        Explosion.containers = (self.updatable, self.drawable)

        Player.containers = (self.updatable, self.drawable)
        ProjectilePlasma.containers = (self.projectiles, self.updatable, self.drawable, self.moving_objects)
        Bomb.containers = (self.drawable, self.updatable)
        BombExplosion.containers = (self.explosion_hitboxes)

        AsteroidField.containers = (self.updatable)
        Asteroid.containers = (self.asteroids, self.updatable, self.drawable, self.moving_objects)

        # Layers for drawable
        # 0 - StarField
        # 10 - Explosion
        # 20 - Bomb
        # 30 - Asteroid(and children)
        # 50 - Player
        # 60 - ProjectilePlasma
        # 100 - UserInterface

        self.star_field = StarField()


    def game_loop(self):
        self.player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.game_state = GameStateManager(self.player)
        self.ui = UserInterface(self.game_state, self.player)
        self.asteroid_field = AsteroidField(self.player)

        while self.player.is_alive:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
            

            self.screen.fill("black")

            for object in self.updatable:
                object.update(self.dt)

            for object in self.moving_objects:
                if object.is_off_screen():
                    object.kill()

            for object in sorted(list(self.drawable), key = lambda object: object.layer):
                object.draw(self.screen)

            for asteroid in self.asteroids:
                if asteroid.check_colision(self.player) and not self.player.is_invul:
                    player_is_alive = self.player.take_damage_and_check_if_alive(self.game_state)
                    if player_is_alive:
                        asteroid.kill()
                        explosion = Explosion(asteroid.position.x, asteroid.position.y, asteroid.radius)
                    else:
                        return
                    
                for projectile in self.projectiles:
                    if projectile.check_colision(asteroid) and not asteroid.has_been_hit:
                        projectile.kill()
                        asteroid.split()
                        explosion = Explosion(asteroid.position.x, asteroid.position.y, asteroid.radius)
                        self.game_state.score += asteroid.reward
                
            for hitbox in self.explosion_hitboxes:
                for asteroid in self.asteroids:
                    if hitbox.check_colision(asteroid) and not asteroid.has_been_hit:
                        asteroid.split()
                        self.game_state.score += asteroid.reward
                hitbox.kill()


            pygame.display.flip()
            self.dt = self.clock.tick(60) / 1000
