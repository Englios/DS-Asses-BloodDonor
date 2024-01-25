#!/usr/bin/env python
# coding: utf-8

# # Auto Import test

# In[101]:


import requests
import pandas as pd
from datetime import datetime


from pprint import pprint
from io import BytesIO


# ## Gran Data

# In[102]:


gran_data = requests.get('https://dub.sh/ds-data-granular')
gran_data_df = pd.read_parquet((BytesIO(gran_data.content)))
# gran_data_df.to_csv(f'./data/granular_data.csv', index=False)


# In[103]:


gran_data_df.info()
copy_gran_df = gran_data_df.copy()


# In[104]:


gran_data_df.sample(5).head()


# In[105]:


print(gran_data_df.describe())


# In[106]:


print(gran_data_df.isna().sum())


# In[107]:


print(gran_data_df['birth_date'].hist())


# In[108]:


copy_gran_df['visit_date'] = pd.to_datetime(gran_data_df['visit_date'])


# In[109]:


copy_gran_df['current_age'] = datetime.now().year - copy_gran_df['birth_date']
copy_gran_df['visit_age'] = pd.to_datetime(copy_gran_df['visit_date']).dt.year - copy_gran_df['birth_date']
copy_gran_df


# In[110]:


copy_gran_df['days_since_last_visit'] = copy_gran_df.groupby('donor_id')['visit_date'].diff().dt.days
copy_gran_df['months_since_last_visit'] = copy_gran_df['days_since_last_visit'] // 30
copy_gran_df['years_since_last_vist'] = copy_gran_df['months_since_last_visit'] // 12
copy_gran_df = copy_gran_df.fillna(0)
copy_gran_df


# In[111]:


age_bins = [17, 19, 31, 41, 51, 61, 100]
age_labels = ['17-18', '19-30', '31-40', '41-50', '51-60', '61+']

copy_gran_df['age_group'] = pd.cut(copy_gran_df['current_age'], 
                                   bins=age_bins, labels=age_labels, right=False)

print(copy_gran_df[['current_age', 'age_group']])


# In[112]:


visits_age_df = copy_gran_df.groupby(['age_group', copy_gran_df['visit_date'].dt.year])['donor_id'].count().reset_index()
visits_age_df.columns = ['age_group', 'year', 'count']
visits_age_pivot_df = visits_age_df.pivot(index='year', columns='age_group', values='count')
print(visits_age_pivot_df)


# In[113]:


visits_df = copy_gran_df.groupby(copy_gran_df['visit_date'].dt.year)['donor_id'].count().reset_index()
visits_df.columns = ['year', 'count']
print(visits_df)


# ## Trend Plot

# In[114]:


import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

plt.figure(figsize=(10,5))
sns.set(style="whitegrid")

sns.lineplot(data=visits_df, x='year', y='count', color='red')
plt.fill_between(visits_df['year'], visits_df['count'], color='red', alpha=0.3)

formatter = ticker.FuncFormatter(lambda x, pos: f"{int(x/1000)}K")
plt.gca().yaxis.set_major_formatter(formatter)

plt.ylabel('Donation Count')
plt.xlabel('Year')
plt.ylim(0)
plt.title("Trend of Donations in Malaysia")
plt.show()


# In[115]:


age_bins = ['19-30', '31-40', '41-50', '51-60', '61+']
age_bins.sort()  # Sort the age bins

plt.bar(visits_age_pivot_df.index, visits_age_pivot_df[age_bins[1]], label=f'{age_bins[1]}')
plt.bar(visits_age_pivot_df.index, visits_age_pivot_df[age_bins[2]], label=f'{age_bins[2]}') 
plt.bar(visits_age_pivot_df.index, visits_age_pivot_df[age_bins[3]], label=f'{age_bins[3]}')
plt.bar(visits_age_pivot_df.index, visits_age_pivot_df[age_bins[0]], label=f'{age_bins[0]}', color='r')
plt.bar(visits_age_pivot_df.index, visits_age_pivot_df[age_bins[4]], label=f'{age_bins[4]}', color='violet')
plt.bar(visits_age_pivot_df.index[:1], visits_age_pivot_df[age_bins[0]][:1], color='r')

