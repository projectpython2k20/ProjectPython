import pygame
import sys
import warnings
from pygame.locals import *
from pygame import mixer
from os import path
import pickle 


mixer.init()
pygame.init()


class Menu():       #aexikopoioume to menu +metablhtes
    def __init__(self, game):
        self.game = game
        self.mid_w, self.mid_h  = self.game.DISPLAY_W / 3, self.game.DISPLAY_H / 2
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.offset = - 100


    def blit_screen(self):
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()
        self.game.reset_keys()

class MainMenu(Menu):                                                              
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Play"
        self.startx, self.starty = self.mid_w, self.mid_h / 2
        self.optionsx, self.optionsy = self.mid_w, self.mid_h / 2 + 30
        self.shopx, self.shopy = self.mid_w, self.mid_h / 2 + 60
        self.lorex, self.lorey = self.mid_w, self.mid_h / 2 + 90
        self.profilex, self.profiley = self.mid_w, self.mid_h / 2 + 120
        self.creditsx, self.creditsy = self.mid_w, self.mid_h / 2 + 150
        self.quitx, self.quity = self.mid_w, self.mid_h / 2 + 180
        self.versionx, self.versiony = self.mid_w / 2 - 350, self.mid_h /2 + 590
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty)

    def display_menu(self):                                                            
        dis = pygame.display.set_mode ((960 , 540))
        bg = pygame.image.load('./img/wallpapper01.png').convert_alpha()
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            pygame.display.update()
            self.game.display.blit(bg, (0,0))
            self.game.draw_text('Life of a uni-student', 40 , self.game.DISPLAY_W / 3, self.game.DISPLAY_H /2 - 290)
            self.game.draw_text("Play", self.highlighted("Play"), self.startx, self.starty)
            
            self.game.draw_text("Options", self.highlighted("Options"), self.optionsx, self.optionsy)
            self.game.draw_text("Shop", self.highlighted("Shop"), self.shopx, self.shopy)
            self.game.draw_text("Lore", self.highlighted("Lore"), self.lorex, self.lorey)
            self.game.draw_text("Profile", self.highlighted("Profile"), self.profilex, self.profiley)
            self.game.draw_text("Credits", self.highlighted("Credits"), self.creditsx, self.creditsy)
            self.game.draw_text("Quit", self.highlighted("Quit"), self.quitx, self.quity)
            self.game.draw_text("version 0.1", 8, self.versionx, self.versiony)
            self.blit_screen()

    def move_cursor(self):
        if self.game.DOWN_KEY:
            move_arrow = mixer.Sound('clips/down_up_arrow.wav')
            move_arrow.play()
            if self.state == 'Play':
                self.state = 'Options'
            elif self.state == 'Options':
                self.state = 'Shop'
            elif self.state == 'Shop':
                self.state = 'Lore'
            elif self.state == 'Lore':
                self.state = 'Profile'
            elif self.state == 'Profile':
                self.state = 'Credits'
            elif self.state == 'Credits':
                self.state = 'Quit'
            elif self.state == 'Quit':
                self.state = 'Play'
        elif self.game.UP_KEY:
            move_arrow = mixer.Sound('clips/down_up_arrow.wav')
            move_arrow.play()
            if self.state == 'Play':
                self.state = 'Quit'
            elif self.state == 'Quit':
                self.state = 'Credits'
            elif self.state == 'Credits':
                self.state = 'Profile'
            elif self.state == 'Profile':
                self.state = 'Lore'
            elif self.state == 'Lore':
                self.state = 'Shop'
            elif self.state == 'Shop':
                self.state = 'Options'
            elif self.state == 'Options':
                self.state = 'Play'
                
    def highlighted(self,a):
        if a == self.state:
            return 30
        return 25

    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            enter_button = mixer.Sound('clips/enter_button.wav')
            enter_button.play()
            if self.state == 'Play':
                self.game.playing = True
            elif self.state == 'Options':
                self.game.curr_menu = self.game.options
            elif self.state == 'Credits':
                self.game.curr_menu = self.game.credits
            elif self.state == 'Shop':
                self.game.curr_menu = self.game.shop
            elif self.state == 'Profile':
                self.game.curr_menu = self.game.profile
            elif self.state == 'Quit':
                self.game.curr_menu = self.game.quit
            elif  self.state == 'Volume':
                self.game.options = self.game.volume
            elif self.state == 'Lore':
                self.game.curr_menu = self.game.lore
            self.run_display = False


class OptionsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'Volume'
        self.volx, self.voly = self.mid_w, self.mid_h + 200
        self.controlsx, self.controlsy = self.mid_w, self.mid_h + 300
        self.backx, self.backy = self.mid_w, self.mid_h + 400
        self.cursor_rect.midtop = (self.volx + self.offset, self.voly)

    
    def highlighted(self,a):
        if a == self.state:
            return 25
        return 20

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            background_credits = pygame.image.load('./img/wallpapper01.png').convert_alpha()        #allazei to backround gia ta options
            self.game.display.blit(background_credits, (0,0))
            self.game.draw_text('Options', 40, self.game.DISPLAY_W / 3, self.game.DISPLAY_H / 2 - 290)
            self.game.draw_text("Volume", self.highlighted("Volume"), self.volx, self.voly / 2 - 100)
            self.game.draw_text("Controls", self.highlighted("Controls"), self.controlsx, self.controlsy / 2 - 80)
            self.game.draw_text("Back", self.highlighted("Back"), self.backx, self.backy / 2 - 60)
            self.blit_screen()

    def check_input(self):
        if self.game.BACK_KEY:
            #MUSIC
            back_button = mixer.Sound('clips/back_button.wav')
            back_button.play()
            #backbutton.play()
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
        elif self.game.UP_KEY:
            #music
            move_arrow = mixer.Sound('clips/down_up_arrow.wav')
            move_arrow.play()
            if self.state == 'Volume':
                self.state = 'Back'
            elif self.state == 'Back':
                self.state = 'Controls'
            elif self.state == 'Controls':
                self.state = 'Volume'
        elif self.game.DOWN_KEY:
            #music
            move_arrow = mixer.Sound('clips/down_up_arrow.wav')
            move_arrow.play()
            if self.state == 'Volume':
                self.state = 'Controls'
            elif self.state == 'Controls':
                self.state = 'Back'
            elif self.state == 'Back':
                self.state = 'Volume'
        elif self.game.START_KEY:
           enter_button= mixer.Sound('clips/enter_button.wav')
           enter_button.play()
           if self.state == 'Volume':
              self.game.options = self.game.volume
           elif self.state == 'Back':
               #music
                back_button = mixer.Sound('clips/back_button.wav')
                back_button.play()
                #backbutton.play()
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
                pass
class VolumeMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'MenuMusic'
        self.MenuMusic, self.MenuMusicy = self.mid_w, self.mid_h + 20
        self.Yesx, self.Yesy = self.mid_w, self.mid_h + 40
        self.Nox, self.Noy = self.mid_w, self.mid_h + 60
        self.cursor_rect.midtop = (self.Yesx + self.offset, self.Yesy)

        def highlighted(self,a):
            if a == self.state:
                return 25
            return 20

    def display_menu(self):
        self.run_display = True
        while self.run_display:
                self.game.check_events()
                self.check_input()
                background_credits = pygame.image.load('./img/wallpapper01.png').convert_alpha()
                self.game.display.blit(background_credits, (0,0))
                self.game.draw_text('MenuMusic', 40, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 350)
                self.game.draw_text("Yes", self.highlighted("Yes"), self.volx, self.voly / 2 - 100)
                self.game.draw_text("No", self.highlighted("No"), self.controlsx, self.controlsy / 2 - 80)
                self.game.draw_text("Back", self.highlighted("Back"), self.backx, self.backy / 2 - 60)
                self.blit_screen()
    def check_input(self):
        if self.game.BACK_KEY:
            #MUSIC
            back_button = mixer.Sound('clips/back_button.wav')
            back_button.play()
            #backbutton.play()
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
        elif self.game.UP_KEY:
            #music
            move_arrow = mixer.Sound('clips/down_up_arrow.wav')
            move_arrow.play()
            if self.state == 'Yes':
                self.state = 'No'
            elif self.state == 'No':
                self.state = 'Back'
            elif self.state == 'Back':
                self.state = 'Yes'
        elif self.game.DOWN_KEY:
            #music
            move_arrow = mixer.Sound('clips/down_up_arrow.wav')
            move_arrow.play()
            if self.state == 'Back':
                self.state = 'No'
            elif self.state == 'No':
                self.state = 'Yes'
            elif self.state == 'Yes':
                self.state = 'Back'
            




class CreditsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            if self.game.START_KEY or self.game.BACK_KEY:
                #music
                back_button = mixer.Sound('clips/back_button.wav')
                back_button.play()
                #backbutton.play()
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
            background_credits = pygame.image.load('./img/wallpapper01.png').convert_alpha()            #allazei to backround sta CREDITS
            self.game.display.blit(background_credits, (0,0))
            self.game.draw_text('Credits', 40, self.game.DISPLAY_W / 3, self.game.DISPLAY_H / 2 - 290)
            self.game.draw_text('Made by: Φοιτητές εξ-αποστάσεως', 30, self.game.DISPLAY_W / 3, self.game.DISPLAY_H / 2 - 250)
            self.game.draw_text('Πολίτης Σπυρίδων ', 20, self.game.DISPLAY_W / 3, self.game.DISPLAY_H / 2 - 200)
            self.game.draw_text('Γιανκούλης Αλέξανδρος', 20, self.game.DISPLAY_W / 3, self.game.DISPLAY_H / 2 - 150)
            self.game.draw_text('Φελλαχίδης Γεώργιος', 20, self.game.DISPLAY_W / 3, self.game.DISPLAY_H / 2 - 100)
            self.game.draw_text('Ντούρος Σπυρίδων', 20, self.game.DISPLAY_W / 3, self.game.DISPLAY_H / 2 - 50)
            self.blit_screen()

class LoreMenu(Menu):
       def __init__(self, game):
        Menu.__init__(self, game)
        

       def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            if self.game.START_KEY or self.game.BACK_KEY:
                #music
                back_button = mixer.Sound('clips/back_button.wav')
                back_button.play()
                #backbutton.play()
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
            background_credits = pygame.image.load('./img/wallpapper01.png').convert_alpha()
            self.game.display.blit(background_credits, (0,0))
            self.game.draw_text('This is how we ended up here', 30, self.game.DISPLAY_W / 3, self.game.DISPLAY_H / 2 - 300)
            self.game.draw_text("One rainy day the results of your SAT's got announced , ", 20, self.game.DISPLAY_W / 3, self.game.DISPLAY_H / 2 - 250)
            self.game.draw_text("you passed in a university and you were happy thinking ", 20, self.game.DISPLAY_W / 3, self.game.DISPLAY_H / 2 - 230)
            self.game.draw_text('that you don’t have to study anymore', 20, self.game.DISPLAY_W / 3, self.game.DISPLAY_H / 2 - 210)
            self.game.draw_text('you thought that you will have the best time of your life ', 20, self.game.DISPLAY_W / 3, self.game.DISPLAY_H / 2 - 190)
            self.game.draw_text("hanging out all day and going to roadtrips with your friends", 20, self.game.DISPLAY_W / 3, self.game.DISPLAY_H / 2 -170)

            
            self.game.draw_text('but little did you know...you realised that you were terribly wrong', 20, self.game.DISPLAY_W / 3, self.game.DISPLAY_H / 2 - 150)
            self.game.draw_text('The first day of the university came and each and everyone ', 20, self.game.DISPLAY_W / 3, self.game.DISPLAY_H / 2 - 130)
            self.game.draw_text('tries to get the required amount of ECTS to get out of here', 20, self.game.DISPLAY_W / 3, self.game.DISPLAY_H / 2 - 110)
            self.game.draw_text('but every time a student fails to pass an exam , September awaits them.  ', 20, self.game.DISPLAY_W / 3, self.game.DISPLAY_H / 2 - 90)
            self.game.draw_text('So you are at your last year before graduation and you need to gather  ', 20, self.game.DISPLAY_W / 3, self.game.DISPLAY_H / 2 - 70)
            self.game.draw_text('the rest ECTS while Septermber is right around the corner ', 20, self.game.DISPLAY_W / 3, self.game.DISPLAY_H / 2 - 50)
            self.game.draw_text('Will you succeed on getting out of there alive and with your degree?  ', 20, self.game.DISPLAY_W / 3, self.game.DISPLAY_H / 2 - 30)
            self.game.draw_text('Try to collect as many ECTS you can in order to succeed', 20, self.game.DISPLAY_W / 3, self.game.DISPLAY_H / 2 - 10)
            self.game.draw_text('GOOD LUCK', 20, self.game.DISPLAY_W / 3, self.game.DISPLAY_H / 2 + 40)
            self.blit_screen()

