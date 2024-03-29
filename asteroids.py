#!/usr/bin/python3

# Importing necessary modules
import pygame
from random import randrange, random,randint

from math import pi, sin, cos, sqrt, acos, radians, degrees, atan
from time import time
from game_objects import spaceShip, pewPew, asteroid, life, powerUp

#from ai import SpaceGameAI
# Defining the class for the Asteroids game
class asteroidsGame:

    # The constructor function, which is called when the object is created
    def __init__(self, options):


        #  Initializing pygame
        pygame.init()

        screen_info = pygame.display.Info()
        # Setting up the default values
        self.defaults = {
        "width":screen_info.current_w,
        "height":screen_info.current_h,
        "title":"Asteroids",
        "background":(0,0,0),
        "labelColour":(255,255,255),
        "shipColour":(255,200,0),
        "pewColour":(0,0,255),
        "font":"arial",
        "pewRange":300,
        "maxPews":10,
        "pewTime":100,
        "intialLives":3,
        "highScoreFile":'high_scores.txt',
        "AI_PLAY" : False
        }
        
        # Setting up the game over variable
        self.game_over = False

        # Combining the default values and the given options
        self.options = {**self.defaults, **options}

        

        # Setting up the screen size
        self.width = self.options['width']
        self.height = self.options['height']

        # Creating the screen
        size = [self.width, self.height]
        self.screen = pygame.display.set_mode(size, pygame.FULLSCREEN)

        # Defining some constants
        self.TWOPI = pi * 2

        # Setting up the lives and score
        self.lives = self.options["intialLives"]
        self.score = 0

        # Intial Pew Settings
        self.pewTime = self.options['pewTime']
        self.maxPews = self.options['maxPews']
        self.pewRange = self.options['pewRange']
        
        # Setting up the pewPew and asteroids list
        self.pewPews = []
        self.asteroids = []
        self.powers=[]
        
        # Setting up the spawn time for the asteroids
        self.spawnTime = 10000
        self.powerTime = 200000
        # Setting up the centre of the screen
        self.centreX = self.width / 2
        self.centreY = self.height / 2

        # Setting up the clock and the ship
        self.clock = pygame.time.Clock()
        self.ship = spaceShip(self.centreX, self.centreY, self.options['shipColour'])

        # Setting up the window caption
        pygame.display.set_caption(self.options['title'])

        # Setting the done flag to False
        self.done = False

        # Setting up the key flags
        self.K_UP = False
        self.K_LEFT = False
        self.K_RIGHT = False
        self.K_SPACE = False
        self.K_s = False
        self.K_y = False
        self.K_j = False
        
        # Setting up the previous timers
        self.prevTime = time() * 1000
        self.prevPew = time() * 1000
        self.prevSpawn = time() * 1000
        self.prevPower = time() * 1000


        self.high_score = self.get_high_score()
        
        # Starting the main loop
        if (self.options["AI_PLAY"]==False):    
            self.mainLoop()

    def mainLoop(self):
        while not self.done:
            self.getEvents()  # Get user input
            self.clock.tick()  # Tick the clock
            if(self.game_over == False):
                self.updateGame()
            else:
                self.gameOver ()
                pygame.display.flip()
                if (self.K_y==True):
                    self.playAgain()

    def updateGame(self):
        
        self.spawnTimer()  # Spawn asteroids
        self.ship.shieldsTimer()  # Update shield timer
        self.powerTimer()
        self.parseInputs()  # Handle user input
        self.doMovements()  # Move game objects
        if (self.ship.shieldsUp == False):
            if(self.K_s==True):
                self.ship.deployShields()  # Deploy shields
            if(self.detectCrash()):  # Check for collisions
                if (self.lives > 0):                   
                    self.respawn()  # Respawn ship
                else:
                    self.game_over = True  # Game over
                    self.update_high_scores(self.score)              
        self.screen.fill(self.options['background'])  # Fill screen with background color
        self.displayPews()  # Draw pew pews
        self.displayAsteroids() # Draw the asteroids
        self.ship.drawObject(self.screen) # Draw the ship
        self.displayPowers()
        self.displayScore() # Display the score
        self.displayLives() # Display lives
        pygame.display.flip() # Update the screen

    def playAgain(self):
        self.lives=4
        self.respawn()
        self.asteroids=[]
        self.pewPews=[]
        self.score=0
        self.game_over=False
        
    def respawn(self):
        self.ship.x = self.centreX
        self.ship.y = self.centreY
        self.ship.shieldsUp = True
        self.ship.shieldTimer = time() * 1000
        self.ship.setColour((0,200,200))                            
        self.ship.setAngle(0)
        self.ship.speed=0
        self.pewTime = self.options['pewTime']
        self.maxPews = self.options['maxPews']
        self.pewRange = self.options['pewRange']
        self.lives -= 1


                
    def displayScore(self):
        self.drawLabel ((20,20),str(int(self.score)),12)

    def displayLives(self):
        for i in range (0,self.lives,1):            
            x = 780 - i * 20
            y = 20
            l = life(x,y)
            l.drawObject(self.screen)

    def parseInputs (self):            
        now = time() * 1000        
        interval = now - self.prevTime
        if (interval > 200):
            if (self.K_UP==True):
                self.ship.thrust(interval)    
            self.prevTime = now                      

        if (self.K_RIGHT==True):
            self.ship.rotation(0.5)
            
        if (self.K_LEFT==True):
            self.ship.rotation(-0.5)

        if (self.K_SPACE == True):
            self.pew()          

        if (self.K_j == True):
            self.ship.jump(self.width,self.height)          

    def bastardTrajectory(self, targetX, targetY, originX, originY):
        return degrees(atan((targetY - originY)/(   targetX - originX)))

    def spawnTimer(self):
        
        maxAsteroids = int(1 + self.score/1000) # initial value plus one asteroid per 1000 points
        spawnTime = int(1000 - 10*self.score/1000) # initial value minus 10 ms per 1000 points
       
        if (maxAsteroids>10):
            maxAsteroids =10
       
        if (len(self.asteroids) < maxAsteroids):
            now = time() * 2000
            
            if (now - self.prevSpawn > spawnTime):  
                if (randint(1, 5) == 1):
                    self.spawn_asteroid(aim_at_ship=True)
                    self.spawn_asteroid(aim_at_ship=True)
                else:
                    self.spawn_asteroid(aim_at_ship=False)      
                self.prevSpawn = now
     
    def spawn_asteroid (self,aim_at_ship=False):
        x = randrange(0,self.width,1)  + self.ship.x
        y = randrange(0,self.height,1) + self.ship.y
        r = randrange(30,100,1)
        a = randrange(0,180)
        s = random()
        p = randrange(2,6,1)
        
        if(aim_at_ship ==True):
            a = self.bastardTrajectory( self.ship.x,self.ship.y,x,y)
            s = 10
            print("Incoming") 
        ast = asteroid(x,y,r,a,s,p)
        self.asteroids.append(ast)

    def powerTimer(self):
        if (len(self.asteroids) < 3):
            now = time() * 2000
            if (now - self.prevPower > self.powerTime):        
                self.spawn_power()    
                self.prevPower = now

    def spawn_power (self):
        x = randrange(100,self.width-100,1)  + self.ship.x
        y = randrange(100,self.height-100,1) - self.ship.y
        pUp = powerUp(x,y)
        self.powers.append(pUp)
        
    
    def doMovements(self):
        self.ship.doMovement(self.width,self.height)
        self.doAsteroids()
        self.doPews()
        self.doPowers()
        
    def pew(self):
        now = time() * 1000
        if (now - self.prevPew > self.pewTime):
            if (len(self.pewPews) < self.maxPews):
                pew = pewPew(
                self.ship.x + self.ship.nodes[0][0],
                self.ship.y + self.ship.nodes[0][1],
                self.options['pewColour'],
                self.ship.angle,
                self.ship.speed*2+1,
                self.pewRange
                )
                self.pewPews.append(pew)
            self.prevPew=now

    def doPews(self):
        for pew in self.pewPews[:]:
            if (pew.range == 0):
                self.pewPews.remove(pew)
            elif (pew.range > 0):
                pew.doMovement(self.width,self.height)
                self.detectHits(pew)

    def doPowers(self):
        for power in self.powers[:]:
            if (power.range == 0):
                self.powers.remove(power)
            elif (power.range > 0):
              power.doMovement(self.width,self.height)

    def detectHits(self,pew):        
        for ast in self.asteroids[:]:
            if (ast.detectHit(pew.x,pew.y)):
                self.score += int(ast.r)
                subAsts = ast.breakUp()
                if (ast in self.asteroids):
                    self.asteroids.remove(ast)
                if (pew in self.pewPews):
                    self.pewPews.remove(pew)
                if (subAsts != False):
                    for subAst in subAsts[:]:
                        self.asteroids.append(subAst)    

        for power in self.powers[:]:
            if (power.detectHit(pew.x,pew.y)):
                p_type = power.powerType
                
                if (p_type==3):
                   self.pewRange += 10 
                if (p_type==4):
                   self.maxPews += 10
                if (p_type==5):
                   self.lives += 1
                if (power in self.powers):
                    self.powers.remove(power)     

    def gameOver (self):

        self.drawLabel ((self.centreX,self.centreY),"GAME OVER",30)
        self.drawLabel ((self.centreX,self.centreY+30),"Press Y To Play Again",20)
        self.display_high_scores()
    def detectCrash(self):
        for ast in self.asteroids[:]:        
            if (ast.detectCollision(self.ship)):
                return True
        return False

    def doAsteroids(self):
        for ast in self.asteroids[:]:
            ast.doMovement(self.width,self.height)
                    
    def drawLabel (self,cords,message,fontsize):
        font = pygame.font.SysFont(self.options["font"], fontsize, True, False)
        text = font.render(message, True, self.options['labelColour'])
        self.screen.blit(text,(cords[0]-text.get_width()/2, cords[1]-text.get_height()/2))   

    def getEvents(self):
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                self.done=True 
            elif event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_q):
                    self.done=True
                elif (event.key == pygame.K_UP):
                    self.K_UP=True
                elif (event.key == pygame.K_DOWN):
                    self.K_DOWN=True
                elif (event.key == pygame.K_LEFT):
                    self.K_LEFT=True
                elif (event.key == pygame.K_RIGHT):
                    self.K_RIGHT=True
                elif (event.key == pygame.K_SPACE):
                    self.K_SPACE=True
                elif (event.key == pygame.K_s):
                    self.K_s=True
                elif (event.key == pygame.K_y):
                    self.K_y=True
                elif (event.key == pygame.K_j):
                    self.K_j=True
            elif event.type == pygame.KEYUP:
                if (event.key == pygame.K_UP):
                    self.K_UP=False
                elif (event.key == pygame.K_DOWN):
                    self.K_DOWN=False
                elif (event.key == pygame.K_LEFT):
                    self.K_LEFT=False
                elif (event.key == pygame.K_RIGHT):
                    self.K_RIGHT=False
                elif (event.key == pygame.K_SPACE):
                    self.K_SPACE=False
                elif (event.key == pygame.K_s):
                    self.K_s=False
                elif (event.key == pygame.K_y):
                    self.K_y=False
                elif (event.key == pygame.K_j):
                    self.K_j=False

    def displayPews(self):
        stop = len(self.pewPews)
        for i in range(0,stop,1):
            self.pewPews[i].drawObject(self.screen)

    def displayAsteroids(self):
        for ast in self.asteroids[:]:
            ast.drawObject(self.screen)

    def displayPowers(self):
        for power in self.powers[:]:
            power.drawObject(self.screen)

    def printFonts(self):
        fonts = pygame.font.get_fonts()
        print(len(fonts))
        for f in fonts:
            print(f)            

    def save_high_scores(self,scores):
        with open(self.options['highScoreFile'], 'w') as file:
            for score in scores:
                file.write(str(score) + '\n')

    def load_high_scores(self):
        with open(self.options['highScoreFile'], 'r') as file:
            scores = []
            for line in file:
                scores.append(int(line.strip()))
        return scores

    def update_high_scores(self,player_score):
        high_scores = self.load_high_scores()
        high_scores.append(player_score)
        high_scores.sort(reverse=True)
        high_scores = high_scores[:10]  # Keep only the top 10 scores
        self.save_high_scores(high_scores)


    def display_high_scores(self):
        high_scores = self.load_high_scores()
        self.drawLabel ((self.centreX,self.centreY+50),"HIGH SCORES",20)
        for i, score in enumerate(high_scores):
            scoreStr="%i"%(score)
            self.drawLabel ((self.centreX,self.centreY+70+(i*22)),scoreStr ,20)
    def get_high_score(self):
        scores = self.load_high_scores()
        if scores:
            return max(scores)
        else:
            return 0
    
    # AI INTERFACE SET AI_PLAY to True
    
    def get_state(self):
        shieldState=''
        if (self.ship.shieldsUp == False and self.ship.shieldOverloaded== False ):
            shieldState = 'DOWN_CAN'
        elif (self.ship.shieldsUp == False and self.ship.shieldOverloaded== True):
            shieldState = 'DOWN_CANT'
        else:
            shieldState = 'UP'
        state = {
            'ship': self.ship,
            'asteroids': self.asteroids,
            'powerups': self.powers,
            'pewpews' : self.pewPews,
            'score': self.score,
            'lives': self.lives,
            'shield_state': shieldState,
            'game_over' : self.game_over
        }
        return state
        
    def sendCommands (self,commands):
        self.K_UP = commands["K_UP"]
        self.K_LEFT = commands["K_LEFT"]
        self.K_RIGHT = commands["K_RIGHT"]
        self.K_SPACE = commands["K_SPACE"]
        self.K_s = commands["K_s"]
        self.K_j = commands["K_j"]
        self.K_y = commands["K_y"]
    
        
