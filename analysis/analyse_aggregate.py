import os
import sys

script_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(script_dir)
sys.path.insert(0, parent_dir)

import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

from utils.data_loader import *
from utils.save_fig import save_fig
from datetime import datetime

sns.set(style="whitegrid")
plt.figure(figsize=(15,6))
plt.tight_layout()
formatter = ticker.FuncFormatter(lambda x,pos: f"{float(x/1000)}K")

if not os.path.exists("./images/"):
    os.makedirs("./images/")

#Read Data
print('Acquiring Data...')
AGGREGATE_DATA_REPO= "MoH-Malaysia/data-darah-public"
aggregate_data_dict = get_data_from_repo(AGGREGATE_DATA_REPO)

donations_state_df = aggregate_data_dict['donations_state_df'][['date', 
                                                    'state', 
                                                    'daily',
                                                    'location_centre',
                                                    'location_mobile',
                                                    'donations_new',
                                                    'donations_regular',
                                                    'donations_irregular',
                                                    ]].copy()

print("Finding Trends in Malaysia ...")
# Get Trends in Malaysia
malaysia_donations_df = donations_state_df.loc[donations_state_df['state'] == 'Malaysia']
malaysia_donations_df['date'] = pd.to_datetime(malaysia_donations_df['date'])
malaysia_visits_df = malaysia_donations_df.groupby(malaysia_donations_df['date'].dt.year)['daily'].sum().reset_index()
malaysia_visits_df.columns = ['year', 'count']

## Plot Malaysia Trend
sns.lineplot(data=malaysia_visits_df, x='year', y='count', color='red')
plt.fill_between(malaysia_visits_df['year'], malaysia_visits_df['count'], color='red', alpha=0.3)

plt.gca().yaxis.set_major_formatter(formatter)
plt.gca().xaxis.set_major_locator(ticker.MaxNLocator(integer=True))

plt.ylabel('Donation Count')
plt.xlabel('Year')
plt.title("Trend of Donations in Malaysia")
save_fig("./images/trend_donations_malaysia.jpg")

# Get 7 Day Average Trend
print("Looking for a 7 Day Average ...")
average_7_df = malaysia_donations_df.drop(['location_mobile',
                                            'location_centre'],axis=1).copy()
average_7_df['7_days_avg'] = np.int32(average_7_df['daily'].rolling(window=7).mean().fillna(0))
average_7_df['7_days_avg_regular'] = np.int32(average_7_df['donations_regular'].rolling(window=7).mean().fillna(0))
average_7_df

## Plot Figure
filtered_df = average_7_df[(pd.to_datetime(average_7_df['date']).dt.year >=  datetime.now().year - 1) & (pd.to_datetime(average_7_df['date']).dt.year <= datetime.now().year)]
plt.figure(figsize=(15,6))
plt.plot(pd.to_datetime(filtered_df['date']), filtered_df['7_days_avg'],color = 'red')
plt.fill_between(pd.to_datetime(filtered_df['date']), filtered_df['7_days_avg'],color = 'red',alpha =0.3,label = 'Total Donors')
plt.fill_between(pd.to_datetime(filtered_df['date']), filtered_df['7_days_avg_regular'],color = 'red',alpha =0.5,label = 'Regular Donors')

plt.gca().yaxis.set_major_formatter(formatter)
plt.gca().xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
plt.xlabel('Date')
plt.ylabel('Donors')
plt.title(f'7-day Average of Daily Donations from {datetime.now().year - 1} - {datetime.now().year}')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
save_fig("./images/trend_7_day_avg_malaysia.jpg")

# New Donors
print("Looking For New Donors ...")
new_donors_df = aggregate_data_dict['newdonors_state_df'].copy()
malaysia_new_donors_df = new_donors_df.loc[new_donors_df['state'] == 'Malaysia']
malaysia_new_donors_df['date'] = pd.to_datetime(malaysia_new_donors_df['date'])
malaysia_new_donors_count= malaysia_new_donors_df.groupby(malaysia_new_donors_df['date'].dt.year)['total'].sum().reset_index()
malaysia_new_donors_count.columns = ['year', 'count']

## Plot
sns.barplot(data=malaysia_new_donors_count, x='year', y='count', color='salmon')

plt.gca().yaxis.set_major_formatter(formatter)
plt.gca().xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
plt.ylabel('Donation Count')
plt.xlabel('Year')
plt.title("Trend of New Donors in Malaysia")
save_fig("./images/trend_new_donors_malaysia.jpg")

#Get New Donors By Age
malaysia_new_donors_age_count = malaysia_new_donors_df.groupby(malaysia_new_donors_df['date'])[['17-24','25-29','30-34','35-39','40-44','45-49','50-54','55-59','60-64']].sum().reset_index()
malaysia_new_donors_age_count.columns = ['date', '17-24','25-29','30-34','35-39','40-44','45-49','50-54','55-59','60-64']
malaysia_new_donors_age_count

filtered_df = malaysia_new_donors_age_count[(pd.to_datetime(malaysia_new_donors_age_count['date']).dt.year >=  datetime.now().year - 1) & (pd.to_datetime(malaysia_new_donors_age_count['date']).dt.year <= datetime.now().year)]
filtered_df = filtered_df.drop('date',axis=1)
filtered_df = filtered_df.sum()

# Plot Figure
plt.bar(filtered_df.index[:-1],filtered_df.values[:-1],color='salmon')

plt.gca().yaxis.set_major_formatter(formatter)
plt.xlabel('Age Groups')
plt.ylabel('Donors')
plt.title(f'New Donors By Age Group From {datetime.now().year - 1} - {datetime.now().year}')
save_fig("./images/trend_new_donors_age_group.jpg")

print("Finished")







