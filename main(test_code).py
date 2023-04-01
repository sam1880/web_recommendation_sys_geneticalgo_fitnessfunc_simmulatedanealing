#generating web id's
import random
random_list = []
for i in range(500):
    n = i+1
    random_list.append(n)
##print(random_list)

#generating keywords for each web
random_keywords = []
for i in range(500):
    n = i+1000
    random_keywords.append(n)
##print(random_keywords)

#generating access frequesncy for each web
random_access = []
for i in range(500):
    n = i+2000
    random_access.append(n)
##print(random_access)

#generating population (10 combinations of 5 websites)
population = []
p = 5
for i in range (100):
    combinations = random.sample(random_list,p)
    ##print(combinations)
    population.append(combinations)
##print(population)


generations = 1
while(generations < 100): 


    #calculating fitness fucntions
    #assigning web to their attributes using indexes
    fitness = []
    total_access = []
    total_keyword = []
    for list in population:
        totalforkeyword = 0
        totalforaccess = 0
        for combination in list:
            ##print(combination)
            index = random_list.index(combination)
            ##print(index)
            ##print(random_keywords[index])
            ##print(random_access[index])
            totalforkeyword = totalforkeyword + random_keywords[index]
            totalforaccess = totalforaccess + random_access[index]
            ##print(totalforkeyword)
            ##print(totalforaccess)
            fitness_elements = totalforaccess + totalforkeyword
        ##print('result : ' + str(fitness_elements))
        total_keyword.append(totalforkeyword)
        total_access.append(totalforaccess)
        fitness.append(fitness_elements)
    ##print(total_keyword)
    ##print(total_access)
    ##print(fitness)

    #comparing random two fitness fucntions, for new population generation
    fitness_new = []
    size = len(fitness)

    for i in range (int(size/2)):
        k = .70
        r = random.uniform(0,1)
        ##print(str(r))
        t1 = random.choice(fitness)
        t2 = random.choice(fitness)
        ##print (str(t1), str(t2))
        min_fitness = min(t1,t2)
        max_fitness = max(t1,t2)
        if(r>k):
            ##print(str(min_fitness))
            fitness_new.append(min_fitness)
        elif(r<k):
            ##print(str(max_fitness))
            fitness_new.append(max_fitness)
    ##print(fitness_new)

    #generating new population
    new_population = []
    for list in fitness_new:
        element = list
        ##print(element)
        index = fitness.index(list)
        ##print(str(index))
        new_popu_data = population[index]
        new_population.append(new_popu_data)
    ##print("\nNEW POPULATION:\n")
    ##print(new_population)

    parents = []
    for i in range(int(size/2)):
        cross_parent = random.sample(new_population, 2)
        parents.append(cross_parent)
    ##print(parents)

    offspring = []
    for parent_pair in parents:
        crossover_point = random.randint(1, len(random_list)-1)
        offspring_1 = []
        offspring_2 = []
        offspring_1.extend(parent_pair[0][:crossover_point])
        offspring_1.extend(parent_pair[1][crossover_point:])
        offspring_2.extend(parent_pair[1][:crossover_point])
        offspring_2.extend(parent_pair[0][crossover_point:])
        offspring = offspring + [offspring_1, offspring_2]

    for i in range(len(offspring)):
        for j in range(len(offspring[i])):
            mutation_probability = 0.01
            if random.uniform(0, 1) <= mutation_probability:
                offspring[i][j] = random.choice(random_list)

    print("\n\n\n")
    print(offspring)
    population = offspring

    generations += 1