if __name__ == "__main__":


    game =  asteroidsGame({
 
    "title":"Asteroids",
    "background":(0,0,0),
    "labelColour":(255,255,255),
    "shipColour":(255,200,0),
    "pewColour":(0,0,255),
    "font":"arial",
    "pewRange":200,
    "maxPews":3,
    "pewTime":100,
    "intialLives":3,
    "highScoreFile":'high_scores.txt',
    "AI_PLAY":False # Work in progress
    })
    
#    ai = SpaceGameAI(game.width,game.height)
#    if (game.options['AI_PLAY'] == True):
#  
#        dqn = DeepQNetwork(game.get_state_size(), game.get_action_size())
#        state = game.get_state()
#        while not game.game_over:
#            # get Q-values for each action
#            q_values = dqn.predict(state)
#            # select action based on Q-values
#            action = np.argmax(q_values)
#            # send action to game
#            game.sendCommands(game.actions[action])
#            # update game state
#            game.updateGame()
            # get new state
#            new_state = game.get_state()
            # get reward for current action
#            reward = game.get_reward()
            # store transition in replay memory
 #           dqn.remember(state, action, reward, new_state, game.game_over)
            # update current state
 #           state = new_state
            # train DQN on a batch of transitions from replay memory
  #          dqn.train_batch()
