import os
import sys

script_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(script_dir)
sys.path.insert(0, parent_dir)

from main_utils.data_loader import *
from main_utils.save_fig import save_fig
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

if not os.path.exists("./images/"):
    os.makedirs("./images/")

sns.set(style="whitegrid")

#Read Data
GRANULAR_DATA_LINK ="https://dub.sh/ds-data-granular"
gran_data_df = read_parquet(GRANULAR_DATA_LINK)

#Change gran data columsn
print('Transforming Data...')
gran_data_df['visit_date'] = pd.to_datetime(gran_data_df['visit_date'])
gran_data_df['days_since_last_visit'] = gran_data_df.groupby('donor_id')['visit_date'].diff().dt.days
gran_data_df['months_since_last_visit'] = gran_data_df['days_since_last_visit'] // 30
gran_data_df['years_since_last_vist'] = gran_data_df['months_since_last_visit'] // 12
gran_data_df = gran_data_df.fillna(0)

# Get visits Df
visits_df = gran_data_df.groupby(gran_data_df['visit_date'].dt.year)['donor_id'].count().reset_index()
visits_df.columns = ['year', 'count']

#Get Returning Donors
print('Looking for Returning Donors...')
returning_donors = gran_data_df.groupby('donor_id').filter(lambda x: len(x) > 1)
returning_donors_count = returning_donors.groupby(returning_donors['visit_date'].dt.year)['donor_id'].nunique().reset_index()
returning_donors_count.columns = ['year', 'returning_donors_count']

#Make Retention Rate Count
visits_df = visits_df.merge(returning_donors_count, on='year', how='left').fillna(0)
visits_df['retention_rate'] = round(visits_df['returning_donors_count'].div(visits_df['count']) * 100,1)

""" 
See Retention of All Donor Types in Malaysia 
"""
print('Getting Retentions...')
#Regular Donors 
regular_donors = returning_donors[returning_donors['days_since_last_visit'] <= 720]
regular_donors_count = regular_donors.groupby(regular_donors['visit_date'].dt.year)['donor_id'].nunique().reset_index()
regular_donors_count.columns = ['year', 'regular_donors_count']

# Lapsed Donors
lapsed_donors = returning_donors[returning_donors['days_since_last_visit'] > 720]
lapsed_donors_count = lapsed_donors.groupby(lapsed_donors['visit_date'].dt.year)['donor_id'].nunique().reset_index()
lapsed_donors_count.columns = ['year', 'lapsed_donor_count']

#New Donors
new_donors_count = visits_df.copy()
new_donors_count['new_donors_count'] = new_donors_count['count'] - (returning_donors_count['returning_donors_count'])
new_donors_count = new_donors_count.fillna(0)
new_donors_count = new_donors_count.drop(['returning_donors_count','retention_rate'],axis=1)

#Create New Visits DF
new_visits_df = new_donors_count.merge(returning_donors_count, on='year', how='outer').merge(regular_donors_count, on='year', how='outer').merge(lapsed_donors_count, on='year', how='outer')
new_visits_df = new_visits_df.fillna(0)
new_visits_df['lapsed_donor_count'] = new_visits_df['lapsed_donor_count'].apply(lambda x:int(x))


# Plot Type of Donors Figure
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

formatter = ticker.FuncFormatter(lambda x,pos: f"{int(x/1000)}K")
plt.gca().yaxis.set_major_formatter(formatter)
plt.xlabel('Year')
plt.ylabel('Donors')
plt.title('Types of Donors in Malaysia per Year')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
save_fig("./images/trend_donor_type_malaysia.jpg")

## Plot Retention Rates
new_retention_df = pd.DataFrame()
new_retention_df['year'] = new_visits_df['year'].copy()
new_retention_df['regular_donors_rtn'] = round(new_visits_df['regular_donors_count'].div(new_visits_df['count'])*100,2)
new_retention_df['lapsed_donors_rtn'] = round(new_visits_df['lapsed_donor_count'].div(new_visits_df['count'])*100,2)

plt.figure(figsize=(10,5))

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

plt.ylabel('Retention Rate (%)')
plt.xlabel('Year')
plt.ylim(0)
plt.title("Trend of Retention in Malaysia")
save_fig("./images/trend_retention_malaysia.jpg")

print('Finished ...')