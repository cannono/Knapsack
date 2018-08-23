# Creating an item set to test my code.
import random

random.seed(42)

prob_mut = .1


class Item:
    def __init__(self, weight, value):
        self.weight = weight
        self.value = value

    def __repr__(self):
        return "Item value: {0}, weight: {1}".format(self.value, self.weight)


num_items = 1000
max_weight = 200
itemset = [Item(random.randint(10, 100), random.randint(10, 100)) for _ in range(num_items)]


def run_knapsack_ga(itemset, max_weight, max_time):
    import time
    import numpy as np
    import random

    start_time = time.time()
    pop_size = 100

    # Create the initial poulation made of up 100 knapsack genotypes
    def random_individual():
        total_weight = 0
        knap_genotype = []
        while True:
            item_index = random.randint(0, len(itemset) - 1)

            if itemset not in knap_genotype:
                if total_weight + itemset[item_index].weight > max_weight:
                    if knap_genotype == []:
                        random_individual()
                    else:
                        return knap_genotype
                else:
                    knap_genotype.append(item_index)
                    total_weight += itemset[item_index].weight

    population = [random_individual() for _ in range(pop_size)]

    # Called if doing tournament selection
    def tournament(population, k):
        # Determine the players in the tournament
        # Keeps track of what indexes have been added to players
        index_list = []
        players = []
        d = k
        # Determines the probability that each individual is selected.
        p = .9

        # Creates a list of k genotypes which will be the players in the tournament
        while k > 0:
            index = random.randint(0, pop_size - 1)
            if not players:
                players.append(population[index])
                index_list.append(index)
                k += -1
            elif index not in index_list:
                players.append(population[index])
                index_list.append(index)
                k += -1
        # Gets the value of the players and sorts the list of values in descending order.
        players_fitness = [value(i) for i in players]
        players_fitness = sorted(players_fitness, key=int, reverse=True)
        # The winner will get a fitness of p.
        players_fitness[0] = p

        # The rest of the players will get fitness based on the formula
        for x in range(1, d):
            players_fitness[x] = p * ((1 - p) ** x)

        # Creates the new population from the players and it is weighted based on their fitness.
        # There is a probability that there will be point mutations.
        population = random.choices(players, k=pop_size, weights=players_fitness)
        new_pop = [mutate_genotype(i, prob_mut=.1) for i in population]
        return new_pop

    # Keeps around the most fit or valuable m individuals. The rest of the population will be randomized.
    def elitism(population, m):
        fitness = [value(i) for i in population]
        # sort the population in decreasing fitness
        sorted_fitness = sorted(fitness, key=int, reverse=True)
        # Get the original index of the genotypes
        og_index = sorted(range(len(fitness) - 1), key=lambda k: fitness[k], reverse=True)

        # The most valuable m genotypes. These will be passed on to the next generation unchanged
        # and pop_size - m   random genotypes will be made
        elite = [population[og_index[i]] for i in range(0, m)]
        new_pop = elite

        k = 1
        while k <= pop_size - m:
            random_genotype = random_individual()
            if random_genotype not in new_pop:
                new_pop.append(random_genotype)
                k += 1
        return new_pop

    # Elitism where the most valuable m genotypes in the population will be passed on to the next generation unchanged.
    # Another set of these m genotypes will be passed onto the next generation with point mutations. The rest of the
    # population will be randomized
    def elite_mut(population, m):
        fitness = [value(i) for i in population]
        # sort the population in decreasing fitness
        sorted_fitness = sorted(fitness, key=int, reverse=True)
        # Get the original index of the genotypes
        og_index = sorted(range(len(fitness) - 1), key=lambda k: fitness[k], reverse=True)

        # The most valuable m genotypes. These will be passed on to the next generation unchanged
        # and pop_size - m   random genotypes will be made
        elite = [population[og_index[i]] for i in range(0, m)]
        mutated_elite = [mutate_genotype(i, prob_mut) for i in elite]
        new_pop = elite + mutated_elite

        k = 1
        # Create the rest of the population by creating random genotypes
        while k <= pop_size - 2 * m:
            random_genotype = random_individual()
            if random_genotype not in new_pop:
                new_pop.append(random_genotype)
                k += 1

        return new_pop

    # Has a certain probabability of mutating a single point in the genotype.
    def mutate_genotype(genotype, prob_mut):

        if random.random() < prob_mut:

            x = random.randint(0, len(genotype) - 1)
            y = random.randint(0, len(itemset) - 1)

            # Checks if the item is not already in the knapsack and if the item will put the
            # knapsack over the maximum weight.
            if genotype[x] != y:
                if weight(genotype) - itemset[genotype[x]].weight + itemset[y].weight > max_weight:
                    return genotype
                else:
                    genotype[x] = y
        return genotype

    # Takes a population and the highest value of all generations in its parameter. It will
    # Then check if any genotype in the population has a higher value the the current highest.
    # If it does then that value will become the new highest.
    def get_maxValue(population, best_so_far):
        for i in population:
            total_weight = sum([itemset[i].weight for i in genotype])
            if total_weight < max_weight:
                value = sum([itemset[x].value for x in i])
                if value > best_so_far:
                    best_so_far = value
        return best_so_far

    # Determines the value of a genotype
    def value(genotype):
        return sum([itemset[i].value for i in genotype])

    # Determiens the weight of a genotype
    def weight(genotype):
        return sum([itemset[i].weight for i in genotype])

    best_so_far = 0
    new_pop = []
    while (time.time() - start_time) < max_time - 0.1:

        new_pop = []
        for i in population:
            if i != None:
                if value(i) > best_so_far:
                    best_so_far = value(i)

        # Uncomment which ever selection methd one you want to run.
        # elite_mut works the best.

        # population = tournament(population, 25)
        # population= elitism(population, 10)
        population = elite_mut(population, 10)
    return best_so_far


best = run_knapsack_ga(itemset, max_weight, 10)
print(best)