# Order the legends
handles, labels = plt.gca().get_legend_handles_labels()
order = [age_bins.index(label) for label in labels]
plt.legend([handles[idx] for idx in order], [labels[idx] for idx in order], loc='upper left', bbox_to_anchor=(1.02, 1))



# In[116]:


returning_donors = copy_gran_df.groupby('donor_id').filter(lambda x: len(x) > 1)
returning_donors_count = returning_donors.groupby(returning_donors['visit_date'].dt.year)['donor_id'].nunique().reset_index()
returning_donors_count.columns = ['year', 'returning_donors_count']
visits_df = visits_df.merge(returning_donors_count, on='year', how='left').fillna(0)
visits_df


# ### General Retention Rate of Donors

# In[117]:


visits_df['retention_rate'] = round(visits_df['returning_donors_count'].div(visits_df['count']) * 100,1)
print(visits_df)


# In[118]:


plt.figure(figsize=(10,5))
sns.set(style="whitegrid")

sns.lineplot(data=visits_df, x='year', y='retention_rate', color='black')
sns.scatterplot(data=visits_df, x='year', y='retention_rate', color='red')

plt.ylabel('Retention Rate')
plt.xlabel('Year')
plt.ylim(0)
plt.title("Trend of Retention in Malaysia")
plt.show()


# ### More Detailed Retention Rate of Donors

# In[119]:


regular_donors = returning_donors[returning_donors['days_since_last_visit'] <= 720]
regular_donors_count = regular_donors.groupby(regular_donors['visit_date'].dt.year)['donor_id'].nunique().reset_index()
regular_donors_count.columns = ['year', 'regular_donors_count']

regular_donors_count


# In[120]:


lapsed_donors = returning_donors[returning_donors['days_since_last_visit'] > 720]
lapsed_donors_count = lapsed_donors.groupby(lapsed_donors['visit_date'].dt.year)['donor_id'].nunique().reset_index()
lapsed_donors_count.columns = ['year', 'lapsed_donor_count']

lapsed_donors_count


# In[121]:


new_donors_count = visits_df.copy()
new_donors_count['new_donors_count'] = new_donors_count['count'] - (returning_donors_count['returning_donors_count'])
new_donors_count = new_donors_count.fillna(0)
new_donors_count = new_donors_count.drop(['returning_donors_count','retention_rate'],axis=1)
new_donors_count


# In[122]:


new_visits_df = new_donors_count.merge(returning_donors_count, on='year', how='outer').merge(regular_donors_count, on='year', how='outer').merge(lapsed_donors_count, on='year', how='outer')
new_visits_df = new_visits_df.fillna(0)
new_visits_df['lapsed_donor_count'] = new_visits_df['lapsed_donor_count'].apply(lambda x:int(x))
new_visits_df


# In[123]:


new_visits_df.to_csv('new_visits_df.csv')


# In[124]:


plt.figure(figsize=(10,5))

plt.bar(new_visits_df['year'],new_visits_df['returning_donors_count'],
        width=1,color='b',label='Returning Donors')
plt.bar(new_visits_df['year'],new_visits_df['new_donors_count'],
        width=1,color='r',label='New Donors')
plt.bar(new_visits_df['year'],new_visits_df['regular_donors_count'],
        width=1,color='c',label='Regular Donors')
plt.bar(new_visits_df['year'][:-3],new_visits_df['new_donors_count'][:-3],
        width=1,color='r')
plt.bar(new_visits_df['year'],new_visits_df['lapsed_donor_count'],
        width=1,color='g',label='Lapsed Donors')

formatter = ticker.FuncFormatter(lambda x: f"{int(x/1000)}K")
plt.gca().yaxis.set_major_formatter(formatter)

plt.xlabel('Year')
plt.ylabel('Donors')
plt.title('Types of Donors in Malaysia per Year')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

# Percentage Maybe?
# for i, value in enumerate(new_visits_df['returning_donors_count'][2:-1]):
#     plt.text(new_visits_df['year'][i+2], value - 30000 , f"{int(value/new_visits_df['count'][i+2]*100)}%", ha='center', color='k')
# # for i, value in enumerate(new_visits_df['new_donors_count'][:-1]):
# #     plt.text(new_visits_df['year'][i], value/2 , f"{int(value/new_visits_df['count'][i]*100)}%", ha='center', color='white')
# # for i, value in enumerate(new_visits_df['regular_donors_count'][:-1]):
# #     plt.text(new_visits_df['year'][i], value + 100, f"{int(value/new_visits_df['count'][i]*100)}%", ha='center', color='white')
# for i, value in enumerate(new_visits_df['lapsed_donor_count'][2:-1]):
#     plt.text(new_visits_df['year'][i+2], value/4, f"{int(value/new_visits_df['count'][i+2]*100)}%", ha='center', color='white')

