import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
months_options = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
day_options = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("Which city do you want to filter by? (chicago, new york city, washington): \n").lower()

    while city not in CITY_DATA :
        city = input("Please enter one of the three cities in the specified format: \n").lower()

    # print the filtering info
    print("Filtering for {} data".format(city))

    # get user input for month
    print("Which month do you want to filter by? (january, february, ... , june)")
    print("type all for no filters")
    month = input().lower()

    while month not in months_options :
        month = input("Please enter a valid month: \n").lower()

    # get user input for day of week
    print("Which day do you want to filter by? ((monday, tuesday, ... sunday))")
    print("type all for no filters")
    day = input().lower()

    while day not in day_options :
        day = input("Please enter a valid day of week: \n").lower()

    # print the filtering info
    print("Filtering for {} month data".format(month))
    print("Filtering for {} day data".format(day))

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
        df - pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].mode()[0]
    print("The most common month for those filters is {}".format(months_options[common_month - 1].title()))

    # display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print("The most common day for those filters is {}".format(common_day))

    # display the most common start hour
    common_start_time = df['Start Time'].mode()[0]
    print("The most common start time for those filters is {}".format(common_start_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print("The most common start station for those filters is {}".format(common_start_station))

    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print("The most common end station for those filters is {}".format(common_end_station))

    # display most frequent combination of start station and end station trip
    common_trip = df.groupby(['Start Station', 'End Station']).size().sort_values(ascending=False)
    common_trip_data = common_trip.index[0]
    common_trip_count = common_trip[0]
    print("The most common trip for those filters is {} with a count of {}".format(common_trip_data, common_trip_count))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel = df['Trip Duration'].sum()
    print("The total travel time for these filters is {}".format(total_travel))

    # display mean travel time
    avg_travel = df['Trip Duration'].mean()
    print("The average travel time for these filters is {}".format(avg_travel))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    # Make sure it's in the data first

    if 'User Type' in df.columns :
        print(df['User Type'].value_counts())
    else :
        print("User Type is not available for this city")

    # Display counts of gender
    # Make sure it's in the data first

    if 'Gender' in df.columns :
        print(df['Gender'].value_counts())
    else :
        print("Gender is not available for this city")

    # Display earliest, most recent, and most common year of birth
    # Make sure it's in the data first
    
    if 'Birth Year' in df.columns :
        print("Most recent date of birth: {}".format(df['Birth Year'].max()))
        print("Earliest date of birth: {}".format(df['Birth Year'].min()))
        print("Most common date of birth: {}".format(df['Birth Year'].mode()[0]))
    else :
        print("Birth Year is not available for this city")


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

        # check if user wants to see rows of input
        display_data = input("Would you like to see individual trip data? Enter yes or no.\n")
        if display_data.lower() == "yes":
            print(df.head())

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
