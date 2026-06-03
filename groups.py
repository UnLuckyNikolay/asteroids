# pyright: reportAttributeAccessIssue=false

import pygame

class GroupManager:
    def __init__(self):
        # Updatables
        self.updatable_ui = pygame.sprite.Group()         # Always updated, DO NOT use with other updatable groups
        self.updatable_gameplay = pygame.sprite.Group()   # For player/asteroids/etc during a round
        self.updatable_ambient = pygame.sprite.Group()    # For asteroids in menus

        self.drawable = pygame.sprite.Group()
        # Layers for drawable
        # 0 - StarField
        # 10 - Explosion
        # 20 - Bomb
        # 30 - Asteroid(and children)
        # 40 - Loot
        # 50 - Player
        # 60 - ProjectilePlasma
        # 90 - ExplosionRound (overwrites Explosion, used as player's death animation)
        # 100 - UserInterface

        self.asteroids = pygame.sprite.Group()            # Used for colision detection
        self.loot = pygame.sprite.Group()                 # ^ + magnet
        self.projectiles = pygame.sprite.Group()          # ^
        self.explosion_hitboxes = pygame.sprite.Group()   # ^

        self.moving_objects = pygame.sprite.Group()       # Used to destroy objects that are off-screen
        self.cleanup = pygame.sprite.Group()              # This group is cleaned (object.kill()) after each round
    