plt.show()


# In[125]:


new_retention_df = pd.DataFrame()
new_retention_df['year'] = new_visits_df['year'].copy()
new_retention_df['regular_donors_rtn'] = round(new_visits_df['regular_donors_count'].div(new_visits_df['count'])*100,2)
new_retention_df['lapsed_donors_rtn'] = round(new_visits_df['lapsed_donor_count'].div(new_visits_df['count'])*100,2)


# In[126]:


plt.figure(figsize=(10,5))
sns.set(style="whitegrid")

sns.lineplot(data=visits_df, 
             x='year', 
             y='retention_rate', 
             label='Returning Donors',
             color='r')

sns.lineplot(data=new_retention_df, 
             x='year', 
             y='regular_donors_rtn', 
             label='Regular Donors',
             color = 'slateblue')

sns.lineplot(data=new_retention_df, 
             x='year', 
             y='lapsed_donors_rtn', 
             label='Lapsed Donors',
             color='darkseagreen')

# plt.fill_between(visits_df['year'], visits_df['retention_rate'], color='pink')
# plt.fill_between(new_retention_df['year'], new_retention_df['regular_donors_rtn'], color='c')
# plt.fill_between(new_retention_df['year'], new_retention_df['lapsed_donors_rtn'], color='palegreen')

plt.ylabel('Retention Rate')
plt.xlabel('Year')
plt.ylim(0)
plt.title("Trend of Retention in Malaysia")
plt.show()


# ## Aggregate Data
# 

# ## Import
# 

# In[140]:


import os
os.chdir('..')

from github import Github
import main_utils.vars as vars
import typing 


token = vars.GITHUB_KEY
g = Github(token)
repo = g.get_repo("MoH-Malaysia/data-darah-public")
contents = repo.get_contents('./')
content_links = [c.download_url for c in contents]


if not os.path.exists('data'):
    os.makedirs('data')

df_dict = {}
for link in content_links:
    filename = link.split('/')[-1]
    df_name = filename.split(".csv")[0]+"_df"
    
    df_dict[df_name] = pd.read_csv(link)
    # df_dict[df_name].to_csv(f'./data/{filename}', index=False)


# In[141]:


df_dict.keys()


# In[142]:


df_dict['donations_facility_df']


# In[143]:


df_dict['donations_state_df'].keys()


# In[144]:


donations_state_df = df_dict['donations_state_df'][['date', 
                                                    'state', 
                                                    'daily',
                                                    'location_centre',
                                                    'location_mobile',
                                                    'donations_new',
                                                    'donations_regular',
                                                    'donations_irregular',
                                                    ]].copy()
donations_state_df


# In[168]:


malaysia_donations_df = donations_state_df.loc[donations_state_df['state'] == 'Malaysia']
malaysia_donations_df


# In[154]:


malaysia_donations_df['date'] = pd.to_datetime(malaysia_donations_df['date'])
malaysia_visits_df = malaysia_donations_df.groupby(malaysia_donations_df['date'].dt.year)['daily'].sum().reset_index()
malaysia_visits_df.columns = ['year', 'count']
print(malaysia_visits_df)


# In[147]:


import numpy as np
import matplotlib.ticker as ticker

plt.figure(figsize=(10,5))
sns.set(style="whitegrid")

sns.lineplot(data=malaysia_visits_df, x='year', y='count', color='red')
plt.fill_between(malaysia_visits_df['year'], malaysia_visits_df['count'], color='red', alpha=0.3)

formatter = ticker.FuncFormatter(lambda x: f"{int(x/1000)}K")
plt.gca().yaxis.set_major_formatter(formatter)
plt.gca().xaxis.set_major_locator(ticker.MaxNLocator(integer=True))

