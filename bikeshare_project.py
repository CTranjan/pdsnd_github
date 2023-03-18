import time
import pandas as pd
import numpy as np
import os
import calendar

pd.options.mode.chained_assignment = None  # default='warn'

#Loading the data frame
def load_file():
    data = pd.DataFrame()
    directory = os.getcwd()
    # Checking for files in current directory
    for filename in os.listdir(directory):
        ext = os.path.splitext(filename)[-1].lower()
        city = str(filename).lower().split('.')[0]
        # Loading only city csv databases
        if ext=='.csv':
            df_temp = pd.read_csv(f'{filename}')
            df_temp['city'] = city 
            data = pd.concat([data, df_temp], ignore_index=True)
        else:
            pass
    data = data.rename(columns={'Unnamed: 0': 'id'})
    # df_append.to_excel(f'{directory}/result.xlsx')
    return data

#Filtering the data frame
def filters_lists(data):
    delay_time = 0
    data['Start Time'] = pd.to_datetime(data['Start Time'])

    # Avaiable Cities 
    cities = data['city'].unique()
    city_list = cities.tolist()
    city_list.append('all')
    print('\nAvaiable city filters: ', city_list)
    time.sleep(delay_time)

    # Filtering by city
    while True:
        try:
            city_filter = input('\nWhich of the cities you want to see data from? ')
            city_filter = city_filter.lower()
            if city_filter == 'all':
                print('-> you chose all')
                df_city_filter = data
                break
            elif city_filter in city_list and city_filter != 'all':
                print(f'-> you chose {city_filter}')
                df_city_filter = data[data['city'] == city_filter]
                break
            else:
                raise ValueError('\nThat\'s not a valid input, try again!\n')
        except ValueError as e:
            print(e)
            continue

    # Avaiable years 
    df_city_filter['year'] = df_city_filter['Start Time'].dt.year
    df_city_filter['year'] = df_city_filter['year'].astype(str)
    year_list = df_city_filter['year'].unique().tolist()
    year_list = sorted(year_list)
    year_list.append('all')
    print('\nAvaiable year filters: ', year_list)
    time.sleep(delay_time)

    # Filtering by year
    while True:
        try:
            year_filter = input('\nWhich of the years you want to see data from? ')
            year_filter = year_filter.lower()
            if year_filter == 'all':
                print('-> you chose all')
                df_year_filter = df_city_filter
                break
            elif year_filter in year_list and year_filter != 'all':
                print(f'-> you chose {year_filter}')
                df_year_filter = df_city_filter[df_city_filter['year'] == year_filter]
                break
            else:
                raise ValueError('\nThat\'s not a valid input, try again!\n')
        except ValueError as e:
            print(e)
            continue

    # Avaiable Months
    df_year_filter['month'] = df_year_filter['Start Time'].dt.month
    df_year_filter['month'] = df_year_filter['month'].astype(str)
    month_list =  df_year_filter['month'].unique().tolist()
    month_list = sorted(month_list)
    month_list.append('all')
    print('\nAvaiable month filters: ', month_list)
    time.sleep(delay_time)

    # Filtering by month
    while True:
        try:
            month_filter = input('\nWhich of the monhts you want to see data from? ')
            month_filter = month_filter.lower()
            if month_filter == 'all':
                print('-> you chose all')
                df_month_filter = df_year_filter
                break
            elif month_filter in month_list and month_filter != 'all':
                print(f'-> you chose {month_filter}')
                df_month_filter = df_year_filter[df_year_filter['month'] == month_filter]
                break
            else:
                raise ValueError('\nThat\'s not a valid input, try again!\n')
        except ValueError as e:
            print(e)
            continue

    # months Days of week
    df_month_filter['dow'] = df_month_filter['Start Time'].dt.dayofweek
    day_of_week_list = df_month_filter['dow'].unique().tolist()
    day_of_week_list = sorted(day_of_week_list)
    day_of_week_list = [calendar.day_name[x] for x in day_of_week_list]
    day_of_week_list.append('all')
    df_month_filter['dow'] = df_month_filter['dow'].apply(lambda x: calendar.day_name[x])
    print('\nAvaiable day of week filters: ', day_of_week_list)
    time.sleep(delay_time)

    # Filtering by Days of week
    while True:
        try:
            dow_filter = input('\nWhich day of week you want to see data from? ')
            if dow_filter == 'all':
                print('-> you chose all')
                df_dow_filter = df_month_filter
                break
            elif dow_filter in day_of_week_list and dow_filter != 'all':
                print(f'-> you chose {dow_filter}')
                df_dow_filter = df_month_filter[df_month_filter['dow'] == dow_filter]
                break
            else:
                raise ValueError('\nThat\'s not a valid input, try again!\n')
        except ValueError as e:
            print(e)
            continue

    df_filtered = df_dow_filter
    return df_filtered

