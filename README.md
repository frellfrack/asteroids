Asteroids Game
This is a simple implementation of the classic Asteroids game, written in Python 3 using the Pygame library. The game consists of a space ship that the player controls, and various asteroids that move around the screen and must be avoided or destroyed. The player can fire projectiles to destroy the asteroids, and must navigate through the space avoiding collisions and incoming asteroids.

Requirements
To run the game, you will need to have Python 3 and the Pygame library installed. You can install Pygame by running:

Copy code
pip install pygame
Usage
To run the game, simply execute the asteroids.py file with Python:

Copy code
python asteroids.py
The game will start immediately, and you can control the space ship using the arrow keys (up/down to move forward/backward, left/right to rotate). You can fire projectiles using the space bar, and deploy shields using the 's' key. The game is over when the player loses all lives or crashes into an asteroid.

Options
The game has several customizable options that can be set when creating a new instance of the asteroidsGame class. These options are passed as a dictionary argument to the constructor function, and include:

title (str): The title of the game window.
background (tuple): The background color of the game screen, specified as an RGB tuple.
shipColour (tuple): The color of the space ship, specified as an RGB tuple.
intialLives (int): The number of lives the player starts with.
width (int): The width of the game screen, in pixels.
height (int): The height of the game screen, in pixels.
