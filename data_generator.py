import numpy as np
import pandas as pd

def generate_data(n_points=100, noise=0.1, slope=2.0):
    """
    Generate synthetic data for regression analysis
    
    Parameters:
    -----------
    n_points : int
        Number of data points to generate
    noise : float
        Level of noise to add to the data
    slope : float
        True slope of the linear relationship
    
    Returns:
    --------
    pandas.DataFrame
        DataFrame containing the generated data
    """
    np.random.seed(42)  # For reproducibility
    X = np.random.uniform(0, 10, n_points)
    y = slope * X + np.random.normal(0, noise, n_points)
    
    return pd.DataFrame({
        'X1': X,
        'Y': y
    })
