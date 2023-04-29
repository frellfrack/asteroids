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
        self.r=25
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

    def jump(self,width,height):
        self.x = randrange (0,width,1)       
        self.y = randrange (0,height,1)

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
    def getVertices(self):
        vertices = []
        for node in self.nodes:
            vertices.append([node[0]+self.x, node[1]+self.y])
        return vertices
                
        
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
        
        self.rr=randrange(-9,9,1)/100 


        self.vertices = self.getVertices()

    def getVertices(self):
        vertices = []
        for node in self.nodes:
            vertices.append([node[0]+self.x, node[1]+self.y])
        return vertices

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
    
        self.angle+=self.rr                  
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
        self.rotateNodes()    
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


    def detectHit(self, x, y):
        dx = x - self.x
        dy = y - self.y        
        if (dx > self.r or dy > self.r):
            return False
        else:
            dist = sqrt((dx * dx) + (dy * dy))
            if (dist <= self.r):
                return True
            else:
                for vertex in self.getVertices():
                    vdx = vertex[0] - x
                    vdy = vertex[1] - y
                    vdist = sqrt(vdx**2 + vdy**2)
                    if vdist <= 1:
                        return True
                return False

    def detectCollision(self, ship):
        # calculate the distance between the centers of the asteroid and the ship
        dx = ship.x - self.x
        dy = ship.y - self.y
        # if the distance is greater than the sum of the radii, then there is no collision
        if (dx > self.r + ship.r or dy > self.r + ship.r):
            return False
        else:
            dist = sqrt((dx * dx) + (dy * dy))
            # if the distance is greater than or equal to the sum of the radii, there isn't a collision
            if (dist > self.r+20+ ship.r):
                return False
            else:
                asteroid_vertices = self.getVertices()
                ship_vertices = ship.getVertices()

                for a_index, a_vert in enumerate(asteroid_vertices):
                    for s_index, s_vert in enumerate(ship_vertices):
                        a_vert_next = asteroid_vertices[(a_index + 1) % len(asteroid_vertices)]
                        s_vert_next = ship_vertices[(s_index + 1) % len(ship_vertices)]
                        collision = intersect(a_vert, a_vert_next, s_vert, s_vert_next)
                        if collision:
                            return True
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





def intersect(p1, q1, p2, q2):
    """
    Check if line segment p1-q1 intersects line segment p2-q2.
    Code adapted from: https://stackoverflow.com/a/20679579
    """
    def ccw(A,B,C):
        return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])

    return ccw(p1,q1,p2) != ccw(p1,q1,q2) and ccw(p2,q2,p1) != ccw(p2,q2,q1)


class life(base_object):

    def __init__(self,x,y):
    
        super().__init__([
        [10,0],
        [-5,5],
        [-5,-5]
        ],x,y,(200,200,0))
        self.setAngle(-90)
        self.rotateNodes()
        
        
class powerUp (base_object):

    def __init__(self,x,y):
        # Initialize powerUp object with random powerType and color
        self.r=10
        self.powerType = randrange(3,6,1) # 3, 4, or 5
        super().__init__(
            self.returnCords(self.r,self.powerType), # Get coordinates of vertices for powerUp shape
            x,y,(200,200,0) # Set initial position and color
        )
        self.setAngle(-90) # Set initial angle
        
        # Set initial radians and speed for movement
        self.radians = radians(randrange(1,360,1))
        self.speed=0.25
        self.range=2000
    def returnCords(self,r,numNodes):
        # Get coordinates of vertices for powerUp shape
        cords  = []
        for i in range(0,numNodes,1):            
            cords.append([
            r * cos((i*360/numNodes) * pi/180),
            r * sin((i*360/numNodes) * pi/180)
            ]
            )
        return cords

    def doMovement(self,width,height): 
    
        self.range -=1
        # Move powerUp object and wrap around screen if necessary
        self.x += cos(self.radians) * self.speed
        self.y += sin(self.radians) * self.speed
        
        if (self.x > width):
            self.x = 0
        elif (self.x < 0):
            self.x = width
        if(self.y > height):
            self.y = 0
        elif(self.y < 0):
            self.y = height
                
    def detectHit(self, x, y):
        # Check if powerUp object has been hit by another object
        dx = x - self.x
        dy = y - self.y        
        if (dx > self.r or dy > self.r):
            return False          
        dist = sqrt((dx * dx) + (dy * dy))
        if (dist > self.r):
            return False
        return True
