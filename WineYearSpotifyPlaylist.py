#!/usr/bin/env python
# coding: utf-8

# In[1]:


import spotipy
import webbrowser
import json
import urllib.request
import geocoder
from nltk.corpus import stopwords
import spotipy.util as util
import random

# In[2]:


wine_type = ['reds', 'whites', 'sparkling', 'rose', 'dessert', 'port']
wine_type_choice = random.choice(wine_type)

print(wine_type_choice)

# In[3]:


# copy and paste the url into your browser to see what data you are getting back
request = urllib.request.Request("https://api.sampleapis.com/wines/" + wine_type_choice)
response = urllib.request.urlopen(request)

# In[4]:


list_of_wine = json.loads(response.read())

# In[5]:


type(request)

# In[6]:


print(list_of_wine)

# In[7]:


# list_of_wine[0]

# In[8]:


choice_of_wine = random.choice(list_of_wine)
name_of_wine = random.choice(list_of_wine)['wine']
year_of_wine = name_of_wine[-4:]
winery_of_wine = choice_of_wine['winery']

print(choice_of_wine)
print(name_of_wine)
print(year_of_wine)
print(winery_of_wine)

# In[9]:


country_of_wine = choice_of_wine['location'].split('\n·\n')[0]
region_of_wine = choice_of_wine['location'].split('\n·\n')[1]
print(country_of_wine)
print(region_of_wine)

# In[11]:


# open file with keys and set the path to your credentials JSON file
credentials = "spotify_keys.json"
with open(credentials, "r") as keys:
    api_tokens = json.load(keys)

# In[12]:


api_tokens

# In[13]:


client_id = api_tokens["client_id"]
client_secret = api_tokens["client_secret"]
redirectURI = api_tokens["redirect"]
username = api_tokens["username"]

# In[14]:


scope = 'user-read-private user-read-playback-state user-modify-playback-state playlist-modify-public user-library-read'
token = util.prompt_for_user_token(username, scope, client_id=client_id,
                           client_secret=client_secret,
                           redirect_uri=redirectURI)

# In[15]:


token

# In[16]:


#if wine_type_choice == wine_type[0]:
   # print(wine_type_choice[:-1])
#elif wine_type_choice == wine_type[1]:
   # print(wine_type_choice[:-1])
#else:
    #print(wine_type_choice)

new_name = wine_type_choice
if wine_type_choice == str(wine_type[0]):
    new_name = wine_type_choice.replace('s', '')
elif wine_type_choice == str(wine_type[1]):
     new_name = wine_type_choice.replace('s', '')
    
print(new_name)

# In[17]:


# create my Spotify object
sp = spotipy.Spotify(auth=token)

# In[18]:


# start a list of songs for my headline playlist
songs_for_playlist = []
#have for loop run 50 times
for x in range(50):
    # search for artist based on the year of the wine
    searchResults = sp.search(q="year:" + str(year_of_wine), type="track", limit=50, offset = 100)
    # if the search returns anything
    if len(searchResults['tracks']['items']) > 0:
        songs_for_playlist.append(searchResults['tracks']['items'][x]['uri'])
        
print(songs_for_playlist)

# In[19]:


searchResults = sp.search(q=2002, type="track", limit=1, offset = 100)
print(searchResults)

# In[20]:


my_playlist = sp.user_playlist_create(user=username, name="Playlist paired with year of " + year_of_wine, public=True,
                                      description="Songs for " + new_name + " wine " + name_of_wine + " from winery " + winery_of_wine + " in " + region_of_wine + ", " + country_of_wine)
results = sp.user_playlist_add_tracks(username, my_playlist['id'], songs_for_playlist)
print(results)

print(my_playlist)

# In[21]:


webbrowser.open(my_playlist['external_urls']['spotify'])

# In[ ]:



