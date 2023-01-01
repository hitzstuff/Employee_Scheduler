import math
import pathlib
from datetime import datetime
import warnings
import numpy as np
import pandas as pd
import PySimpleGUI as sg
from __init__ import __version__

SCHEDULES_DIRECTORY = ''
EMPLOYEES_FILE = ''
STORE_FILE = ''
STORE_HOURS = ''
HOLIDAY_HOURS = ''
CURRENT_VALUE = ''
YEAR_MON = ''
YEAR_SUN = ''
PROGRESS = ''
CURRENT_VALUE = ''
OUTPUT = ''

# ignore by message
warnings.filterwarnings(
    'ignore', message='Data Validation extension is not supported and will be removed')
# Create a dictionary of months with the number of days in each month
months = {
    1: 31,
    2: 28,
    3: 31,
    4: 30,
    5: 31,
    6: 30,
    7: 31,
    8: 31,
    9: 30,
    10: 31,
    11: 30,
    12: 31
}

def leap_year(year):
    """Given a year, calculates whether or not it is a leap year,
    and returns a True or False value."""
    if (year % 4) == 0:
        if (year % 100) == 0:
            if (year % 400) == 0:
                leap = True
            else:
                leap = False
        else:
            leap = True
    else:
        leap = False
    return leap

def week_day(year, month, day, start_day='mon'):
    '''Finds the day of the week (0-6)'''
    # Break up the year into century and year within that century
    year = str(year)
    century = int(year[:2])
    year = int(year[2:])
    # Establish values for each variable in the equation
    # For the equation to work, January and February must belong to the previous year
    if month == 1:
        month = 11
        year = year - 1
    elif month == 2:
        month = 12
        year = year - 1
    else:
        month = month - 2
    # Use a proven mathematical formula to determine the day of the week on a Gregorian calendar
    w_d = (day + math.floor((2.6 * month) - 0.2) - (2 * century) +
           year + math.floor(year / 4) + math.floor(century / 4)) % 7
    if start_day != 'sun':
        # Convert the week to start on a Monday, instead of a Sunday
        if w_d == 0:
            w_d = 6
        else:
            w_d = w_d - 1
    # Return the day of the week (0-6)
    return w_d
# Populate a Numpy array with numbered days of the week
# Week starts on a Monday and ends on a Sunday

def month_array(month, year, start_day='mon'):
    '''Populates a Numpy array with numbered days of the week.'''
    # Create an array with 6 rows and 7 columns, populated with zeros
    array = np.zeros((6, 7), dtype=np.object_)
    leap = leap_year(year)
    # The number of days in the month.
    days = months[month]
    # Add an extra day to February if the year is a leap year
    if month == 2 and leap is True:
        days += 1
    # Starting position within the array
    if start_day == 'sun':
        pos = week_day(year, month, 1, start_day='sun')
    else:
        pos = week_day(year, month, 1)
    # Handle the numbered days of the previous month.
    # If the first day of the month isn't also the first day of the week
    if pos > 0:
        if month == 1:
            days_pm = months[12]
        else:
            # Find the total number of days in the previous month
            days_pm = months[month - 1]
        i = pos - 1
        while i >= 0:
            array[0][i] = days_pm
            days_pm -= 1
            i -= 1
    # The week number (0-5)
    week = 0
    # The day number (1-31)
    day_num = 1
    # Iterate over the array, replacing zeros with the correct values
    while day_num <= days:
        for _ in array:
            if day_num > days:
                break
            elif pos == 7:
                pos = 0
                week += 1
            array[week][pos] = day_num
            pos += 1
            day_num += 1
    # Iterate over the array, populating the last week with values from the following month.
    day_num = 1
    while pos < 7:
        array[week][pos] = day_num
        pos += 1
        day_num += 1
    return array

