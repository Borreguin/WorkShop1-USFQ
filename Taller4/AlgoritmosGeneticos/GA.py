from generalSteps import *
import pandas as pd
import matplotlib.pyplot as plt
import decimal

class GA:
    def __init__(self, population, objetive, mutation_rate, n_iterations):
        self.population = population
        self.n_generation = 0
        self.n_iterations = n_iterations
        self.objetive = objetive
        self.mutation_rate = mutation_rate
        self.evaluation_type = AptitudeType.DEFAULT
        self.best_individual_selection_type = BestIndividualSelectionType.DEFAULT
        self.new_generation_type = NewGenerationType.DEFAULT

    def set_evaluation_type(self, evaluation_type: AptitudeType):
        self.evaluation_type = evaluation_type

    def set_best_individual_selection_type(self, _type:BestIndividualSelectionType):
        self.best_individual_selection_type = _type

    def set_new_generation_type(self, _type):
        self.new_generation_type = _type

    def run(self):
        success = False
        for _ in range(self.n_iterations):
            # las aptitudes son los valores que se obtienen al evaluar la función de aptitud
            aptitudes = [evaluate_aptitude(self.evaluation_type, individual, self.objetive) for individual in self.population]
            # el mejor individuo es el que tiene la mejor aptitud
            # (esto se puede elegir como maximo o minimo, depende de como se defina la aptitud)
            best_individual, best_aptitude = select_best_individual(self.best_individual_selection_type, self.population, aptitudes)
            # si el mejor individuo es igual al objetivo, se termina el algoritmo
            if best_individual == self.objetive:
                success = True
                print("Objetivo alcanzado:")
                print(f"Generación {self.n_generation}: {best_individual} - Aptitud: {best_aptitude}")
                return self.n_generation
            print(f"Generación {self.n_generation}: {best_individual} - población: {len(self.population)} - Aptitud: {best_aptitude}")

            # la nueva generación se obtiene a partir de la población actual, interactuando entre los individuos
            self.population = generate_new_population(self.new_generation_type, self.population, aptitudes, self.mutation_rate)
            self.n_generation += 1

        if not success:
            print(f"Objetivo no alcanzado en las iteraciones establecidas {self.n_iterations}")
            return 1001

def plot_scatter_with_line(df, x_column, y_column):
    # Crear el gráfico de dispersión
    plt.scatter(df[x_column], df[y_column], color='red')
    # Unir los puntos con una línea
    plt.plot(df[x_column], df[y_column], color='skyblue')
    # Agregar etiquetas de los valores en cada punto
    for index, value in enumerate(df[y_column]):
        plt.text(df[x_column][index], value, str(value), fontsize=8)
    # Títulos y etiquetas de los ejes
    plt.xlabel(x_column)
    plt.ylabel(y_column)
    plt.title(f'{y_column} vs {x_column}')
    # Mostrar el gráfico
    plt.show()


def case_study_1(_objetive):
    # Definición de la población inicial
    population = generate_population(100, len(_objetive))
    mutation_rate = 0.01
    n_iterations = 1000
    ga = GA(population, _objetive, mutation_rate, n_iterations)
    ga.run()

def case_study_2(_objetive):
    population = generate_population(100, len(_objetive))
    mutation_rate = 0.01
    n_iterations = 1000
    ga = GA(population, _objetive, mutation_rate, n_iterations)
    ga.set_evaluation_type(AptitudeType.BY_DISTANCE)
    ga.set_best_individual_selection_type(BestIndividualSelectionType.MIN_DISTANCE)
    ga.set_new_generation_type(NewGenerationType.MIN_DISTANCE)
    ga.run()

def case_study_2_mejorado(_objetive):
    population = generate_population(100, len(_objetive))
    mutation_rate = 0.01
    n_iterations = 1000
    ga = GA(population, _objetive, mutation_rate, n_iterations)
    ga.set_evaluation_type(AptitudeType.BY_DISTANCE)
    ga.set_best_individual_selection_type(BestIndividualSelectionType.MIN_DISTANCE)
    ga.set_new_generation_type(NewGenerationType.NEW)
    ga.run()
    
def case_study_3(_objetive):
    population = generate_population(100, len(_objetive))
    # Almacenar los resultados
    resultados_mutation_rate = pd.DataFrame(columns=['Mutation Rate', 'Generación de convergencia'])

    i = 0
    while i < 0.15:
        mutation = i
        mutation_rate = mutation
        n_iterations = 1000
        ga = GA(population, _objetive, mutation_rate, n_iterations)
        ga.set_evaluation_type(AptitudeType.BY_DISTANCE)
        ga.set_best_individual_selection_type(BestIndividualSelectionType.MIN_DISTANCE)
        ga.set_new_generation_type(NewGenerationType.MIN_DISTANCE)
        n_generation = ga.run()
        # Añade los resultados al DataFrame
        resultados_mutation_rate.loc[len(resultados_mutation_rate)] = {'Mutation Rate': mutation_rate, 'Generación de convergencia': n_generation}
        i += 0.01
    
    print(resultados_mutation_rate)
    resultados_mutation_rate.to_excel('resultados_mutation_rate.xlsx', index=False)
    plot_scatter_with_line(resultados_mutation_rate, 'Mutation Rate', 'Generación de convergencia')


def case_study_4(_objetive):
    # Almacenar los resultados
    resultados_population = pd.DataFrame(columns=['Population', 'Generación de convergencia'])

    for popul in range(10, 1000, 10): 
        population = generate_population(popul, len(_objetive))
        mutation_rate = 0.01
        n_iterations = 1000
        ga = GA(population, _objetive, mutation_rate, n_iterations)
        ga.set_evaluation_type(AptitudeType.BY_DISTANCE)
        ga.set_best_individual_selection_type(BestIndividualSelectionType.MIN_DISTANCE)
        ga.set_new_generation_type(NewGenerationType.NEW)
        n_generation = ga.run()
        # Añade los resultados al DataFrame
        resultados_population.loc[len(resultados_population)] = {'Population': len(population), 'Generación de convergencia': n_generation}
    
    print(resultados_population)
    resultados_population.to_excel('resultados_population.xlsx', index=False)
    plot_scatter_with_line(resultados_population, 'Population', 'Generación de convergencia')

def case_study_5(_objetive):
    population = generate_population(100, len(_objetive))
    mutation_rate = 0.01
    n_iterations = 1000
    ga = GA(population, _objetive, mutation_rate, n_iterations)
    ga.set_evaluation_type(AptitudeType.BY_DISTANCE)
    ga.set_best_individual_selection_type(BestIndividualSelectionType.MIN_DISTANCE)
    ga.set_new_generation_type(NewGenerationType.NEW)
    ga.run()

    
if __name__ == "__main__":
    objetive = "GA Workshop! USFQ"
    # case_study_1(objetive)
    # case_study_2(objetive)
    #case_study_2_mejorado(objetive)
    case_study_3(objetive)
    #case_study_4(objetive)
    #case_study_5(objetive)
    