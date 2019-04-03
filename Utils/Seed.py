import numpy as np
import random


class Seed:

    def __init__(self, seed=None, display_seed=True):
        if seed and display_seed:
            #print('Using existing seed:', seed)
            pass
        else:
            seed = np.random.randint(4190)

        random.seed(seed)
        np.random.seed(seed)
