# Boids-simulation
Boids is an artifical life program with a huge presence within computer graphics; originally developed by Craig Reynolds, it simulates emergent behavior for a population of objects. It specifies the behavior of each object individually instead of the whole collection. Defining a few rules for the individual objects, the program dynamically changes the positions and accelerations of each object to achieve a group "flocking" behavior.
<br>

![boids (1)](https://github.com/rayhant2/Boids-simulation/assets/61428939/9b802e96-7140-4689-b60c-d6cf131e3351)

## Overview

The Boids program simulates the movement of individuals, often represented as birds. Each individual, or "boid," follows a set of simple rules that results in emergent behaviors;
<br>


### &emsp;Cohesion

&emsp;&ensp; The cohesion rule accounts for the grouping of birds. Each bird is initialized with a random position, displacement, and velocity. Within a given ```cohesionRadius```, the birds travel towards each other; the birds look at every other bird within the given radius, take the average position of those birds, and change its trajectory to accelerate towards the average position. 
