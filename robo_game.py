# In this game the player needs to collect a required amount of coins
# while avoiding monsters to unlock the door, passing through which
# results in winning the game. The player has 3 lives, losing all results in losing.
 
# Since I use heavily classes in rendering the objects on screen, the game is broken into several
# classes and functions (main one being called "play_game"), rather than utilizing one main 
# class with subclasses (doing so resulted in bugs). Additionally, throughout the game, I use
# pixel sizes of images instead of, for example, "650 - image.get_width()", as it makes it easier for me to 
# orient myself in the code. In case anyone is wondering where I came up with the numbers :)
 
# robot: w: 50 h: 86
# coin: w: 40 h: 40
# door: w: 50 h: 70
# monster: w: 50 h: 70
 
import pygame
import random
 
# monster classes, along with movement functions
class AMonster:
    def __init__(self, x: int, y: int, right_goal: int, down_goal: int):
        self.x = x
        self.y = y
        self.right = right_goal
        self.down = down_goal 
        self.left = x
        self.top = y
        self.direction = 'right'
 
    def clockwiseMotion(self):
        if self.direction == 'right':
            self.x += 1
            if self.x == self.right:
                self.direction = 'down'
        if self.direction == 'down': 
            self.y += 1
            if self.y == self.down:
                self.direction = 'left'
        if self.direction == 'left':
            self.x -= 1
            if self.x == self.left:
                self.direction = 'up'
        if self.direction == 'up':
            self.y -= 1
            if self.y == self.top:
                self.direction = 'right'
 
class ZMonster:
    def __init__(self, x: int, y: int, right_goal: int, down_goal: int):
        self.x = x
        self.y = y
        self.right = right_goal
        self.down = down_goal 
        self.left = x
        self.top = y
        self.direction = 'down'
 
    def counterclockwiseMotion(self):
        if self.direction == 'down': 
            self.y += 1
            if self.y == self.down:
                self.direction = 'right'
        if self.direction == 'right':
            self.x += 1
            if self.x == self.right:
                self.direction = 'up'
        if self.direction == 'up':
            self.y -= 1
            if self.y == self.top:
                self.direction = 'left'
        if self.direction == 'left': 
            self.x -= 1
            if self.x == self.left:
                self.direction = 'down'
 
# Creating the player, along with the necessary functions:
# movement, checking for collisions, collecting coins, and entering through doors
class Player:
    def __init__(self):
        self.image = robo
        self.x = 0
        self.y = 275-robo.get_height()/2
        self.left = False
        self.right = False
        self.down = False
        self.up = False
 
    def move(self):
        if self.right:
            if self.x <= 650:
                self.x += 2
        if self.left:
            if self.x >= 0:
                self.x -= 2
        if self.up:
            if self.y >= 50:
                self.y -= 2
        if self.down:
            if self.y <= 464:
                self.y += 2
 
    def got_hit(self, clockwise_monsters: list, counterclockwise_moonsters: list):
        hits = []
        # measurements cut in half so the hits are less sensitive, otherwise player would run out of lives 
        # immediately after bumbing a monster just once
        for i in range(len(clockwise_monsters)):
            if clockwise_monsters[i].x + 25 >= self.x and clockwise_monsters[i].x <= self.x + 25:
                if clockwise_monsters[i].y + 35 >= self.y and clockwise_monsters[i].y <= self.y + 43:
                    hits.append(i)
        for i in range(len(counterclockwise_monsters)):
            if counterclockwise_monsters[i].x + 25 >= self.x and counterclockwise_monsters[i].x <= self.x + 25:
                if counterclockwise_monsters[i].y + 35 >= self.y and counterclockwise_monsters[i].y <= self.y + 43:
                    hits.append(i)
        if len(hits) > 0:
            return hits
        return -1
    
    def got_coin(self, coin: object): 
        gathered_coins = []
        # measurements cut in half so the game isn't too easy :)
        if coin.x + 20 >= self.x and coin.x <= self.x + 25:
            if coin.y + 20 >= self.y and coin.y <= self.y + 43:
                gathered_coins.append(coin)
        if len(gathered_coins) > 0:
            return gathered_coins
        return -1
    
    def passed_door(self, door: object):
        check = -1
        if door.x + 25 >= self.x and door.x <= self.x + 25:
            if door.y + 35 >= self.y and door.y <= self.y + 43:
                check = 1
        return check
 
 
