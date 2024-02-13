import subprocess
import os
import pandas as pd
import numpy as np
from typing import Tuple

cwd = os.getcwd()
print(f'Here: {cwd}')

def remove_invalid_values(simulated, observed):
    valid_indices = np.where((observed != -9999) & (simulated != -9999))
    return simulated[valid_indices], observed[valid_indices]

def remove_nan_rows(
    array1: np.ndarray, 
    array2: np.ndarray
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Removes rows from two arrays where either array has NaN values.
    Retains the first row if it doesn't have any NaN values.
    
    Arguments:
    array1: np.ndarray:
        First input array
    array2: np.ndarray
        Second input array
    
    Returns:
    cleaned_array1: : np.ndarray
        Cleaned array1 without NaN rows
    cleaned_array2: np.ndarray
        Cleaned array2 without NaN rows
    """
    # checks for and removes any rows where either array has a value of NaN at a corresponding row 
    # including the first one
    
    mask = np.logical_and(~np.isnan(array1), ~np.isnan(array2))
    if not np.isnan(array1[0]) and not np.isnan(array2[0]):
        mask[0] = True
    cleaned_array1 = array1[mask]
    cleaned_array2 = array2[mask]
    return cleaned_array1, cleaned_array2

def nse(simulated, observed):
	denominator = np.sum((observed - np.mean(observed)) ** 2)
	numerator = np.sum((simulated - observed) ** 2)
	nse = 1 - numerator / denominator
	return nse

def kge(simulated, observed):
    # Calculate Pearson correlation coefficient
    correlation_coefficient = np.corrcoef(observed, simulated)[0, 1]
    
    # Calculate standard deviation ratio
    std_observed = np.std(observed)
    std_simulated = np.std(simulated)
    std_ratio = std_simulated / std_observed
    
    # Calculate bias ratio
    mean_observed = np.mean(observed)
    mean_simulated = np.mean(simulated)
    bias_ratio = mean_simulated / mean_observed
    
    # Calculate KGE
    kge = 1 - np.sqrt((correlation_coefficient - 1)**2 + (std_ratio - 1)**2 + (bias_ratio - 1)**2)
    return -kge

def percent_bias(simulated, observed):
    numerator = sum(np.abs(sim - obs) for obs, sim in zip(observed, simulated))
    denominator = sum(observed)

    absolute_percent_bias_value = (numerator / denominator) * 100

    return absolute_percent_bias_value

# run mesh
os.chdir('./assets/')
mesh_command  = './sa_mesh'
subprocess.run([mesh_command])

# read simulated data
sim_df = pd.read_csv('./results/RFF_D.csv', header=None)
sim = sim_df[649].to_numpy()

# read observed data
obs_df = pd.read_csv('../obs/05BL027_Daily_Flow_ts.csv', skiprows=1, header=None, names=['ID','PARAM','Date','Flow','SYM'])
obs_df['Date'] = pd.to_datetime(obs_df['Date'])

# extract values for observed data
start_date = '1980-05-02'
end_date = '1980-05-29'
mask = (obs_df['Date'] >= start_date) & (obs_df['Date'] <= end_date)
obs = obs_df.loc[mask]['Flow'].to_numpy()

# compute and export metric
metric = -1.0*nse(sim,obs)


import csv

with open('./MetricTest.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow([metric])
    

