#!/usr/bin/env python
# coding: utf-8

# # Neighborhoods in Toronto

# ### Importing Packages

# In[42]:


#Installing the packages
#get_ipython().system(u' pip install --upgrade pip')
#get_ipython().system(u' pip install beautifulsoup4')
#!pip install lxml
#!pip install html5lib
#!pip install requests

#Importing packages
import pandas as pd
import requests
from bs4 import BeautifulSoup


# ## Reading HTMLPage and getting rows and columns

# In[43]:


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


# ### Creating a Dataframe for 3 columns PostalCode, Borough, and Neighborhood

# In[44]:


rows = get_row()
columns_get = ['Postcode', 'Borough', 'Neighbourhood']
df = pd.DataFrame(rows, columns=columns_get)
df.head()


# #### Shape of the dataframe before dropping

# In[45]:


df.shape


# #### Cleaning the data

# In[46]:


df=df[df.Borough != 'Not assigned']
df = df.sort_values(by=['Postcode','Borough'])

df.reset_index(inplace=True)
df.drop('index',axis=1,inplace=True)

df.head()


# #### Dropping the duplicates

# In[47]:


df_post = df['Postcode']
df_post.drop_duplicates(inplace=True)
#df_post
df_new = pd.DataFrame(df_post)
df_new['Borough'] = '';
df_new['Neighbourhood'] = '';


# In[48]:


df_new.reset_index(inplace=True)
df_new.drop('index', axis=1, inplace=True)
df.reset_index(inplace=True)
df.drop('index', axis=1, inplace=True)


# #### Using groupby function to group the same Postcode nad Borough in neighbourhood.

# In[50]:


df_2 = df.groupby(['Postcode', 'Borough'])['Neighbourhood'].apply(', '.join).reset_index()
df_2.head()


# #### Getting new Dataframe shape after cleaning

# In[51]:


df_2.shape


# In[ ]:




