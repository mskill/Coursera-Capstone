#!/usr/bin/env python
# coding: utf-8

# ## <center>DATA SCIENCE CAPSTONE</center>
# ### <center>BATTLE OF NEIGHBOURHOOD</center>
# ### <center> TORONTO RESTURANTS </center>

# ### Introduction
# 
# <p> Toronto is a most populated city of Canada. Most of people migrated there due to jobs and most Indian are also there. A big community of Indians are residing currently in Toronto.</p>
#     
# #### Problem Description: 
# 
# <p>When one changes the city, he/she wants to be in the same environment in which he/she is currently residing. Like, if he/she is living in a family, he/she wants to be in the society in which most of the families are living. Say this is you and you live on the west side of the city of Toronto in Canada. You love your neighborhood, mainly because of all the great amenities and other types of venues that exist in the neighborhood, such as gourmet fast food joints, pharmacies, parks, grad schools. Now say you receive a job offer from a great company on the other side of the city with great career prospects. However, given the far distance from your current place you unfortunately must move if you decide to accept the offer. Wouldn't it be great if you're able to determine neighborhoods on the other side of the city that are the same as your current neighborhood, and if not, perhaps similar neighborhoods that are at least closer to your new job? </p>
# 
# So, we need to compare different neighborhoods in terms of a service, search for potential explanation of <br>
# 1) Using API, we will get the resturants,<br>
# 2) Getting the Indian Resturant on basis of user location, <br>
# 3) Using Map to check the locations of resturants. <br>
# 
# 
# I will segment it into different neighborhoods using the geographical coordinates of the center of each neighborhood, and then using a combination of location data and machine learning, I will group the neighborhoods into clusters. 

# ### Target audience:
# 
# <p>I believe this is for every person who is shifting from one place to another. As the need for a job everyone must travel and wants to be in a place where he got all the amenities. After a long hour of job, he needs that the daily needs should be nearer as much it can be. So, predicting the Battle of neighborhood is correct for description for this project. 
# </p>

# ### Dataset:
# I would be using the Canada data to explore the neighborhood. The link for the wikipedia is 'https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M'

# #### <i>Installing and Importing Packages</i>

# In[47]:


#Installing the packages
#get_ipython().system(u' pip install --upgrade pip')
#get_ipython().system(u' pip install beautifulsoup4')
#!pip install lxml
#!pip install html5lib
#!pip install requests

#Importing packages
from bs4 import BeautifulSoup
import requests # library to handle requests
import pandas as pd # library for data analsysis
import numpy as np # library to handle data in a vectorized manner
import random # library for random number generation

#!conda install -c conda-forge geopy --yes 
from geopy.geocoders import Nominatim # module to convert an address into latitude and longitude values

# libraries for displaying images
from IPython.display import Image 
from IPython.core.display import HTML 
    
# tranforming json file into a pandas dataframe library
from pandas.io.json import json_normalize

#!conda install -c conda-forge folium=0.5.0 --yes
import folium # plotting library

print('Folium installed')
print('Libraries imported.')


# #### Reading HTMLPage and getting rows and columns

# In[48]:


#Reading HTMl page 
url='https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M'
response=requests.get(url)
html = response.text
page = BeautifulSoup(html,'html.parser')
#print(page)


#Getting table from the page that is saved in page1
wiki_table = page.body.table.tbody
#print(wiki_table)

# table = page.find_all('table')[0] # Grab the first table

# definition for getting cell
def get_cell(element):
    cells = element.find_all('td')
    row = []
    
    for cell in cells:
        if cell.a:            
            if (cell.a.text):
                row.append(cell.a.text)
                continue
        row.append(cell.string.strip())
        
    return row
#Definition for getting rows.
def get_row():    
    data = []  
    
    for tr in wiki_table.find_all('tr'):
        row = get_cell(tr)
        if len(row) != 3:
            continue
        data.append(row)        
    
    return data


# #### Creating a Dataframe for 3 columns PostalCode, Borough, and Neighborhood

# In[49]:


rows = get_row()
columns_get = ['Postcode', 'Borough', 'Neighbourhood']
df = pd.DataFrame(rows, columns=columns_get)
df.head()


# #### Shape of the dataframe before dropping

# In[50]:


df.shape


# #### Cleaning the data

# In[51]:


df=df[df.Borough != 'Not assigned']
df = df.sort_values(by=['Postcode','Borough'])

df.reset_index(inplace=True)
df.drop('index',axis=1,inplace=True)

df.head()


# #### Dropping the duplicates

# In[52]:


df_post = df['Postcode']
df_post.drop_duplicates(inplace=True)
#df_post
df_new = pd.DataFrame(df_post)
df_new['Borough'] = '';
df_new['Neighbourhood'] = '';


# In[53]:


df_new.reset_index(inplace=True)
df_new.drop('index', axis=1, inplace=True)
df.reset_index(inplace=True)
df.drop('index', axis=1, inplace=True)


# #### Using groupby function to group the same Postcode nad Borough in neighbourhood.

