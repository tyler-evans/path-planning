import numpy as np
import random


class Seed:

    def __init__(self, seed=None):
        if seed:
            print('Using existing seed:', seed)
        else:
            seed = np.random.randint(4190)

        random.seed(seed)
        np.random.seed(seed)
