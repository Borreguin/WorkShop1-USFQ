import random
from constants import *
from util import *


def parent_selection(_type: ParentSelectionType, population, aptitudes, pareja=None):
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
        
        
        def obtener_individuo_por_posicion(poblacion, aptitudes, pareja):
            # Combinar las listas en una sola para ordenarlas juntas
            combinada = list(zip(population, aptitudes))

            # Ordenar basado en el valor de la primera columna de los datos (i[1][0])
            combinada_ordenada = sorted(combinada, key=lambda i: i[1][0])

            # Descomprimir las listas ordenadas
            nombres_ordenados, aptitudes_ordenadas = zip(*combinada_ordenada)

            # Obtener el individuo en la posición especificada
            individuo_en_posicion = nombres_ordenados[pareja]
            aptitudes_en_posicion = aptitudes_ordenadas[pareja][1]
            
            return individuo_en_posicion, aptitudes_en_posicion

        # Obtener el individuo en la posición especificada
        parent1, aptitudes1 = obtener_individuo_por_posicion(population, aptitudes, 2*pareja)#pareja)#)
        parent2, aptitudes2 = obtener_individuo_por_posicion(population, aptitudes, 2*pareja+1)#99-pareja)#)            
        
        return parent1, parent2, aptitudes1, aptitudes2


def crossover(_type: CrossoverType, parent1, parent2, aptitudes1=None, aptitudes2=None):
    if _type == CrossoverType.DEFAULT:
        # Cruce de dos padres para producir descendencia
        crossover_point = random.randint(1, len(parent1) - 1)
        child1 = parent1[:crossover_point] + parent2[crossover_point:]
        child2 = parent2[:crossover_point] + parent1[crossover_point:]
        return child1, child2
    if _type == CrossoverType.NEW:
        child1 = []
        child2 = []

        for i in range(len(parent1)):
            if random.randint(0,1) == 1:
                child1.append(parent1[i])
                child2.append(parent2[i])
            else:
                child1.append(parent2[i])
                child2.append(parent1[i])
        
        child1 = ''.join(child1) 
        child2 = ''.join(child2)

        return child1, child2

        # child1=""
        # for i in range(len(parent1)):
        #     if aptitudes1[i] < aptitudes2[i]:
        #         child1 = child1 + parent1[i]
        #     else:
        #         child1 = child1 + parent2[i]
        # return child1`


def mutate(_type: MutationType, individual, mutation_rate):
    if _type == MutationType.DEFAULT:
        # Mutación de un individuo
        for i in range(len(individual)):
            if random.random() < mutation_rate:
                individual = individual[:i] + random.choice(all_possible_gens) + individual[i + 1:]
        return individual
    if _type == MutationType.NEW:
        '''MUTACION UNIFORME'''
        individual = list(individual)  # Convertir a lista para mutación
        for i in range(len(individual)):
            if random.random() < mutation_rate:  # Verificar probabilidad de mutación
                # Seleccionar un nuevo gen aleatoriamente que sea diferente al actual
                new_gen = random.choice([gen for gen in all_possible_gens if gen != individual[i]])
                individual[i] = new_gen
        return ''.join(individual)  # Convertir de vuelta a string