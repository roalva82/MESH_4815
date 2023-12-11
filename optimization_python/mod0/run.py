#!/usr/bin/env python
# coding: utf-8

# In[1]:


import subprocess
import os
import pandas as pd
import numpy as np
from typing import Tuple


# In[2]:
cwd = os.getcwd()
print(f'Here: {cwd}')


def remove_invalid_values(simulated, observed):
    valid_indices = np.where((observed != -9999) & (simulated != -9999))
    return simulated[valid_indices], observed[valid_indices]


# In[3]:


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


# In[4]:


def compute_kge(simulated_array, observed_array):
    """
    Computes KGE (Kling-Gupta Efficiency) between observed and simulated values.

    Parameters:
        observed_array (numpy.ndarray): Array of observed values.
        simulated_array (numpy.ndarray): Array of simulated values.

    Returns:
        float: KGE value.
    """
    
    # Calculate Pearson correlation coefficient
    correlation_coefficient = np.corrcoef(observed_array, simulated_array)[0, 1]
    
    # Calculate standard deviation ratio
    std_observed = np.std(observed_array)
    std_simulated = np.std(simulated_array)
    std_ratio = std_simulated / std_observed
    
    # Calculate bias ratio
    mean_observed = np.mean(observed_array)
    mean_simulated = np.mean(simulated_array)
    bias_ratio = mean_simulated / mean_observed
    
    # Calculate KGE
    kge = 1 - np.sqrt((correlation_coefficient - 1)**2 + (std_ratio - 1)**2 + (bias_ratio - 1)**2)
    return -kge


# In[5]:


def percent_bias(simulated, observed):
    """
    Calculate percent bias between observed and simulated hydrographs.

    Parameters:
    - observed: List or array of observed values
    - simulated: List or array of simulated values

    Returns:
    - Percent bias
    """
    
    numerator = sum(np.abs(sim - obs) for obs, sim in zip(observed, simulated))
    denominator = sum(observed)

    absolute_percent_bias_value = (numerator / denominator) * 100

    return absolute_percent_bias_value


# In[6]:


# run mesh
os.chdir('./assets/')
mesh_command  = './sa_mesh'
subprocess.run([mesh_command])


# In[7]:
df = pd.read_csv('./results/Metrics_Out.txt',delim_whitespace=True)

df['RMSE'].to_csv('./RMSE.csv',header=False, index=False)


# Create an empty list to store total KGE values for each file
total_kge_values = []


# In[8]:


total_bias_values = []


# In[9]:


file_names = []


# In[10]:


