import pygame
from math import floor
from random import randint, uniform

class MoneyRain:
	screen_width = 640
	screen_height = 480

	running = True #Is the game running
	fps = 60
	clock = pygame.time.Clock() #Clock for the game
	seconds = 0

	player_speed = 5
	player_movement = 0
	
	totalMoney = 0
	
	element_speed = 3 #Speed of the falling objects
	falling_objects = set()
	deleting_falling_objects = set()

	def __init__(self): #Constructor
		pygame.init()

		self.player = Player(self.screen_width, self.screen_height, self.player_speed) #Creates the player
		self.screen = pygame.display.set_mode((self.screen_width, self.screen_height)) #Creates the screen

		self.font = pygame.font.SysFont("Arial", 24) #Font for the text
		pygame.display.set_caption("Moneyrain") #Sets the title of the screen

		self.ticking() #Starts the game

	def showText(self): #Shows the text on the screen
		text = self.font.render("Amount of money: " + str(self.totalMoney), True, (255, 0, 0)) #Creates a text
		self.screen.blit(text, (self.screen_width - text.get_width(), self.font.get_height())) #Shows the text

		text = self.font.render("F2 = New game", True, (255, 0, 0)) #Creates a text
		self.screen.blit(text, (0, 0)) #Shows the text

		text = self.font.render("Esc = Close the game", True, (255, 0, 0)) #Creates a text
		self.screen.blit(text, (0, self.font.get_height())) #Shows the text

		text = self.font.render(f"Time: {self.seconds // 60:.0f}:{floor(self.seconds % 60):02}", True, (255, 0, 0)) #Creates a text
		self.screen.blit(text, (self.screen_width - text.get_width(), 0)) #Shows the text

	def ticking(self): #Main loop of the game
		while True:
			self.handleEvents()
			self.checkCollision()
			if self.running == True:
				self.element_speed += 0.001 #Increases the speed of the falling objects
				self.seconds += 1 / self.fps #Increases the seconds
				if uniform(0, 300) < self.element_speed: #Creates a falling object
					self.create_falling_obj() 
				for object in self.falling_objects: #Moves the falling objects
					object.moveObject()
				for object in self.deleting_falling_objects: #Deletes the falling objects
					self.falling_objects.remove(object)
				self.deleting_falling_objects.clear() #Clears the deleting falling objects
				self.screen.fill((75, 0, 130)) #Fills the screen with a color
				for object in self.falling_objects: #Renders the falling objects
					object.render(self.screen)
				self.player.render(self.screen) #Renders the player
				self.showText()
				pygame.display.flip() #Updates the screen
			self.clock.tick(self.fps) #Sets the frames per second

	def handleEvents(self):
		keys = pygame.key.get_pressed() #Gets the pressed keys
		if keys[pygame.K_LEFT]:
			self.player.movePlayer(-1) #Moves the player to the left
		if keys[pygame.K_RIGHT]:
			self.player.movePlayer(1) #Moves the player to the right

		for event in pygame.event.get():
			if event.type == pygame.QUIT: #If the event is quit
				self.running = False #Stops the game
				pygame.quit()
				exit()

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					self.running = False #Stops the game
					pygame.quit()
					exit()
				if event.key == pygame.K_F2:
					self.totalMoney = 0
					self.falling_objects.clear()
					self.deleting_falling_objects.clear()
					self.running = True #Starts the game
					self.element_speed = 3 #Resets the speed of the falling objects
					self.seconds = 0

	def create_falling_obj(self, type = randint(0, 1)): #Creates a falling object
		self.falling_objects.add(FallingObj(self.screen_width, self.screen_height, self.element_speed, self)) #Adds the falling object to the set

	def delete_falling_obj(self, obj): #Deletes a falling object
		self.deleting_falling_objects.add(obj) #Adds the falling object to the deleting falling objects

	def checkCollision(self): #Checks the collisions
		for object in self.falling_objects: #Goes through the falling objects
			if object.y + object.image.get_height() <= self.player.y or object.y >= self.screen_height: #If the falling object is not in the player's area
				continue
			if object.x + object.image.get_width() >= self.player.x and object.x <= self.player.x + self.player.image.get_width(): #If the falling object is in the player's area
				if object.type == 0: #If the falling object is a coin
					self.totalMoney += 1
					self.deleting_falling_objects.add(object) #Deletes the falling object
				else: #If the falling object is a monster
					self.running = False
					text = self.font.render(f"Amount of money: {self.totalMoney} - Time: {self.seconds // 60:.0f}:{floor(self.seconds % 60):02}", True, (255, 0, 0)) #Creates a text
					self.screen.blit(text, ((self.screen_width - text.get_width()) / 2, (self.screen_height - text.get_height()) / 2)) #Shows the text
					pygame.display.flip() #Updates the screen



class Player:
	def __init__(self, width, height, speed): #Constructor
		self.speed = speed
		self.image = pygame.image.load("robo.png")
		self.x = width / 2 - self.image.get_width() / 2 #X position of the player
		self.y = height - self.image.get_height() #Y position of the player
		self.width = width

	def movePlayer(self, x): #Moves the player
		self.x += x * self.speed #Moves the player by the speed
		if self.x < 0: #If the player is too left out of the screen 
			self.x = 0 #Sets the player to the left
		elif self.x > self.width - self.image.get_width(): #If the player is too right out of the screen
			self.x = self.width - self.image.get_width() #Sets the player to the right

	def render(self, display): #Renders the player
		display.blit(self.image, (self.x, self.y))



class FallingObj: #Falling object class
	image_map = {0: pygame.image.load("kolikko.png"), 1: pygame.image.load("hirvio.png")} #Images of the falling objects

	def __init__(self, width, height, speed, parent): #Constructor
		self.type = randint(0, 1) #Type of the falling object
		self.image = self.image_map.get(self.type) #Image of the falling object
		self.speed = speed #Speed of the falling object
		self.x = randint(0, width - self.image.get_width()) #X position of the falling object
		self.y = -self.image.get_height() #Y position of the falling object
		self.width = width #Width of the screen 
		self.height = height #Height of the screen
		self.parent = parent #Parent of the falling object

	def moveObject(self):
		self.y += self.speed #Moves the falling object by the speed
		if self.y > self.height: #If the falling object is out of the screen
			self.parent.delete_falling_obj(self) #Deletes the falling object

	def render(self, display): #Renders the falling object
		display.blit(self.image, (self.x, self.y)) #Shows the falling object

if __name__ == "__main__":
	MoneyRain() #Creates the game