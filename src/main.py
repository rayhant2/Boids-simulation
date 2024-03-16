import pygame
import tools as tl
import numpy as np
import scipy as sp
import random
from copy import deepcopy



def _setRuleWeights(self):
    self.maxSpeed = 5
    self.maxAcceleration = 1

    self.alignmentWeight = 0.25  # 0.25
    self.cohesionWeight = 0.2   # 0.2
    self.separationWeight = 0.3 # 0.2
    self.mouseFollowWeight = 0.1 # 0.1
    self.randomPerturbationWeight = 0.05   #0.05

    self.alignmentRadius = 70
    self.cohesionRadius = 100   # 100
    self.separationRadius = 50
    self.mouseFollowRadius = 200




def limit(vector, length):
    tmp = deepcopy(vector)
    if tmp.length() > length:
        tmp.normalize_ip()
        tmp *= length
    return tmp




def _ruleCohesion(self, flock):
    acceleration = pygame.Vector2(0, 0)
    bird_pos = ""
    sum_pos = pygame.Vector2(0,0)
    ct = 0
    for birds in flock:

        if birds == self:
            continue

        displacement = self.boundary.periodicDisplacement(self.position, birds.position)
        distance = displacement.length()
        if distance <= self.cohesionRadius:
            sum_pos += birds.position
            ct +=1 
    
    if ct == 0:
        return acceleration
    
    sum_pos /= ct
    acceleration = sum_pos - (self.position + self.velocity)
    acceleration.normalize_ip()
    acceleration *= self.maxSpeed
    acceleration -= self.velocity
    acceleration = limit(acceleration, self.maxAcceleration)


    return acceleration




def _ruleAlignment(self, flock):

    acceleration = pygame.Vector2(0, 0)
    avg_disp = pygame.Vector2(0,0)
    ct = 0

    for bird in flock: 

        if bird == self:
            continue
        
        displacement = self.boundary.periodicDisplacement(self.position, bird.position)

        distance = displacement.length()
        displacement /= distance*distance

        if distance <= self.alignmentRadius:
            acceleration += bird.velocity.normalize()
            ct += 1
    

    if ct == 0:
        return acceleration

    acceleration /= ct
    acceleration.normalize_ip()         # Cant normalize 0 so put in a else statement
    acceleration *= self.maxSpeed
    acceleration -= self.velocity
    acceleration = limit(acceleration, self.maxAcceleration)

    
    return acceleration






def _ruleSeparation(self, flock):
    acceleration = pygame.Vector2(0, 0)
    avg_disp = pygame.Vector2(0,0)
    ct = 0

    for bird in flock: 

        if bird == self:
            continue
        
        displacement = self.boundary.periodicDisplacement(self.position, bird.position)

        distance = displacement.length()
        displacement /= distance*distance

        if distance <= self.separationRadius:
            acceleration += displacement
            ct += 1
    

    if ct == 0:
        return acceleration

    acceleration /= ct
    acceleration.normalize_ip()         # Cant normalize 0 so put in a else statement
    acceleration *= self.maxSpeed
    acceleration -= self.velocity
    acceleration = limit(acceleration, self.maxAcceleration)
    
    return acceleration






def _ruleRandomPerturbation(self):
    acceleration = pygame.Vector2(np.random.uniform(-1,1), np.random.uniform(-1,1))

    acceleration.normalize_ip()         # Cant normalize 0 so put in a else statement
    acceleration *= self.maxSpeed
    acceleration -= self.velocity
    acceleration = limit(acceleration, self.maxAcceleration)
    
    return acceleration






def _ruleMouseFollow(self):
    acceleration = pygame.Vector2(0, 0)

    if self.mouseDown:

        displacement = self.boundary.periodicDisplacement(self.position, self.mousePos)
        acceleration -= displacement    # -
        
        acceleration *= self.maxSpeed
        acceleration -= self.velocity
        acceleration = limit(acceleration, self.maxAcceleration)


    return acceleration








