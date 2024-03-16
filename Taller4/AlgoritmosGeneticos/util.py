from typing import List


def word_to_array(word: str):
    return [ord(w) for w in word]

''' Posibles códigos del ejercicio:
| Carácter | Código Unicode |
|----------|----------------|
|    a     |       97       |
|    b     |       98       |
|    c     |       99       |
|    d     |      100       |
|    e     |      101       |
|    f     |      102       |
|    g     |      103       |
|    h     |      104       |
|    i     |      105       |
|    j     |      106       |
|    k     |      107       |
|    l     |      108       |
|    m     |      109       |
|    n     |      110       |
|    o     |      111       |
|    p     |      112       |
|    q     |      113       |
|    r     |      114       |
|    s     |      115       |
|    t     |      116       |
|    u     |      117       |
|    v     |      118       |
|    w     |      119       |
|    x     |      120       |
|    y     |      121       |
|    z     |      122       |
|    A     |      65        |
|    B     |      66        |
|    C     |      67        |
|    D     |      68        |
|    E     |      69        |
|    F     |      70        |
|    G     |      71        |
|    H     |      72        |
|    I     |      73        |
|    J     |      74        |
|    K     |      75        |
|    L     |      76        |
|    M     |      77        |
|    N     |      78        |
|    O     |      79        |
|    P     |      80        |
|    Q     |      81        |
|    R     |      82        |
|    S     |      83        |
|    T     |      84        |
|    U     |      85        |
|    V     |      86        |
|    W     |      87        |
|    X     |      88        |
|    Y     |      89        |
|    Z     |      90        |
|(espacio) |      32        |
|    !     |      33        |

* Las poblaciones están compuestas por elementos del mismo número de caracteres del objetivo, no se necesita querer aumentar 
las distancias entre los elementos de la población y el objetivo utilizando esto. Estas líneas de código podrían ser retiradas.


* Se deben manejar las distancias entre caracteres en valor absoluto ya que son diferencias relativas.

* Para este método, no se cuenta con una lógica clara que administre la diferencia de "distancias" entre códigos unicode, por lo que se asume
que la distancia entre dos palabras es la suma de las diferencias absolutas entre los códigos unicode de los caracteres de las palabras.
La codificación propia del UNICODE agrega información en pro de encontrar el objetivo en comparación a la comparación básica
del caso 1 ya que encuentra la solución mucho más rápido: Generación 982 vs. Generación 378.

* La evaluación para crear nuevas generaciones se realiza en función de minimizar la distancia entre las palabras, al contrario del caso 1 que se debía
maximizar las coincidencias.

'''

# Algo no está bien con esta función de distancia
def distance(list1:List[int], list2:List[int]):
    acc = 0
    lista_palabra=[]
    for e1, e2 in zip(list1, list2):
        #Las diferencias entre los valores unicode de los individuos debe ser absoluta.
        acc += abs(e1 - e2)
        lista_palabra.append(abs(e1 - e2))
    n_size = min(len(list1), len(list2))
    if n_size == 0:
        return None
    return acc + (len(list1) - len(list2)), lista_palabra

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