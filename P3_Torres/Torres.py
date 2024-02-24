import pygame
import sys
import time

# Set up Pygame
pygame.init()

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Set up display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tower of Hanoi")

# Define tower positions
tower_positions = [(WIDTH // 4, HEIGHT - 50), (WIDTH // 2, HEIGHT - 50), (3 * WIDTH // 4, HEIGHT - 50)]

# Initialize towers with discs
towers = [[3, 2, 1], [], []]

# Function to draw towers and discs
def draw_towers():
    screen.fill(WHITE)

    for i, (x, y) in enumerate(tower_positions):
        pygame.draw.rect(screen, BLACK, (x - 5, y - 150, 10, 150))  # Tower
        for j, disc in enumerate(towers[i]):
            disc_width = disc * 50
            pygame.draw.rect(screen, RED, (x - disc_width // 2, y - 10 - j * 20, disc_width, 20))  # Disc

    pygame.display.flip()

# Function to move a disc from one tower to another
def move_disc(source, target):
    disc = towers[source].pop()
    towers[target].append(disc)
    draw_towers()
    time.sleep(0.5)

# Recursive function to solve Tower of Hanoi
def tower_of_hanoi(n, source, target, auxiliary):
    if n > 0:
        tower_of_hanoi(n - 1, source, auxiliary, target)
        move_disc(source, target)
        tower_of_hanoi(n - 1, auxiliary, target, source)

# Main function
def main():
    draw_towers()
    tower_of_hanoi(3, 0, 2, 1)  # Solve Tower of Hanoi with 3 discs

    # Handle exit
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

if __name__ == "__main__":
    main()
