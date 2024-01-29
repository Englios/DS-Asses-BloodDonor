import os
import sys

script_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(script_dir)
sys.path.insert(0, parent_dir)

import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

from main_utils.data_loader import *
from main_utils.save_fig import save_fig
from utils.helper import parse_comparison
from datetime import datetime,timedelta

sns.set(style="whitegrid")
plt.figure(figsize=(15,6))
plt.tight_layout()
formatter = ticker.FuncFormatter(lambda x,pos: f"{float(x/1000)}K")

if not os.path.exists("./images/"):
    os.makedirs("./images/")
    
if not os.path.exists("./daily_texts/"):    
    os.makedirs('./daily_texts/')
    
#Read Data
print(f"Today's Date @ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print('Acquiring Data...')
AGGREGATE_DATA_REPO= "MoH-Malaysia/data-darah-public"
aggregate_data_dict = get_data_from_repo(AGGREGATE_DATA_REPO)
# Section 1: Aggregate Data
donations_state_df = aggregate_data_dict['donations_state_df'][['date', 
                                                    'state', 
                                                    'daily',
                                                    'blood_a',
                                                    'blood_b',
                                                    'blood_o',
                                                    'blood_ab',
                                                    'location_centre',
                                                    'location_mobile',
                                                    'donations_new',
                                                    'donations_regular',
                                                    'donations_irregular',
                                                    ]].copy()
donations_state_df['date'] = pd.to_datetime(donations_state_df['date'])

print("Finding Trends in Malaysia ...")
# Get Trends in Malaysia
malaysia_donations_df = donations_state_df.loc[donations_state_df['state'] == 'Malaysia']
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
plt.tight_layout()
save_fig("trend_donations_malaysia.jpg")

# Get 7 Day Average Trend
print("Looking for a 7 Day Average ...")
average_7_df = malaysia_donations_df.drop(['location_mobile',
                                            'location_centre'],axis=1).copy()
average_7_df['7_days_avg'] = np.int32(average_7_df['daily'].rolling(window=7).mean().fillna(0))
average_7_df['7_days_avg_regular'] = np.int32(average_7_df['donations_regular'].rolling(window=7).mean().fillna(0))
average_7_df

## Plot Figure
#2024
start_yr = (average_7_df['date'].dt.year >=  datetime.now().year - 1)
end_yr = (average_7_df['date'].dt.year <= datetime.now().year )
filtered_df = average_7_df[(start_yr) & (end_yr)]

plt.figure(figsize=(15,6))
plt.plot(filtered_df['date'], filtered_df['7_days_avg'],color = 'red')
plt.fill_between(filtered_df['date'], filtered_df['7_days_avg'],color = 'red',alpha =0.3,label = 'Total Donors')
plt.fill_between(filtered_df['date'], filtered_df['7_days_avg_regular'],color = 'red',alpha =0.5,label = 'Regular Donors')

plt.gca().yaxis.set_major_formatter(formatter)
plt.gca().xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
plt.xlabel('Date')
plt.ylabel('Donors')
plt.title(f'7-day Average of Daily Donations from {datetime.now().year - 1} - {datetime.now().year}')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
save_fig("trend_7_day_avg_malaysia_2023.jpg")

#2021
start_yr = (average_7_df['date'].dt.year >=  datetime.now().year - 3)
end_yr = (average_7_df['date'].dt.year <= datetime.now().year - 3)
filtered_df = average_7_df[(start_yr) & (end_yr)]

plt.figure(figsize=(15,6))
plt.plot(filtered_df['date'], filtered_df['7_days_avg'],color = 'red')
plt.fill_between(filtered_df['date'], filtered_df['7_days_avg'],color = 'red',alpha =0.3,label = 'Total Donors')
plt.fill_between(filtered_df['date'], filtered_df['7_days_avg_regular'],color = 'red',alpha =0.5,label = 'Regular Donors')

plt.gca().yaxis.set_major_formatter(formatter)
plt.gca().xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
plt.xlabel('Date')
plt.ylabel('Donors')
plt.title(f'7-day Average of Daily Donations from {datetime.now().year - 3} - {datetime.now().year -2}')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
save_fig("trend_7_day_avg_malaysia_2021.jpg")


#Get By State
state_donations_df = donations_state_df.loc[(donations_state_df['state'] != 'Malaysia')]
state_visits_df = state_donations_df.pivot_table(index=state_donations_df['date'].dt.year, columns='state', values='daily', aggfunc='sum').reset_index()
state_visits_df.columns = ['year'] + state_visits_df.columns[1:].tolist()

# Sum the donation counts for all years
state_visits_sum_all_years = state_visits_df.iloc[:, 1:].sum()
plt.figure(figsize=(10,8))
clrs = sns.color_palette('husl', n_colors=len(state_visits_df.columns))
plt.pie(state_visits_sum_all_years, labels=state_visits_sum_all_years.index, autopct='%1.1f%%',colors=clrs)
plt.title(f"Donation Count in Each State - All Years \n Total Donors : {round(state_visits_sum_all_years.sum()/1000,2)}K")
plt.tight_layout()
save_fig("percentage_donations_state_all_years.jpg")

#Finer Bar Chart
# Filter the dataframe for the year 2024
state_visits_df_2024 = state_visits_df[state_visits_df['year'] == 2024].iloc[:, 1:].sum()

sorted_states = state_visits_df_2024.sort_values(ascending=True).index
#Plot
plt.figure(figsize=(10, 5))
colors = plt.cm.get_cmap('OrRd',len(state_visits_df.columns))
plt.barh(sorted_states, state_visits_df_2024[sorted_states], color=colors(np.arange(len(state_visits_df_2024))))
plt.title(f"Donation Count in Each State - 2024 \n Total Donors : {round(state_visits_df_2024.sum()/1000,2)}K")

plt.gca().xaxis.set_major_formatter(formatter)
plt.xlabel('Donation Count')
plt.ylabel('State')
plt.tight_layout()
save_fig('donation_count_state_2024.jpg')

# Filter the dataframe for the year 2022
state_visits_df_2022 = state_visits_df[state_visits_df['year'] == 2022].iloc[:, 1:].sum()
sorted_states = state_visits_df_2022.sort_values(ascending=True).index
#Plot
plt.figure(figsize=(10, 5))
colors = plt.cm.get_cmap('OrRd',len(state_visits_df))
plt.barh(sorted_states, state_visits_df_2022[sorted_states], color=colors(np.arange(len(state_visits_df_2022))))
plt.title(f"Donation Count in Each State - 2022 \n Total Donors : {round(state_visits_df_2022.sum()/1000,2)}K")

plt.gca().xaxis.set_major_formatter(formatter)
plt.xlabel('Donation Count')
plt.ylabel('State')
plt.tight_layout()
save_fig('donation_count_state_2022.jpg')

#Trend Plot of states without WP KL
no_wp_state_donations_df = donations_state_df.loc[(donations_state_df['state'] != 'Malaysia') & (donations_state_df['state'] != 'W.P. Kuala Lumpur')]
state_visits_df = no_wp_state_donations_df.pivot_table(index=no_wp_state_donations_df['date'].dt.year, columns='state', values='daily', aggfunc='sum').reset_index()
state_visits_df.columns = ['year'] + state_visits_df.columns[1:].tolist()

#Plot
clrs = sns.color_palette('husl', n_colors=len(state_visits_df.columns))
state_visits_df.plot(x='year',kind='line',figsize=(10,5),color=clrs)

plt.gca().yaxis.set_major_formatter(formatter)
plt.gca().xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
plt.xlabel('Year')
plt.ylabel('Donation Count')
plt.title('Donation Count in Each State Over the Years')
plt.legend(bbox_to_anchor=(1.05, 1))
plt.tight_layout()
save_fig('donation_trend_all_years.jpg')

# New Donors
print("Looking For New Donors ...")
new_donors_df = aggregate_data_dict['newdonors_state_df'].copy()
malaysia_new_donors_df = new_donors_df.loc[new_donors_df['state'] == 'Malaysia']
malaysia_new_donors_count= malaysia_new_donors_df.groupby(pd.to_datetime(malaysia_new_donors_df['date']).dt.year)['total'].sum().reset_index()
malaysia_new_donors_count.columns = ['year', 'count']

## Plot
sns.barplot(data=malaysia_new_donors_count, x='year', y='count', color='salmon')

plt.gca().yaxis.set_major_formatter(formatter)
plt.gca().xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
plt.ylabel('Donation Count')
plt.xlabel('Year')
plt.title("Trend of New Donors in Malaysia")
plt.tight_layout()
save_fig("trend_new_donors_malaysia.jpg")

#Get New Donors By Age
malaysia_new_donors_age_count = malaysia_new_donors_df.groupby(malaysia_new_donors_df['date'])[['17-24','25-29','30-34','35-39','40-44','45-49','50-54','55-59','60-64']].sum().reset_index()
malaysia_new_donors_age_count.columns = ['date', '17-24','25-29','30-34','35-39','40-44','45-49','50-54','55-59','60-64']

filtered_df = malaysia_new_donors_age_count[(pd.to_datetime(malaysia_new_donors_age_count['date']).dt.year >=  datetime.now().year - 1) & (pd.to_datetime(malaysia_new_donors_age_count['date']).dt.year <= datetime.now().year)]
filtered_df = filtered_df.drop('date',axis=1)
filtered_df = filtered_df.sum()

# Plot Figure
plt.bar(filtered_df.index[:-1],filtered_df.values[:-1],color='salmon')

plt.gca().yaxis.set_major_formatter(formatter)
plt.xlabel('Age Groups')
plt.ylabel('Donors')
plt.title(f'New Donors By Age Group From {datetime.now().year - 1} - {datetime.now().year}')
plt.tight_layout()
save_fig(f"trend_new_donors_age_group_{datetime.now().year - 1}_{datetime.now().year}.jpg")

# New Donors Trend by Year
malaysia_new_donors_df['date'] = pd.to_datetime(malaysia_new_donors_df['date']).dt.year
malaysia_new_donors_df = malaysia_new_donors_df.groupby('date')[['17-24','25-29','30-34','35-39','40-44','45-49','50-54','55-59','60-64']].sum().reset_index()
malaysia_new_donors_df.columns = ['year','17-24','25-29','30-34','35-39','40-44','45-49','50-54','55-59','60-64']
malaysia_new_donors_df.plot(x='year',kind='line',figsize=(10,5))

plt.gca().yaxis.set_major_formatter(formatter)
plt.gca().xaxis.set_major_locator(ticker.MaxNLocator())
plt.xlabel('Years')
plt.ylabel('Donors')
plt.title(f'Trend of New Donors')
plt.legend(bbox_to_anchor=(1.05,1),loc='upper left')
plt.tight_layout()
save_fig("trend_new_donors_age_group_years.jpg")

#Get Daily Message
latest_date = donations_state_df['date'].max()
start_date = latest_date - timedelta(days=2)
daily_df = donations_state_df.loc[(donations_state_df['date'] >= start_date) & (donations_state_df['date'] <= latest_date)].reset_index(drop=True)
my_filter_latest = (daily_df['date'] == latest_date) & (daily_df['state'] == 'Malaysia')
my_filter_previous = (daily_df['date'] == start_date) & (daily_df['state'] == 'Malaysia')


latest_donors = int(daily_df.loc[my_filter_latest & (daily_df['state'] == 'Malaysia'), 'daily'].values[0])
previous_donors = int(daily_df.loc[my_filter_previous & (daily_df['state'] == 'Malaysia'), 'daily'].values[0])

new_latest_donors = int(daily_df.loc[my_filter_latest & (daily_df['state'] == 'Malaysia'), 'donations_new'].values[0])
new_previous_donors = int(daily_df.loc[my_filter_previous & (daily_df['state'] == 'Malaysia'), 'donations_new'].values[0])

regular_latest_donors = int(daily_df.loc[my_filter_latest & (daily_df['state'] == 'Malaysia'), 'donations_regular'].values[0])
regular_previous_donors = int(daily_df.loc[my_filter_previous & (daily_df['state'] == 'Malaysia'), 'donations_regular'].values[0])

others_latest_donors = int(daily_df.loc[my_filter_latest & (daily_df['state'] == 'Malaysia'), 'donations_irregular'].values[0])
others_previous_donors = int(daily_df.loc[my_filter_previous & (daily_df['state'] == 'Malaysia'), 'donations_irregular'].values[0])

latest_blood_a = int(daily_df.loc[my_filter_latest & (daily_df['state'] == 'Malaysia'), 'blood_a'].values[0])
previous_blood_a = int(daily_df.loc[my_filter_previous & (daily_df['state'] == 'Malaysia'), 'blood_a'].values[0])

latest_blood_b = int(daily_df.loc[my_filter_latest & (daily_df['state'] == 'Malaysia'), 'blood_b'].values[0])
previous_blood_b = int(daily_df.loc[my_filter_previous & (daily_df['state'] == 'Malaysia'), 'blood_b'].values[0])

latest_blood_ab = int(daily_df.loc[my_filter_latest & (daily_df['state'] == 'Malaysia'), 'blood_ab'].values[0])
previous_blood_ab = int(daily_df.loc[my_filter_previous & (daily_df['state'] == 'Malaysia'), 'blood_ab'].values[0])

latest_blood_o = int(daily_df.loc[my_filter_latest & (daily_df['state'] == 'Malaysia'), 'blood_o'].values[0])
previous_blood_o = int(daily_df.loc[my_filter_previous & (daily_df['state'] == 'Malaysia'), 'blood_o'].values[0])


with open('./daily_texts/daily_message.txt','w',encoding='utf-8') as f:
    f.write(f'''\n= Latest Update as of {daily_df['date'].loc[daily_df['date'] == latest_date].drop_duplicates().values[0].astype('datetime64[D]')} =\n\nDonor Statistics\n\t- Total Donors   : {latest_donors} ({parse_comparison(latest_donors,previous_donors)})\n\t- New Donors     : {new_latest_donors} ({parse_comparison(new_latest_donors,new_previous_donors)})\n\t- Regular Donors : {regular_latest_donors} ({parse_comparison(regular_latest_donors,regular_previous_donors)})\n\t- Others Donors  : {others_latest_donors} ({parse_comparison(others_latest_donors,others_previous_donors)})\n\nBlood Types Statistics\n\t- Type A  : {latest_blood_a} ({parse_comparison(latest_blood_a,previous_blood_a)})\n\t- Type B  : {latest_blood_b} ({parse_comparison(latest_blood_b,previous_blood_b)})\n\t- Type AB : {latest_blood_ab} ({parse_comparison(latest_blood_ab,previous_blood_ab)})\n\t- Type O  : {latest_blood_o} ({parse_comparison(latest_blood_o,previous_blood_o)})\n\nData is acquired from KKM daily at 0900 hrs and at 2200 hrs\nA comparison of 3 days can be seen by the side
            ''')
print(f"Finished @ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")







