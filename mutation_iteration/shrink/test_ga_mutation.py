# run this file to run simulations

# Population size: 20
# Gene count: 3
# Time steps: 2400
# Mutations
# Point mutation rate: 0.1 for 0.25
# Shrink mutation rate: 0.5
# Grow mutation rate: 0.1
# Number of generations: 100


import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import unittest
import population
import simulation 
import genome 
import creature 
import numpy as np
import csv

class TestGA(unittest.TestCase):
    def testBasicGA(self):
        # create population of 20 creatures with 3 genes each
        pop = population.Population(pop_size=20, 
                                    gene_count=3)
        sim = simulation.Simulation()
        ga_results = [] # array to store all results

        for iteration in range(300): ## number of simulations to run
            for cr in pop.creatures:
                sim.run_creature(cr, 2400) # for each creature, run for 144140000 time steps (10 seconds)
            
            fits = [cr.get_distance_to_top() for cr in pop.creatures] # best fitness
            links = [len(cr.get_expanded_links()) for cr in pop.creatures] # get number of links

            fittest = np.round(np.min(fits), 3) # best fitness in this generation (lowest distance to top)
            mean_fit = np.round(np.mean(fits), 3) # mean fitness
            mean_links = np.round(np.mean(links)) # mean number of links
            max_links = np.round(np.max(links)) # most links in any creature
            
            # print results to console
            print(iteration,
                  "fittest:", fittest, 
                  ", mean fit:", mean_fit,
                  ", max links:", max_links,
                  ", mean links:", mean_links,
                  )  
            
            # append results to array
            ga_results.append([iteration, 
                               fittest, mean_fit,
                               mean_links, max_links])
            
            # invert fitnesses so lower distances (better) become higher fitness values
            max_fit = max(fits) if fits else 1.0
            inverted_fits = [max_fit - f for f in fits]
            fit_map = population.Population.get_fitness_map(inverted_fits)
            new_creatures = []
            
            # for each new creature,
            for i in range(len(pop.creatures)):
                # select 2 parents using fitness map
                p1_ind = population.Population.select_parent(fit_map)
                p2_ind = population.Population.select_parent(fit_map)
                p1 = pop.creatures[p1_ind]
                p2 = pop.creatures[p2_ind]
                
                # combine their DNA
                dna = genome.Genome.crossover(p1.dna, p2.dna)
                
                # apply mutations. increase rates for more exploration, decrease for more exploitation
                dna = genome.Genome.point_mutate(dna, rate=0.1, amount=0.25)
                dna = genome.Genome.shrink_mutate(dna, rate=0.5)
                dna = genome.Genome.grow_mutate(dna, rate=0.1)
                
                # create new creature
                cr = creature.Creature(1)
                cr.update_dna(dna)
                new_creatures.append(cr)
                
            # elitism -- preserve best individual (lowest distance to top)
            best_fit = np.min(fits)
            for cr in pop.creatures:
                if cr.get_distance_to_top() == best_fit: # finds the best fitness according to distance to mountain
                    new_cr = creature.Creature(1)
                    new_cr.update_dna(cr.dna)
                    new_creatures[0] = new_cr
                    
                    # save in elite folder
                    ga_dir = os.path.dirname(os.path.abspath(__file__))
                    elite_dir = os.path.join(ga_dir, "elite")
                    os.makedirs(elite_dir, exist_ok=True)
                    
                    filename = os.path.join(elite_dir, "elite_"+str(iteration)+".csv")
                    genome.Genome.to_csv(cr.dna, filename)
                    break
            
            # replace population with the new generation
            pop.creatures = new_creatures

        # save all results to csv file
        ga_dir = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(ga_dir, "mutateShrink_results.csv")
        with open(filename, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['iteration', 
                                'fittest', 'mean_fit',
                                'mean_links', 'max_links'])
            csvwriter.writerows(ga_results)
                           
        # asserts that one creature moved
        self.assertNotEqual(fits[0], 0)

unittest.main()