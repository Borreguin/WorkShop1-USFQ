from typing import List


def word_to_array(word: str):
    return [ord(w) for w in word]

# Algo no está bien con esta función de distancia (actualizacion: funcion corregida)
def distance(list1: List[int], list2: List[int]):
    acc = 0
    for e1, e2 in zip(list1, list2):
        acc += abs(e1 - e2)  # Uso de valor absoluto para la diferencia de cada par
    diff_len = abs(len(list1) - len(list2))  # Diferencia absoluta de longitud
    acc += diff_len  # Considerar un costo por la diferencia de longitud
    if len(list1) == 0 and len(list2) == 0:
        return None
    return acc

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