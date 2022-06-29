import pandas as pd


def moving_avg(input_arr, window_size=7):
    my_series = pd.Series(input_arr)
    windows = my_series.rolling(window_size)

    # Create a series of moving
    # averages of each window
    moving_averages = windows.mean()

    # Convert pandas series back to list
    moving_averages_list = moving_averages.tolist()

    # Remove null entries from the list
    final_list = moving_averages_list[window_size - 1:]

    return final_list
