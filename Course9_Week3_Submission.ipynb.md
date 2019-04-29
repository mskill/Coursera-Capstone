
# Neighborhoods in Toronto

### Importing Packages


```python
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
```

## Reading HTMLPage and getting rows and columns


```python
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
```

### Creating a Dataframe for 3 columns PostalCode, Borough, and Neighborhood


```python
rows = get_row()
columns_get = ['Postcode', 'Borough', 'Neighbourhood']
df = pd.DataFrame(rows, columns=columns_get)
df.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Postcode</th>
      <th>Borough</th>
      <th>Neighbourhood</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>M1A</td>
      <td>Not assigned</td>
      <td>Not assigned</td>
    </tr>
    <tr>
      <th>1</th>
      <td>M2A</td>
      <td>Not assigned</td>
      <td>Not assigned</td>
    </tr>
    <tr>
      <th>2</th>
      <td>M3A</td>
      <td>North York</td>
      <td>Parkwoods</td>
    </tr>
    <tr>
      <th>3</th>
      <td>M4A</td>
      <td>North York</td>
      <td>Victoria Village</td>
    </tr>
    <tr>
      <th>4</th>
      <td>M5A</td>
      <td>Downtown Toronto</td>
      <td>Harbourfront</td>
    </tr>
  </tbody>
</table>
</div>



#### Shape of the dataframe before dropping


```python
df.shape
```




    (288, 3)



#### Cleaning the data


```python
df=df[df.Borough != 'Not assigned']
df = df.sort_values(by=['Postcode','Borough'])

df.reset_index(inplace=True)
df.drop('index',axis=1,inplace=True)

df.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Postcode</th>
      <th>Borough</th>
      <th>Neighbourhood</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>M1B</td>
      <td>Scarborough</td>
      <td>Rouge</td>
    </tr>
    <tr>
      <th>1</th>
      <td>M1B</td>
      <td>Scarborough</td>
      <td>Malvern</td>
    </tr>
    <tr>
      <th>2</th>
      <td>M1C</td>
      <td>Scarborough</td>
      <td>Highland Creek</td>
    </tr>
    <tr>
      <th>3</th>
      <td>M1C</td>
      <td>Scarborough</td>
      <td>Rouge Hill</td>
    </tr>
    <tr>
      <th>4</th>
      <td>M1C</td>
      <td>Scarborough</td>
      <td>Port Union</td>
    </tr>
  </tbody>
</table>
</div>



#### Dropping the duplicates


```python
df_post = df['Postcode']
df_post.drop_duplicates(inplace=True)
#df_post
df_new = pd.DataFrame(df_post)
df_new['Borough'] = '';
df_new['Neighbourhood'] = '';
```


```python
df_new.reset_index(inplace=True)
df_new.drop('index', axis=1, inplace=True)
df.reset_index(inplace=True)
df.drop('index', axis=1, inplace=True)
```

#### Using groupby function to group the same Postcode nad Borough in neighbourhood.


```python
df_2 = df.groupby(['Postcode', 'Borough'])['Neighbourhood'].apply(', '.join).reset_index()
df_2.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Postcode</th>
      <th>Borough</th>
      <th>Neighbourhood</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>M1B</td>
      <td>Scarborough</td>
      <td>Rouge, Malvern</td>
    </tr>
    <tr>
      <th>1</th>
      <td>M1C</td>
      <td>Scarborough</td>
      <td>Highland Creek, Rouge Hill, Port Union</td>
    </tr>
    <tr>
      <th>2</th>
      <td>M1E</td>
      <td>Scarborough</td>
      <td>Guildwood, Morningside, West Hill</td>
    </tr>
    <tr>
      <th>3</th>
      <td>M1G</td>
      <td>Scarborough</td>
      <td>Woburn</td>
    </tr>
    <tr>
      <th>4</th>
      <td>M1H</td>
      <td>Scarborough</td>
      <td>Cedarbrae</td>
    </tr>
  </tbody>
</table>
</div>



#### Getting new Dataframe shape after cleaning


```python
df_2.shape
```




    (103, 3)




```python

```
