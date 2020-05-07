import time
import pandas as pd
import numpy as np
import statistics
import datetime
import calendar

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
    print('\nHello! Let\'s explore some US bikeshare data!')

    # Get user input for city (chicago, new york city, washington)
    # Use a WHILE loop to handle invalid inputs
    while True:
        city = input('\nWould you like to see the data for Chicago, New York City, or Washington?\n').lower()
        if city in ('new york city', 'washington', 'chicago'):
            break
        else:
            print('Invalid city, check your spelling!')

    filter = input("\nHow would you like to filter the data? Enter month, day, both, or none?\n").lower()

    if filter == 'month':
        day = 'all'
        while True:
            month = input("\nWhich month: January, February, March, April, May, or June?\n").lower()
            if month in ['january', 'february', 'march', 'april', 'may', 'june']:
                break
            else:
                print('Please enter full month name.')
    elif filter == 'day':
        month = 'all'
        while True:
            day = int(input('\nWhich day? type integer that correlates to the day (Monday=0, Sunday=6)\n'))
            if day in [0,1,2,3,4,5,6]:
                break
            else:
                print('Please enter an integer from 0 to 6.')
    elif filter == 'both':
        while True:
            month = input("\nWhich month: January, February, March, April, May, or June?\n").lower()
            if month in ['january', 'february', 'march', 'april', 'may', 'june']:
                break
            else:
                print('Please enter full month name.')
        while True:
            day = int(input('\nWhich day? type integer that correlates to the day (Monday=0, Sunday=6)\n'))
            if day in [0,1,2,3,4,5,6]:
                break
            else:
                print('Please enter an integer from 0 to 6.')
    elif filter == 'none':
        month = 'all'
        day = 'all'
    else:
        print('Looks like something went wrong, restart the program and make sure to enter one of the specified inputs')

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])

    # Create filters based on entered information, use IF for day, month, all, none
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month)+1
        # filter by month to create the new dataframe
        df = df.loc[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df.loc[df['day_of_week'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Convert start time column to datetime format in python
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Display the most common month
    df['month_name'] = df['Start Time'].dt.month
    top_month = calendar.month_name[df['month_name'].mode()[0]]
    print('Most Common Month:', top_month)

    # Display the most common day of week
    df['day'] = df['Start Time'].dt.weekday
    top_day = calendar.day_name[df['day'].mode()[0]]
    print('Most Common Day:', top_day)

    # Display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    top_hour = df['hour'].mode()[0]
    print('Most Common Start Hour:', top_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    print('Most common starting station: {}'.format(df['Start Station'].value_counts(ascending=False).keys()[0]))

    # Display most commonly used end station
    print('Most common ending station: {}'.format(df['End Station'].value_counts(ascending=False).keys()[0]))

    # Display most frequent combination of start station and end station trip
    df['start_end'] = df['Start Station'].str.cat(df['End Station'],sep=" --> ")
    print('Most popular station to station trip: {}'.format(df['start_end'].value_counts(ascending=False).keys()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """ Displays total and average trip duration """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    print('Total travel time: {} minutes'.format(int(sum(df['Trip Duration'])/60)))

    # Display mean travel time
    print('Average length of each trip: {:.2f} minutes'.format((df['Trip Duration'].mean())/60))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = pd.Series(df['User Type']).value_counts().to_frame()
    print('Breakdown of user types:\n   {}'.format(user_types))
    print('')

    # Display counts of gender
    # TO DO: no gender or birth year stats for Washington, need to fix here
    if 'Gender' in df:
        gender_data = pd.Series(df['Gender']).value_counts().to_frame()
        print('Breakdown of user genders:\n {}'.format(gender_data))
        print('')
    else:
        print('The data for this city has no gender data.\n')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        oldest = df['Birth Year'].min()
        youngest = df['Birth Year'].max()
        common = df['Birth Year'].mode()[0]
        print('Birth Year Statistics:')
        print('The earliest birth year is {}'.format(int(oldest)))
        print('The most recent birth year is {}'.format(int(youngest)))
        print('The most common birth year is {}'.format(int(common)))
    else:
        print('The data for this city has no birth year data.')

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

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
