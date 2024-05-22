#!/usr/bin/env python
# coding: utf-8

# In[1]:


# import necessary libraries
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# load the database
df = pd.read_csv("steam-200k.csv")
# df.head()


# In[2]:


# rename the columns
cols = {'151603712':'user_id','The Elder Scrolls V Skyrim':'game_name','purchase':'status','1.0':'Hourplayed'}
df.rename(columns = cols,inplace =True)
# df.head()


# In[3]:


# drop unnecessary columns
df.drop(columns = ['0'], inplace=True)
df.drop_duplicates(inplace=True)


# In[4]:


# df.shape


# In[5]:


# df.head()


# In[6]:


# plotting the top 15 games:
# df['game_name'].value_counts().head(15).plot(kind = 'bar',figsize =(15,5), title = "Most Played and Purchased Games")
def top_games():
    top_games_lst = df['game_name'].value_counts().head(5)
    return top_games_lst


# In[7]:


# from this we get id of player who had played a game for more than or equal to 2 hours
df= df[(df['Hourplayed']>=2) & (df['status']=='play')]

df = df[df.groupby('game_name').user_id.transform(len)>=20]

df['user_id'] = df['user_id'].astype(str)

average = df.groupby(['game_name'],as_index = False).Hourplayed.mean()

average['avg_hourplayed'] = average['Hourplayed']
average.drop(columns ='Hourplayed',inplace = True )
average.sort_values(by=['avg_hourplayed'], ascending=False) # type: ignore
# average.head()
# average.plot.scatter(x="game_name", y="avg_hourplayed")


# In[8]:


# changing avg_hourplayed into ratings
df = df.merge(average,on = 'game_name')

condition = [
    df['Hourplayed']>= (0.8*df['avg_hourplayed']),
   (df['Hourplayed']>=0.6*df['avg_hourplayed'])&(df['Hourplayed']<0.8*df['avg_hourplayed']),
   (df['Hourplayed']>=0.4*df['avg_hourplayed'])&(df['Hourplayed']<0.6*df['avg_hourplayed']),
   (df['Hourplayed']>=0.2*df['avg_hourplayed'])&(df['Hourplayed']<0.4*df['avg_hourplayed']),
    df['Hourplayed']>=0
    
]
values = [5,4,3,2,1]
df['rating'] = np.select(condition,values)

# df.head()


# In[9]:


# keeping necessary data and removing redundant columns
df.drop(columns = ['status', 'Hourplayed', 'avg_hourplayed'], inplace=True)
# df.head()


# In[10]:


# 
pv = df.pivot_table(index=['user_id'],columns=['game_name'],values = 'rating')

pv = pv.apply(lambda x: (x-np.mean(x))/(np.max(x)-np.min(x)),axis=1)

pv = pv.fillna(0)
pv = pv.T
pv = pv.loc[:,(pv != 0).any(axis=0)]

# Collaborative Filtering using KNN
from sklearn.neighbors import NearestNeighbors
knn = NearestNeighbors(algorithm='brute',leaf_size=30,metric='cosine',metric_params=None,n_jobs=-1,n_neighbors=20,p=2,radius=1)
knn.fit(pv) # type: ignore


# In[13]:

def query(name):
    # qury_game = 'Ace of Spades' # input the game name
    for i in range(431):
        if pv.index[i] == name:
            return i



# chooses a game at random
#qury = np.random.choice(pv.shape[0])
#print("The Choosen Game = ", pv.index[qury], qury)


# In[14]:


# compute neighbor based on Euclidian distance
# calculates at most 6 nearest neighbors

def out(qury):
    distance , indices = knn.kneighbors(pv.iloc[qury,:].values.reshape(1,-1),n_neighbors=11) # type: ignore

    lst = []
    for i in range(0,len(distance.flatten())):
        if i == 0:
            # print('Recommendation for {0} \n'.format(pv.index[qury]))
            pass
        else:
            # print('{0} : {1} with distance of {2}'.format(i,pv.index[indices.flatten()[i]], distance.flatten()[i]))
            lst.append(pv.index[indices.flatten()[i]])

    return lst
