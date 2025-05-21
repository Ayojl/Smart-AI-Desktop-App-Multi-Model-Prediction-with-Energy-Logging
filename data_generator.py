import numpy as np
import pandas as pd

def generate_data(n=200):
    X1 = np.random.rand(n)
    X2 = np.random.rand(n)
    X3 = np.random.rand(n)
    y = 4 + 3*X1 - 2*X2 + X3 + np.random.randn(n)
    return pd.DataFrame({'X1': X1, 'X2': X2, 'X3': X3, 'Y': y})