# Outputting Selected Statistics
def statistics(filtered_df):
    while True:
        try:
            delay_time = 0
            options_list = ['time_stats', 'station_stats', 'trip_duration_stats', 'user_stats']
            print('\nAvaiable statistics: ',options_list, '\n')
            time.sleep(delay_time)
            option = input('What kind of statistics you want know about our bikeshare database? ')
            if option.lower() == 'time_stats':
                # Most popular month
                month_counts = filtered_df.groupby('month')['month'].count()
                top_5_months = month_counts.sort_values(ascending=False).head(5)
                top_5_months.name = 'month_count'
                print('The top 5 most popular months by count are:\n',top_5_months,'\n')
                time.sleep(delay_time)
                # Most popular dow
                dow_counts = filtered_df.groupby('dow')['dow'].count()
                top_5_dows = dow_counts.sort_values(ascending=False).head(5)
                top_5_dows.name = 'Day_of_week_count'
                print('The top 5 most popular days of week by count are:\n',top_5_dows,'\n')
                time.sleep(delay_time)
                # Most popular start hour
                filtered_df['hour'] = filtered_df['Start Time'].dt.hour
                hour_counts = filtered_df.groupby('hour')['hour'].count()
                top_5_hours = hour_counts.sort_values(ascending=False).head(5)
                top_5_hours.name = 'hour_count'
                print('The top 5 most popular start hours by count are:\n',top_5_hours,'\n')
                time.sleep(delay_time)
                # Wrapping up 
                sm_yes_list = ['yes', 'y']
                sm_no_list = ['no','n']
                while True:
                    try:
                        see_more = input('Would you like to see any other statistics (y/n)? ')
                        if see_more.lower() in sm_yes_list:
                            break
                        elif see_more.lower() in sm_no_list:
                            break
                        else: 
                            raise ValueError('\nThat\'s not a valid input, try again!\n')
                    except ValueError as e:
                        print(e)
                        continue
                if see_more.lower() in sm_no_list:
                    break
                else:
                    continue
            elif option.lower() == 'station_stats':
                # Most popular start station
                start_station_counts = filtered_df.groupby('Start Station')['Start Station'].count()
                top_5_start_stations = start_station_counts.sort_values(ascending=False).head(5)
                top_5_start_stations.name = 'Start_station_count'
                print('The top 5 most popular start stations by count are:\n',top_5_start_stations,'\n')
                time.sleep(delay_time)
                # Most popular end station
                end_station_counts = filtered_df.groupby('End Station')['End Station'].count()
                top_5_end_stations = end_station_counts.sort_values(ascending=False).head(5)
                top_5_end_stations.name = 'End_station_count'
                print('The top 5 most popular end stations by count are:\n',top_5_end_stations,'\n')
                time.sleep(delay_time)
                # Most popular combination of start and end stations
                filtered_df['start_end_station'] = filtered_df['Start Station'] + ' -> ' + filtered_df['End Station']
                start_end_station_counts = filtered_df.groupby('start_end_station')['start_end_station'].count()
                top_5__start_end_stations = start_end_station_counts.sort_values(ascending=False).head(5)
                top_5__start_end_stations.name = 'Start_End_stations_count'
                print('The top 5 most popular combinations of start and end stations by count are:\n',top_5__start_end_stations,'\n')
                time.sleep(delay_time)
                # Wrapping up 
                sm_yes_list = ['yes', 'y']
                sm_no_list = ['no','n']
                while True:
                    try:
                        see_more = input('Would you like to see any other statistics (y/n)? ')
                        if see_more.lower() in sm_yes_list:
                            break
                        elif see_more.lower() in sm_no_list:
                            break
                        else: 
                            raise ValueError('\nThat\'s not a valid input, try again!\n')
                    except ValueError as e:
                        print(e)
                        continue
                if see_more.lower() in sm_no_list:
                    break
                else:
                    continue
            elif option.lower() == 'trip_duration_stats':
                # Total Travel time
                total_travel_time = filtered_df['Trip Duration'].sum().round(2)
                print('The total travel time for the selected filters is:\n',total_travel_time,'\n')
                time.sleep(delay_time)
                # mean Travel time
                mean_travel_time = filtered_df['Trip Duration'].mean().round(2)
                print('The mean travel time for the selected filters is:\n',mean_travel_time,'\n')
                time.sleep(delay_time)
                # median Travel time
                median_travel_time = filtered_df['Trip Duration'].median().round(2)
                print('The median travel time for the selected filters is:\n',median_travel_time,'\n')
                time.sleep(delay_time)
                # max Travel time
                max_travel_time = filtered_df['Trip Duration'].max().round(2)
                print('The maximum travel time for the selected filters is:\n',max_travel_time,'\n')
                time.sleep(delay_time)
                # min Travel time
                min_travel_time = filtered_df['Trip Duration'].min().round(2)
                print('The minimum travel time for the selected filters is:\n',min_travel_time,'\n')
                time.sleep(delay_time)
                # Wrapping up 
                sm_yes_list = ['yes', 'y']
                sm_no_list = ['no','n']
                while True:
                    try:
                        see_more = input('Would you like to see any other statistics (y/n)? ')
                        if see_more.lower() in sm_yes_list:
                            break
                        elif see_more.lower() in sm_no_list:
                            break
                        else: 
                            raise ValueError('\nThat\'s not a valid input, try again!')
                    except ValueError as e:
                        print(e)
                        continue
                if see_more.lower() in sm_no_list:
                    break
                else:
                    continue
            elif option.lower() == 'user_stats':
                print('\nImportant reminder:\n','-> We do not have data on gender or  year of birth for the city os Washington','\n')
                # Count of user types
                count_user_types = filtered_df.groupby('User Type')['User Type'].count()
                Rank_user_types = count_user_types.sort_values(ascending=False)
                print('The count of user types is:\n',Rank_user_types,'\n')
                time.sleep(delay_time)
                # Count of gender
                count_gender = filtered_df.groupby('Gender')['Gender'].count()
                Rank_gender = count_gender.sort_values(ascending=False)
                print('The count of gender is:\n',Rank_gender,'\n')
                time.sleep(delay_time)
                # earliest year of birth
                earliest_yob = filtered_df['Birth Year'].min()
                print('The earliest year of birth for the selected filters is:\n',earliest_yob,'\n')
                time.sleep(delay_time)
                # most recent year of birth
                most_recent_yob = filtered_df['Birth Year'].max()
                print('The most recent year of birth for the selected filters is:\n',most_recent_yob,'\n')
                time.sleep(delay_time)
                # most common years of birth
                most_common_yobs = filtered_df.groupby('Birth Year')['Birth Year'].count()
                top_5_most_common_yobs = most_common_yobs.sort_values(ascending=False).head(5)
                top_5_most_common_yobs.name = 'Most_commom_year_of_birth_count'
                print('The top 5 most commom years of birth for the selected filters are:\n',top_5_most_common_yobs,'\n')
                time.sleep(delay_time)
                # Wrapping up 
                sm_yes_list = ['yes', 'y']
                sm_no_list = ['no','n']
                while True:
                    try:
                        see_more = input('Would you like to see any other statistics (y/n)? ')
                        if see_more.lower() in sm_yes_list:
                            break
                        elif see_more.lower() in sm_no_list:
                            break
                        else: 
                            raise ValueError('\nThat\'s not a valid input, try again!\n')
                    except ValueError as e:
                        print(e)
                        continue
                if see_more.lower() in sm_no_list:
                    break
                else:
                    continue
            else:
                raise ValueError('\nThat\'s not a valid input, try again!\n')
        except ValueError as e:
            print(e)
            continue
    # Wrapping up
    time.sleep(delay_time) 

