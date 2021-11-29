from bs4 import BeautifulSoup
import requests
import pandas as pd
from random import randint
import re
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from random import randint
from time import sleep
from sklearn import datasets
# K-means
import numpy as np
import matplotlib.pyplot as plt
from sklearn import cluster, datasets
from sklearn.preprocessing import StandardScaler
from matplotlib.lines import Line2D
from sklearn.cluster import KMeans


def recommending_artist_improved(artist):
    songs_to_recommend_top_100 = []
    position_top_100 = []
    songs_to_recommend_second_top = []
    position_second_top = []
    for i in range(len(top_100['artist'])):
        text1 = top_100['artist'][i]
        text2 = second_top['artist'][i]
        pattern = artist
        number_1 = re.findall(pattern, text1)
        number_2 = re.findall(pattern, text2)
        if len(number_1)> 0:
            songs_to_recommend_top_100.append(top_100['song'][i])
            position_top_100.append(i)
            number_1.pop(0)
        if len(number_2)> 0:
            songs_to_recommend_second_top.append(second_top['song'][i])
            position_second_top.append(i)
            number_2.pop(0)
    if len(songs_to_recommend_top_100)> 0:
        print('Good choice! This artist has ' + str(len(songs_to_recommend_top_100)) + ' songs:')
        for i in range(len(songs_to_recommend_top_100)):
            print('-' + songs_to_recommend_top_100[i] + ' in position ' + str(position_top_100[i] + 1))
        return 
    elif len(songs_to_recommend_second_top)> 0:
        print('Good choice! This artist has ' + str(len(songs_to_recommend_second_top)) + ' songs:')
        for i in range(len(songs_to_recommend_second_top)):
            print('-' + songs_to_recommend_second_top[i] + ' in position ' + str(position_second_top[i] + 1))
        return 
    else:
        artist_songs = comparing_table[comparing_table['artist'] == artist].head()
        if len(artist_songs['artist']) > 0:
            random_one = artist_songs['song'].values[0]
            random_two = artist_songs['song'].values[1]
            print("Sorry, this artist isn't now into the top 100, but in my list i have " + str(len(comparing_table[comparing_table['artist'] == artist])) + " " + artist+ "'s songs, for example:\n")
            print("- " + random_one + "\n")
            print("- " + random_two)
            return 0
        else:
            print("Sorry, this artist isn't into the top 100 and in my list there are no songs from this artist")
            return 0

def recommending_song_improved(song):
    songs_to_recommend_top_100 = []
    position_top_100 = []
    songs_to_recommend_second_top = []
    position_second_top = []
    for i in range(len(top_100['song'])):
        if song == top_100['song'][i]:
            songs_to_recommend_top_100.append(top_100['song'][i])
            position_top_100.append(i)
        elif song == second_top['song'][i]:
            songs_to_recommend_second_top.append(second_top['song'][i])
            position_second_top.append(i)
    if len(songs_to_recommend_top_100)> 0:
        random_number = position_top_100[0]
        while random_number == position_top_100[0]:
            random_number = randint(0,99)
        i_recommend = top_100['song'][random_number]
        return print("Good choice! This song is now in the position number " + str(position_top_100[0]+1) + " of our first top from " + top_100['artist'][position_top_100[0]] + ". Here we have another recommendation of this top 100 songs: " + i_recommend + " from " + top_100['artist'][random_number])
    elif len(songs_to_recommend_second_top)> 0:
        random_number = position_second_top[0]
        while random_number == position_second_top[0]:
            random_number = randint(0,99)
        i_recommend = second_top['song'][random_number]
        return print("Good choice! This song is now in the position number " + str(position_second_top[0]+1) + " of our second top from " + second_top['artist'][position_second_top[0]] + ". Here we have another recommendation of this top 100 songs: " + i_recommend + " from " + second_top['artist'][random_number])
    else:
        results = sp.search(q=song, type = 'track', limit=1)
        uri = results["tracks"]["items"][0]["uri"]
        features = sp.audio_features(uri)
        data_features = pd.DataFrame(features)
        numeric_features = data_features._get_numeric_data()
        cluster_prediction = kmeans.predict(numeric_features)[0]
        similar_songs = comparing_table[comparing_table['cluster_type'] == cluster_prediction].sample(1)
        song_recommended = similar_songs['song'].values[0]
        artist_recommended = similar_songs['artist'].values[0]
        print("Your song is not in the top 100, but we can recommend you this song from our database: "+ song_recommended + " from " + artist_recommended+ "... Hope you like it!!!")
        return 0


def asking_song_improved():
    print("Which song do you want?")
    song_name = input()
    value = recommending_song_improved(song_name)
    while value == 0:
        print("Do you want to try again?(yes/no)")
        yes_no = input()
        if yes_no == 'yes':
            print("Which new song do you want to try?")
            song_name = input()
            value = recommending_song_improved(song_name)
        elif yes_no == 'no':
            value = 1
        else:
            print("That's not a valid value")
            value = 1
    return

def asking_artist_improved():
    print("Which artist do you want?")
    artist_name = input()
    value = recommending_artist_improved(artist_name)
    while value == 0:
        print("Do you want to try again?(yes/no)")
        yes_no = input()
        if yes_no == 'yes':
            print("Which new artist do you want to try?")
            song_name = input()
            value = recommending_artist_improved(artist_name)
        elif yes_no == 'no':
            value = 1
        else:
            print("That's not a valid value")
            value = 1
    return

def asking_improved():
    print("If you want to search by song enter 1, and if you want to search by artist enter 2")
    search = input()
    while (search != '1') & (search != '2'):
        print("This isn't a valid value... Try again")
        print("If you want to search by song enter 1, and if you want to search by artist enter 2")
        search = input()
    if search == '1':
        return asking_song_improved()
    elif search == '2':
        return asking_artist_improved()

final_dataframe = pd.read_excel('./files_for_lab/songs_completed.xlsx')
info_dataframe = pd.read_excel('./files_for_lab/songs_info.xlsx')
top_100 = pd.read_excel('./files_for_lab/top_100.xlsx')
second_top = pd.read_excel('./files_for_lab/second_top.xlsx')
comparing_table = pd.read_excel('./files_for_lab/comparing_table.xlsx')


secrets_file = open("secrets.txt","r")

string = secrets_file.read()

secrets_dict={}
for line in string.split('\n'):
    if len(line) > 0:
        secrets_dict[line.split(':')[0]]=line.split(':')[1]

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=secrets_dict['cid'],
                                                           client_secret=secrets_dict['csecret']))


info_dataframe = info_dataframe.drop(['Unnamed: 0'], axis = 1)
scaled_variables = StandardScaler().fit_transform(info_dataframe)
pd.DataFrame(scaled_variables,columns=info_dataframe.columns).head()
kmeans = KMeans(n_clusters=9, random_state=1234)
kmeans.fit(scaled_variables)


asking_improved()