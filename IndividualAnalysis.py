import GeneticAlgorithm

company_list = ['AAPL', 'AVGO', 'MSFT', 'ORCL', 'TSM', 
                'BAC', 'XOM', 'V', 'AMKR', 'FORM', 'NCR'
                'SANM', 'SWI', 'AAPS', 'WU', 'SABR', 'AVT'
                ]

for ticker in company_list:
    fit_individuals_list = []
    fit_return_list = []
    print("Company: ", ticker)
    #Generate initial population

    data_frame = GeneticAlgorithm.acquire_data(ticker)

    #Run Genetic Algorithm for 75 generations
    for trial in range(0, 10):
        print(ticker, " trial ", trial + 1)
        population = []
        population = GeneticAlgorithm.population_generation()
        for i in range (0, 75):
            print("Generation ", i + 1, " :")
    
            #Give fitness function population to calculate return (fitness)
            #Returns the list of returns and dictionary of chromsomome with returns
            return_list = GeneticAlgorithm.fitness_function(population, data_frame)

            #Gets fittest individuals from tournament selection
            fittest_parents_ret = GeneticAlgorithm.selection_function(return_list)

            fittest_parents = []
            for i in range(0, len(return_list)):
                if return_list[i] == fittest_parents_ret[0] or return_list[i] == fittest_parents_ret[1]:
                    fittest_parents.append(population[i])

            #Creates offspring from parentsvidentified as most fit
            offspring_1, offspring_2 = GeneticAlgorithm.crossover_function(fittest_parents, population)

            #Remove two least fit individuals (least return)
            population, return_list = GeneticAlgorithm.remove_function(population, return_list)

            #Mutation
            mutate_1 = 0
            mutate_2 = 0
            for i in population:
                if offspring_1 == i:
                    #Mutation Function
                    mutate_offspring_1 = GeneticAlgorithm.mutation_function(offspring_1, population)
                    population.append(mutate_offspring_1)
                    mutate_1 = 1
                    break

            for i in population:
                if offspring_2 == i:
                    #Mutation Function
                    mutate_offspring_2 = GeneticAlgorithm.mutation_function(offspring_2, population)
                    population.append(mutate_offspring_2)
                    mutate_2 = 1
                    break

            #Add offspring to population
            if mutate_1 == 0:
                population.append(offspring_1)
            
            if mutate_2 == 0:
                population.append(offspring_2)

        return_list = GeneticAlgorithm.fitness_function(population, data_frame)
        high = max(return_list)
        for i in range(0, len(return_list)):
            if return_list[i] == high:
                fit_individual = population[i]
        print('\nMost fit individual: ', high, fit_individual)
    
        fit_individuals_list.append(fit_individual)

        fit_return_list.append(high)

    print(fit_return_list)
    print(fit_individuals_list)