#class StagesMenu(Menu):                                                              
    # def __init__(self, game):
    #     Menu.__init__(self, game)
    #     self.state = "Stage 1"
    #     self.stage1x, self.stage1y = self.mid_w, self.mid_h / 2
    #     self.stage2x, self.stage2y = self.mid_w, self.mid_h / 2 + 30
    #     self.stage3x, self.stage3y = self.mid_w, self.mid_h / 2 + 60
    #     self.stage4x, self.stage4y = self.mid_w, self.mid_h / 2 + 90
    #     self.stage5x, self.stage5y = self.mid_w, self.mid_h / 2 + 110
    #     self.stage6x, self.stage6y = self.mid_w, self.mid_h / 2 + 140
    #     self.stage7x, self.stage7y = self.mid_w, self.mid_h / 2 + 170
    #     self.stage8x, self.stage8y = self.mid_w, self.mid_h / 2 + 200
    #     self.stage9x, self.stage9y = self.mid_w, self.mid_h / 2 +230
    #     self.stage10x, self.stage10y = self.mid_w, self.mid_h / 2 + 260

    #     self.backx, self.backy = self.mid_w, self.mid_h / 2 + 280
    #     self.versionx, self.versiony = self.mid_w / 2 - 350, self.mid_h /2 + 590
    #     self.cursor_rect.midtop = (self.stage1x + self.offset, self.stage1y)



    # def highlighted(self,a):
    #     if a == self.state:
    #         return 30
    #     return 25

    # def display_menu(self):                                                           
    #     dis = pygame.display.set_mode ((960 , 540))
    #     bg = pygame.image.load('./img/wallpapper01.png').convert_alpha()
    #     self.run_display = True
    #     while self.run_display:
    #         self.game.check_events()
    #         self.check_input()
    #         pygame.display.update()
    #         self.game.display.blit(bg, (0,0))
    #         self.game.draw_text('Stages', 40 , self.game.DISPLAY_W / 3, self.game.DISPLAY_H /2 - 300)
    #         self.game.draw_text('Select a stage:', 40 , self.game.DISPLAY_W / 3 , self.game.DISPLAY_H /2 - 250)
    #         self.game.draw_text("Stage 1", self.highlighted("Stage 1"), self.stage1x, self.stage1y)
    #         self.game.draw_text("Stage 2", self.highlighted("Stage 2"), self.stage2x, self.stage2y)
    #         self.game.draw_text("Stage 3", self.highlighted("Stage 3"), self.stage3x, self.stage3y)
    #         self.game.draw_text("Stage 4", self.highlighted("Stage 4"), self.stage4x, self.stage4y)
    #         self.game.draw_text("Stage 5", self.highlighted("Stage 5"), self.stage5x, self.stage5y)
    #         self.game.draw_text("Stage 6", self.highlighted("Stage 6"), self.stage6x, self.stage6y)
    #         self.game.draw_text("Stage 7", self.highlighted("Stage 7"), self.stage7x, self.stage7y)
    #         self.game.draw_text("Stage 8", self.highlighted("Stage 8"), self.stage8x, self.stage8y)
    #         self.game.draw_text("Stage 9", self.highlighted("Stage 9"), self.stage9x, self.stage9y)
    #         self.game.draw_text("Stage 10", self.highlighted("Stage 10"), self.stage10x, self.stage10y)
    #         self.game.draw_text("Back", self.highlighted("Back"), self.backx, self.backy)
    #         self.game.draw_text("version 0.1", 8, self.versionx, self.versiony)
    #         self.blit_screen()

    # def move_cursor(self):
    #     if self.game.BACK_KEY:
    #         #MUSIC
    #         back_button = mixer.Sound('clips/back_button.wav')
    #         back_button.play()
    #         #backbutton.play()
    #         self.game.curr_menu = self.game.main_menu
    #         self.run_display = False
    #     if self.game.DOWN_KEY:
    #         move_arrow = mixer.Sound('clips/down_up_arrow.wav')
    #         move_arrow.play()
    #         if self.state == 'Stage 1':
    #             self.state = 'Stage 2'
    #         elif self.state == 'Stage 2':
    #             self.state = 'Stage 3'
    #         elif self.state == 'Stage 3':
    #             self.state = 'Stage 4'
    #         elif self.state == 'Stage 4':
    #             self.state = 'Stage 5'
    #         elif self.state == 'Stage 5':
    #             self.state = 'Stage 6'
    #         elif self.state == 'Stage 6':
    #             self.state = 'Stage 7'
    #         elif self.state == 'Stage 7':
    #             self.state = 'Stage 8'
    #         elif self.state == 'Stage 8':
    #             self.state = 'Stage 9'
    #         elif self.state == 'Stage 9':
    #             self.state = 'Stage 10'
    #         elif self.state == 'Stage 10':
    #             self.state = 'Back'
    #         elif self.state == 'Back':
    #             self.state = 'Stage 1'
    #     elif self.game.UP_KEY:
    #         move_arrow = mixer.Sound('clips/down_up_arrow.wav')
    #         move_arrow.play()
    #         if self.state == 'Stage 1':
    #             self.state = 'Back'
    #         elif self.state == 'Back':
    #             self.state = 'Stage 10'
    #         elif self.state == 'Stage 10':
    #             self.state = 'Stage 9'
    #         elif self.state == 'Stage 9':
    #             self.state = 'Stage 8'
    #         elif self.state == 'Stage 8':
    #             self.state = 'Stage 7'
    #         elif self.state == 'Stage 7':
    #             self.state = 'Stage 6'
    #         elif self.state == 'Stage 6':
    #             self.state = 'Stage 5'
    #         elif self.state == 'Stage 5':
    #             self.state = 'Stage 4'
    #         elif self.state == 'Stage 4':
    #             self.state = 'Stage 3'
    #         elif self.state == 'Stage 3':
    #             self.state = 'Stage 2'
    #         elif self.state == 'Stage 2':
    #             self.state = 'Stage 1'

    # def check_input(self):
    #     self.move_cursor()
    #     if self.game.START_KEY:
    #         enter_button = mixer.Sound('clips/enter_button.wav')
    #         enter_button.play()
    #         if self.state == 'Stage1':
    #              level = 1
    #              from classes.maingame import maingame
    #         elif self.state == 'Stage2':
    #             self.game.curr_menu = self.game.options
    #         elif self.state == 'Stage3':
    #             self.game.curr_menu = self.game.credits
    #         elif self.state == 'Stage4':
    #             self.game.curr_menu = self.game.shop
    #         elif self.state == 'Back':
    #             back_button = mixer.Sound('clips/back_button.wav')
    #             back_button.play()
    #             #backbutton.play()
    #             self.game.curr_menu = self.game.main_menu
    #             self.run_display = False
    #         self.run_display = False


class QuitMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'No'
        self.yesx, self.yesy = self.mid_w - 40, self.mid_h + 20
        self.nox, self.noy = self.mid_w + 40, self.mid_h + 20
        self.cursor_rect.midtop = (self.nox + self.offset, self.noy)
    

    def highlighted(self,a):
        if a == self.state:
            return 30
        return 20

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            background_credits = pygame.image.load('./img/wallpapper01.png').convert_alpha()
            self.game.display.blit(background_credits, (0,0))
            self.game.draw_text('Are you sure that you want to quit?', 40, self.game.DISPLAY_W / 2-280, self.game.DISPLAY_H / 2 - 280 )
            self.game.draw_text("Yes", self.highlighted("Yes"), self.yesx , self.yesy / 2)
            self.game.draw_text("No", self.highlighted("No"), self.nox, self.noy / 2 )
            self.blit_screen()
    
    def check_input(self):
        if self.game.BACK_KEY:
            back_button = mixer.Sound('clips/back_button.wav')
            back_button.play()
            #backbutton.play()
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
        elif self.game.RIGHT_KEY:
            move_arrow = mixer.Sound('down_up_arrow.wav')
            move_arrow.play()
            if self.state == 'Yes':
                self.state = 'No'
            elif self.state == 'No':
                self.state = 'Yes'
        elif self.game.LEFT_KEY:
            move_arrow = mixer.Sound('clips/down_up_arrow.wav')
            move_arrow.play()
            if self.state == 'Yes':
                self.state = 'No'
            elif self.state == 'No':
                self.state = 'Yes'
        elif self.game.START_KEY:
            if self.state == 'No':
                # pygame.mixer.music.play(-1, 0.0, 5000)
                # pygame.mixer.music.play(0)
                self.game.curr_menu = self.game.main_menu
            elif self.state =='Yes':
                pygame.quit()
                sys.exit()
            self.run_display = False



class ShopMenu(Menu):
   def __init__(self, game):
        Menu.__init__(self, game)

   def display_menu(self):
        background_shop = pygame.image.load('./img/wallpapper02.png').convert_alpha()
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            if self.game.START_KEY or self.game.BACK_KEY:
                back_button = mixer.Sound('clips/back_button.wav')
                back_button.play()
                #backbutton.play()
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
            self.game.display.blit(background_shop, (0,0))
            self.blit_screen()

class ProfileMenu(Menu):
   def __init__(self, game):
        Menu.__init__(self, game)

   def display_menu(self):
        background_shop = pygame.image.load('./img/wallpapper02.png').convert_alpha()
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            if self.game.START_KEY or self.game.BACK_KEY:
                back_button = mixer.Sound('clips/back_button.wav')
                back_button.play()
                #backbutton.play()
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
            self.game.display.blit(background_shop, (0,0))
            self.blit_screen()


        