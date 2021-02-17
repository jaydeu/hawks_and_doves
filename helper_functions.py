# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 13:57:13 2021

@author: joh8708
"""

import pandas as pd
import numpy as np

def matchUp(matches, A, B):
    """
    
    Parameters
    ----------
    A : String
        First critter in match.
    B : String
        Second critter in match.

    Returns
    -------
    Tuple in float form, points for first critter and second respectively.
    
    """
    points_A = matches[B][A]
    points_B = matches[A][B]
    return(points_A, points_B)

def getSurvival(points):
    """
    
    Parameters
    ----------
    points : Float
        Number of food points that the critter received this round.

    Returns
    -------
    survive : integer 0 or 1
        Returns 1 if the critter has enough points to survive.

    """
    if points >= 1:
        survive = 1
    else:
        survive = np.random.binomial(1, points)   # toss a coin!
    return survive

def getReproduction(points):
    """

    Parameters
    ----------
    points : Float
        Number of food points that the critter received this round.

    Returns
    -------
    reproduce : integer 0 or 1
        Returns 1 if the critter has enough points to reproduce

    """
    if points >= 2:
        reproduce = 1
    elif points > 1: 
        reproduce = np.random.binomial(1, points-1)
    else:
        reproduce = 0
    return reproduce   



def oneDay(t, all_critters, time_table, n_food, matches):  
    """

    Runs simulation for one day and updates listing of critters and time series table.

    Parameters
    ----------
    t : integer
        Iteration time.
    all_critters : np.array of strings
        array of critters, e.g. ['D', 'H', 'D', ...].
    time_table : pd.DataFrame
        data frame that includes the number of each critter type at each time t.
    n_food: integer
        Number of food items available each day.
    matches: pd.DataFrame
        Contains point values for each possible matchup.

    Returns
    -------
    new_critters : np.array of strings
        Updated version of all_critters after iteration t.
    time_table : pd.DataFrame
        Updated version of time_table with new row added.

    """
    
    population = len(all_critters)

    # If there are more critters than food, delete the excess at random and assume they did not survive.
    if(population > n_food):
        perish_idx = np.random.choice(population, size=population - n_food, replace=False)
        all_critters = np.delete(all_critters, perish_idx)

    # Now for remaining critters, choose a food index for them to end up at.
    food_idx = np.random.choice(n_food, size=len(all_critters), replace=False)

    # initialize food array
    food = np.array(['none']*n_food)

    # assign letters to food items
    food[food_idx] = all_critters

    food_1 = pd.Series(food[0:50])
    food_2 = pd.Series(food[50:100])

    # initialize food points
    food_points_1 = pd.Series([0.0]*len(food_1))
    food_points_2 = pd.Series([0.0]*len(food_2))

    # calculate how many points each critter gains in each matchup.
    for i in range(50):
        food_points_1[i], food_points_2[i] = matchUp(matches, food_1[i], food_2[i])

    df_1 = pd.DataFrame({'critter': food_1, 'points': food_points_1})
    df_2 = pd.DataFrame({'critter': food_2, 'points': food_points_2})
    df_all = pd.concat([df_1, df_2])

    # Decide whether each critter survives or reproduces, by points.
    df_all['survival'] = [getSurvival(p) for p in df_all['points']]
    df_all['reproduce'] = [getReproduction(p) for p in df_all['points']]

    result = df_all.groupby(by='critter').sum()

    # Get new listing of critters
    new_critters = []

    for c in result.index:
        new_critters = new_critters + [c]*int(result.loc[c].survival) + [c]*int(result.loc[c].reproduce)

    # Save the number of each type at time t
    hawks = new_critters.count('H')
    doves = new_critters.count('D')
    sneaks = new_critters.count('S')
    time_row = pd.DataFrame({'time': [t], 'hawks' : [hawks], 'doves': [doves], 'sneaks': [sneaks]})
    time_table = pd.concat([time_table, time_row])

    return new_critters, time_table