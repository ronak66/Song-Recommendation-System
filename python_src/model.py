import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pickle

from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import PCA
# from yellowbrick.cluster import KElbowVisualizer

class SongReccomender:

    def __init__(self,filename):
        self.df = pd.read_csv(filename)
        self.remove_categorical_Data()
        self.pca()
        self.train_and_add_categorical_columns()

    
    def remove_categorical_Data(self):
        self.cols = ['artist','danceability','energy','key','loudness','mode','speechiness','acousticness','instrumentalness','liveness','valence','tempo','duration_ms','time_signature','label']
        self.non_categorical = ['danceability','energy','loudness','speechiness','acousticness','instrumentalness','liveness','valence','tempo','duration_ms']
        self.categorical = ['artist','key','mode','time_signature','label']

# %ms = MinMaxScaler()
        self.df[self.non_categorical] = self.df[self.non_categorical].apply(lambda x: (x - x.min()) / (x.max() - x.min()))
        
    def pca(self):
        pca = PCA(0.95)
        self.data = self.df.drop_duplicates()
        self.data = pca.fit_transform(self.data[self.non_categorical])
        # cluster_plot(pd.DataFrame(self.data))
        pd.DataFrame(self.data).head()
        return


    def train(self,df_train):
        n = 1
        for _ in range(n):
            self.km = KMeans(
                n_clusters=4, init='random',
                n_init=10, max_iter=1000, 
                tol=1e-04, random_state=0
            )
            y_km = self.km.fit(df_train)
        return self.km

    def k_mean_distance(self,center_coordinates, data_coordiantes):
        summ=0
        mag=0
        for i in range(len(center_coordinates)):
            summ+=(center_coordinates[i]-data_coordiantes[i])**2
            mag+=(data_coordiantes[i])**2
        return (summ)*0.5

    
    def train_and_add_categorical_columns(self):
        self.train(self.data)
        # pickle.dump(km, open('KMeans_Clustering', 'wb'))
        self.data['label'] = self.km.labels_
        self.data['artist'] = self.df.artist
        self.data['name'] = self.df.name
        self.data['preview'] = self.df.preview
        self.data['popularity'] = self.df.popularity
        self.data['type'] = self.df.label
        self.data.head()


    def song_recommendation(self,song,data):
        arr = []
        dummy_df = data.loc[data['label']==song.label.values[0]]
        print(len(dummy_df.values))
        for i in range(len(dummy_df.values)):
            if(i>51): break
            dist = self.k_mean_distance(dummy_df.values[i][0:7],song.values[0][0:7])
            arr.append((
                dummy_df.values[i][11]/(dist+0.00000001)**2,
                dist,
                dummy_df.values[i][11],
                dummy_df.values[i][8],
                dummy_df.values[i][9],
                dummy_df.values[i][10],
                dummy_df.values[i][12]
            ))
        arr.sort()
        return arr

    def song_print(self,song):
        print('='*200)
        print('Artist:  ', song.artist.values[0])
        print('Song Name:   ', song.name.values[0])
        print('Type:   ', song['type'].values[0])
        print('Preview link:   ', song.preview.values[0])
        print('='*200)

    def print_song_reccomendation(self,song_number):
        # song = self.data.loc[[2980]]
        song = self.data.loc[[song_number]]
        ans = self.song_recommendation(song,self.data)
        self.song_print(song)
        j=1
        for i in ans[::-1]:
            print('Number:  ', j)
            print('Popularity/distance:  ',i[0])
            print('Artist:  ', i[3])
            print('Song Name:   ', i[4])
            print('Type:   ', i[6])
            print('Preview link:   ', i[5])
            print('-'*100)
            j+=1
        return


if __name__ == '__main__':
    sr = SongReccomender('../Data/final.csv')
    sr.print_song_reccomendation(song_number=2980)