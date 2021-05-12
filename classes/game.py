import pygame
from menu.MainMenu import *
from pygame.locals import *
from pygame import mixer
import warnings

class Game():
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 2, 512)
        pygame.mixer.set_num_channels(20)
        mixer.init()
        pygame.init()
        #MENU MUSIC
        pygame.mixer.music.load('clips/menu_music.wav')
        pygame.mixer.Channel(0).play(pygame.mixer.Sound('clips/menu_music.wav'),maxtime=5000)
        pygame.mixer.music.play(-1, 0.0, 0)
        self.running, self.playing = True, False
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY , self.LEFT_KEY , self.RIGHT_KEY = False, False, False, False, False , False
        self.DISPLAY_W, self.DISPLAY_H = 1500, 800
        pygame.display.set_caption("Εξεταστικη, on the run")
        self.display = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))
        self.window = pygame.display.set_mode(
            ((self.DISPLAY_W, self.DISPLAY_H)))
        self.font_name = '8-BIT WONDER.TTF'
        self.font_name = pygame.font.get_default_font()
        self.BLACK, self.WHITE, self.RED = (0, 0, 0), (255, 255, 255), (255, 0 ,0)
        self.main_menu = MainMenu(self)
       # self.stages = StagesMenu(self)
        self.options = OptionsMenu(self)
        self.credits = CreditsMenu(self)
        self.quit = QuitMenu(self)
        self.shop = ShopMenu(self)
        self.profile = ProfileMenu(self)
        self.lore = LoreMenu(self)
        self.curr_menu = self.main_menu
        self.fps = 60

    def game_loop(self):
        while self.playing:
            self.check_events()
            if self.START_KEY:
                self.playing = False
            self.display.fill(self.BLACK)
            from classes import maingame
            self.reset_keys()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                self.curr_menu.run_display = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                if event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pygame.K_UP:
                    self.UP_KEY = True
                if event.key == pygame.K_LEFT:
                    self.LEFT_KEY = True
                if event.key == pygame.K_RIGHT:
                    self.RIGHT_KEY = True



    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY , self.LEFT_KEY , self.RIGHT_KEY = False, False, False, False ,False , False

    def draw_text(self, text, size, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.display.blit(text_surface, text_rect)
