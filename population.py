import creature 
import numpy as np

class Population:
    def __init__(self, pop_size, gene_count):
        self.creatures = [creature.Creature(
                          gene_count=gene_count) 
                          for i in range(pop_size)]

    @staticmethod
    def get_fitness_map(fits):
        # Shift all fitness values to be non-negative for proper selection
        # This handles cases where creatures have negative fitness (e.g., moving away from mountain)
        min_fit = min(fits) if fits else 0
        if min_fit < 0:
            # Shift all values to be non-negative
            fits = [f - min_fit + 1.0 for f in fits]  # +1 ensures all values are positive
        
        fitmap = []
        total = 0
        for f in fits:
            total = total + f
            fitmap.append(total)
        return fitmap
    
    @staticmethod
    def select_parent(fitmap):
        if len(fitmap) == 0:
            return 0  # Fallback if empty
        
        # If all fitness values are zero or negative (after shifting), use uniform random selection
        if fitmap[-1] <= 0:
            return np.random.randint(0, len(fitmap))
        
        r = np.random.rand() # 0-1
        r = r * fitmap[-1]
        for i in range(len(fitmap)):
            if r <= fitmap[i]:
                return i
        
        # Fallback: return last index if no match found (shouldn't happen, but safety check)
        return len(fitmap) - 1

