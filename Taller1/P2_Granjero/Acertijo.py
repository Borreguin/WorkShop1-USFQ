import networkx as nx
import matplotlib.pyplot as plt

# Define the problem states and transitions
def valid_state(state):
    """ Check if a state is valid based on the problem's constraints """
    # State representation: (farmer, wolf, goat, cabbage)
    # The farmer must be with the goat, wolf, or cabbage if they are on the same side
    f, w, g, c = state
    if g == w and f != g:
        return False  # The wolf will eat the goat
    if g == c and f != g:
        return False  # The goat will eat the cabbage
    return True

def generate_states():
    """ Generate all possible valid states """
    states = []
    for state in [(f, w, g, c) for f in ['L', 'R'] for w in ['L', 'R'] 
                                     for g in ['L', 'R'] for c in ['L', 'R']]:
        if valid_state(state):
            states.append(state)
    return states

def generate_edges(states):
    """ Generate all possible valid transitions between states """
    edges = []
    for state in states:
        f, w, g, c = state
        # The farmer can take the wolf, the goat, or the cabbage, or go alone
        # Generate new states based on possible movements
        if f == 'L':
            new_side = 'R'
        else:
            new_side = 'L'
        
        # Move the farmer alone
        new_state = (new_side, w, g, c)
        if new_state in states:
            edges.append((state, new_state))
        
        # Move the farmer with the wolf
        if w == f:
            new_state = (new_side, new_side, g, c)
            if new_state in states:
                edges.append((state, new_state))
        
        # Move the farmer with the goat
        if g == f:
            new_state = (new_side, w, new_side, c)
            if new_state in states:
                edges.append((state, new_state))
        
        # Move the farmer with the cabbage
        if c == f:
            new_state = (new_side, w, g, new_side)
            if new_state in states:
                edges.append((state, new_state))
    
    return edges

# Generate the graph
def create_graph():
    states = generate_states()
    edges = generate_edges(states)
    G = nx.DiGraph()
    G.add_nodes_from(states)
    G.add_edges_from(edges)
    return G

if __name__ == "__main__":
    # Create the graph and plot it
    G = create_graph()

    # We will use a spring layout for the graph positions, 
    # but other layouts like circular can also be used depending on the visualization requirement
    pos = nx.spring_layout(G, seed=42)  # Seed for reproducible layout

    # Draw the graph
    plt.figure(figsize=(12, 8))  # Set the size of the graph
    nx.draw(G, pos, with_labels=True, node_size=2500, node_color='lightblue', font_size=10, font_weight='bold', arrows=True)
    plt.title('Farmer, Wolf, Goat, and Cabbage Problem')
    plt.annotate("[L,L,L,L] represents that Farmer is in Left, Wolf in Left, Goat in Left, Cabbage in Left", xy = (0, -0.52))
    plt.show()