# In[54]:


df_postcode = df.groupby(['Postcode', 'Borough'])['Neighbourhood'].apply(', '.join).reset_index()
df_postcode.head()
locgeo_df = pd.read_csv('https://cocl.us/Geospatial_data', index_col='Postal Code')
toronto_data = df_postcode.join(locgeo_df, on='Postcode')
toronto_data.drop('Postcode', axis=1, inplace=True)
toronto_data.shape


# In[55]:


# toronto_data = df_postcode.join(df, on='Postcode')
# toronto_data.drop('Postcode', axis=1, inplace=True)
# toronto_data.shape


# #### Getting new Dataframe shape after cleaning

# In[56]:


df_postcode.shape


# #### Plotting different Neighbourhood

# In[57]:


import matplotlib.pyplot as plt
plt.figure(figsize=(9,5), dpi = 100)
plt.title('Number of Neighbourhood ')
#On x-axis
#plt.xlabel('Borough', fontsize = 15)
#On y-axis
#plt.ylabel('No.of Neighbourhood', fontsize=15)
#giving a line plot
toronto_data.groupby('Borough')['Neighbourhood'].count().plot(kind='line')
#legend
plt.legend()
#displays the plot
plt.show()


# ### Define Foursquare Credentials and Version

# In[58]:


CLIENT_ID = 'VQEMV3MW5RJ3JOJ2VFAUYG50KYQY5UEIEQBQVOCPMWFOSUOI' # your Foursquare ID
CLIENT_SECRET = '0HVGRNG2OFBOG1WFFC3RS3BPME5J4KDTNBOKMLXLI0OGBIQ4' # your Foursquare Secret
VERSION = '20180604'
LIMIT = 30
print('Your credentails:')
print('CLIENT_ID: ' + CLIENT_ID)
print('CLIENT_SECRET:' + CLIENT_SECRET)


# #### Let's again assume that you are staying at Hotel/Residence. So let's start by converting the ddress to its latitude and longitude coordinates.

# In order to define an instance of the geocoder, we need to define a user_agent. We will name our agent <em>foursquare_agent</em>, as shown below
# 
# Enter the address and specify city in city codes like Delhi as DL, New York as NY etc. and press "Enter".

# In[59]:


address = input('Enter your address: ')


# In[60]:


#address = '123 Queen St W, Toronto, CA'

geolocator = Nominatim(user_agent="foursquare_agent")
location = geolocator.geocode(address)
latitude = location.latitude
longitude = location.longitude
print(latitude, longitude)


# ## 1. Search for a specific venue category

# #### Now, let's assume that it is lunch time, and you are craving food. So, let's define a query to search for food that is within 500 metres from the address Hotel. 
# 
# Enter your inputs and press "Enter".

# In[61]:


search_query = input('What type of food you want to eat? (Italian/Chinese/Indian etc.): ')


# In[62]:


#search_query = 'Indian Resturants'
radius = 500
print(search_query + ' .... OK!')
auth='https://api.foursquare.com/oauth2/authenticate?client_id=VQEMV3MW5RJ3JOJ2VFAUYG50KYQY5UEIEQBQVOCPMWFOSUOI'
auth


# #### Define the corresponding URL

# In[63]:


url = 'https://api.foursquare.com/v2/venues/search?client_id={}&client_secret={}&ll={},{}&v={}&query={}&radius={}&limit={}'.format(CLIENT_ID, CLIENT_SECRET, latitude, longitude, VERSION, search_query, radius, LIMIT)
#url = 'https://api.foursquare.com/v2/venues/search?client_id=CLIENT_ID&client_secret=CLIENT_SECRET&ll=LATITUDE,LONGITUDE&v=VERSION&query=QUERY&radius=radius&limit=LIMIT'.format(CLIENT_ID, CLIENT_SECRET, latitude, longitude, VERSION, search_query, radius, LIMIT)
url


# #### Define the corresponding URL

# #### Send the GET Request and examine the results

# In[64]:


import json
results = requests.get(url).json()
results


# #### Get relevant part of JSON and transform it into a *pandas* dataframe

# In[65]:


# assign relevant part of JSON to venues
venues = results['response']['venues']

# tranform venues into a dataframe
dataframe = json_normalize(venues)
dataframe.head()


# #### Define information of interest and filter dataframe

# In[66]:


# keep only columns that include venue name, and anything that is associated with location
filtered_columns = ['name', 'categories'] + [col for col in dataframe.columns if col.startswith('location.')] + ['id']
dataframe_filtered = dataframe.loc[:, filtered_columns]

# function that extracts the category of the venue
def get_category_type(row):
    try:
        categories_list = row['categories']
    except:
        categories_list = row['venue.categories']
        
    if len(categories_list) == 0:
        return None
    else:
        return categories_list[0]['name']

# filter the category for each row
dataframe_filtered['categories'] = dataframe_filtered.apply(get_category_type, axis=1)

