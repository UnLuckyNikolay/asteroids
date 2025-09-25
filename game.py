# pyright: reportAttributeAccessIssue=false

import pygame, json
from tkinter import Tk, simpledialog
from random import randint

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
from ui.userinterface import UserInterface, Menu


class Game():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Asteroids from Outer Space")
        self.clock = pygame.time.Clock()
        self.dt = 0
        self.is_running = True
        self.is_paused = False
        self.space_color = SPACE_COLOR_LIST[randint(0, len(SPACE_COLOR_LIST)-1)]

        self.updatable = pygame.sprite.Group()   # This group is cleaned (object.kill()) after each round
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
        self.ui = UserInterface(self)

    def run(self):
        while self.is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == pygame.BUTTON_LEFT:
                        self.ui.check_click(pygame.mouse.get_pos())
                
            self.redraw_objects_and_ui()

            pygame.display.flip()
            self.clock.tick(60)

    def game_loop(self):
        self.player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.gsm = GameStateManager(self.player)
        self.asteroid_field = AsteroidField(self.player)
        self.ui.switch_menu(Menu.HUD)
        self.ui.player = self.player
        self.ui.gsm = self.gsm
        self.is_paused = False


        while self.player.is_alive:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if not self.is_paused:
                            self.is_paused = True
                            self.ui.switch_menu(Menu.PAUSE_MENU)
                        else:
                            self.is_paused = False
                            self.ui.switch_menu(Menu.HUD)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == pygame.BUTTON_LEFT:
                        self.ui.check_click(pygame.mouse.get_pos())

            if not self.is_paused:
                for object in self.updatable:
                    object.update(self.dt)

                for object in self.moving_objects:
                    if object.is_off_screen():
                        object.kill()

                self.redraw_objects_and_ui()

                for asteroid in self.asteroids:
                    if asteroid.check_colision(self.player) and not self.player.is_invul:
                        if self.player.take_damage_and_check_if_alive(self.gsm):
                            asteroid.kill()
                            explosion = Explosion(asteroid.position.x, asteroid.position.y, asteroid.radius)
                        
                    for projectile in self.projectiles:
                        if projectile.check_colision(asteroid) and not asteroid.has_been_hit:
                            projectile.kill()
                            asteroid.split()
                            explosion = Explosion(asteroid.position.x, asteroid.position.y, asteroid.radius)
                            self.gsm.score += asteroid.reward
                    
                for hitbox in self.explosion_hitboxes:
                    for asteroid in self.asteroids:
                        if hitbox.check_colision(asteroid) and not asteroid.has_been_hit:
                            asteroid.split()
                            self.gsm.score += asteroid.reward
                    hitbox.kill()
            else:
                self.redraw_objects_and_ui()
                    
            pygame.display.flip()
            self.dt = self.clock.tick(60) / 1000

        if not self.player.is_invul:
            self.check_score(self.gsm.score)
        self.ui.switch_menu(Menu.MAIN_MENU)

        self.player = None
        self.gsm = None
        self.asteroid_field = None
        self.ui.player = None
        self.ui.gsm = None

        for object in self.updatable:
            object.kill()

    ### Helpers
    
    def redraw_objects_and_ui(self):
        self.screen.fill(self.space_color)

        for object in sorted(list(self.drawable), key = lambda object: object.layer):
            object.draw(self.screen)

    def check_score(self, score):
        try:
            with open("leaderboard.json", "r") as file:
                scores = json.load(file)
        except FileNotFoundError:
            scores = []

        while len(scores) > LEADERBOARD_LENGTH:   # Shortens leaderboard if max length was reduced
            scores.pop()
        if len(scores) == LEADERBOARD_LENGTH and score > scores[LEADERBOARD_LENGTH - 1]["score"]:
            scores.pop()
        if len(scores) != LEADERBOARD_LENGTH:
            name = self.ask_player_name()
            scores.append({"name": name, "score": score})
            scores.sort(key=lambda x: x["score"], reverse=True)

        with open("leaderboard.json", "w") as file:
            json.dump(scores, file)

    def ask_player_name(self):
        root = Tk()
        root.withdraw()

        name = simpledialog.askstring("New record!", "Please enter your name: ")

        root.destroy()

        return name if name else "Player"
    
    ### Handlers
    
    def handler_turn_off(self):
        self.is_running = False

    def handler_finish_round(self):
        if self.player != None and self.player.is_alive:
            self.player.is_alive = False

    def get_current_weapon_name(self) -> str:
        if self.player == None:
            return "Missing"
        return self.player.weapon.get_name()

    def get_current_lives(self) -> int:
        if self.gsm == None:
            return 0
        return self.gsm.lives
    
    def get_current_score(self) -> int:
        if self.gsm == None:
            return 0
        return self.gsm.score
