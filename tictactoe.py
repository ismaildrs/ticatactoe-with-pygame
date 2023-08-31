import pygame
import time

pygame.init()

#starting the screen
screen_width = 600
bloc_width = screen_width/3
bloc_center = screen_width/6


title_size = 80
smalltext_size = 30

grid_color = (155,215,213)
background_color = (43,55,75)
image_scale = 0.3
button_scale = 0.8
button2_scale = 0.4
button3_scale = 0.37

screen = pygame.display.set_mode((screen_width, screen_width))

class Game():
    def __init__(self):
        self.players = ['X', 'O']
        self.winner_char = None

        self.title_text = pygame.font.Font('font/Micro.ttf', title_size)
        self.small_text = pygame.font.Font('font/Micro.ttf', smalltext_size)

        self.game_menu = True
        self.game_active = False
        self.game_ended = False
        self.game_settings = False

        self.player_x_score = 0
        self.player_o_score = 0
        self.player_tomove = 0

        self.player_x_img = pygame.image.load('graphics/cancel.png').convert_alpha()
        self.player_o_img = pygame.image.load('graphics/o.png').convert_alpha()

        self.start_button = pygame.image.load('graphics/start_btn.png').convert_alpha()
        self.exit_button = pygame.image.load('graphics/exit_btn.png').convert_alpha()

        self.back_surf = pygame.transform.rotozoom(pygame.image.load('graphics/Back.png').convert_alpha(), False, button3_scale)
        self.restart_surf = pygame.transform.rotozoom(pygame.image.load('graphics/Restart.png').convert_alpha(), False, button2_scale)
        #self.settings_surf = pygame.transform.rotozoom(pygame.image.load('graphics/Settings.png').convert_alpha(), False, button2_scale)
        self.back_rect = self.back_surf.get_rect(center = (screen_width//3, screen_width//1.5))
        self.restart_rect = self.restart_surf.get_rect(center = (screen_width//1.5, screen_width//1.5))
        #self.settings_rect = self.settings_surf.get_rect(center = (screen_width//1.5, screen_width//1.5))

        str_width = self.start_button.get_width()
        str_height = self.start_button.get_height()
        ex_width = self.exit_button.get_width()
        ex_height = self.exit_button.get_height()
        self.start_button=pygame.transform.scale(self.start_button, (str_width*button_scale, str_height*button_scale))
        self.exit_button=pygame.transform.scale(self.exit_button,(ex_width*button_scale, ex_height*button_scale)) 
        self.start_rect = self.start_button.get_rect(midtop = (screen_width/2, screen_width/1.9))
        self.exit_rect = self.exit_button.get_rect(midtop  = (screen_width/2, screen_width/1.9 + str_height + 20))
        self.player_x_img = pygame.transform.scale(self.player_x_img, (screen_width*image_scale, screen_width*image_scale))
        self.player_o_img = pygame.transform.scale(self.player_o_img, (screen_width*image_scale, screen_width*image_scale))
        self.board = [['', '', ''], ['', '', ''], ['', '', '']]
        self.numberofplays = 0
        self.color_line = (248,131,121)
        self.grid_size = screen_width//100
    
    def choose_menu(self, game_active, game_menu, game_ended):
        self.game_active =game_active
        self.game_menu = game_menu
        self.game_ended = game_ended

    def show_menu(self):
        tictactoe_surf = self.title_text.render('Tic Tac Toe', False, 'White')
        tictactoe_rect = tictactoe_surf.get_rect(center = (screen_width//2, screen_width//3))
        tictactoe_surf_bg = self.title_text.render('Tic Tac Toe', False, 'Black')
        tictactoe_rect_bg = tictactoe_surf.get_rect(center = (screen_width//2, screen_width//3+10))

        madeby_surf = self.small_text.render('made by ISMAIL DRISSI', False, 'White')
        madeby_rect = madeby_surf.get_rect(center = (screen_width//2, tictactoe_rect.bottom + smalltext_size//2))
        madeby_surf_bg = self.small_text.render('made by ISMAIL DRISSI', False, 'Black')
        madeby_rect_bg = madeby_surf.get_rect(center = (screen_width//2, tictactoe_rect.bottom + smalltext_size//2 +5))

        screen.blits(((tictactoe_surf_bg, tictactoe_rect_bg), (tictactoe_surf, tictactoe_rect)))
        screen.blits(((self.start_button, self.start_rect), (self.exit_button, self.exit_rect)))
        screen.blits(((madeby_surf_bg, madeby_rect_bg), (madeby_surf, madeby_rect)))

    def show_board(self):
        pygame.display.set_caption(f"Player '{self.players[self.player_tomove]}' turn")
        for i in range(1,3):
            pygame.draw.line(screen, grid_color, (i * screen_width //3, 0), (i * screen_width /3, screen_width), self.grid_size)
            pygame.draw.line(screen, grid_color, (0, i * screen_width //3), (screen_width, i * screen_width /3), self.grid_size)
        for i in range(0,3):
            for j in range(0, 3):
                if self.board[i][j] == 'X':
                    self.player_x_rect = self.player_x_img.get_rect(center= (j * screen_width/3 + screen_width/6, i * screen_width/3 + screen_width/6))
                    screen.blit(self.player_x_img, self.player_x_rect)
                elif self.board[i][j] == 'O':
                    self.player_o_rect = self.player_o_img.get_rect(center = (j * screen_width/3 + screen_width/6, i * screen_width/3 + screen_width/6))
                    screen.blit(self.player_o_img, self.player_o_rect)

    def show_game_ended(self):
        if self.winner_char is None:
            pygame.display.set_caption('Draw!')
            draw_surf = self.title_text.render('DRAW!', False, 'White')
            draw_rect = draw_surf.get_rect(center = (screen_width//2, screen_width//4))
            draw_surf_bg = self.title_text.render('DRAW!', False, 'Black')
            draw_rect_bg = draw_surf_bg.get_rect(center = (screen_width//2, screen_width//4 + 10))
            screen.blits(((draw_surf_bg, draw_rect_bg), (draw_surf, draw_rect)))
        else:
            pygame.display.set_caption(f"Player '{self.winner_char}' is the winner")
            winner_surf = self.title_text.render('WINNER!', False, 'White')
            winner_rect = winner_surf.get_rect(center = (screen_width//2, screen_width//4))
            winner_surf_bg = self.title_text.render('WINNER!', False, 'Black')
            winner_rect_bg = winner_surf_bg.get_rect(center = (screen_width//2, screen_width//4 + 10))

            winner_surf = self.title_text.render('WINNER!', False, 'White')
            winner_rect = winner_surf.get_rect(center = (screen_width//2, screen_width//4))
            winner_surf_bg = self.title_text.render('WINNER!', False, 'Black')
            winner_rect_bg = winner_surf_bg.get_rect(center = (screen_width//2, screen_width//4 + 10))

            player_surf = self.small_text.render(f"Player '{self.winner_char}' is the winner", False, 'White')
            player_rect = winner_surf.get_rect(midtop = (screen_width//2, screen_width//4 + title_size))
            player_surf_bg = self.small_text.render(f"Player '{self.winner_char}' is the Winner", False, 'Black')
            player_rect_bg = winner_surf_bg.get_rect(midtop = (screen_width//2, screen_width//4 + title_size+5))

            screen.blits(((winner_surf_bg, winner_rect_bg), (winner_surf, winner_rect), (player_surf_bg, player_rect_bg), (player_surf, player_rect)))

        screen.blits(((self.back_surf, self.back_rect), (self.restart_surf, self.restart_rect)))
        
    def player_input(self):
        global clicked, run
        mouse_pressed = pygame.mouse.get_pressed()
        if mouse_pressed[0] == True and clicked == False :
            clicked = True
        if mouse_pressed[0] == False and clicked == True:
            clicked = False
            mouse_pos = pygame.mouse.get_pos()
            if self.game_active == True:
                i_converted = ((mouse_pos[1])//(screen_width // 3))
                j_converted = ((mouse_pos[0])//(screen_width // 3))
                if self.board[i_converted][j_converted] == '':
                    self.board[i_converted][j_converted] = self.players[self.player_tomove]
                    self.numberofplays += 1
                    if self.player_tomove == 0: self.player_tomove = 1
                    else: self.player_tomove = 0
            else:
                if self.game_menu == True:
                    if self.start_rect.collidepoint(mouse_pos):
                        time.sleep(0.2)
                        self.game_menu = False
                        self.game_active = True
                    elif self.exit_rect.collidepoint(mouse_pos):
                        run = False 
                if self.game_ended == True:
                    if self.restart_rect.collidepoint(mouse_pos):
                        time.sleep(0.2)
                        self.choose_menu(True, False, False)
                    elif self.back_rect.collidepoint(mouse_pos):
                        self.choose_menu(False, True, False)
                        
                    

    def check_end_game(self):
        for i in range(0,3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != '':
                return False, ((0, i), (2,i)), self.board[i][0]
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != '':
                return False, ((i, 0), (i, 2)), self.board[0][i]
        if self.board[0][0] == self.board[1][1] == self.board[2][2] !='':
                return False, ((0, 0), (2,2)), self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0]!='':
                return False, ((0, 2), (2, 0)), self.board[0][2]
        if self.numberofplays ==9:
            return False, None, None
        return  True, None, None

                
    def show_ligne(self):
        ligne_width = screen_width//80
        _,  winning_line, _ = self.check_end_game()
        if winning_line :
            pygame.draw.line(screen, self.color_line, 
            (winning_line[0][0]*bloc_width+bloc_center,winning_line[0][1]*bloc_width+bloc_center), 
            (winning_line[1][0]*bloc_width+bloc_center, winning_line[1][1]*bloc_width+bloc_center), ligne_width)
    
    def initialize(self):
        self.board = [['', '', ''], ['', '', ''], ['', '', '']]
        self.numberofplays = 0

    def update(self):
        self.player_input()
        if self.game_active == True:
            self.show_board()
            self.show_ligne()
            self.game_active,_, self.winner_char =  self.check_end_game()
            if self.game_active == False:
                self.choose_menu(False, False, True)
                if self.winner_char == 'X': self.player_x_score += 1
                elif self.winner_char == 'O': self.player_o_score += 1
                self.initialize()
        else:
            if self.game_menu == True:
                pygame.display.set_caption('TicTacToe!')
                self.show_menu()
            if self.game_ended == True:
                time.sleep(1)
                self.show_game_ended()
    

#defining game instance
game_setup = Game()
     

run = True
clicked = False

#while loop
while run:
    #event handler
    screen.fill(background_color)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
                run = False

    game_setup.update()

    pygame.display.update()

pygame.quit()