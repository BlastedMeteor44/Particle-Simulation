import random
import math
from .particle import Particle

def find_particle_at_position(x, y, particles):
    for index, particle in enumerate(particles):
        distance = math.sqrt((x - particle.x) ** 2 + (y - particle.y) ** 2)
        if distance <= particle.radius:
            return index
    return None

def is_valid_position(x, y, radius, particles):
    for particle in particles:
        distance = math.sqrt((x - particle.x) ** 2 + (y - particle.y) ** 2)
        if distance < radius + particle.radius:
            return False
    return True

def spawn_particle(particles, window_width, window_height, radius, color):
    max_attempts = 100
    for _ in range(max_attempts):
        x = random.randint(radius, window_width - radius)
        y = random.randint(radius, window_height - radius)
        if is_valid_position(x, y, radius, particles):
            particles.append(Particle(x, y, radius, color, velocity=[random.uniform(-2, 2), random.uniform(-2, 2)]))
            return True
    print("Failed to spawn particle after max attempts.")
    return False