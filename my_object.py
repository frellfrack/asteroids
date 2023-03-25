import pygame
from math import sin, cos, pi

class base_object:

    def __init__(self,nodes,x,y,colour):
        # Initialize the object with a given set of nodes, x and y coordinates, and colour
        self.nodesOrginal = nodes  # Store the original set of nodes
        self.nodesLen = len(self.nodesOrginal)  # Store the length of the nodes list
        self.nodes=[]  # Create an empty list to store the rotated nodes
        self.copyNodes()  # Create a copy of the original nodes and store them in the nodes list
        self.setAngle(0)  # Initialize the angle to 0 degrees   
        self.setX(x)  # Set the initial x coordinate
        self.setY(y)  # Set the initial y coordinate
        self.setColour(colour)  # Set the colour of the object
        

    def setX(self,x):
        # Set the x coordinate of the object
        self.x=x
 
    def setY(self,y):
        # Set the y coordinate of the object
        self.y=y

    def setAngle(self,angle):
        # Set the angle of the object in degrees
        self.angle=angle
        
    def setColour(self,colour):
        # Set the colour of the object
        self.colour = colour

    def copyNodes(self):
        # Create a deep copy of the original set of nodes and store them in the nodes list
        for i in range(0, self.nodesLen,1):
            self.nodes.append([self.nodesOrginal[i][0],self.nodesOrginal[i][1]])
 
    def rotateNodes(self):
        # Rotate the object's nodes based on its current angle
        radians =  (pi/180) * self.angle  # Convert the angle to radians   
        sinTheta = sin(radians)  # Calculate the sine of the angle
        cosTheta = cos(radians)  # Calculate the cosine of the angle
        for i in range(0, self.nodesLen,1):
            # Apply the rotation transformation to each node's x and y coordinates
            x = self.nodesOrginal[i][0]
            y = self.nodesOrginal[i][1]
            self.nodes[i][0] = x * cosTheta - y * sinTheta
            self.nodes[i][1] = y * cosTheta + x * sinTheta

    def drawObject(self,surface):
        # Draw the object on a given pygame surface
        cords = []
        for i in range(0,self.nodesLen,1):
            # Calculate the absolute coordinates of each node
            x=self.x+self.nodes[i][0]
            y=self.y+self.nodes[i][1]
            cords.append((x,y))
        # Draw a polygon on the surface using the calculated coordinates and the object's colour
        pygame.draw.polygon(
        surface, 
        self.colour, 
        cords
        )
