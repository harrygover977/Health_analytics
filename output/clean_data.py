import pandas as pd

def clean_data(hr_df, sleep_df):
    """Returns the cleaned and combined sleep and heart rate dataframe"""
    
    # Find the average heart rate for each day
    hr_df = hr_df["heartRate"].groupby(hr_df["date"])
    hr_df = hr_df.mean().astype(int)
    
    # remove the naps column
    sleep_df = sleep_df.drop(["naps"], axis=1)
    # remove the "+0000" from the start and stop columns 
    def strip_time(time):
        time = time.split(" ")[1].split("+")[0]
        return time
    sleep_df["start"] = sleep_df["start"].astype(str).apply(strip_time)
    sleep_df["stop"] = sleep_df["stop"].astype(str).apply(strip_time)
    # Turn the start and stop times into minutes after 00:00
    def time_to_minutes(time):
        hours = int(time.split(":")[0])
        minutes = int(time.split(":")[1])
        time = (hours * 60) + minutes
        return time 
    sleep_df["start"] = sleep_df["start"].apply(time_to_minutes)
    sleep_df["stop"] = sleep_df["stop"].apply(time_to_minutes)
    
    # merge the two dataframes
    combined_df = pd.merge(hr_df, sleep_df, on="date")
    # Format the date column as DD-MM-YYYY
    def reverse_date(date):
        date = date.split("-")
        reversed_date = []
        for i in range(len(date), 0, -1):
            reversed_date.append(date[i-1])
        reversed_date = "-".join(reversed_date)
        return reversed_date
    combined_df["date"] = combined_df["date"].astype(str).apply(reverse_date)
    # change dates into two digit integers
    def standardize_date(date):
        standard_date = date.split("-")[0]
        return standard_date
    combined_df["date"] = combined_df["date"].apply(standardize_date)
    # create a total sleep time column 
    combined_df["totalSleepTime"] = combined_df["deepSleepTime"].astype(int) + combined_df["shallowSleepTime"].astype(int) + combined_df["REMTime"].astype(int)
    # Remove any rows where the total sleep time was 0
    combined_df = combined_df[combined_df["totalSleepTime"] > 0]
    # remove any rows where start time is less that 1200
    combined_df = combined_df[combined_df["start"] > 1260]
    
    return combined_df
    
    
    