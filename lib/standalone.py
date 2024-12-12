import pygame
import time
import math
import random

pygame.init()

screen_info = pygame.display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h

# Global variable for the window's size
window_size = [screen_width, screen_height]
win = pygame.display.set_mode((window_size[0], window_size[1]), pygame.RESIZABLE)
pygame.display.set_caption('Particle Simulator')


def find_particle_at_position(x, y, particles):
    """
    Find the index of the particle at a specific (x, y) position.

    Parameters:
        x (float): The x-coordinate to check.
        y (float): The y-coordinate to check.
        particles (list): List of Particle objects.

    Returns:
        int or None: The index of the particle at the position, or None if no particle is found.
    """
    for index, particle in enumerate(particles):
        # Calculate the distance from the position to the center of the particle
        distance = math.sqrt((x - particle.x) ** 2 + (y - particle.y) ** 2)
        if distance <= particle.radius:
            return index
    return None

def increase_velocity_of_particle(particle_id, particles, factor):
    """
    Increase the velocity of a particle in the same direction it is currently moving.

    Parameters:
        particle_id (int): The index of the particle to modify.
        particles (list): List of Particle objects.
        factor (float): The factor by which to increase the velocity.

    Returns:
        bool: True if the velocity was successfully updated, False otherwise.
    """
    try:
        int(particle_id)
    except (ValueError, TypeError):
        return False

    if 0 <= particle_id < len(particles):
        particle = particles[particle_id]
        # Calculate the magnitude of the current velocity
        velocity_magnitude = math.sqrt(particle.velocity[0] ** 2 + particle.velocity[1] ** 2)
        
        if velocity_magnitude > 0:
            # Normalize the velocity vector and scale it by the factor
            particle.velocity[0] += (particle.velocity[0] / velocity_magnitude) * factor
            particle.velocity[1] += (particle.velocity[1] / velocity_magnitude) * factor
            return True
    return False


def is_valid_position(x, y, radius, particles):
    for particle in particles:
        distance = math.sqrt((x - particle.x) ** 2 + (y - particle.y) ** 2)
        if distance < radius + particle.radius:  # Overlap detected
            return False
    return True

def spawn_particle(particles, window_width, window_height, radius, color):
    max_attempts = 100  # Limit the number of attempts to avoid infinite loops
    for _ in range(max_attempts):
        x = random.randint(radius, window_width - radius)
        y = random.randint(radius, window_height - radius)
        if is_valid_position(x, y, radius, particles):
            particles.append(Particle(x, y, radius, color, velocity=[random.uniform(-2, 2), random.uniform(-2, 2)]))
            return True  # Successfully spawned
    print("Failed to spawn particle after max attempts.")
    return False

particles = []

class Particle:
    def __init__(self, x, y, radius, color, velocity=[0, 0]):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.velocity = velocity

    def draw(self, win):
        pygame.draw.circle(win, self.color, (int(self.x), int(self.y)), self.radius)

    def update(self):
        global window_size, friction
        # Update position based on velocity
        self.x += self.velocity[0]
        self.y += self.velocity[1]

        # Apply friction to slow down the velocity
        self.velocity[0] *= (1 - friction)
        self.velocity[1] *= (1 - friction)

        # Check for collision with window boundaries
        if self.x - self.radius <= 0:
            self.x = self.radius  # Ensure particle stays within bounds
            self.velocity[0] = -self.velocity[0]  # Reverse velocity
        elif self.x + self.radius >= window_size[0]:
            self.x = window_size[0] - self.radius
            self.velocity[0] = -self.velocity[0]

        if self.y - self.radius <= 0:
            self.y = self.radius
            self.velocity[1] = -self.velocity[1]
        elif self.y + self.radius >= window_size[1]:
            self.y = window_size[1] - self.radius
            self.velocity[1] = -self.velocity[1]

        # Teleport particle if it's outside the edges
        edge_threshold = 21
        if self.x - self.radius < -edge_threshold or self.x + self.radius > window_size[0] + edge_threshold or \
           self.y - self.radius < -edge_threshold or self.y + self.radius > window_size[1] + edge_threshold:
            self.teleport_to_safe_location()

        # Ensure particles don't completely stop
        if abs(self.velocity[0]) < 0.01 and abs(self.velocity[1]) < 0.01:
            self.velocity = [random.uniform(-1, 1), random.uniform(-1, 1)]

    def teleport_to_safe_location(self):
        global window_size, particles
        max_attempts = 100
        for _ in range(max_attempts):
            new_x = random.randint(self.radius, window_size[0] - self.radius)
            new_y = random.randint(self.radius, window_size[1] - self.radius)
            if is_valid_position(new_x, new_y, self.radius, particles):
                self.x = new_x
                self.y = new_y
                return
        print("Failed to teleport particle to a safe location.")

    def is_colliding(self, other):
        # Check if this particle is colliding with another
        distance = math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)
        return distance <= self.radius + other.radius

    def get_collided_particle(self, particles):
        """Check for collisions and return the first colliding particle, or None if no collision."""
        for particle in particles:
            if particle is not self and self.is_colliding(particle):
                return particle
        return None

    def handle_collision(self, other):
        # Introduce random factors for velocity adjustment
        randomness_factor_self = [random.uniform(0.8, 1.2), random.uniform(0.8, 1.2)]
        randomness_factor_other = [random.uniform(0.8, 1.2), random.uniform(0.8, 1.2)]
        
        # Reverse and adjust velocities with randomness
        self.velocity[0] = -self.velocity[0] * randomness_factor_self[0]
        self.velocity[1] = -self.velocity[1] * randomness_factor_self[1]
        other.velocity[0] = -other.velocity[0] * randomness_factor_other[0]
        other.velocity[1] = -other.velocity[1] * randomness_factor_other[1]
        
        # Resolve overlap
        distance = math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)
        overlap = (self.radius + other.radius) - distance
        if overlap > 0:
            # Move particles apart
            try:
                dx = (self.x - other.x) / distance
                dy = (self.y - other.y) / distance
                
                self.x += dx * overlap / 2
                self.y += dy * overlap / 2
                other.x -= dx * overlap / 2
                other.y -= dy * overlap / 2
            
            except ZeroDivisionError:
                pass

