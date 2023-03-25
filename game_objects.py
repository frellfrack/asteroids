import pygame
from random import randrange,random
from math import pi,sin,cos,sqrt,acos,radians,degrees
from time import time
from my_object import base_object

class spaceShip (base_object):

    def __init__ (self,x,y,colour):
    
        super().__init__([
        [30,0],
        [-25,25],
        [-25,-25]
        ],x,y,colour)
        
        self.heading=0
        self.speed = 0
        self.dX = False
        self.dY = False
        self.TWOPI =pi*2
        self.shieldOverloaded = False
        self.setAngle(0)
        self.deployShields()
        
    def thrust(self,interval):
        currentRad = radians(self.angle)
        prevRad =  radians(self.heading)                    
        scaledAcceleration = interval * 0.0002
        self.dX = self.speed * cos(prevRad) + scaledAcceleration * cos(currentRad + self.TWOPI)
        self.dY = self.speed * sin(prevRad) + scaledAcceleration * sin(currentRad + self.TWOPI)
        self.speed = sqrt(self.dX * self.dX + self.dY * self.dY)
        self.heading = degrees(acos(self.dX / self.speed))
        if (self.dY < 0):
            self.heading *= -1           

    def rotation(self,plusmin):
        self.angle += plusmin
        if (self.angle > 180):
            self.angle=-180           
        elif (self.angle < -180):
            self.angle=180

    def doMovement(self,width,height):
        radians =  (pi/180) * self.heading      
        if(self.dX != False):
            self.x += self.dX
            self.dX = False
        else:
            self.x += cos(radians) * self.speed
        if(self.dY != False):
            self.y += self.dY
            self.dY = False
        else:
            self.y += sin(radians) * self.speed 
             
        if (self.y > height):
            self.y = 0
        elif (self.y < 0):
            self.y = height
        if (self.x > width):
            self.x = 0
        elif (self.x < 0):
            self.x = width
        self.rotateNodes()

    def deployShields(self):
        if(self.shieldOverloaded == False):
            self.shieldsUp = True
            self.shieldTimer = time() * 1000
            self.setColour((0,200,200))
            self.shieldOverloaded = False

    def shieldsTimer(self):
        if (self.shieldsUp == True):
            now = time() * 1000
            interval = now - self.shieldTimer
            if (interval > 10000):
                self.shieldsUp = False
                self.setColour((200,200,0))
                self.shieldTimer = time() * 1000
                self.shieldOverloaded = True

        elif(self.shieldOverloaded == True):
            now = time() * 1000
            interval = now - self.shieldTimer
            if (interval > 10000):
                self.shieldOverloaded = False
                self.setColour((0,200,0))
                
        
class pewPew(base_object):

    def __init__(self,x,y,colour,angle,speed,pewRange):

        super().__init__([
        [2,0],
        [-2,2],
        [-2,-2]
        ],x,y,colour)

        self.angle=angle
        self.speed=speed
        self.range=pewRange
        self.rotateNodes()
        self.radians = radians(self.angle)

    def doMovement(self,width,height): 
        self.x += cos(self.radians) * self.speed
        self.y += sin(self.radians) * self.speed
        self.range -=1
        if (self.x > width):
            self.x = 0
        elif (self.x < 0):
            self.x = width
            if(self.y > height):
                self.y = 0
            elif(self.y < 0):
                self.y = height
                

class asteroid(base_object): 
    def __init__(self,x,y,r,a,s,p):

        if (s > 0.3):
            s = 0.2

        if (r <20):
            r = 20

        cords = self.returnCords(r)

        c = 128 * s  
        colour=(
        self.sinwv(c,0.25,3,128),
        self.sinwv(c,0.25,1,128),
        self.sinwv(c,0.25,0,128)
        )

        super().__init__(cords,x,y,colour)

        self.r=r
        self.a=a
        self.s=s
        self.p=p


    def returnCords(self,r):
        cords  = []
        for i in range(0,15,1):            
            cords.append(
            [
            r * cos((i*360/15-randrange(0,int(r/3),1)) * pi/180)+randrange(0,10,1),
            r * sin((i*360/15-randrange(0,int(r/3),1)) * pi/180)+randrange(0,20,1)
            ]
            )
        return cords
        
    def doMovement (self,w,h):                  
        self.x += cos(radians(self.a))*self.s
        self.y += sin(radians(self.a))*self.s
        if (self.x > w):
            self.x = 0
        elif(self.x < 0):        
            self.x = w
        if (self.y>h):
            self.y = 0
        elif(self.y < 0):        
            self.y = h
    
    def sinwv(self,t,frequency,offset,amp):
        return sin(frequency*t+offset)*(amp-1)+amp;
 
    def drawAsteroid(self,screen):
        c = 128 * self.s
        colour=(
        self.sinwv(c,0.25,3,128),
        self.sinwv(c,0.25,1,128),
        self.sinwv(c,0.25,0,128)
        )
        pygame.draw.circle(screen,colour,[self.x,self.y],self.r)

    def detectHit(self,x,y):
        dx = x - self.x
        dy = y - self.y        
        if (dx > self.r or dy > self.r):
            return False
        else:
            dist = sqrt((dx * dx) + (dy * dy))
            if (dist <= self.r):
                return True
            else:
                return False

    def detectCollision(self,x,y,r):
        dx = x - self.x
        dy = y - self.y        
        if (dx > self.r+r or dy > self.r+r):
            return False
        else:
            dist = sqrt((dx * dx) + (dy * dy))
            if (dist <= self.r+r):
                return True
            else:
                return False
            
    def breakUp(self):
        if (self.p > 0):
            rr = randrange(0,180,1)
            subAstreroids =[]
            for i in range(0, self.p,1):            
                x = self.x - self.r * cos((i*360/self.p+rr) * pi/180)    
                y = self.y - self.r * sin((i*360/self.p+rr) * pi/180)
                a = i * 360 / self.p + 180+rr
                r = self.r / self.p
                s = random()
                p = 0
                if (s < 0.1):
                    s = 0.1        
                ast = asteroid(x,y,r,a,s,p)
                subAstreroids.append(ast)
            return subAstreroids
        else:
            return False

                  
class life(base_object):

    def __init__(self,x,y):
    
        super().__init__([
        [10,0],
        [-5,5],
        [-5,-5]
        ],x,y,(200,200,0))
        self.setAngle(-90)
        self.rotateNodes()
