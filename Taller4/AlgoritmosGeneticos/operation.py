import random
from constants import *
from util import *


def parent_selection(_type: ParentSelectionType, population, aptitudes):
    if _type == ParentSelectionType.DEFAULT:
        # Selección de padres por ruleta
        cumulative = sum(aptitudes)
        selection_probability = [aptitude / cumulative for aptitude in aptitudes]
        parents = random.choices(population, weights=selection_probability, k=2)
        return parents
    if _type == ParentSelectionType.MIN_DISTANCE:
        # seleccionando randomicamente dos poblaciones diferentes para cada padre
        # se podria seleccionar de otra manera?
        partition_size = random.randint(1, len(population)-1)
        parent1 = choose_best_individual_by_distance(population[:partition_size], aptitudes[:partition_size])
        parent2 = choose_best_individual_by_distance(population[partition_size:], aptitudes[partition_size:])
        return parent1, parent2

    if _type == ParentSelectionType.NEW:
        print("implement here the new parent selection")
        return None
    
    elif _type == ParentSelectionType.RANK:
        return rank_selection(population, aptitudes)

def crossover(_type: CrossoverType, parent1, parent2):
    if _type == CrossoverType.DEFAULT:
        # Cruce de dos padres para producir descendencia
        crossover_point = random.randint(1, len(parent1) - 1)
        child1 = parent1[:crossover_point] + parent2[crossover_point:]
        child2 = parent2[:crossover_point] + parent1[crossover_point:]
        return child1, child2
    if _type == CrossoverType.NEW:
        print("implement here the new crossover")
        return None
    
    elif _type == CrossoverType.TWO_POINT:
        return two_point_crossover(parent1, parent2)

def mutate(_type: MutationType, individual, mutation_rate):
    if _type == MutationType.DEFAULT:
        # Mutación de un individuo
        for i in range(len(individual)):
            if random.random() < mutation_rate:
                individual = individual[:i] + random.choice(all_possible_gens) + individual[i + 1:]
        return individual
    if _type == MutationType.NEW:
        print("implement here the new mutation")
        return None
    
def tournament_selection(population, aptitudes, tournament_size=3):
    selected_parents = []
    for _ in range(2):  # Seleccionar dos padres
        participants = random.sample(list(zip(population, aptitudes)), tournament_size)
        winner = min(participants, key=lambda x: x[1])
        selected_parents.append(winner[0])
    return selected_parents[0], selected_parents[1]

def uniform_crossover(parent1, parent2):
    child1, child2 = '', ''
    for i in range(len(parent1)):
        if random.random() < 0.5:
            child1 += parent1[i]
            child2 += parent2[i]
        else:
            child1 += parent2[i]
            child2 += parent1[i]
    return child1, child2

def swap_mutation(individual, mutation_rate):
    if random.random() < mutation_rate:
        index1, index2 = random.sample(range(len(individual)), 2)
        individual = list(individual)
        individual[index1], individual[index2] = individual[index2], individual[index1]
        individual = ''.join(individual)
    return individual

def rank_selection(population, aptitudes):
    ranked_population = [x for _, x in sorted(zip(aptitudes, population))]
    selection_probabilities = [((rank+1)/len(population)) for rank in range(len(population))]
    parents = random.choices(ranked_population, weights=selection_probabilities, k=2)
    return parents

def two_point_crossover(parent1, parent2):
    if len(parent1) < 3:
        return parent1, parent2
    crossover_point1 = random.randint(1, len(parent1)//2)
    crossover_point2 = random.randint(crossover_point1+1, len(parent1)-1)
    child1 = parent1[:crossover_point1] + parent2[crossover_point1:crossover_point2] + parent1[crossover_point2:]
    child2 = parent2[:crossover_point1] + parent1[crossover_point1:crossover_point2] + parent2[crossover_point2:]
    return child1, child2
