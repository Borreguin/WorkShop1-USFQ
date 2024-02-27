import matplotlib.pyplot as plt

def print_towers(towers):
    # Function to print the towers graphically
    fig, ax = plt.subplots()
    n_disks = sum(len(t) for t in towers)
    tower_width = max(n_disks / 2, 1)
    disk_height = 1
    tower_height = n_disks * disk_height
    tower_distance = n_disks * 1.5
    tower_positions = [i * tower_distance for i in range(3)]
    colors = ['red', 'green', 'blue', 'yellow', 'purple', 'orange', 'pink', 'brown', 'grey', 'cyan']

    # Draw the towers
    for pos in tower_positions:
        ax.plot([pos, pos], [0, tower_height], color='brown', linewidth=tower_width)

    # Draw the disks
    for i, tower in enumerate(towers):
        for j, disk in enumerate(tower):
            left = tower_positions[i] - disk / 2
            bottom = j * disk_height
            color = colors[(disk - 1) % len(colors)]
            ax.add_patch(plt.Rectangle((left, bottom), disk, disk_height, color=color))

    ax.set_aspect('equal')
    ax.axis('off')
    plt.xlim(-tower_width, max(tower_positions) + tower_width)
    plt.ylim(0, tower_height + disk_height)

    plt.show()


def move_disk(towers, from_tower, to_tower):
    # Function to move a disk from one tower to another
    towers[to_tower].append(towers[from_tower].pop())
    print_towers(towers)


def solve_hanoi(towers, n, from_tower, to_tower, aux_tower):
    # Recursive function to solve the puzzle
    if n == 0:
        return
    solve_hanoi(towers, n - 1, from_tower, aux_tower, to_tower)
    move_disk(towers, from_tower, to_tower)
    solve_hanoi(towers, n - 1, aux_tower, to_tower, from_tower)


# Initialize the towers with 3 disks
towers = [[3, 2, 1], [], []]

# Print the initial state of the towers
print_towers(towers)

# Solve the puzzle
solve_hanoi(towers, len(towers[0]), 0, 2, 1)



if __name__ == '__main__':
    print("Implementa tu código aquí")
