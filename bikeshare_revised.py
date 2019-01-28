import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


def get_filters():

    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of city to analyze
        (str) month - name of month to filter by (Jan-Jun), or "all" to apply no month filter
        (str) day - name of day to filter (Mon-Sun), or "all" to apply no day filter
    """
    VALID_CITIES = ['Chicago', 'New York City', 'Washington']
    VALID_MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'All']
    VALID_DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', 'All']

    print('\nHello! Let\'s explore some US bikeshare data!')

    city = input('\nWhich one of these cities would you like more information on: Chicago, New York City, or Washington? ').title()

    while city not in VALID_CITIES:
        print("\nI don't have information on {}.".format(city))
        city = input('\nWhich one of these cities would you like more information on: Chicago, New York City, or Washington? ').title()

    month = input('\nWhich month are you interested in exploring: January, February, March, April, May, June, or all? ').title()

    while month not in VALID_MONTHS:
        print("\nI don't have any data for {}.".format(month))
        month = input('\nWhich month are you interested in exploring: January, February, March, April, May, June or all? ').title()

    day = input('\nAnd which day of the week are you interested in exploring: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, or all? ').title()

    while day not in VALID_DAYS:
        print("\nI don't have any data for {}.".format(day))
        day = input('\nWhich day of the week are you interested in exploring: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, or all? ').title()

    print('-'*40)
    return city, month, day


def load_data(city, month, day):

    """
    Loads data for  specified city and filters by month and day if applicable

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    df = pd.read_csv(CITY_DATA[city.lower()])

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    if month.title() != 'All':
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month = months.index(month.title()) + 1
        df = df[df['month'] == month]

    if day.title() != 'All':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):

    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Create a new column that takes starting hour from the Start Time column
    df['hour'] = df['Start Time'].dt.hour

    # Get the number of the month with highest usage and convert number to name of month
    most_common_month = df['month'].mode()[0]
    if most_common_month == 1:
        most_common_month = 'January'
    elif most_common_month == 2:
        most_common_month = 'February'
    elif most_common_month == 3:
        most_common_month = 'March'
    elif most_common_month == 4:
        most_common_month = 'April'
    elif most_common_month == 5:
        most_common_month = 'May'
    else:
        most_common_month = 'June'

    # Converts hour in military time to standard time
    most_common_hour = df['hour'].mode()[0]
    if most_common_hour == 0:
        convert_hour = '12 AM'
    elif 12 < most_common_hour:
        convert_hour = '{} PM'.format(most_common_hour - 12)
    else:
        convert_hour = '{} AM'.format(most_common_hour)

    print('Most common month:', most_common_month)
    print('Most common day:', df['day_of_week'].mode()[0])
    print('Most common hour:', convert_hour)
    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Create a new column that combines start and end station in order to find most common combination
    df['Station Combination'] = df['Start Station'] + " / " + df['End Station']

    print('Most commonly used start station:', df['Start Station'].mode()[0])
    print('Most commonly used end station:', df['End Station'].mode()[0])
    print('Most commonly used start and end station combination:', df['Station Combination'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration Statistics...\n')
    start_time = time.time()

    # Calculate total amount of seconds travelled and convert to hours, minutes, seconds
    total_travel_seconds = df['Trip Duration'].sum()
    convert_total_hours = int(total_travel_seconds // 3600)
    convert_total_minutes = int((total_travel_seconds % 3600) // 60)
    convert_total_seconds = int((total_travel_seconds % 3600) % 60)

    print('Total travel time: {} hours, {} minutes, {} seconds'.format(convert_total_hours, convert_total_minutes, convert_total_seconds))

    # Calculate average travel time in seconds and converts to hours, minutes, seconds
    ave_travel_seconds = df['Trip Duration'].mean()
    convert_ave_hours = int(ave_travel_seconds // 3600)
    convert_ave_minutes = int((ave_travel_seconds % 3600) // 60)
    convert_ave_seconds = int((ave_travel_seconds % 3600) % 60)

    print('Mean travel time: {} hours, {} minutes, {} seconds'.format(convert_ave_hours, convert_ave_minutes, convert_ave_seconds))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    print('Number of Users by Type:\n', df['User Type'].value_counts())

    # The Washington table does not have gender or birth year data. These if/else statements will let the user know that the data doesn't exist for Washington.
    if 'Gender' in df.columns:
        print('\nNumber of Users by Gender:\n', df['Gender'].value_counts())
    else:
        print('\nGender data not available for Washington')

    if 'Birth Year' in df.columns:
        print("\nYoungest customer's birth year:", int(df['Birth Year'].max()))
        print("Oldest customer's birth year:", int(df['Birth Year'].min()))
        print('Most common birth year:', int(df['Birth Year'].mode()[0]))
    else:
        print("\nBirth year data is not available for Washington.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def descriptive_stats(df):
    """Displays the raw data 5 rows at a time if the user wants to see it."""

    more_details = input("Would you like to see the first 5 rows of raw data('y' or 'n')?")
    while more_details != 'y' and more_details != 'n':
        more_details = input("Please enter 'y' or 'n'.")
    index = np.array([0, 1, 2, 3, 4])
    while more_details == 'y':
            print(df.iloc[index])
            index = index + 5
            more_details = input("Would you like to see the next 5 rows of raw data('y' or 'n')?")


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        descriptive_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()