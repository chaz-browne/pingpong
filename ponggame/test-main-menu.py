import pygame, sys
from button import Button

pygame.init()

SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Chaz's Playground")

BG = pygame.image.load("assets/Background.png")

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)

level = 5
#all of the following code is for my own ping pong game.

def play():
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()


        WIDTH, HEIGHT = 1280, 720
        WIN = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("PONG")

        FPS = 60

        PURPLE = (102, 51, 153)
        GRAY = (102, 51, 153)
        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)

        PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
        BALL_RADIUS = 7

        SCORE_FONT = pygame.font.SysFont("Times New Roman", 50)
        WINNING_SCORE = 10


        class Paddle:
            COLOR = WHITE
            VEL = 4

            def __init__(self, x, y, width, height):
                self.x = self.original_x = x
                self.y = self.original_y = y
                self.width = width
                self.height = height

            def draw(self, win):
                pygame.draw.rect(
                    win, self.COLOR, (self.x, self.y, self.width, self.height))

            def move(self, up=True):
                if up:
                    self.y -= self.VEL
                else:
                    self.y += self.VEL

            def reset(self):
                self.x = self.original_x
                self.y = self.original_y


        class Ball:
            MAX_VEL = level
            COLOR = WHITE

            def __init__(self, x, y, radius):
                self.x = self.original_x = x
                self.y = self.original_y = y
                self.radius = radius
                self.x_vel = self.MAX_VEL
                self.y_vel = 0

            def draw(self, win):
                pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.radius)

            def move(self):
                self.x += self.x_vel
                self.y += self.y_vel

            def reset(self):
                self.x = self.original_x
                self.y = self.original_y
                self.y_vel = 0
                self.x_vel *= -1


        def draw(win, paddles, ball, left_score, right_score):
            win.fill(PURPLE)

            left_score_text = SCORE_FONT.render(f"{left_score}", 1, WHITE)
            right_score_text = SCORE_FONT.render(f"{right_score}", 1, WHITE)
            win.blit(left_score_text, (WIDTH//4 - left_score_text.get_width()//2, 20))
            win.blit(right_score_text, (WIDTH * (3/4) -
                                        right_score_text.get_width()//2, 20))

            for paddle in paddles:
                paddle.draw(win)

            for i in range(10, HEIGHT, HEIGHT//20):
                if i % 2 == 1:
                    continue
                pygame.draw.rect(win, WHITE, (WIDTH//2 - 5, i, 10, HEIGHT//20))

            ball.draw(win)
            pygame.display.update()


        def handle_collision(ball, left_paddle, right_paddle):
            if ball.y + ball.radius >= HEIGHT:
                ball.y_vel *= -1
            elif ball.y - ball.radius <= 0:
                ball.y_vel *= -1

            if ball.x_vel < 0:
                if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height:
                    if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                        ball.x_vel *= -1

                        middle_y = left_paddle.y + left_paddle.height / 2
                        difference_in_y = middle_y - ball.y
                        reduction_factor = (left_paddle.height / 2) / ball.MAX_VEL
                        y_vel = difference_in_y / reduction_factor
                        ball.y_vel = -1 * y_vel

            else:
                if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height:
                    if ball.x + ball.radius >= right_paddle.x:
                        ball.x_vel *= -1

                        middle_y = right_paddle.y + right_paddle.height / 2
                        difference_in_y = middle_y - ball.y
                        reduction_factor = (right_paddle.height / 2) / ball.MAX_VEL
                        y_vel = difference_in_y / reduction_factor
                        ball.y_vel = -1 * y_vel


        def handle_paddle_movement(keys, left_paddle, right_paddle):
            if keys[pygame.K_w] and left_paddle.y - left_paddle.VEL >= 0:
                left_paddle.move(up=True)
            if keys[pygame.K_s] and left_paddle.y + left_paddle.VEL + left_paddle.height <= HEIGHT:
                left_paddle.move(up=False)

            if keys[pygame.K_UP] and right_paddle.y - right_paddle.VEL >= 0:
                right_paddle.move(up=True)
            if keys[pygame.K_DOWN] and right_paddle.y + right_paddle.VEL + right_paddle.height <= HEIGHT:
                right_paddle.move(up=False)


        def main():
            run = True
            clock = pygame.time.Clock()

            left_paddle = Paddle(10, HEIGHT//2 - PADDLE_HEIGHT //
                                2, PADDLE_WIDTH, PADDLE_HEIGHT)
            right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT //
                                2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
            ball = Ball(WIDTH // 2, HEIGHT // 2, BALL_RADIUS)

            left_score = 0
            right_score = 0

            while run:
                clock.tick(FPS)
                draw(WIN, [left_paddle, right_paddle], ball, left_score, right_score)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                        break

                keys = pygame.key.get_pressed()
                handle_paddle_movement(keys, left_paddle, right_paddle)

                ball.move()
                handle_collision(ball, left_paddle, right_paddle)

                if ball.x < 0:
                    right_score += 1
                    ball.reset()
                elif ball.x > WIDTH:
                    left_score += 1
                    ball.reset()

                won = False
                if left_score >= WINNING_SCORE:
                    won = True
                    win_text = "Left Player Won!"
                elif right_score >= WINNING_SCORE:
                    won = True
                    win_text = "Right Player Won!"

                if won:
                    text = SCORE_FONT.render(win_text, 1, WHITE)
                    WIN.blit(text, (WIDTH//2 - text.get_width() //
                                    2, HEIGHT//2 - text.get_height()//2))
                    pygame.display.update()
                    pygame.time.delay(5000)
                    ball.reset()
                    left_paddle.reset()
                    right_paddle.reset()
                    left_score = 0
                    right_score = 0
            pygame.quit()


        if __name__ == '__main__':
            main()

        PLAY_BACK = Button(image=None, pos=(640, 460), 
                            text_input="BACK", font=get_font(75), base_color="White", hovering_color="Green")

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()

        pygame.display.update()
    
def options():

    global level

    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("Black")

        #this is just text to the screen.
        DIFF_TEXT = get_font(25).render("what kind of difficulty would you like?", True, "White")
        DIFF_RECT = DIFF_TEXT.get_rect(center=(640, 80))
        SCREEN.blit(DIFF_TEXT, DIFF_RECT)

        #this handles button logic,
        #allowing me to make new buttons that can be clicked. 
        LEVEL_1 = Button(image=None, pos=(640, 200), 
                            text_input="LEVEL 1", font=get_font(15), base_color="White", hovering_color="RED")

        LEVEL_1.changeColor(OPTIONS_MOUSE_POS)
        LEVEL_1.update(SCREEN)

        LEVEL_2 = Button(image=None, pos=(640, 400), 
                            text_input="LEVEL 2", font=get_font(15), base_color="White", hovering_color="RED")

        LEVEL_2.changeColor(OPTIONS_MOUSE_POS)
        LEVEL_2.update(SCREEN)


        LEVEL_3 = Button(image=None, pos=(640, 600), 
                            text_input="LEVEL 3", font=get_font(15), base_color="White", hovering_color="RED")

        LEVEL_3.changeColor(OPTIONS_MOUSE_POS)
        LEVEL_3.update(SCREEN)
    
        OPTIONS_BACK = Button(image=None, pos=(640, 460), 
                            text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if LEVEL_1.checkForInput(OPTIONS_MOUSE_POS):
                    level = 5
                    main_menu()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if LEVEL_2.checkForInput(OPTIONS_MOUSE_POS):
                    level = 10
                    main_menu()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if LEVEL_3.checkForInput(OPTIONS_MOUSE_POS):
                    level = 15
                    main_menu()

        pygame.display.update()

def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("PING PONG", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 250), 
                            text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 400), 
                            text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 550), 
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()