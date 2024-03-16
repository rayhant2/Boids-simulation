# Boids-simulation
Boids is an artifical life program with a huge presence within computer graphics; originally developed by Craig Reynolds, it simulates emergent behavior for a population of objects. It specifies the behavior of each object individually instead of the whole collection. Defining a few rules for the individual objects, the program dynamically changes the positions and accelerations of each object to achieve a group "flocking" behavior.
<br>

![boids (1)](https://github.com/rayhant2/Boids-simulation/assets/61428939/9b802e96-7140-4689-b60c-d6cf131e3351)

## Overview

The Boids program simulates the movement of individuals, often represented as birds. Each individual, or "boid," follows a set of simple rules that results in emergent behaviors;
<br>


### &emsp;Cohesion

- The cohesion rule accounts for the grouping of birds. Each bird is initialized with a random position, displacement, and velocity. Within a given ```cohesionRadius```, the birds travel towards each other; the birds look at every other bird within the given radius, take the average position of those birds, and change its trajectory to accelerate towards the average position. 

### &emsp;Alignment

- The alignment rule describes the behaior in which the birds fly in the same direction; it allows the birds to travel in the same direction to one another. Within a given ```alignmentRadius``` of a bird, the average velocity is taken of all the birds within that radius. The velocity vectors are then normalized, since direction is the only component of interest, and the average direction for which the bird should fly is found. The bird's acceleration is updated to travel in this new direction.

### &emsp;Separation

- The separation rule ensures that the birds maintain an appropriate distance from each other and does not stack together. Each bird is compared to every other bird and is checked to see if they are within the ```separationRadius```. The function then calculates the average displacement for all the birds within that radius, slightly adjusting the acceleration so it deviates away from the other birds.

### &emsp;Mouse

- The mouse rule was added to add a more interactive element to the simulation; it also translates to more appliactions as we can observe the behavior of flocks as they travel to a specific point. If the mouse is pressed, the rule finds the position of the cursor at that instance. Each bird's  position is subtracted from the mouse's position to get the displacement and the direction; the acceleration is updated accordingly.

### &emsp;Random

- This rule gives the birds a random deviation, accounting for birds having their own minds. The acceleration for a bird may change in terms of direction at random, which may cause a sub-group of boids to diverge from the group and follow their own path, before joining the main flock again.
<br>


## Prerequisites:
Before running the script, make sure the following is installed:
- Python
- PyGame
- Tools
- NumPy
- SciPy

The modules can be installed via terminal with the following command:
```bash
pip install pygame tools numpy scipy
```

<br>

## Usage:

1. Clone the repository:
   ```bash git clone https://github.com/rayhant2/Boids-simulation.git```
2. Run the script:
   ```bash python main.py```
<br>

## Future Extensions:
- Predator/Prey simulation
- Obstacles
- Boid simulation within complex structures (e.g mazes/maps)

<br>
<br>
*This program was made in collaboration with graduate students at the University of Toronto's Department of Computer Science, at the Dynamics Graphics Project laboratory.*
<br>

## License:
MIT
