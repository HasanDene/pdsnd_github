import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

months = ['january', 'february', 'march', 'april', 'may', 'june']    # defined upfront, as used in several functions
days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']    # defined upfront, as used in several functions

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Bonjour! Let\'s explore some US bikeshare data.')
    
    # Define complete lists upfront, so they're not recreated with every while loop
    cities = ['chicago', 'new york city', 'washington']
    
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        print()
        city = input('Would you like to see data for Chicago, New York City or Washington? ').strip().lower()
        if city in cities:
            print()
            print(f'You\'ve chosen {city.title()}')
            break      
        else:
            print()
            print('That\'s not a valid city - try again, and be wary of spelling')
                  
    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        print()
        month = input('Would you like to see data for all months, or a single month? Input either "all" or a single month name: ').strip().lower()
        if month == 'all':
            print()
            print('You\'ve chosen all months')
            break      
        elif month in months:
            print()
            print(f'You\'ve chosen {month.title()}')
            break      
        else:
            print()
            print('That\'s not a valid answer - try again, and be wary of spelling')  

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        print()
        day = input('Would you like to see data for all days, or a single day? Input either "all" or a single day name: ').strip().lower()
        if day == 'all':
            print()
            print('You\'ve chosen all days')
            break
        elif day in days:
            print()
            print(f'You\'ve chosen {day.title()}')
            break      
        else:
            print()
            print('That\'s not a valid answer - try again, and be wary of spelling')  
    
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
    
    # Create dataframe, df, using data for selected city
    df = pd.read_csv(CITY_DATA[city])

    # Convert 'Start Time' column to datetime format to support day and month extraction
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # Create new 'Month' and 'Day_of_week' columns from re-formatted 'Start Time' column
    df['Month'] = df['Start Time'].dt.month
    df['Day_of_week'] = df['Start Time'].dt.weekday_name        # weekday_name has been deprecated - should be .day_name ?
    
    # Filter df by month
    if month != 'all':
        month_num = months.index(month) + 1
        df = df[df['Month'] == month_num]
        
    # Filter by day
    if day != 'all':
        df = df[df['Day_of_week'].str.lower() == day.lower()]       # set both sides to lower case as a guard
    
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel.
    
    Added in guards against potential errors."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    print()

    # Display the most common month; included try/except to counter potential errors
    try:
        month_mode_series = df['Month'].dropna().mode()       # .dropna() to ignore missing values
        if not month_mode_series.empty:     # check if series is empty or not
            common_month = months[int(month_mode_series.iloc[0])-1]      # Use int() to avoid unexpected floats
            print(f'The most popular month is {common_month.title()}')
        else:
            print('No data available to determine the most popular month.')    
    # except statements to advise on specific exceptions
    except Exception as e:      # updated this to only cover general errors
        print(f'Cannot display data due to an error: {e}.')
    print()

    # Display the most common day of the week; included try/except to counter potential errors
    try:
        day_mode_series = df['Day_of_week'].dropna().mode()     # .dropna() to ignore missing values
        if not day_mode_series.empty:       # check if series is empty or not
            common_day = day_mode_series.iloc[0]    
            print(f'The most popular day is {common_day.title()}')
        else:
            print('No data available to determine the most popular day.')    
    # except statements to advise on specific exceptions
    except KeyError:
        print('Cannot display data - column is missing.')
    except (TypeError, ValueError):
        print('Cannot display data - data is not in expected format.')
    except Exception as e:
        print(f'Cannot display data due to an unexpected error: {e}.')
    print()
    
    # TO DO: display the most common start hour
    try:
        hour_mode_series = df['Start Time'].dt.hour.dropna().mode()   # no need to convert to datetime again
        if not hour_mode_series.empty:      # check if series is empty or not
            common_hour = hour_mode_series.iloc[0]
            print(f'The most popular start hour is {common_hour}')
        else:
            print('No data available to determine the most popular hour.')    
    # except statements to advise on specific exceptions
    except KeyError:
        print('Cannot display data - column is missing.')
    except (TypeError, ValueError):
        print('Cannot display data - data is not in expected format.')
    except Exception as e:
        print(f'Cannot display data due to an unexpected error: {e}.')
    print()
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    print()

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    print()

    # TO DO: display most commonly used start station
    try:
        start_station_mode = df['Start Station'].dropna().mode()
        if not start_station_mode.empty:
            common_start_station = start_station_mode.iloc[0]
            print(f'The most popular start station is {common_start_station}')
        else:
            print('No data available to determine the most popular start station.')
    # except statements to advise on specific exceptions
    except KeyError:
        print('Cannot display data - column is missing.')
    except (TypeError, ValueError):
        print('Cannot display data - data is not in expected format.')
    except Exception as e:
        print(f'Cannot display data due to an unexpected error: {e}.')
    print()
    
    # TO DO: display most commonly used end station
    try:
        end_station_mode = df['End Station'].dropna().mode()
        if not end_station_mode.empty:
            common_end_station = end_station_mode.iloc[0]
            print(f'The most popular end station is {common_end_station}')
        else:
            print('No data available to determine the most popular end station.')
    # except statements to advise on specific exceptions
    except KeyError:
        print('Cannot display data - column is missing.')
    except (TypeError, ValueError):
        print('Cannot display data - data is not in expected format.')
    except Exception as e:
        print(f'Cannot display data due to an unexpected error: {e}.')
    print()
    
    # TO DO: display most frequent combination of start station and end station trip
    df.loc[:, 'Start-End Combo'] = df['Start Station'] + ' to ' + df['End Station']     # .loc as a precaution
    try:
        station_combo_mode = df['Start-End Combo'].dropna().mode()
        if not station_combo_mode.empty:
            common_station_combo = station_combo_mode.iloc[0]
            print(f'The most popular combo of start and end station is {common_station_combo}')
        else:
            print('No data available to determine the most popular combo of start and end station.')
    # except statements to advise on specific exceptions
    except KeyError:
        print('Cannot display data - column is missing.')
    except (TypeError, ValueError):
        print('Cannot display data - data is not in expected format.')
    except Exception as e:
        print(f'Cannot display data due to an unexpected error: {e}.')
    print()
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    print()

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    
    print('\nCalculating key stats on total and average trip duration...\n')
    start_time = time.time()
    print()
    
    # TO DO: display total travel time
    total_travel_time_secs = df['Trip Duration'].sum()
    total_travel_time_hours = total_travel_time_secs / (3600)    # converted to hours for readability
    print(f'Total travel time was {total_travel_time_hours:,.1f} hours')    # adjusted formatting
    print()
    
    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print(f'Average travel time was {mean_travel_time:,.0f} seconds')
    print()
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):       # made "city" an argument, so that it's passed to this function to produce gender/birth messages for Washington
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    print()
    
    # TO DO: Display counts of user types
    print('Count of users, by type: ')
    print()
    print(df['User Type'].value_counts())
    print()

    # TO DO: Display counts of gender
    if city == 'chicago' or city == 'new york city':
        print('Count of users, by gender: ')
        print()
        print(df['Gender'].value_counts())
        print()
    else:
        print('Gender data is not available for this city.')
        print()

    # TO DO: Display earliest, most recent, and most common year of birth
    if city == 'chicago' or city == 'new york city':
        birth_year_series = df['Birth Year'].dropna()       
        if not birth_year_series.empty:     # check if series is empty
            print('Birth year stats:')
            print()
            print(f"Earliest birth year: {df['Birth Year'].min():.0f}")
            print(f"Most recent birth year: {df['Birth Year'].max():.0f}")
            print(f"Most common birth year: {df['Birth Year'].mode()[0]:.0f}")
        else:
            print('No birth year data available.')
    else:
        print('Birth year data is not available for this city.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df, page_size = 5):        # page_size is set to 5 as default
    """ 
    Purpose: Asks user if they want to see raw data, and prints a given number of lines at a time until the user says no
    
    Args:
        df: takes in the filtered dataframe
        page_size: number of lines per page - set to 5 by default
    
    Note: Uses safeguards to ensure that total number of rows printed does not exceed those in the df, and 
    adjusts the last page to remaining number of rows if that is less than page_size by using a 
    min() function to define the variable "end"
    """
    
    start = 0       # setting start = 0 outside of any loops
    first_prompt = True     # set to True at start of function, to help show correct initial message
        
    # Get initial user input re: would they like to see raw data?
    while True:
        print()
        user_prompt = input(f'Would you like to see the first {page_size} rows of raw data? Answer "yes" or "no": ').strip().lower()
        if user_prompt == 'yes':
            break
        elif user_prompt == 'no':
            print()
            print('Okay, we\'ll keep the data to ourselves.')
            return      # Used return to exit the entire function, as next loop is not relevant
        else:
            print()
            print('That\'s not a valid answer - please type "yes" or "no"')
    
    # If they requested to see data, show first 5 rows, ask if they want more, then keep showing until they say no or rows run out
    while True:
        if start >= len(df):     # Ensure that we have rows left to show
            print()
            print('Sorry - there\'s no more data to show!')
            break        
        if first_prompt:        # Show correct message if first prompt
            print()
            print(f'Great, here\'s the first {page_size} rows of data: ')
            end = min(start + page_size, len(df))
            print(df.iloc[start: end, :])
            first_prompt = False
            start = end
            continue        
        
        # If not first prompt, ask user if they want to see more rows
        print()
        user_prompt = input(f'Would you like to see {page_size} more rows of raw data? Answer "yes" or "no": ').strip().lower()
        if user_prompt == 'yes':
            print()
            print(f'Great, here\'s the next {page_size} rows: ')
            end = min(start + page_size, len(df))
            print(df.iloc[start: end, :])
            start = end
            continue
        elif user_prompt == 'no':
            print()
            print('Okay, no more data for you!')
            break
        else:
            print()
            print('That\'s not a valid answer - please type "yes" or "no"')

def main():
    while True:
        city, month, day = get_filters()    # this assigns variable values such that other functions can use them
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        raw_data(df)

        # put an inner loop to collect valid user input for restart
        while True:
            restart = input('\nWould you like to restart? Enter "yes" or "no".\n').strip().lower()
            if restart == 'no':
                print()
                print('No worries - have a great day!')
                return      # exits entire function
            elif restart == 'yes':
                break
            else:
                print('That\'s not a valid answer - please type "yes" or "no"')


if __name__ == "__main__":
	main()