# clean column names by keeping only last term
dataframe_filtered.columns = [column.split('.')[-1] for column in dataframe_filtered.columns]

dataframe_filtered


# #### Let's visualize the restaurants that are nearby

# In[67]:


dataframe_filtered.name


# In[68]:


dataframe_filtered=dataframe_filtered.set_index(['id'])


# In[69]:


# venues_map = folium.Map(location=[latitude, longitude], zoom_start=13) # generate map centred around the Conrad Hotel

# # add a red circle marker to represent the Conrad Hotel
# folium.features.CircleMarker(
#     [latitude, longitude],
#     radius=10,
#     color='red',
#     popup='Conrad Hotel',
#     fill = True,
#     fill_color = 'red',
#     fill_opacity = 0.6
# ).add_to(venues_map)

# # add the Italian restaurants as blue circle markers
# for lat, lng, label in zip(dataframe_filtered.lat, dataframe_filtered.lng, dataframe_filtered.categories):
#     folium.features.CircleMarker(
#         [lat, lng],
#         radius=5,
#         color='blue',
#         popup=label,
#         fill = True,
#         fill_color='blue',
#         fill_opacity=0.6
#     ).add_to(venues_map)

# # display map
# venues_map


# ## 2. Explore Neighborhoods in Toronto

# In[70]:


for x in range(len(dataframe_filtered.index)):
    venue_id=dataframe_filtered.index[x]
    print(venue_id)
    url = 'https://api.foursquare.com/v2/venues/{}?client_id={}&client_secret={}&v={}'.format(venue_id, CLIENT_ID, CLIENT_SECRET, VERSION)
    result = requests.get(url).json()
    try:
        dataframe_filtered.loc[venue_id,'Rating']=result['response']['venue']['rating']
        #print(result['response']['venue']['rating'])
    except:
        dataframe_filtered.loc[venue_id,'Rating']=0
        #print('This venue has not been rated yet.')
    try:
        dataframe_filtered.loc[venue_id,'Pricing']=result['response']['venue']['price']['tier']
        #print(result['response']['venue']['rating'])
    except:
        dataframe_filtered.loc[venue_id,'Pricing']=0    
    try:
        dataframe_filtered.loc[venue_id,'Likes']=result['response']['venue']['likes']['count']
        #print(result['response']['venue']['rating'])
    except:
        dataframe_filtered.loc[venue_id,'Likes']=0
dataframe_filtered


# In[71]:


dataframe_filtered.to_csv('IndianResturants.csv')


# In[72]:


indiandf = pd.read_csv("IndianResturants.csv")
indiandf


# In[73]:


indiandf=indiandf.sort_values(by=['Likes'], ascending=False)
#indiandf


# In[74]:


indiandf[['name','lat','lng','categories','Rating','Pricing','Likes','distance']]


# In[75]:


indiandf


# In[76]:


indiandf['Rating'].max()


# In[77]:


indiandf1=indiandf.groupby('name',as_index=False).mean()[['name','Rating']]
indiandf1.columns=['Name','Average Rating']
indiandf1


# In[78]:


indiandf1.sort_values(['Average Rating'],ascending=False).head()


# #### Plotting average rating

# In[79]:


plt.figure(figsize=(9,5), dpi = 100)
# title
plt.title('Average rating of Indian Resturants')
#On x-axis
plt.xlabel('Name', fontsize = 15)
#On y-axis
plt.ylabel('Average Rating', fontsize=15)
#giving a bar plot
indiandf1.groupby('Name').mean()['Average Rating'].plot(kind='bar')
#legend
plt.legend()
#displays the plot
plt.show()


# In[80]:


def color(avg): 
    if avg >= 5:
        col ='Green'
    elif 3 <= avg < 5: 
        col = 'yellow'
    else: 
        col='blue'
    return col 


# In[81]:


venues_map = folium.Map(location=[latitude, longitude], zoom_start=13) # generate map centred around the Conrad Hotel

# add a red circle marker to represent the Conrad Hotel
folium.features.CircleMarker(
    [latitude, longitude],
    radius=10,
    color='red',
    popup='Toronto',
    fill = True,
    fill_color = 'red',
    fill_opacity = 0.6
).add_to(venues_map)

for lat, lng, label,avg in zip(indiandf.lat, indiandf.lng, indiandf.categories,indiandf.Rating):
    folium.features.CircleMarker(
        [lat, lng],
        radius=5,
        color=color(avg),
        popup=label,
        fill = True,
        #fill_color='blue',
        fill_opacity=0.6
    ).add_to(venues_map)

# for index,row in indiandf.iterrows():
#     folium.features.CircleMarker(
#         [row['lat'],row['lng']],
#         radius=5,
#         color=color(avg),
#         popup=(row['categories']),
#         fill = True,
#         #fill_color='blue',
#         fill_opacity=0.6
#     ).add_to(venues_map)

# # display map
venues_map


# #### Conclusion <br>
# Green dot showing the map is having the highest rating and this for Indian Biriyani House.

# In[ ]:




