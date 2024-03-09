from collections import deque

class State:
    def __init__(self, farmer, wolf, sheep, lettuce):
        self.farmer = farmer
        self.wolf = wolf
        self.sheep = sheep
        self.lettuce = lettuce

    def is_valid(self):
        if self.wolf == self.sheep and self.farmer != self.wolf:
            return False
        if self.sheep == self.lettuce and self.farmer != self.sheep:
            return False
        return True

    def is_goal(self):
        return self.farmer == 1 and self.wolf == 1 and self.sheep == 1 and self.lettuce == 1

    def __eq__(self, other):
        return self.farmer == other.farmer and self.wolf == other.wolf and self.sheep == other.sheep and self.lettuce == other.lettuce

    def __hash__(self):
        return hash((self.farmer, self.wolf, self.sheep, self.lettuce))

    def __str__(self):
        return f"Farmer: {'W' if self.farmer == 1 else 'E'}, Wolf: {'W' if self.wolf == 1 else 'E'}, Sheep: {'W' if self.sheep == 1 else 'E'}, Lettuce: {'W' if self.lettuce == 1 else 'E'}"

def get_next_states(current_state):
    next_states = []
    for move in [(1, 0, 0, 0), (-1, 0, 0, 0), (1, 1, 0, 0), (-1, -1, 0, 0), (1, 0, 1, 0), (-1, 0, -1, 0), (1, 0, 0, 1), (-1, 0, 0, -1)]:
        new_state = State(current_state.farmer + move[0], current_state.wolf + move[1], current_state.sheep + move[2], current_state.lettuce + move[3])
        if 0 <= new_state.farmer <= 1 and 0 <= new_state.wolf <= 1 and 0 <= new_state.sheep <= 1 and 0 <= new_state.lettuce <= 1 and new_state.is_valid():
            next_states.append(new_state)
    return next_states

def bfs():
    start_state = State(0, 0, 0, 0)
    if start_state.is_goal():
        return [start_state]
    visited = set()
    queue = deque([(start_state, [])])
    while queue:
        current_state, path = queue.popleft()
        for next_state in get_next_states(current_state):
            if next_state not in visited:
                if next_state.is_goal():
                    return path + [current_state, next_state]
                visited.add(next_state)
                queue.append((next_state, path + [current_state]))

solution = bfs()
if solution:
    for i, state in enumerate(solution):
        print(f"Step {i+1}: {state}")
else:
    print("No solution found.")