class Bird:
    def __init__(self, x, y):
        # init position
        self.position = pygame.Vector2(x, y)
        # init velocity
        vx = np.random.uniform(-1, 1)
        vy = np.random.uniform(-1, 1)
        self.velocity = pygame.Vector2(vx, vy)
        self.velocity.normalize_ip()
        self.velocity *= np.random.uniform(1, 5)
        self.maxSpeed = 5
        # init acceleration
        self.acceleration = pygame.Vector2(0, 0)
        self.maxAcceleration = 1
        # init boundary
        self.boundary = Boundary(0, 800, 0, 600)
        # init display
        self.size = 3
        self.angle = 0
        self.color = (255, 255, 255)
        self.secondaryColor = (0, 0, 0)
        self.stroke = 2
        self.mouseDown = False
        self.mousePos = pygame.Vector2(0, 0)
        # init rule weights
        self.setRuleWeights()
    
    def computeAcceleration(self, flock):
        self.acceleration *= 0
        alignment = self.ruleAlignment(flock)
        self.acceleration += alignment*self.alignmentWeight
        cohesion = self.ruleCohesion(flock)
        self.acceleration += cohesion*self.cohesionWeight
        separation = self.ruleSeparation(flock)
        self.acceleration += separation*self.separationWeight
        randomPerturbation = self.ruleRandomPerturbation()
        self.acceleration += randomPerturbation*self.randomPerturbationWeight
        mouseFollow = self.ruleMouseFollow()
        self.acceleration += mouseFollow*self.mouseFollowWeight

    def update(self, flock):
        self.computeAcceleration(flock)

        self.velocity += self.acceleration
        self.velocity = limit(self.velocity, self.maxSpeed)
        
        self.position += self.velocity
        self.boundary.periodicProject(self.position)
        
        self.angle = np.arctan2(self.velocity.y, self.velocity.x) + np.pi/2

    def setRuleWeights(self):
        _setRuleWeights(self)

    def ruleAlignment(self, flock):
        return _ruleAlignment(self, flock)
    
    def ruleCohesion(self, flock):

        
        return _ruleCohesion(self, flock)

    def ruleSeparation(self, flock):
        return _ruleSeparation(self, flock)

    def ruleRandomPerturbation(self):
        return _ruleRandomPerturbation(self)

    def ruleMouseFollow(self):
        return _ruleMouseFollow(self)

    def Draw(self, screen, distance, scale):
        ps = []
        #initialize a 3x3 np array
        points = np.zeros((3, 2), dtype=int)

        # create a triangle
        points[0,:] = np.array([0,-self.size])
        points[1,:] = np.array([np.sqrt(self.size),np.sqrt(self.size)])
        points[2,:] = np.array([-np.sqrt(self.size),np.sqrt(self.size)])

        for point in points:
            rotation_matrix = np.array([[np.cos(self.angle), -np.sin(self.angle)], [np.sin(self.angle), np.cos(self.angle)]])
            rotated = np.matmul(rotation_matrix,point)

            x = int(rotated[0] * scale) + self.position.x
            y = int(rotated[1] * scale) + self.position.y
            ps.append((x, y))

        pygame.draw.polygon(screen, self.secondaryColor, ps)
        pygame.draw.polygon(screen, self.color, ps, self.stroke)





class Boundary:
    def __init__(self, min_x, max_x, min_y, max_y):
        self.min_x = min_x
        self.max_x = max_x
        self.min_y = min_y
        self.max_y = max_y
    
    def size_x(self):
        return self.max_x - self.min_x

    def size_y(self):
        return self.max_y - self.min_y
    
    def periodicProject(self, p):
        while p.x > self.max_x:
            p.x -= self.size_x()
        while p.x < self.min_x:
            p.x += self.size_x()
        while p.y > self.max_y:
            p.y -= self.size_y()
        while p.y < self.min_y:
            p.y += self.size_y()
    
    def periodicDisplacement(self, p, q):
        # gives the vector pointing from q to p, taking into account periodic boundary conditions
        displacement = p - q
        if displacement.x > self.size_x()/2:
            displacement.x -= self.size_x()
        if displacement.x < -self.size_x()/2:
            displacement.x += self.size_x()
        if displacement.y > self.size_y()/2:
            displacement.y -= self.size_y()
        if displacement.y < -self.size_y()/2:
            displacement.y += self.size_y()
        return displacement
    


#######################################################################################################################
    


Width, Height = 1920, 1080
Width = 960
Height = 540
white, black = (217, 217, 217), (12, 12, 12)
size = (Width, Height)

window = pygame.display.set_mode(size, pygame.RESIZABLE)
clock = pygame.time.Clock()
fps = 60

scale = 10
Distance = 5
speed = 0.0005

flock = []
n = 50

for i in range(n):
	flock.append(Bird(random.randint(20, Width-20), random.randint(20, Height-20)))

keyPressed = False
run = True
while run:
	clock.tick(fps)
	window.fill((10, 10, 15))

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				run = False
			keyPressed = True

	# update the window size
	Width, Height = window.get_size()

	for boid in flock:
		boid.radius = scale
		boid.boundary = Boundary(0, Width, 0, Height)
		boid.mousePos = pygame.Vector2(pygame.mouse.get_pos())
		boid.mouseDown = pygame.mouse.get_pressed()[0]
		boid.update(flock)
		boid.Draw(window, Distance, scale)

	keyPressed = False
	pygame.display.flip()
pygame.quit()