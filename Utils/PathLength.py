import numpy as np


def path_length(path):
    return np.sqrt(np.sum(np.diff(path, axis=0)**2, axis=1)).sum() if path is not None else np.nan
