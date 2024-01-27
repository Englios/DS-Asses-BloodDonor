from telegram import Update
from telegram.ext import ContextTypes
from main_utils.vars import BOT_USERNAME

## Show Commands  
async def show_malaysia_command(update:Update,context:ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id

    #Show Trend
    await context.bot.send_photo(chat_id=chat_id,
                                 photo=open('./images/trend_donations_malaysia.jpg', 'rb'),
                                 caption = f'As we can see,Malaysia is on the rise with Blood Donations,which means more and more people are donating blood.\nThe data for 2024 is still in collection,but it will most likely rise from previous years')
    #Show 7 Day Avg
    await context.bot.send_photo(chat_id=chat_id,
                                 photo=open('./images/trend_7_day_avg_malaysia_2023.jpg', 'rb'),
                                 caption = f'By Taking a closer look over 2023 - 2024.\nIt can be seen that our daily Blood Donations are stable,with daily an average daily donation count.\nThe valley formed around 2023-4 to 2023-5 is most likely due to fasting month,where less blood donations are peformed by the Muslim population.')
    
    await context.bot.send_photo(chat_id=chat_id,
                                photo=open('./images/trend_7_day_avg_malaysia_2021.jpg', 'rb'),
                                caption = f'This is further reinforced by looking at the data from 2021 - 2022,where a valley is formed early in 2021-5,which for that year,Ramadhan falls on May.')
    

async def show_states_command(update:Update,context:ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    
    await context.bot.send_message(chat_id=chat_id,text='Here are the trends in Malaysian States.')
    
    await context.bot.send_photo(chat_id=chat_id,
                                 photo=open('./images/percentage_donations_state_all_years.jpg', 'rb'),
                                 caption = f'As in the figure we see that W.P Kuala Lumpur having the most donors,but this does not incdicate that most donors are living in KL.\nKKM has mobile donation centers which goes around Selangor and W.P Putrajaya,the donations towards these mobile donation spots are counted under W.P Kuala Lumpur ')
    
    await context.bot.send_photo(chat_id=chat_id,
                                 photo=open('./images/donation_count_state_2024.jpg', 'rb'),
                                 caption = f'Looking at the count by each state for the year 2024,we see that W.P is the largest donating state with Johor and Perak trailing behind.\nAgain this does not reflect the true donor counts for KL as donors from Selangor and Putrajaya being counted as well,which was taken by Pusat Darah Negara')
    
    await context.bot.send_photo(chat_id=chat_id,
                                photo=open('./images/donation_count_state_2022.jpg', 'rb'),
                                caption = f'There are fluctuations according to year,which can be seen from donor counts in 2022,where Perak is the largest donor when we exclude KL')
    
    await context.bot.send_photo(chat_id=chat_id,
                                photo=open('./images/donation_trend_all_years.jpg', 'rb'),
                                caption = f"So by plotting the time series data by year for all the states excluding KL(because it's an outlier),we can see a much clearer trend of donation for all the states within Malaysia.There's no data for Labuan,Putrajaya and Perli,which explains the absence of these states")
    
    
async def show_retention_command(update:Update,context:ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    
    await context.bot.send_photo(chat_id=chat_id,
                                photo=open('./images/trend_donor_type_malaysia.jpg', 'rb'),
                                caption = f"Donors in Malaysia can be divided into two types,New and Returning Donors.\nReturning Donors can further be broken down into Regular Donor(those who donate regularly within 2 years) and Lapsed Donor(those who donate again after 2 years).\nThe plot shows the trend of donors in Malaysia,where we see more returning donors and new donors.\nThe dip in regular donors after 2020 can be attributed to COVID19,which made donating difficult,but is on the rise again.")
    
    await context.bot.send_photo(chat_id=chat_id,
                                photo=open('./images/trend_retention_malaysia.jpg', 'rb'),
                                caption = f"Thus a plot of retention rates can be used.\nThe retention rate is calculated by using (type of returning donors/total_donors)*100.\nHere we see a trend of more regular donors returning in the year 2023.")

async def show_new_donors_command(update:Update,context:ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    
    await context.bot.send_photo(chat_id=chat_id,
                                photo=open('./images/trend_donor_type_malaysia.jpg', 'rb'),
                                caption = f"Malaysia is also receiving new donors amongst all blood donors,and the number is steadily rising again after COVID19")
    
    await context.bot.send_photo(chat_id=chat_id,
                                photo=open('./images/trend_new_donors_malaysia.jpg', 'rb'),
                                caption = f"A clearer picture can be seen in this plot,where we see a decline after 2020,which was due to COVID19.\n Another things to attribute towards the decline is the previous new donors being classified as returning donors,which shows that Malaysia is retaining donors well")
    
    await context.bot.send_photo(chat_id=chat_id,
                                photo=open('./images/trend_new_donors_age_groups_2023_2024.jpg', 'rb'),
                                caption = f"From 2023 - 2024, the younger generation (17-24) makes up the brunt of the donation force")
    
    await context.bot.send_photo(chat_id=chat_id,
                                photo=open('./images/trend_new_donors_age_groups_years.jpg', 'rb'),
                                caption = f"A more general trend of the new donors over the years can be seen here")
    

    
    