def raw_data(filtered_df):
    # Displaying Raw Data
    current_row = 0
    rows_per_iteration = 5
    while True:
        try:
            raw_data = input('\nWould you like to see 5 rows of raw data (y/n)?\n')
            # Stop the program if there is no more raw data to display
            if current_row >= len(filtered_df.index):
                print("There is no more raw data to display.")
                break
            else:
                pass
            if raw_data.lower() == 'y' or raw_data.lower() == 'yes':
                print(filtered_df.iloc[current_row:current_row+rows_per_iteration])
                current_row += rows_per_iteration
            elif raw_data.lower() == 'n' or raw_data.lower() == 'no':
                break
            else: 
                raise ValueError('\nThat\'s not a valid input, try again!\n')
        except ValueError as e:
            print(e)
            continue
        
def main():
    print('Welcome to the Bikeshare_DB interactive Analytics interface')
    while True:
        data = load_file()
        filtered_df = filters_lists(data)
        statistics(filtered_df)
        raw_data(filtered_df)
        while True:
            try:
                restart = input('\nWould you like to restart (y/n)?\n')
                if restart.lower() == 'n' or restart.lower() == 'no':
                    break
                elif restart.lower() == 'y' or restart.lower() == 'yes':
                    break
                else:
                    raise ValueError('\nThat\'s not a valid input, try again!\n')
            except ValueError as e:
                print(e)
                continue
        if restart.lower() == 'n' or restart.lower() == 'no':
            break
        elif restart.lower() == 'y' or restart.lower() == 'yes':
            print('Restarting...')
            continue
    print('\nThanks for consulting the Bikeshare_DB interactive Analytics interface, hope you found what you were looking fore ;)\n')

if __name__ == "__main__":
	main()