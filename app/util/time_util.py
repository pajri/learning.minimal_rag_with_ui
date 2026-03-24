import datetime

def current_timestamp_str():
    current_time = datetime.datetime.now()
    timestamp_str = current_time.strftime("%Y%m%d_%H%M%S")
    return timestamp_str