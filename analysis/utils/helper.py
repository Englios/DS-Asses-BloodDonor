import pandas as pd
from datetime import timedelta

def parse_comparison(latest, previous):
    delta = int((latest - previous) / latest * 100)
    if delta > 0:
        return f"{chr(0x1F53A)} {abs(delta)}% "  # Up arrow
    else:
        return f"{chr(0x1F53B)} {abs(delta)}%"  # Down arrow

def get_daily_msg(df:pd.DataFrame,state:str) -> None:
    """
    Generate a daily message based on the given DataFrame and state.

    Parameters:
    - df (pd.DataFrame): The DataFrame containing the data.
    - state (str): The Malaysian State for which the daily message is generated.

    Returns:
    - None

    This function calculates various statistics from the DataFrame for the given state and generates a daily message
    with the statistics. The message is then written to a file named 'daily_message.txt' in the './daily_texts/' directory.
    The message includes information about the total donors, new donors, regular donors, others donors, and blood type statistics.
    The message also includes a comparison with the previous 3 day's statistics.
    """
    
    #Get Daily Message
    state_up = state.upper()
    df['date'] = pd.to_datetime(df['date'])
    latest_date = df['date'].max()
    start_date = latest_date - timedelta(days=2)
    daily_df = df.loc[(df['date'] >= start_date) & (df['date'] <= latest_date)].reset_index(drop=True)
    my_filter_latest = (daily_df['date'] == latest_date) & (daily_df['state'] == state_up)
    my_filter_previous = (daily_df['date'] == start_date) & (daily_df['state'] == state_up)
    
    def locate_columns(filter,column:str):
        return int(daily_df.loc[filter, column].values[0])

    latest_donors = int(daily_df.loc[my_filter_latest, 'daily'].values[0])
    previous_donors = int(daily_df.loc[my_filter_previous, 'daily'].values[0])

    new_latest_donors = int(daily_df.loc[my_filter_latest & (daily_df['state'] == state), 'donations_new'].values[0])
    new_previous_donors = int(daily_df.loc[my_filter_previous, 'donations_new'].values[0])

    regular_latest_donors = int(daily_df.loc[my_filter_latest, 'donations_regular'].values[0])
    regular_previous_donors = int(daily_df.loc[my_filter_previous, 'donations_regular'].values[0])

    others_latest_donors = int(daily_df.loc[my_filter_latest, 'donations_irregular'].values[0])
    others_previous_donors = int(daily_df.loc[my_filter_previous, 'donations_irregular'].values[0])

    latest_blood_a = int(daily_df.loc[my_filter_latest, 'blood_a'].values[0])
    previous_blood_a = int(daily_df.loc[my_filter_previous, 'blood_a'].values[0])

    latest_blood_b = int(daily_df.loc[my_filter_latest & (daily_df['state'] == state), 'blood_b'].values[0])
    previous_blood_b = int(daily_df.loc[my_filter_previous, 'blood_b'].values[0])

    latest_blood_ab = int(daily_df.loc[my_filter_latest, 'blood_ab'].values[0])
    previous_blood_ab = int(daily_df.loc[my_filter_previous, 'blood_ab'].values[0])

    latest_blood_o = int(daily_df.loc[my_filter_latest, 'blood_o'].values[0])
    previous_blood_o = int(daily_df.loc[my_filter_previous, 'blood_o'].values[0])
    
    with open(f'./daily_texts/daily_message_{state}.txt','w',encoding='utf-8') as f:
        f.write(f'''\n= Latest Update as of {daily_df['date'].loc[daily_df['date'] == latest_date].drop_duplicates().values[0].astype('datetime64[D]')} for {state_up} =\n\nDonor Statistics\n\t- Total Donors   : {latest_donors} ({parse_comparison(latest_donors,previous_donors)})\n\t- New Donors     : {new_latest_donors} ({parse_comparison(new_latest_donors,new_previous_donors)})\n\t- Regular Donors : {regular_latest_donors} ({parse_comparison(regular_latest_donors,regular_previous_donors)})\n\t- Others Donors  : {others_latest_donors} ({parse_comparison(others_latest_donors,others_previous_donors)})\n\nBlood Types Statistics\n\t- Type A  : {latest_blood_a} ({parse_comparison(latest_blood_a,previous_blood_a)})\n\t- Type B  : {latest_blood_b} ({parse_comparison(latest_blood_b,previous_blood_b)})\n\t- Type AB : {latest_blood_ab} ({parse_comparison(latest_blood_ab,previous_blood_ab)})\n\t- Type O  : {latest_blood_o} ({parse_comparison(latest_blood_o,previous_blood_o)})\n\nData is acquired from KKM daily at 0900 hrs and at 2200 hrs\nA comparison of 3 days can be seen by the side
                ''')
    