plt.ylabel('Donation Count')
plt.xlabel('Year')
plt.title("Trend of Donations in Malaysia")
plt.show()


# In[204]:


average_7_df = malaysia_donations_df.drop(['location_mobile',
                                            'location_centre'],axis=1).copy()
average_7_df['7_days_avg'] = np.int32(average_7_df['daily'].rolling(window=7).mean().fillna(0))
average_7_df['7_days_avg_regular'] = np.int32(average_7_df['donations_regular'].rolling(window=7).mean().fillna(0))
average_7_df


# In[235]:


plt.figure(figsize=(15,6))
filtered_df = average_7_df[(pd.to_datetime(average_7_df['date']).dt.year >=  datetime.now().year - 1) & (pd.to_datetime(average_7_df['date']).dt.year <= datetime.now().year)]
plt.plot(pd.to_datetime(filtered_df['date']), filtered_df['7_days_avg'],color = 'red')
plt.fill_between(pd.to_datetime(filtered_df['date']), filtered_df['7_days_avg'],color = 'red',alpha =0.3,label = 'Total Donors')
plt.fill_between(pd.to_datetime(filtered_df['date']), filtered_df['7_days_avg_regular'],color = 'red',alpha =0.5,label = 'Regular Donors')

formatter = ticker.FuncFormatter(lambda x: f"{float(x/1000)}K")
plt.gca().yaxis.set_major_formatter(formatter)
plt.gca().xaxis.set_major_locator(ticker.MaxNLocator(integer=True))

plt.xlabel('Date')
plt.ylabel('Donors')
plt.title(f'7-day Average of Daily Donations from {datetime.now().year - 1} - {datetime.now().year}')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.show()


# ## New Donors Trend

# In[236]:


df_dict['newdonors_state_df'].keys()


# In[260]:


new_donors_df = df_dict['newdonors_state_df'].copy()
malaysia_new_donors_df = new_donors_df.loc[new_donors_df['state'] == 'Malaysia']
malaysia_new_donors_df


# In[238]:


malaysia_new_donors_df['date'] = pd.to_datetime(malaysia_new_donors_df['date'])
malaysia_new_donors_count= malaysia_new_donors_df.groupby(malaysia_new_donors_df['date'].dt.year)['total'].sum().reset_index()
malaysia_new_donors_count.columns = ['year', 'count']
print(malaysia_new_donors_count)


# In[259]:


plt.figure(figsize=(10,5))
sns.set(style="whitegrid")

sns.barplot(data=malaysia_new_donors_count, x='year', y='count', color='salmon')

formatter = ticker.FuncFormatter(lambda x:f"{int(x/1000)}K")
plt.gca().yaxis.set_major_formatter(formatter)
plt.gca().xaxis.set_major_locator(ticker.MaxNLocator(integer=True))

plt.ylabel('Donation Count')
plt.xlabel('Year')
plt.title("Trend of New Donors in Malaysia")
plt.show()


# In[294]:


malaysia_new_donors_df['date'] = pd.to_datetime(malaysia_new_donors_df['date'])
malaysia_new_donors_age_count = malaysia_new_donors_df.groupby(malaysia_new_donors_df['date'])[['17-24','25-29','30-34','35-39','40-44','45-49','50-54','55-59','60-64']].sum().reset_index()
malaysia_new_donors_age_count.columns = ['date', '17-24','25-29','30-34','35-39','40-44','45-49','50-54','55-59','60-64']
malaysia_new_donors_age_count


# In[310]:


filtered_df = malaysia_new_donors_age_count[(pd.to_datetime(malaysia_new_donors_age_count['date']).dt.year >=  datetime.now().year - 1) & (pd.to_datetime(malaysia_new_donors_age_count['date']).dt.year <= datetime.now().year)]
filtered_df = filtered_df.drop('date',axis=1)
filtered_df = filtered_df.sum()


plt.figure(figsize=(15,8))
plt.bar(filtered_df.index[:-1],filtered_df.values[:-1],color='salmon')

formatter = ticker.FuncFormatter(lambda x, pos: f"{int(x/1000)}K")
plt.gca().yaxis.set_major_formatter(formatter)

plt.xlabel('Age Groups')
plt.ylabel('Donors')
plt.title(f'New Donors By Age Group From {datetime.now().year - 1} - {datetime.now().year}')






