import itertools
import matplotlib.pyplot as plt


def calculate_distance(city1, city2):
    # Calculate Euclidean distance between two cities
    return ((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2) ** 0.5


def plot_tsp_solution(cities, optimal_route):
    # Plot the cities
    plt.figure(figsize=(8, 6))
    plt.scatter([city[0] for city in cities.values()], [city[1] for city in cities.values()], c='blue', zorder=5)
    for city_name, city_coord in cities.items():
        plt.text(city_coord[0], city_coord[1], city_name, fontsize=12, ha='right')

    # Plot the optimal route
    optimal_route = list(optimal_route) + [optimal_route[0]]  # Closing the loop
    for i in range(len(optimal_route) - 1):
        city1 = optimal_route[i]
        city2 = optimal_route[i + 1]
        plt.plot([cities[city1][0], cities[city2][0]], [cities[city1][1], cities[city2][1]], c='red', zorder=10)

    plt.title("TSP Solution")
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.grid(True)
    plt.show()


def tsp_brute_force_plot(cities):
    # Generate all possible permutations of cities
    permuted_cities = itertools.permutations(cities)

    min_distance = float('inf')
    optimal_route = None

    # Iterate through each permutation
    for permuted_city_list in permuted_cities:
        distance = 0
        # Calculate the total distance for the current permutation
        for i in range(len(permuted_city_list) - 1):
            distance += calculate_distance(permuted_city_list[i], permuted_city_list[i + 1])
        # Add distance from the last city back to the start city
        distance += calculate_distance(permuted_city_list[-1], permuted_city_list[0])

        # Update minimum distance and optimal route if applicable
        if distance < min_distance:
            min_distance = distance
            optimal_route = permuted_city_list

    return min_distance, optimal_route


# Example usage:
# Define the cities as (x, y) coordinates
cities = {'A': (0, 0), 'B': (1, 3), 'C': (2, 1), 'D': (4, 2)}

# Solve TSP and get the optimal route
min_distance, optimal_route = tsp_brute_force_plot(cities.values())

# Plot the TSP solution
plot_tsp_solution(cities, optimal_route)
