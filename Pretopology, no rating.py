# -*- coding: utf-8 -*-
"""
Created on Tue Nov  3 09:57:02 2020

@author: Amir
"""


import pandas as pd
import numpy as np
import scipy as sp


anime = pd.read_csv('AnimeList.csv')
data = anime[['anime_id','title','type','score','rank','popularity','studio','genre']]
# we don't have ratings, need to do it without a notion of similarity, or anything. Use pretopology:
    
# For this analysis I'm only interest in finding recommendations for the TV category

data = data[data['type']=='TV']
data = data.dropna()
#similarity_matrix_genre = [[similarity_in_genre(data.iloc[i,7].split(','),data.iloc[j,7].split(','))/len(data.iloc[i,7].split()) for i in range(len(data))]for j in range(len(data))]

def similarity_in_genre(anime_genre_string_1,anime_genre_string_2):
    genre_in_common = 0
    for elem in anime_genre_string_1:
        if (elem in anime_genre_string_2):
            genre_in_common += 1
    return genre_in_common

def similarity_in_studio(anime_studio_string_1,anime_studio_string_2):
    for elem in anime_studio_string_1:
        if (elem in anime_studio_string_2):
            return 1
    return 0
# similarity_in_studio(data.iloc[7,6].split(','),data.iloc[8,6].split(','))

def similarity_in_author(anime_studio_string_1,anime_studio_string_2):
    for elem in anime_studio_string_1:
        if (elem in anime_studio_string_2):
            return 1
    return 0

def similarity_anime_i_anime_j(i,j):
    similarity_genre = similarity_in_genre(data.iloc[i,7].split(','),data.iloc[j,7].split(','))/len(data.iloc[i,7].split(','))
    similarity_studio = similarity_in_studio(data.iloc[i,6].split(','),data.iloc[j,6].split(','))
    return similarity_genre + 0.5*similarity_studio

def similarity_anime_i(i):
    list_similarity = []
    for j in range(0,len(data)):
        list_similarity.append([similarity_anime_i_anime_j(i, j),j])
    return list_similarity

# 14 c'est bleach
similarity_anime_14 = similarity_anime_i(14)
similarity_anime_14.sort()
# 19 c'est toradora!
similarity_anime_19 = similarity_anime_i(19)
similarity_anime_19.sort()
# on choppe du naruto, trop d'importances pour les studios je pense, à voir