class Coins:
    def __init__(self, image: str, x: int, y: int):
        self.image = image
        self.x = x
        self.y = y        
 
class Door:
    def __init__(self, image: str, x: int, y: int):
        self.image = image
        self.x = x
        self.y = y
 
 
# creating monsters - having one class with two functions for movements (clockwise and counterclockwise)
# resulted in bugs, hence two lists for each type:
def get_amonsters():
    clockwise_monsters = []
    monster1 = AMonster(0, 50, 300, 165)
    clockwise_monsters.append(monster1)
    monster2 = AMonster(0, 320,300, 480)
    clockwise_monsters.append(monster2)
    monster3 = AMonster(250, 140, 600, 410)
    clockwise_monsters.append(monster3)
    return clockwise_monsters
 
def get_zmonsters():
    counterclockwise_monsters = []
    monster4 = ZMonster(350, 50, 600, 250)
    counterclockwise_monsters.append(monster4)
    monster5 = ZMonster(350, 320, 650, 480)
    counterclockwise_monsters.append(monster5)
    monster6 = ZMonster(50, 140, 400, 410)
    counterclockwise_monsters.append(monster6)
    return counterclockwise_monsters
 
def get_coins():
    # Creating coins, random positions in four different quadrants
    # (one quadrant == roughly where one of the corner monsters patrols), 2 coins per quadrant.
    # This is to make sure the player needs to actually cross the field (with fully random coordinates they
    # often cluster), in addition to ensuring that the last coin collected isn't in the same place as the door
    # - again, so the player has to cross the field again to get to it
    coins = []
    coin1 = Coins(coin, random.randint(50, 300), random.randint(150, 200))
    coins.append(coin1)
    coin2 = Coins(coin, random.randint(50, 300), random.randint(150, 200))
    coins.append(coin2)
    coin3 = Coins(coin, random.randint(50, 500), random.randint(325, 500))
    coins.append(coin3)
    coin4 = Coins(coin, random.randint(50, 500), random.randint(325, 500))
    coins.append(coin4)
    coin5 = Coins(coin, random.randint(400, 650), random.randint(150, 200))
    coins.append(coin5)
    coin6 = Coins(coin, random.randint(400, 650), random.randint(150, 200))
    coins.append(coin6)
    coin7 = Coins(coin, random.randint(400, 650), random.randint(325, 500))
    coins.append(coin7)
    coin8 = Coins(coin, random.randint(400, 650), random.randint(325, 500))
    coins.append(coin8)
    return coins
 
 
# the variables here need to be global (otherwise there be bugs aplenty). I also opted for loading
# the images here, since separate function was just as long, and refering to them by name
# throughout the code is clearer than using index numbers (I do not have a map, so a shorthand
# isn't necesssary in this case).
pygame.init()
window = pygame.display.set_mode((700, 550))
pygame.display.set_caption('Robot vs Monsters (MOOC fall 2020 submission)')
font = pygame.font.SysFont("Arial", 24)
robo = pygame.image.load('robo.png')
gate = pygame.image.load('ovi.png')
orc = pygame.image.load('hirvio.png')
coin = pygame.image.load('kolikko.png')
clockwise_monsters = get_amonsters()
counterclockwise_monsters = get_zmonsters()
player = Player()
doors = Door(gate, 350-gate.get_width()/2, 290-gate.get_height()/2)
time = pygame.time.Clock()
    
 
# checking for key bound events
def check_events():
    for game_event in pygame.event.get():
        if game_event.type == pygame.KEYDOWN:
            if game_event.key == pygame.K_LEFT:
                player.left = True
            if game_event.key == pygame.K_RIGHT:
                player.right = True
 
        if game_event.type == pygame.KEYUP:
            if game_event.key == pygame.K_LEFT:
                player.left = False
            if game_event.key == pygame.K_RIGHT:
                player.right = False
            
        if game_event.type == pygame.KEYDOWN:
            if game_event.key == pygame.K_UP:
                player.up = True
            if game_event.key == pygame.K_DOWN:
                player.down = True
 
        if game_event.type == pygame.KEYUP:
            if game_event.key == pygame.K_UP:
                player.up = False
            if game_event.key == pygame.K_DOWN:
                player.down = False
 
        if game_event.type == pygame.KEYDOWN:
            # I know that F2 is customary, but on my laptop I need to press fn key along with F keys,
            # and it didn't work very well here, hence the n-key binding
            if game_event.key == pygame.K_n:
                play_game()
            if game_event.key == pygame.K_ESCAPE:
                exit()
 
        if game_event.type == pygame.QUIT:
            exit()
 
       