def year_array(year, start_day='mon'):
    '''Creates an array containing every week of a given year.'''
    if start_day == 'sun':
        m_jan = pd.DataFrame(month_array(1, year, start_day='sun'))
        m_feb = pd.DataFrame(month_array(2, year, start_day='sun'))
        m_mar = pd.DataFrame(month_array(3, year, start_day='sun'))
        m_apr = pd.DataFrame(month_array(4, year, start_day='sun'))
        m_may = pd.DataFrame(month_array(5, year, start_day='sun'))
        m_jun = pd.DataFrame(month_array(6, year, start_day='sun'))
        m_jul = pd.DataFrame(month_array(7, year, start_day='sun'))
        m_aug = pd.DataFrame(month_array(8, year, start_day='sun'))
        m_sep = pd.DataFrame(month_array(9, year, start_day='sun'))
        m_oct = pd.DataFrame(month_array(10, year, start_day='sun'))
        m_nov = pd.DataFrame(month_array(11, year, start_day='sun'))
        m_dec = pd.DataFrame(month_array(12, year, start_day='sun'))
    else:
        # Create Numpy arrays for each month
        m_jan = pd.DataFrame(month_array(1, year))
        m_feb = pd.DataFrame(month_array(2, year))
        m_mar = pd.DataFrame(month_array(3, year))
        m_apr = pd.DataFrame(month_array(4, year))
        m_may = pd.DataFrame(month_array(5, year))
        m_jun = pd.DataFrame(month_array(6, year))
        m_jul = pd.DataFrame(month_array(7, year))
        m_aug = pd.DataFrame(month_array(8, year))
        m_sep = pd.DataFrame(month_array(9, year))
        m_oct = pd.DataFrame(month_array(10, year))
        m_nov = pd.DataFrame(month_array(11, year))
        m_dec = pd.DataFrame(month_array(12, year))
    # Merge the months together
    months_array = pd.concat([m_jan, m_feb, m_mar, m_apr, m_may, m_jun,
                             m_jul, m_aug, m_sep, m_oct, m_nov, m_dec], ignore_index=True)
    # Rename the headers
    if start_day == 'sun':
        months_array.columns = ['Sunday', 'Monday', 'Tuesday',
                                'Wednesday', 'Thursday', 'Friday', 'Saturday']
    else:
        months_array.columns = [
            'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    # Copy to a new Numpy array
    array = months_array.copy()
    # Clean up the array by removing blank or duplicate weeks
    i = 0
    for i in range(len(months_array) - 1):
        temp_array = months_array[months_array.index == i].sum().sum()
        if temp_array == 0:
            array = array.drop(i)
            if months_array.Sunday[i - 1] == months_array.Sunday[i + 1]:
                array = array.drop(i - 1)
        elif months_array.Sunday[i] == months_array.Sunday[i + 1]:
            array = array.drop(i)
        i += 1
    # Clean the array up further by resetting the index numbers and renaming them to "week_number"
    array = array.reset_index()
    array = array.drop(columns='index')
    array.index.name = 'week_number'
    return array

def create_calendar(year, start_day='mon'):
    '''Iterates over a year_array, inserting the month into each day of the year'''
    array = year_array(year, start_day)
    year = []
    if start_day == 'sun':
        for i in range(53):
            day_1 = array[array.index == i].Sunday[i]
            day_2 = array[array.index == i].Monday[i]
            day_3 = array[array.index == i].Tuesday[i]
            day_4 = array[array.index == i].Wednesday[i]
            day_5 = array[array.index == i].Thursday[i]
            day_6 = array[array.index == i].Friday[i]
            day_7 = array[array.index == i].Saturday[i]
            week = [day_1, day_2, day_3, day_4, day_5, day_6, day_7]
            year.append(week)
            i += 1
    else:
        for i in range(53):
            day_1 = array[array.index == i].Monday[i]
            day_2 = array[array.index == i].Tuesday[i]
            day_3 = array[array.index == i].Wednesday[i]
            day_4 = array[array.index == i].Thursday[i]
            day_5 = array[array.index == i].Friday[i]
            day_6 = array[array.index == i].Saturday[i]
            day_7 = array[array.index == i].Sunday[i]
            week = [day_1, day_2, day_3, day_4, day_5, day_6, day_7]
            year.append(week)
            i += 1
    new_year = []
    i = 0
    for week in year:
        new_week = []
        for day in week:
            if (i == 0) and (day > 1):
                month = 12
                i = 1
            elif (i == 0) and (day == 1):
                month = 1
                i = 1
            else:
                if (month == 12) and (day == 1):
                    month = 1
                elif (month != 12) and (day == 1):
                    month += 1
            month_num = month
            day_num = day
            if (day_num > 0) and (day_num < 10):
                day_num = '0' + str(day_num)
            if (month_num > 0) and (month_num < 10):
                month_num = '0' + str(month_num)
            date = str(f'{month_num}/{day_num}')
            new_week.append(date)
        new_year.append(new_week)
    new_year = pd.DataFrame(new_year)
    if start_day == 'sun':
        new_year.columns = ['Sunday', 'Monday', 'Tuesday',
                            'Wednesday', 'Thursday', 'Friday', 'Saturday']
    else:
        new_year.columns = ['Monday', 'Tuesday', 'Wednesday',
                            'Thursday', 'Friday', 'Saturday', 'Sunday']
    new_year.index.name = 'week_number'
    return new_year

def create_week(year_df, week, start_day='mon'):
    '''Creates a calendar week that starts on either Monday or Sunday.'''
    dataframe = year_df
    if start_day == 'sun':
        day_1 = dataframe[dataframe.index == week].Sunday[week]
        day_2 = dataframe[dataframe.index == week].Monday[week]
        day_3 = dataframe[dataframe.index == week].Tuesday[week]
        day_4 = dataframe[dataframe.index == week].Wednesday[week]
        day_5 = dataframe[dataframe.index == week].Thursday[week]
        day_6 = dataframe[dataframe.index == week].Friday[week]
        day_7 = dataframe[dataframe.index == week].Saturday[week]
    else:
        day_1 = dataframe[dataframe.index == week].Monday[week]
        day_2 = dataframe[dataframe.index == week].Tuesday[week]
        day_3 = dataframe[dataframe.index == week].Wednesday[week]
        day_4 = dataframe[dataframe.index == week].Thursday[week]
        day_5 = dataframe[dataframe.index == week].Friday[week]
        day_6 = dataframe[dataframe.index == week].Saturday[week]
        day_7 = dataframe[dataframe.index == week].Sunday[week]
    week_array = [day_1, day_2, day_3, day_4, day_5, day_6, day_7]
    return week_array

def create_schedule(year, week_number=0, start_day='mon'):
    '''Creates a weekly schedule, with dates and days.'''
    global YEAR_MON, YEAR_SUN
    YEAR_MON = create_calendar(year)
    YEAR_SUN = create_calendar(year, start_day='sun')
    if start_day == 'sun':
        calendar = create_calendar(year, start_day='sun')
        week = create_week(calendar, week_number, start_day='sun')
        week_labels = ['Sunday', 'Monday', 'Tuesday', 'Wednesday',
             'Thursday', 'Friday', 'Saturday']
    else:
        calendar = create_calendar(year)
        week = create_week(calendar, week_number)
        week_labels = ['Monday', 'Tuesday', 'Wednesday',
             'Thursday', 'Friday', 'Saturday', 'Sunday']
    week_df = np.zeros((7, 10), dtype=np.object_)
    week_df[0][0] = ''
    week_df[0][1] = 'Date:'
    week_df[0][2:-1] = week
    week_df[0][-1] = ''
    week_df[1][0] = ''
    week_df[1][1] = 'Store Hours:'
    week_df[1][2:-1] = ''
    week_df[1][-1] = ''
    week_df[2][0] = ''
    week_df[2][1] = 'Sales Forecast:'
    week_df[2][2:-1] = ''
    week_df[2][-1] = ''
    week_df[3][0] = ''
    week_df[3][1] = 'Forecasted Hours:'
    week_df[3][2:-1] = ''
    week_df[3][-1] = ''
    week_df[4][0] = ''
    week_df[4][1] = 'Scheduled Hours:'
    week_df[4][2:-1] = ''
    week_df[4][-1] = ''
    week_df[5] = ''
    week_df[6][0] = 'Position'
    week_df[6][1] = 'Employee Name'
    week_df[6][2:-1] = week_labels
    week_df[6][-1] = 'Total Hours'
    # Fill in the schedule with the employees and their job positions
    employee_list = pd.read_excel(EMPLOYEES_FILE, sheet_name='employee_list')
    i = 7
    # Iterate over each row
    for _, row in employee_list.iterrows():
        new_row = ['', '', '', '', '', '', '', '', '', '']
        week_df = np.vstack([week_df, new_row])
        employee_row = [row.Position, row.First_Name + ' ' + row.Last_Name]
        week_df[i][0] = employee_row[0]
        week_df[i][1] = employee_row[1]
        i += 1
    week_df = pd.DataFrame(week_df)
    week_df.columns = ['A', 'B', 'Day_1', 'Day_2', 'Day_3',
                       'Day_4', 'Day_5', 'Day_6', 'Day_7', 'Total']
    return week_df

def convert_times(dataframe, c_type='datetime'):
    '''Converts a DataFrame to/from a datetime64/string data type.'''
    dataframe_2 = dataframe.copy()
    if c_type == 'string':
        open_times = []
        close_times = []
        for row in dataframe_2.Open:
            row = row.time()
            hour = row.strftime('%H')
            minute = row.strftime('%M')
            time = f'{hour}:{minute}'
            open_times.append(time)
        dataframe_2['Open'] = open_times
        for row in dataframe_2.Close:
            row = row.time()
            hour = row.strftime('%H')
            minute = row.strftime('%M')
            time = f'{hour}:{minute}'
            close_times.append(time)
        dataframe_2['Close'] = close_times
    else:
        dataframe_2['Open'] = pd.to_datetime(dataframe_2['Open'].astype(str))
        dataframe_2['Close'] = pd.to_datetime(dataframe_2['Close'].astype(str))
    return dataframe_2

def convert_am_pm(time):
    '''Converts the time from 24-hours to 12-hours.'''
    hour = int(str(time).split(':', maxsplit=1)[0])
    minute = str(time).split(':')[1]
    if hour >= 12:
        period = 'PM'
        if hour > 12:
            hour = hour - 12
    else:
        period = 'AM'
    hour = str(hour)
    time = f'{hour}:{minute} {period}'
    return time

def holiday_check(date):
    '''Checks if the date is a holiday.'''
    if isinstance(date, pd.Timestamp):
        if len(HOLIDAY_HOURS[HOLIDAY_HOURS.Date == date]) == 0:
            holiday = False
        else:
            holiday = True
    elif isinstance(date, str):
        month = int(date.split('/')[0])
        day = int(date.split('/')[1])
        md_id = str(month) + str(day)
        if len(HOLIDAY_HOURS[HOLIDAY_HOURS.md_id == md_id]) >= 1:
            holiday = True
        else:
            holiday = False
    else:
        holiday = False
    return holiday

def populate_store_hours(dataframe, period=24):
    '''Populates the store hours for a given schedule.'''
    schedule = dataframe.copy()
    hours = []
    # Find the store hours
    date_1 = schedule.iloc[0][2]
    date_2 = schedule.iloc[0][3]
    date_3 = schedule.iloc[0][4]
    date_4 = schedule.iloc[0][5]
    date_5 = schedule.iloc[0][6]
    date_6 = schedule.iloc[0][7]
    date_7 = schedule.iloc[0][8]
    total = schedule.iloc[1][9]
    day_1 = schedule.iloc[6][2]
    day_2 = schedule.iloc[6][3]
    day_3 = schedule.iloc[6][4]
    day_4 = schedule.iloc[6][5]
    day_5 = schedule.iloc[6][6]
    day_6 = schedule.iloc[6][7]
    day_7 = schedule.iloc[6][8]
    dates = [date_1, date_2, date_3, date_4, date_5, date_6, date_7]
    days = [day_1, day_2, day_3, day_4, day_5, day_6, day_7]
    store_hours_2 = convert_times(STORE_HOURS, 'string')
    total = 0
    i = 0
    for _ in days:
        date = dates[i]
        holiday = holiday_check(date)
        if holiday is False:
            if schedule.iloc[6][2] == 'Sunday':
                if i == 0:
                    store_open = store_hours_2.Open.iloc[6]
                    store_close = store_hours_2.Close.iloc[6]
                elif i == 1:
                    store_open = store_hours_2.Open.iloc[0]
                    store_close = store_hours_2.Close.iloc[0]
                elif i == 2:
                    store_open = store_hours_2.Open.iloc[1]
                    store_close = store_hours_2.Close.iloc[1]
                elif i == 3:
                    store_open = store_hours_2.Open.iloc[2]
                    store_close = store_hours_2.Close.iloc[2]
                elif i == 4:
                    store_open = store_hours_2.Open.iloc[3]
                    store_close = store_hours_2.Close.iloc[3]
                elif i == 5:
                    store_open = store_hours_2.Open.iloc[4]
                    store_close = store_hours_2.Close.iloc[4]
                elif i == 6:
                    store_open = store_hours_2.Open.iloc[5]
                    store_close = store_hours_2.Close.iloc[5]
            else:
                store_open = store_hours_2.Open.iloc[i]
                store_close = store_hours_2.Close.iloc[i]
            if period == 12:
                store_open = convert_am_pm(store_open)
                store_close = convert_am_pm(store_close)
            store_hours = store_open + ' - ' + store_close
            m_1 = (int(str(pd.to_datetime(STORE_HOURS.Close.iloc[i]) - pd.to_datetime(
                STORE_HOURS.Open.iloc[i])).split()[-1].split(':')[0]) * 60)
            m_2 = int(str(pd.to_datetime(STORE_HOURS.Close.iloc[i]) - pd.to_datetime(
                STORE_HOURS.Open.iloc[i])).split()[-1].split(':')[1])
            m_total = m_1 + m_2
        else:
            month_num = int(date.split('/')[0])
            day_num = int(date.split('/')[1])
            md_id = str(month_num) + str(day_num)
            pos = HOLIDAY_HOURS[(HOLIDAY_HOURS.md_id == md_id)].index[0]
            if HOLIDAY_HOURS.Open.isna().iloc[pos] is True:
                store_hours = 'CLOSED'
                m_total = 0
            else:
                store_open = str(HOLIDAY_HOURS.Open.iloc[pos]).split()[-1]
                store_close = str(HOLIDAY_HOURS.Close.iloc[pos]).split()[-1]
                store_open = store_open.split(':')[0:2]
                store_open = store_open[0] + ':' + store_open[1]
                store_close = store_close.split(':')[0:2]
                store_close = store_close[0] + ':' + store_close[1]
                if period == 12:
                    store_open = convert_am_pm(store_open)
                    store_close = convert_am_pm(store_close)
                store_hours = store_open + ' - ' + store_close
                m_1 = (int(str(pd.to_datetime(store_close) -
                       pd.to_datetime(store_open)).split()[-1].split(':')[0]) * 60)
                m_2 = int(str(pd.to_datetime(store_close) -
                          pd.to_datetime(store_open)).split()[-1].split(':')[1])
                m_total = m_1 + m_2
        hours.append(store_hours)
        total += m_total
        i += 1
    hours.append(total / 60)
    schedule.iloc[1][2:] = hours
    return schedule

def initialize():
    '''Initializes the file path locations'''
    global SCHEDULES_DIRECTORY, EMPLOYEES_FILE, STORE_FILE, STORE_HOURS, HOLIDAY_HOURS
    working_directory = str(pathlib.Path( __file__ ).parent.absolute())
    work_schedule_directory = pathlib.PurePath(
        working_directory, 'work_schedule')
    SCHEDULES_DIRECTORY = pathlib.PurePath(
        work_schedule_directory, 'schedules')
    employees_directory = pathlib.PurePath(
        work_schedule_directory, 'employees')
    store_directory = pathlib.PurePath(work_schedule_directory, 'store')
    EMPLOYEES_FILE = pathlib.PurePath(employees_directory, 'Employees.xlsx')
    STORE_FILE = pathlib.PurePath(store_directory, 'Store.xlsx')
    STORE_HOURS = pd.read_excel(STORE_FILE, sheet_name='store_hours')
    HOLIDAY_HOURS = pd.read_excel(
        STORE_FILE, sheet_name='holiday_hours', na_values=None)
    STORE_HOURS = convert_times(STORE_HOURS)
    HOLIDAY_HOURS = convert_times(HOLIDAY_HOURS)
    md_ids = []
    for _ in HOLIDAY_HOURS.Date:
        month = _.month
        day = _.day
        md_id = str(month) + str(day)
        md_ids.append(md_id)
    HOLIDAY_HOURS['md_id'] = md_ids
    return None

def save_schedules(year, week_num_start, week_num_end, start_day='mon', period=24):
    '''Saves the schedules to Excel files in the Schedules folder.'''
    global CURRENT_VALUE, PROGRESS, OUTPUT
    w_range = (week_num_end - week_num_start) + 1
    prog_val = 53 / w_range
    CURRENT_VALUE = prog_val
    week = week_num_start
    num = week_num_start
    for _ in range(w_range):
        schedule = create_schedule(year, week_number=week_num_start - 1, start_day=start_day)
        if period == 12:
            schedule = populate_store_hours(schedule, period=12)
        else:
            schedule = populate_store_hours(schedule)
        if num <= 9:
            schedule_num = '0' + str(num)
        else:
            schedule_num = num
        schedule_name = 'schedule_' + str(schedule_num) + '.xlsx'
        schedule_file = pathlib.PurePath(SCHEDULES_DIRECTORY, schedule_name)
        with pd.ExcelWriter(schedule_file, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
            schedule.to_excel(writer, sheet_name='schedule', index=False)
        week += 1
        num += 1
        CURRENT_VALUE += prog_val
        path_parts = str(schedule_file).split('\\')[-3:]
        delimiter = '\\'
        file_path = delimiter.join(path_parts)
        OUTPUT.update(f'Saving...\n\n...\{file_path}')
        PROGRESS.update(CURRENT_VALUE)
        if _ == (w_range - 1):
            CURRENT_VALUE = 53
            PROGRESS.update(CURRENT_VALUE)
    return None

def main():
    '''Primary program functionality.'''
    global PROGRESS, CURRENT_VALUE, OUTPUT
    current_year = datetime.now().year
    initialize()
    sg.theme('Green')
    sg.set_options(element_padding=(0, 4))
    layout = [
        [sg.Text('Year:'),
        sg.In(
            default_text=current_year,
            size=(5, 1),
            key='year',
            do_not_clear=True,
            pad=((3, 0), 0))],
        [sg.Text('Week Start:'),
        sg.In(
            default_text='1',
            size=(3, 1),
            key='week_start',
            do_not_clear=True,
            pad=((3, 0), 0))],
        [sg.Text('Week End:'),
        sg.In(
            default_text='53',
            size=(3, 1),
            key='week_end',
            do_not_clear=True,
            pad=((3, 0), 0))],
        [sg.Text('Time Period:', pad=((3, 0), 0)),
        sg.OptionMenu(
            values=('12-hour Format', '24-hour Format'),
            default_value='12-hour Format',
            key='time_period',
            size=(13, 1))],
        [sg.Text('First Day of Week:', pad=((3, 0), 0)),
        sg.OptionMenu(
            values=('Monday', 'Sunday'),
            default_value='Monday',
            key='start_day',
            size=(13, 1))],
        [sg.Button('Create Schedule(s)', size=(15, 1))],
        [sg.Multiline(
            size=(40, 3),
            key='output',
            no_scrollbar=True,
            autoscroll=True,
            do_not_clear=True)],
        [sg.ProgressBar(max_value=53, orientation='h', size=(26, 20), key='progress_1')],
        [sg.Text(f'\n\nVersion: {__version__}', size=(35, 3), justification='r')]]

    window = sg.Window("Employee Scheduler", layout,
                       default_element_size=(15, 1),
                       text_justification='r',
                       auto_size_text=False,
                       auto_size_buttons=False,
                       default_button_element_size=(12, 1),
                       finalize=True)
    OUTPUT = window['output']
    PROGRESS = window['progress_1']
    current_value = 0
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        elif event == 'Create Schedule(s)':
            try:
                if values['year'] == '':
                    raise ValueError('\n[Year] cannot be blank.')
                year = int(values['year'])
                week_start = int(values['week_start'])
                week_end = int(values['week_end'])
                time_period = values['time_period']
                start_day = values['start_day']
                if (week_start < 1) or (week_start > 53):
                    raise ValueError(
                        '\n[Week Start] must be a value between 1 and 53.'
                    )
                if (week_end < 1) or (week_end > 53):
                    raise ValueError(
                        '\n[Week End] must be a value between 1 and 53.'
                    )
                if week_start > week_end:
                    raise ValueError(
                        '\n[Week Start] value must be less than or equal to [Week End] value.'
                    )
                if time_period == '12-hour Format':
                    time_period = 12
                if time_period == '24-hour Format':
                    time_period = 24
                if start_day == 'Monday':
                    start_day = 'mon'
                if start_day == 'Sunday':
                    start_day = 'sun'
                current_value = 0
                PROGRESS.update(current_value)
                save_schedules(
                    year,
                    week_num_start=week_start,
                    week_num_end=week_end,
                    start_day=start_day,
                    period=time_period)
                sg.popup('All schedules were\nsuccessfully saved!')
            except ValueError as excpt:
                sg.popup(f'Invalid Input Error\n{excpt}')
    window.close()

if __name__ == '__main__':
    main()