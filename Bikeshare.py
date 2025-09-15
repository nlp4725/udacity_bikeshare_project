import time as time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('\nWould you like to see data for Chicago, New York, or Washington? Please type the city\'s name.\n')
        city = city.lower().strip()
        if city in ['chicago', 'new york', 'washington']:
            break
        else:
            print('Error: wrong input. Please retype the city\'s name.')
    # get user input for month, day, both or not at all
    while True:
        choice = input('\nWould you like to filter by month, day, both or not at all.\n')
        choice = choice.lower().strip()
        if choice in ['month', 'day', 'both', 'not at all']:
            break
        else:
            print('Error: wrong input.')
    # TO DO: get user input for month (all, january, february, ... , june)
    if choice == 'month':
        while True:
            month = input('\nWhich month? Please select one of the following months: Jan, Feb, Mar, Apr, May, Jun.\n')
            month = month.lower().strip()
            if month in ['jan', 'feb', 'mar', 'apr', 'may', 'jun']:
                day = [0, 1, 2, 3, 4, 5, 6]
                break
            elif month in ['jul', 'aug', 'sep', 'oct', 'nov', 'dec']:
                print('Error: month selection is out of range. Please select a month between Jan and Jun.')
            else:
                print('Error: wrong input. Please retype the three-letter month between Jan and Jun.')
    elif choice == 'day':
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
        while True:
            try:
                day = input('\nWhich day? please type your input as a number between 0 and 6. Monday = 0, Tuesday = 1, Wednesday = 2, Thursday = 3, Friday = 4, Saturday = 5, Sunday = 6.\n')
                day = int(day)
                if day >= 0 and day <= 6:
                    month = ['jan', 'feb', 'mar', 'apr', 'may', 'jun']
                    break
                else:
                    print('Error: input out of range.')
            except ValueError:
                print('Error:wrong input. Please type your input as a number.')
    elif choice == 'both':
        while True:
                month = input('\nWhich month? Please select one of the following months: Jan, Feb, Mar, Apr, May, Jun.\n')
                month = month.lower().strip()
                if month in ['jan', 'feb', 'mar', 'apr', 'may', 'jun']:
                    break
                elif month in ['jul', 'aug', 'sep', 'oct', 'nov', 'dec']:
                    print('Error: month selection is out of range. Please select a month between Jan and Jun.')
                else:
                    print('Error: wrong input. Please retype the three-letter month between Jan and Jun.')
        while True:
            try:
                day = input('\nWhich day? please type your input as a number between 0 and 6. Monday = 0, Tuesday = 1, Wednesday = 2, Thursday = 3, Friday = 4, Saturday = 5, Sunday = 6.\n')
                day = int(day)
                if day >= 0 and day <= 6:
                    break
                else:
                    print('Error: input out of range.')
            except ValueError:
                print('Error:wrong input. Please type your input as a number.')
    else:
        month = ['jan', 'feb', 'mar', 'apr', 'may', 'jun']
        day = [0, 1, 2, 3, 4, 5, 6]

    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or 'all' to apply no month filter
        (int) day - name of the day of week to filter by, or 'all' to apply no day filter
    
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # get the dataframe from the input city
    df = pd.read_csv(CITY_DATA['new york city' if city.lower() == 'new york' else city])
    # convert the start time to datetime format
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract the month info from df into a sperate column
    df['month'] = df['Start Time'].dt.month
    # filter based on the input of the month
    months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun']
    month_list = [i for i, name in enumerate(months) if name in month]
    month_list = [month + 1 for month in month_list]
    df = df[df['month'].isin(month_list)]
    # extract the day of the week info from df into a sperate column
    df['day'] = df['Start Time'].dt.dayofweek
    # filter based on the input of the day
    df = df[df['day'].isin([day] if isinstance(day, int) else day)]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df.get('month')
    # some month are not in the database, to prevent error, use a condition to filter
    if len(common_month.unique()) != 1:
        common_month = common_month.mode()[0]
        months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun']
        common_month = months[common_month - 1]
        print(f'The most common month is {common_month.title()}.')

    # display the most common day of week
    if len(df.get('day').unique()) != 1:
        common_day = df.get('day').mode()[0]
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        common_day = days[common_day]
        print(f'The most common day of week is {common_day}.')

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df.get('hour').mode()[0]
    print(f'The most common hour is {common_hour} o\'clock.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print(f'The most common start station is {common_start_station}.')

    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print(f'The most common end station is {common_end_station}.')

    # display most frequent combination of start station and end station trip
    df['start_to_end'] = df['Start Station'] + ' to ' + df['End Station']
    common_combo = df['start_to_end'].mode()[0]
    print(f'The most frequent combination of start station and end station trip is from {common_combo}.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    df['Trip Duration'] = pd.to_timedelta(df['Trip Duration'], unit='s')
    max_time = df['Trip Duration'].max()

    # Convert the time to userfriendly format
    days = max_time.components.days
    hours = max_time.components.hours
    minutes = max_time.components.minutes
    seconds = max_time.components.seconds
    print(f'The longest travel time duration is {days} days, {hours} hours, {minutes} minutes, {seconds} seconds.')

    # Display mean travel time
    mean_time = df['Trip Duration'].mean()
    days_mean = mean_time.components.days
    hours_mean = mean_time.components.hours
    minutes_mean = mean_time.components.minutes
    seconds_mean = mean_time.components.seconds
    print(f'The average travel time duration is {days_mean} days, {hours_mean} hours, {minutes_mean} minutes, {seconds_mean} seconds.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    # Get rid of Nan value in user type column, 
    df_user_types = df.dropna(axis = 0, subset=['User Type'])
    print(pd.DataFrame(df_user_types['User Type'].value_counts().reset_index().rename(columns={'index':'User Type', 'User Type':'Count'})))
    print("\n")
                       
    # Display counts of gender
    # Some database does not have gender or birth year column, to prevent error, we need to filter it first.
    if df.get("Gender") is None:
        print('Unfortunately, there is no gender info in this data set.')
    else: 
        df_gender = df.dropna(axis = 0, subset=['Gender'])
        print(df_gender['Gender'].value_counts().reset_index().rename(columns={'index':'Gender', 'Gender':'Count'}))
        print('\n')
    
    # Display earliest, most recent, and most common year of birth
    # Some database does not have gender or birth year column, to prevent error, we need to filter it first.
    if df.get('Birth Year') is None:
        print('Unfortunately, there is no birth year info in this data set.')
    else: 
        df_birth = df.dropna(axis = 0, subset=['Birth Year'])
        print(f'The earliest year of birth is {int(df_birth["Birth Year"].min())}.')
        print(f'The most recent year of birth is {int(df_birth["Birth Year"].max())}.')
        print(f'The most common year of birth is {int(df_birth["Birth Year"].mode().iloc[0])}.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
def main():
    while True: 
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        # prompt use to show raw data
        index = 0
        while True:
            user_input = input('\nWould you like to see the raw data? Answer yes or no.\n')
            if user_input.lower().strip() == 'yes':
                while index < len(df):
                    if index == 0:
                        print(df.iloc[index:index+5].to_dict(orient='records'))
                        index += 5
                    else:
                        more_input = input('\nMore raw data? Answer yes or no.\n')
                        if more_input.lower().strip() == 'no':
                            break
                        elif more_input.lower().strip() == 'yes':
                            print(df.iloc[index:index+5].to_dict(orient='records'))
                            index += 5
                        else:
                            print('Error: wrong input')
                break
            elif user_input.lower().strip() == 'no':
                break
            else: 
                print('Error: wrong input')
        # prompt user to restart the process
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower().strip() != 'yes':
            break

if __name__ == '__main__':
    main()