from typing import List
import math

def word_to_array(word: str):
    return [ord(w) for w in word]

# Algo no está bien con esta función de distancia
def manhattan_distance(list1: List[int], list2: List[int]) -> float:
    if len(list1) != len(list2):
        raise ValueError("Lists must be of equal length")

    manhattan_dist = sum(abs(x - y) for x, y in zip(list1, list2))
    return manhattan_dist

def distance(list1: List[int], list2: List[int]):
    if len(list1) != len(list2):
        raise ValueError("Lists must be of equal length")

    squared_diff = sum((x - y) ** 2 for x, y in zip(list1, list2))
    euclidean_dist = math.sqrt(squared_diff)
    return euclidean_dist

def word_distance(word1:str, word2:str):
    return distance(word_to_array(word1), word_to_array(word2))

def choose_best_individual_by_distance(population, aptitudes):
    best_individual = population[0]
    best_aptitude = aptitudes[0]
    for ind, apt in zip(population, aptitudes):
        if apt < best_aptitude:
            best_aptitude = apt
            best_individual = ind
    return best_individual



# print(word_distance("abc", "abc"))
# print(word_distance("abc", "abd"))
# print(word_distance("abc", "abz"))
# print(word_distance("abc", "cba"))
# print(word_distance("abc", "cbad"))