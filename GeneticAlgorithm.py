import copy
import datetime
import pandas_datareader.data as pdr
import random
import RSIGeneration
import SimTrading

#Add the RSI and long-term Moving Averages to Dataframe
def acquire_data(ticker):
    start = datetime.datetime(2005, 1, 1)
    end = datetime.datetime(2021, 1, 1)
    data_frame = pdr.DataReader(ticker, 'yahoo', start, end)

    close = data_frame.Close

    for i in range(0, close.size):
        #Form SMA values of 50 and 200 days
        data_frame['SMA50'] = close.rolling(50).mean()
        data_frame['SMA200'] = close.rolling(200).mean()

    data_frame = RSIGeneration.generate(data_frame)

    #Start at the 200th observance to allow for all indicators to be formed
    data_frame = data_frame.iloc[503:]

    return data_frame

def population_generation():
    population = []
    chromosome = []
    gene = 0
    while len(population) < 75: #Fill population to x individuals
        if len(chromosome) == 0 or len(chromosome) % 4 == 0: #Generate buy values every 4 values
            gene = random.randint(15, 40) 
        elif len(chromosome) == 1 or len(chromosome) == 3 or len(chromosome) % 4 == 1 or len(chromosome) % 4 == 3: #Generate intervals every 2 values
            gene = random.randint(5, 20)
        elif len(chromosome) == 2 or len(chromosome) % 4 == 2: #Generate sell value every 4 values
            gene = random.randint(60, 95)
        else:
            print('error')
            break
        
        chromosome.append(gene) #Add gene to individual

        if len(chromosome) >= 8: #When chromosome is filled
            population.append(chromosome) #Add individual to population
            chromosome = [] #Empty chromosome for next individual

    return population

def fitness_function(population, data_frame): #Find returns of each chromosome
    #Execute "trades" based on individuals "genes"

    fitness_list = []

    for i in range(0, len(population)):
        individual = population[i]
        fitness_value = SimTrading.trade_function(data_frame, individual)
        fitness_list.append(fitness_value)

    return fitness_list

def selection_function(return_list):
    #Pick 32 random individuals (16 for each tournament)
    #Store 32 individuals in a list, compare values next to each other
    parents_list = []
    rand_list = []
    tournament_list = []
    returns = return_list

    #Generate 16 unique random integers
    while len(tournament_list) < 16:
        rand = random.randint(0, 75 - 1)
        #print(rand)
        if rand not in rand_list:
            rand_list.append(rand)
            tournament_list.append(returns[rand])

    def tournament_selection(tournament_list):
        #Take top two values from tournament
        new_tournament_list = []
        for i in range(0, len(tournament_list), 2):
            if tournament_list[i] > tournament_list[i + 1]:
                new_tournament_list.append(tournament_list[i])
            else:
                new_tournament_list.append(tournament_list[i + 1])

        return new_tournament_list

    parents_list = tournament_selection(tournament_list)
    while len(parents_list) != 2:
        parents_list = tournament_selection(parents_list)
    
    if len(parents_list) == 2:
        return parents_list

def crossover_function(parents, population):
    crossover = random.randint(2, 6)
    offspring_a = []
    offspring_b = []
    parent_a = parents[0]
    parent_b = parents[1]
    #Creates offspring with both parents traits (splits up and downtrend traits)
    offspring_a = parent_a[0:crossover] + parent_b[crossover:8]
    offspring_b = parent_b[0:crossover] + parent_a[crossover:8]

    return offspring_a, offspring_b

def mutation_function(offspring, population):
    random_index = random.randint(0,7)
    if random_index == 0 or random_index % 4 == 0: #Generate buy values every 4 values
        offspring[random_index] = random.randint(15, 40) 
    elif random_index == 1 or random_index == 3 or random_index % 4 == 1 or random_index % 4 == 3: #Generate intervals every 2 values
        offspring[random_index] = random.randint(5, 20)
    elif random_index == 2 or random_index % 4 == 2: #Generate sell value every 4 values
        offspring[random_index] = random.randint(60, 95)

    for i in population:
        if offspring == i:
            mutation_function(offspring, population)
    
    return offspring

#Find lowest two returns and remove the corresponding chromosomes from the population
def remove_function(population, return_list):
    test_return_list = copy.deepcopy(return_list)
    lowest_list = []
    lowest_index = []
    for i in range(0, 2):
        low = min(test_return_list)
        test_return_list.remove(low)
        lowest_list.append(low)

    for i in range(0, len(return_list)):
        if return_list[i] == lowest_list[0] or return_list[i] == lowest_list[1]:
            lowest_index.append(i)

    lowest_index.sort()

    return_list.remove(return_list[lowest_index[1]])
    return_list.remove(return_list[lowest_index[0]])
    population.remove(population[lowest_index[1]])
    population.remove(population[lowest_index[0]])

    return population, return_list

