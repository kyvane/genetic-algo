# Genetic Algorithm Creatures

This genetic algorithm project evolves creatures to climb a mountain, simulated in PyBullet.

## Requirements

- Python 3
- [NumPy](https://numpy.org/)
- [PyBullet](https://pybullet.org/)

## Run an evolution

The default experiment is `test_ga.py`. It evolves a population of 20 creatures for 20 generations. Each creature is simulated for 2400 physics steps.

```
python test_ga.py
```

Each generation prints the best and mean distance to the peak, plus link counts. Results are written to `gen_100_results.csv` in the working directory. The best creature of each generation is saved as `elite/elite_<generation>.csv`.

Longer and varied runs live under the experiment folders. Run them the same way:

```
python gen_iteration/100/test_ga_gen.py
python pop_iteration/test_ga_pop.py
python mutation_iteration/grow/test_ga_mutation.py
```

These runs take a while. A 300-generation run evaluates every creature in the population for 2400 steps each generation.

## Watch a saved creature

Replay an elite creature in the PyBullet GUI:

```
python realtime_from_csv.py elite/elite_19.csv
```

Replace the path with any `elite_*.csv`. The window runs for about 60 seconds and prints how far the creature moved.

`motor_test.py` drops a random creature on a flat plane so you can check motor output without the mountain.