# game over screen:
def game_over():
    window.fill((40, 40, 40))
    pygame.draw.line(window, (255, 255, 255), (0, 48), (700, 48), 2)
    game_over_text = font.render('GAME OVER!', True, (255, 0, 0))
    new_game_text = font.render('NEW GAME: Press N', True, (255, 255, 255)) 
    quit_game_text = font.render('QUIT: Press ESC', True, (255, 255, 255))
    window.blit(game_over_text, (250, 10))
    window.blit(new_game_text, (200, 200))
    window.blit(quit_game_text, (200, 350))  
    pygame.display.flip()
 
 
# winning screen
def game_won():
    window.fill((40, 40, 40))
    pygame.draw.line(window, (255, 255, 255), (0, 48), (700, 48), 2)
    won_text = font.render("YOU WON!", True, (255, 255, 0))
    new_game_text = font.render('NEW GAME: N', True, (255, 255, 255)) 
    quit_game_text = font.render('QUIT: Press ESC', True, (255, 255, 255))
    window.blit(won_text, (250, 10))
    window.blit(new_game_text, (200, 200))
    window.blit(quit_game_text, (200, 350))
    pygame.display.flip()
 
 
#unlocking doors:
def open_sezame():
    door_text = font.render("Door Unlocked!", True, (255, 255, 255))
    window.blit(door_text, (250, 10))
    window.blit(doors.image, (doors.x,doors.y))
 
 
# the main game code:
def play_game():
    coins = get_coins()
    lives_count = 3
    while lives_count > 0:
        
        door_state = 'locked'
        check_events()
 
        # these texts need to be within the main loop, otherwise they would be static
        coins_text = font.render("Coins Left: " + str(len(coins)), True, (255, 255, 255))
        lives_text = font.render("Lives: " + str(lives_count), True, (255, 255, 255))
 
        # loading the main screen and the player
        window.fill((40, 40, 40))
        window.blit(lives_text, (10, 10))
        pygame.draw.line(window, (255, 255, 255), (0, 48), (700, 48), 2)
        window.blit(player.image, (player.x, player.y))
        player.move()
 
        # rendering and counting collected coins:
        for coin in coins:
            window.blit(coin.image, (coin.x, coin.y)) 
            score = player.got_coin(coin)
            # if a player gets a coin, the coin is removed
            if score != -1:
                coins.remove(coin)   
        
        # score (coins collected) conditions:
        if len(coins) > 0:
            window.blit(coins_text, (250, 10))
        # if the player collects all the coins, the door is unlocked:
        elif len(coins) == 0:
            open_sezame() #loads the doors
            door_state = 'open'     
        
        # rendering and animating monsters:
        for monster in clockwise_monsters:
            window.blit(orc, (monster.x, monster.y))
            monster.clockwiseMotion()
        for monster in counterclockwise_monsters:
            window.blit(orc, (monster.x, monster.y))
            monster.counterclockwiseMotion()
 
        # if the player touches a monster, player loses a life and returns to the starting position:
        hits = player.got_hit(clockwise_monsters, counterclockwise_monsters)
        if hits != -1:
            player.x = 0
            player.y = 275-robo.get_height()/2
            lives_count -= 1    
 
        # once the door is opened, the game checks whether or not the player passed through:                    
        if door_state == 'open':
            check = player.passed_door(doors)
            if check == 1:
                game_won()  # loads gaming screen
                time.tick(0)    # stops the player from moving and accidentally continuing 
                                # the game (by moving away from the passed_door position)
        
        pygame.display.flip()
        time.tick(60)
 
    # if player loses all lives, the game is over:
    while lives_count == 0:    
        check_events()      # included so as to prevent the game crashing once the game over screen loads
        game_over()         # loads game over screen
 
 
if __name__ == "__main__":
    play_game()
