import numpy,math,random

def cal_pop_fitness(genes_weights, pop):
    fitness = numpy.sum(pop*genes_weights, axis = 1)
    return fitness

def select_parents(pop, fitness, num_parents, constrains_validation = None):
    parents = numpy.empty((num_parents, pop.shape[1]))
    copy_fitness = numpy.copy(fitness)
    num_selected = 0
    num_turn = 0
    valid_fitness = numpy.full(fitness.shape[0], -math.inf)

    if constrains_validation == None:
        print("No Constrains!")
        for parent_num in range(num_parents):
            max_fitness_idx = numpy.where(fitness == numpy.max(fitness))
            max_fitness_idx = max_fitness_idx[0][0]
            parents[parent_num, :] = pop[max_fitness_idx, :]
            fitness[max_fitness_idx] = -math.inf
        valid_fitness = fitness
    else:
        while num_selected < num_parents:
            if num_turn < pop.shape[0]:
                max_fitness_idx = numpy.where(fitness == numpy.max(fitness))
                max_fitness_idx = max_fitness_idx[0][0]
                to_be_verify = pop[max_fitness_idx, :]
                if constrains_validation(to_be_verify) == True:
                    print("Population",max_fitness_idx,"Pass Constrains Validation!")
                    parents[num_selected, :] = to_be_verify
                    copy_fitness[max_fitness_idx] = -math.inf
                    num_selected = num_selected + 1
                    valid_fitness[max_fitness_idx] = fitness[max_fitness_idx]
                else:
                    print("Population",max_fitness_idx,"Fail Constrains Validation!")

                fitness[max_fitness_idx] = -math.inf
                num_turn = num_turn + 1
            else:
                print("No more valid parents,choose high fitness invalid parents")
                max_fitness_idx = numpy.where(copy_fitness == numpy.max(copy_fitness))
                max_fitness_idx = max_fitness_idx[0][0]
                parents[num_selected, :] = pop[max_fitness_idx, :]
                copy_fitness[max_fitness_idx] = -math.inf
                num_selected = num_selected + 1
    return parents, valid_fitness

def crossover(parents, offspring_size, Pco = 0.95):
    offspring = numpy.empty(offspring_size)
    crossover_point = numpy.uint8(offspring_size[1]/2)

    for k in range(offspring_size[0]//2):
        parent1_idx = (k*2)%parents.shape[0]
        parent2_idx = (k*2+1)%parents.shape[0]
        if random.random() < Pco:
            print("Crossover Between Parents (",parent1_idx,"<->",parent2_idx,")")
            offspring[k*2, 0:crossover_point] = parents[parent1_idx, 0:crossover_point]
            offspring[k*2, crossover_point:] = parents[parent2_idx, crossover_point:]
            offspring[k*2+1, 0:crossover_point] = parents[parent2_idx, 0:crossover_point]
            offspring[k*2+1, crossover_point:] = parents[parent1_idx, crossover_point:]
        else:
            print("NO Crossover!")            
            offspring[k*2, :] = parents[parent1_idx, :]
            offspring[k*2+1, :] = parents[parent2_idx, :]
            
    return offspring

def mutation(offspring_crossover, Pmut = 0.1):
    for i in range(offspring_crossover.shape[0]):
        for j in range(offspring_crossover.shape[1]):
            if random.random() < Pmut:
                print("Mutation at",j,"th bit of chromosome",i)
                if offspring_crossover[i][j] == 0:
                    offspring_crossover[i][j] = 1
                else:
                    offspring_crossover[i][j] = 0
            else:
                print("NO Mutation!")
    return offspring_crossover
