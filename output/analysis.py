import numpy as np

def average_heartrate(df):
    """Returns the average heartrate across the month"""
    avg_hr = df["heartRate"].mean()
    return round(avg_hr)

def average_sleep_time(df):
    """Returns the average sleep time across the month"""
    avg_sleep_time = df["totalSleepTime"].mean()
    avg_sleep_hrs = int(avg_sleep_time // 60)
    avg_sleep_mins = round(avg_sleep_time % 60)
    return avg_sleep_hrs, avg_sleep_mins

def average_bedtime(df):
    """Returns the average bedtime across the month"""
    avg_start_time = df["start"].mean()
    avg_bedtime_hrs = int(avg_start_time // 60)
    avg_bedtime_mins = round(avg_start_time % 60)
    if len(str(avg_bedtime_mins)) == 1:
        avg_bedtime_mins = "0"+str(avg_bedtime_mins)
    return avg_bedtime_hrs, avg_bedtime_mins

def average_waketime(df):
    """Returns the average wake time across the month"""
    avg_wake_time = df["wakeTime"].mean()
    avg_wake_hrs = int(avg_wake_time // 60)
    avg_wake_mins = round(avg_wake_time % 60)
    return avg_wake_hrs, avg_wake_mins

def average_sleep_stages(df):
    """Returns the average times for each sleep stage across the month"""
    avg_deep_time = round(df["deepSleepTime"].mean())
    avg_shallow_time = round(df["shallowSleepTime"].mean())
    avg_rem_time = round(df["REMTime"].mean())
    avg_wake_time = round(df["wakeTime"].mean())
    return avg_deep_time, avg_rem_time, avg_shallow_time, avg_wake_time

def format_time(x, pos):
    total_minutes = int(x) % 1440
    hours, minutes = divmod(total_minutes, 60)
    return f"{hours:02d}:{minutes:02d}"

def sleep_bar_color(value, low_threshold=420, goal=480):
    if value < low_threshold:
        return "#d9534f"
    elif value < goal:
        return "#e8b04b"
    else:
        return "#4b8a6f"
    
def monthly_sleep_time(total_sleep_time):
    total = total_sleep_time.sum()
    total_hrs = total // 60
    total_mins = total % 60
    return total_hrs, total_mins

def sleep_dept(total_sleep_time):
    dept = total_sleep_time.sum() - 480 * len(total_sleep_time)
    dept_hrs = dept // 60
    dept_mins = dept % 60
    return dept_hrs, dept_mins
    
def hr_stats(heart_rate):
    """Returns the minimum and maximum heart rates recorded"""
    
    min_hr = min(heart_rate)
    max_hr = max(heart_rate)
    hr_std = round(np.std(heart_rate), 2)
    return min_hr, max_hr, hr_std