# Create particles with random velocities
for _ in range(10):  # Spawn 100 particles
    if not spawn_particle(particles, window_size[0], window_size[1], 10, (255, 0, 0)):
        print("Could not spawn a particle. Screen might be too crowded.")

run = True
clock = 0.05
friction = 0.0
paused = False  # Global variable to track if the simulation is paused

while run:
    time.sleep(clock)
    win.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.VIDEORESIZE:
            window_size[0], window_size[1] = event.w, event.h
            win = pygame.display.set_mode((window_size[0], window_size[1]), pygame.RESIZABLE)
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            print("Mouse position: ({}, {})".format(mouse_x, mouse_y) + ", Particle index: " + str(find_particle_at_position(mouse_x, mouse_y, particles)))
            increase_velocity_of_particle(find_particle_at_position(mouse_x, mouse_y, particles=particles), particles, 2)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_EQUALS:
                clock += 0.01
            if event.key == pygame.K_MINUS:
                if clock > 0.01:
                    clock -= 0.01
                else:
                    print("Can't go below 0.01 on clock!")
            
            if event.key == pygame.K_1:
                clock = 0.001
            if event.key == pygame.K_2:
                clock = 0.002
            if event.key == pygame.K_3:
                clock = 0.003
            if event.key == pygame.K_4:
                clock = 0.004
            if event.key == pygame.K_5:
                clock = 0.005
            if event.key == pygame.K_6:
                clock = 0.006
            if event.key == pygame.K_7:
                clock = 0.007
            if event.key == pygame.K_8:
                clock = 0.008
            if event.key == pygame.K_9:
                clock = 0.009
            if event.key == pygame.K_0:
                clock = 0
            
            if event.key == pygame.K_m:
                friction = min(friction + 0.01, 1)  # Increase friction, max value 1
                print(f"Friction increased to {friction:.2f}")
            if event.key == pygame.K_n:
                friction = max(friction - 0.01, -1)  # Decrease friction, min value 0
                print(f"Friction decreased to {friction:.2f}")
            if event.key == pygame.K_e:
                if not spawn_particle(particles, window_size[0], window_size[1], 10, (255, 0, 0)):
                    print("Could not spawn a particle. Try again.")
            if event.key == pygame.K_p:  # Pause or unpause
                paused = not paused
                print("Paused" if paused else "Unpaused")
            if event.key == pygame.K_f:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for particle in particles:
                    # Check if the particle is within 50 pixels of the mouse
                    if abs(particle.x - mouse_x) < 50 and abs(particle.y - mouse_y) < 50:
                        # Calculate direction vector away from the mouse
                        dx = particle.x - mouse_x
                        dy = particle.y - mouse_y
                        distance = math.sqrt(dx**2 + dy**2)
                        if distance != 0:
                            dx /= distance
                            dy /= distance

                        # Increase velocity by 5 in the direction away from the mouse
                        particle.velocity[0] += dx * 5
                        particle.velocity[1] += dy * 5

    # Check collisions and update particles
    if not paused:  # Only update particle movement if not paused
        for i, particle in enumerate(particles):
            for j in range(i + 1, len(particles)):
                if particle.is_colliding(particles[j]):
                    particle.handle_collision(particles[j])

            particle.update()

    # Always draw particles
    for particle in particles:
        particle.draw(win)

    pygame.display.update()

