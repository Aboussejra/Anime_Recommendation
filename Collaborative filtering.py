
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 31 14:08:57 2020

@author: Amir
"""

# Import relevant libraries 

import pandas as pd
import numpy as np
import scipy as sp
from sklearn.metrics.pairwise import cosine_similarity
import operator


anime = pd.read_csv('anime.csv')
rating = pd.read_csv('rating.csv')

# Before alteration the ratings dataset uses a "-1" to represent missing ratings. I'm replacing these placeholders with a null value because I will later be calculating the average rating per user and don't want the average to be distorted

rating.rating.replace({-1: np.nan}, regex=True, inplace = True)
rating.head()

# For this analysis I'm only interest in finding recommendations for the TV category

anime_tv = anime[anime['type']=='TV']

# Join the two dataframes on the anime_id columns

merged = rating.merge(anime_tv, left_on = 'anime_id', right_on = 'anime_id', suffixes= ['_user', ''])
merged.rename(columns = {'rating_user':'user_rating'}, inplace = True)

# For computing reasons I'm limiting the dataframe length to 10,000 users

merged=merged[['user_id', 'name', 'user_rating']]
merged_sub= merged[merged.user_id <= 10000]
# For collaborative filtering we'll need to create a pivot table of users on one axis and tv show names along the other. The pivot table will help us in defining the similarity between users and shows to better predict who will like what.

piv = merged_sub.pivot_table(index=['user_id'], columns=['name'], values='user_rating')

# Note: As we are subtracting the mean from each rating to standardize
# all users with only one rating or who had rated everything the same will be dropped

# Normalize the values
piv_norm = piv.apply(lambda x: (x-np.mean(x))/(np.max(x)-np.min(x)), axis=1)


# Drop all columns containing only zeros representing users who did not rate
piv_norm.fillna(0, inplace=True)
piv_norm = piv_norm.T
piv_norm = piv_norm.loc[:, (piv_norm != 0).any(axis=0)]

# Our data needs to be in a sparse matrix format to be read by the following functions

piv_sparse = sp.sparse.csr_matrix(piv_norm.values)

item_similarity = cosine_similarity(piv_sparse)
user_similarity = cosine_similarity(piv_sparse.T)

# Inserting the similarity matricies into dataframe objects

item_sim_df = pd.DataFrame(item_similarity, index = piv_norm.index, columns = piv_norm.index)
user_sim_df = pd.DataFrame(user_similarity, index = piv_norm.columns, columns = piv_norm.columns)

# This function will return the top 10 shows with the highest cosine similarity value

def top_animes(anime_name):
    count = 1
    print('Animés similaires à {} incluent:\n'.format(anime_name))
    for item in item_sim_df.sort_values(by = anime_name, ascending = False).index[1:11]:
        print('No. {}: {}'.format(count, item))
        count +=1  


top_animes('Nisekoi')