import pygame
import time
import math
from lib.particle import Particle
from lib.utils import find_particle_at_position, spawn_particle
from lib.config import window_size, clock, friction

pygame.display.set_caption('Particle Simulator')
win = pygame.display.set_mode(window_size, pygame.RESIZABLE)

# Initialize particles
particles = []
for _ in range(10):
    if not spawn_particle(particles, window_size[0], window_size[1], 10, (255, 0, 0)):
        print("Could not spawn a particle.")

paused = False
run = True

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
            particle_index = find_particle_at_position(mouse_x, mouse_y, particles)
            if particle_index is not None:
                print(f"Mouse position: ({mouse_x}, {mouse_y}), Particle index: {particle_index}")
                particles[particle_index].velocity[0] += 2
                particles[particle_index].velocity[1] += 2

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_EQUALS:
                clock += 0.01
            elif event.key == pygame.K_MINUS:
                clock = max(clock - 0.01, 0.01)

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
                friction = min(friction + 0.01, 1.0)
                print(f"Friction increased to {friction:.2f}")
            elif event.key == pygame.K_n:
                friction = max(friction - 0.01, 0.0)
                print(f"Friction decreased to {friction:.2f}")

            if event.key == pygame.K_e:
                if not spawn_particle(particles, window_size[0], window_size[1], 10, (255, 0, 0)):
                    print("Could not spawn a particle. Try again.")

            if event.key == pygame.K_p:
                paused = not paused
                print("Paused" if paused else "Unpaused")

            if event.key == pygame.K_f:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for particle in particles:
                    dx = particle.x - mouse_x
                    dy = particle.y - mouse_y
                    distance = math.sqrt(dx**2 + dy**2)
                    if distance < 50 and distance != 0:
                        particle.velocity[0] += dx / distance * 5
                        particle.velocity[1] += dy / distance * 5

    if not paused:
        for i, particle in enumerate(particles):
            for j in range(i + 1, len(particles)):
                if particle.is_colliding(particles[j]):
                    particle.handle_collision(particles[j])
            particle.update(window_size, friction, particles)

    for particle in particles:
        particle.draw(win)

    pygame.display.update()
