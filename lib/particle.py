import pygame
import math
import random

class Particle:
    def __init__(self, x, y, radius, color, velocity=[0, 0]):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.velocity = velocity

    def draw(self, win):
        pygame.draw.circle(win, self.color, (int(self.x), int(self.y)), self.radius)

    def update(self, window_size, friction, particles):
        self.x += self.velocity[0]
        self.y += self.velocity[1]

        self.velocity[0] *= (1 - friction)
        self.velocity[1] *= (1 - friction)

        if self.x - self.radius <= 0:
            self.x = self.radius
            self.velocity[0] = -self.velocity[0]
        elif self.x + self.radius >= window_size[0]:
            self.x = window_size[0] - self.radius
            self.velocity[0] = -self.velocity[0]

        if self.y - self.radius <= 0:
            self.y = self.radius
            self.velocity[1] = -self.velocity[1]
        elif self.y + self.radius >= window_size[1]:
            self.y = window_size[1] - self.radius
            self.velocity[1] = -self.velocity[1]

        if abs(self.velocity[0]) < 0.01 and abs(self.velocity[1]) < 0.01:
            self.velocity = [random.uniform(-1, 1), random.uniform(-1, 1)]

    def is_colliding(self, other):
        distance = math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)
        return distance <= self.radius + other.radius

    def handle_collision(self, other):
        randomness_self = [random.uniform(0.8, 1.2), random.uniform(0.8, 1.2)]
        randomness_other = [random.uniform(0.8, 1.2), random.uniform(0.8, 1.2)]

        self.velocity[0] = -self.velocity[0] * randomness_self[0]
        self.velocity[1] = -self.velocity[1] * randomness_self[1]
        other.velocity[0] = -other.velocity[0] * randomness_other[0]
        other.velocity[1] = -other.velocity[1] * randomness_other[1]

        distance = math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)
        overlap = (self.radius + other.radius) - distance
        if overlap > 0:
            dx = (self.x - other.x) / distance
            dy = (self.y - other.y) / distance

            self.x += dx * overlap / 2
            self.y += dy * overlap / 2
            other.x -= dx * overlap / 2
            other.y -= dy * overlap / 2