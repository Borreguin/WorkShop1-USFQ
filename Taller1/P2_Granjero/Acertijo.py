import matplotlib.pyplot as plt
from collections import deque

# Reimplement the plotting within the puzzle solution for a complete grid at the end

# Initialize the plot
fig, ax = plt.subplots(figsize=(12, 6))

# Set up the plot space
items = ['Farmer', 'Wolf', 'Goat', 'Cabbage']
ax.set_xlim(-0.5, 7.5)
ax.set_ylim(-1, len(items))
ax.set_xticks(range(8))  # 7 steps plus the start and end
ax.set_xticklabels(['Start', '1', '2', '3', '4', '5', '6', 'End'])
ax.set_yticks(range(len(items)))
ax.set_yticklabels(items)
ax.set_title('Farmer, Wolf, Goat, and Cabbage River Crossing')

# Draw the grid for each step
for x in range(8):  # 7 steps including start and end
    for y in range(len(items)):
        ax.add_patch(plt.Rectangle((x - 0.5, y - 0.5), 1, 1, fill=None, edgecolor='black', lw=1))

# Solve the farmer puzzle
def solve_farmer_puzzle():
    # Possible states (farmer, wolf, goat, cabbage)
    # 0 means on the original side, 1 means on the other side.
    start_state = (0, 0, 0, 0)
    end_state = (1, 1, 1, 1)

    # Rules that must never be broken
    def is_valid(state):
        # Farmer must be with the wolf or goat or on the same side as both
        if state[1] == state[2] and state[0] != state[1]:
            return False
        # Farmer must be with the goat or cabbage or on the same side as both
        if state[2] == state[3] and state[0] != state[2]:
            return False
        return True

    # Generate possible next moves
    def next_moves(state):
        moves = []
        # Try moving each object (including just the farmer himself)
        for i in range(1, 4):
            new_state = list(state)
            # Move only if both farmer and object are on the same side
            if state[0] == state[i]:
                # Move farmer and the object
                new_state[0] = 1 - state[0]
                new_state[i] = 1 - state[i]
                # Check if the new state is valid
                if is_valid(tuple(new_state)):
                    moves.append(tuple(new_state))
        # Farmer goes alone
        new_state = list(state)
        new_state[0] = 1 - state[0]
        if is_valid(tuple(new_state)):
            moves.append(tuple(new_state))
        return moves

    # Perform a breadth-first search
    queue = deque([(start_state, [])])
    visited = set()

    while queue:
        current_state, path = queue.popleft()
        # Check if we are at the end state
        if current_state == end_state:
            return path + [end_state]

        visited.add(current_state)

        for move in next_moves(current_state):
            if move not in visited:
                queue.append((move, path + [current_state]))

    return None

# Plot the positions
def plot_positions(states):
    # Plot the positions of the farmer, wolf, goat, and cabbage for each step
    for step, state in enumerate(states):
        for i, position in enumerate(state):
            color = 'green' if position == 1 else 'red'
            ax.plot(step, i, 'o', color=color, markersize=10)

# Run the puzzle solver
solution = solve_farmer_puzzle()

# Plot the final positions
plot_positions(solution)

# Add legend
red_patch = plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='r', markersize=10, label='Original side')
green_patch = plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='g', markersize=10, label='Other side')
ax.legend(handles=[red_patch, green_patch], loc='upper right')

plt.show()










