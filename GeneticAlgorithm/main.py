import numpy,math
import GA

# given weights
genes_weights = [0.2,0.3,0.5,0.1]
# given number of weights/genes
num_weights = 4

# solutions/chromosomes generated per population
sol_per_pop = 8
# number of parents to select
num_parents = 4
# crossover probability
Pco = 0.95
# mutation probability 
Pmut = 0.1
# stopping criteria
target_fitness = 0.6
current_fitness = -math.inf
generation = 1

# defining population size
pop_size = (sol_per_pop,num_weights)

# initial randomly generated population
new_population = numpy.random.randint(low=0, high=2, size=pop_size)

# verify selected parents by given constrains
def constrains_validation(to_verify):
    capital_year_one = [0.5,1.0,1.5,0.1]
    capital_year_two = [0.3,0.8,1.5,0.4]
    capital_year_three = [0.2,0.2,0.3,0.1]
    budget_year_one = 3.1
    budget_year_two = 2.5
    budget_year_three = 0.4
    return (numpy.sum(numpy.multiply(to_verify,capital_year_one)) <= budget_year_one and \
        numpy.sum(numpy.multiply(to_verify,capital_year_two)) <= budget_year_two and \
        numpy.sum(numpy.multiply(to_verify,capital_year_three)) <= budget_year_three)

# stop when reach target fitness
while current_fitness < target_fitness:
#while generation <5:
    print(" ")
    print("Generation :", generation)
    print("Population:")
    print("",new_population)

    # calculate the fitness of each chromosome in the population
    fitness = GA.cal_pop_fitness(genes_weights, new_population)
    print("Fitness :")
    print("",fitness)

    # select the best parents in the population
    parents, fitness = GA.select_parents(new_population, fitness, num_parents, constrains_validation)
    print("Parents :")
    print("",parents)

    # local best solution
    current_fitness = numpy.max(fitness)
    print("Current Best Fitness :",current_fitness)
    
    # check stoping criteria and show final results
    if current_fitness >= target_fitness:
        total_fitness = len(numpy.where(fitness == numpy.max(fitness))[0])
        for i in range(total_fitness):
            best_match_idx = numpy.where(fitness == numpy.max(fitness))[0][i]
            if constrains_validation(new_population[best_match_idx,:]):
                print("-------------------------------")
                print("Crossover Probability Pco:",Pco)
                print("Mutation Probability Pmut:",Pmut)
                print("Size Of Population:",new_population.shape[0])
                print("Size Of Mating Pool:",num_parents)
                print("Stoping Fitness:",target_fitness)
                print("Final Solution ",new_population[best_match_idx,:])
                print("Final Fitness ",current_fitness)
                break
        break
    # crossover parents in the middle based on Pco(default 0.95)
    offspring_crossover = GA.crossover(parents, offspring_size=(pop_size[0]-parents.shape[0], num_weights))
    print("Offsprings :")
    print("",offspring_crossover)

    # add variations to offsrpings using mutation based on Pmut(default 0.1)
    offspring_mutation = GA.mutation(offspring_crossover)
    print("Mutations :")
    print("",offspring_mutation)

    # create next population based on the parents and offsprings
    new_population[0:parents.shape[0], :] = parents
    new_population[parents.shape[0]:, :] = offspring_mutation

    generation += 1
