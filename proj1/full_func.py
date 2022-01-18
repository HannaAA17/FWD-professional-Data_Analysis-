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
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city_test = input("Enter filter input for city (chicago, new york city, washington):").lower()

        city_list = ['chicago', 'new york city', 'washington']
        city_list_short = ['chi', 'new', 'wash']

        if city_test in city_list:
            city = city_test
            break
        elif city_test in city_list_short:
            print("I got your back lazy bro ;)")
            city = city_list[city_list_short.index(city_test)]  
            break
        else:
            print("Unvaild city name, please enter one of the following \n chicago, new york city, washington")
            continue
    if city: print(city)    
    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        month_test = input("Enter filter input for month (all, january, february, ... , june):").lower() 

        month_list = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
        month_list_short = ["9999",'jan', 'feb', 'mar', 'apr', 'may', 'jun']

        if month_test in month_list:
            month = month_test  
            break
        elif month_test in month_list_short:
            print("I got your back lazy bro ;)")
            month = month_list[month_list_short.index(month_test)]  
            break
        else:
            print("Unvaild month name, please enter one of the following \n all, january, february, ... , june")
            continue
    if month: print(month)

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day_test = input("Enter filter input for day (all, monday, tuesday, ... sunday):").lower()

        day_list = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        day_list_short = ["9999",'mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
        
        if day_test in day_list:
            day = day_test
            break
        elif day_test in day_list_short:
            print("I got your back lazy bro ;)")
            day = day_list[day_list_short.index(day_test)]
            break
        else:
            print("Unvaild day name, please enter one of the following \n all, monday, tuesday, ... sunday")
            continue
    if day: print(day)
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
    
    ########prepare data#########
    df = prepare_data(df)
    
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month.lower())+1
    
        # filter by month to create the new dataframe
        df = df[df['month']==month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df =  df[df['day_of_week']==day.title()]
    return df

def prepare_data(df):
    '''df['day_of_week'] = df['Start Time'].dt.strftime("%A")
    %A -Full weekday name like MONDAY, TUESDAY etc
    %w -Weekday as a decimal number like 1,2,3 etc
    %a -Abbreviated weekday name like SUN,MON etc
    %Y -year
    %m -month
    %d -day
    %H -hours
    %M -minutes
    %S -seconds'''
    
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df["Start Time"])

    # extract month and day of week from Start Time to create new ##monthcolumns##
    df['month'] = df['Start Time'].dt.month
       
    df['day_of_week'] = df['Start Time'].dt.strftime("%A")
    #or df['day_of_week'] = df['Start Time'].dt.weekday_name

    # extract hour from the Start Time column to create an ###hour column###
    df['hour'] = df['Start Time'].dt.hour
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    popular_month = df['month'].value_counts().idxmax()
    ##or #popular_month = df['month'].value_counts().index[0]
    ##or #popular_month = df['month'].mode()[0]    
    print('Most Common Month:', popular_month)
    
    # TO DO: display the most common day of week
    popular_day_of_week = df['day_of_week'].value_counts().index[0]
    print('Most Common Day of Week:', popular_day_of_week)
    
    # TO DO: display the most common start hour
    # find the most common start hour (from 0 to 23)
    popular_hour = df['hour'].mode()[0]
    print('Most Common Start Hour:', popular_hour)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_start_station = df['Start Station'].value_counts().idxmax()
    print('Most Common Start Station:', popular_start_station)
    
    # TO DO: display most commonly used end station
    popular_end_station = df['End Station'].value_counts().idxmax()
    print('Most Common End Station:', popular_end_station)
    
    # TO DO: display most frequent combination of start station and end station trip
    popular_combination = df.groupby(['Start Station','End Station']).size().idxmax()
    print('Most Common Combination of Start Station and End Station:', popular_combination)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print("Total Travel Time:",total_travel_time)
    
    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print("Mean Travel Time:",mean_travel_time)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print("Counts of User Types:\n",user_types)
    
    ##check which city##
    if city != "washington":
        # TO DO: Display counts of gender
        gender = df['Gender'].value_counts()
        print("Counts of User gender:\n",gender)
        
        # TO DO: Display earliest, most recent, and most common year of birth
        earliest_year_of_birth = df['Birth Year'].max()
        print("Earliest Year of Birth:",earliest_year_of_birth)
        
        most_recent_year_of_birth = df['Birth Year'].min()
        print("Most Recent Year of Birth:",most_recent_year_of_birth)
        
        most_common_year_of_birth = df['Birth Year'].value_counts().idxmax()
        print("Most Common Year of Birth:",most_common_year_of_birth)
        
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def rawcode5lines(city):
    dff = pd.read_csv(CITY_DATA[city])
    startnum = 0
    while True:
        ans = input('\nWould you like to show raw data? Enter yes or no.\n')
        if ans.lower() != 'yes':
            break
        print(dff.iloc[startnum:startnum+5,:])
        startnum += 5
    
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        rawcode5lines(city)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

            
if __name__ == "__main__":
	main()
