import datetime
import openpyxl

def Read_timetable(room_num, sec, subj_code):
    current_day = current_datetime.strftime('%A')

current_datetime = datetime.datetime.now()

# Extract date, time, and day from the current datetime
current_date = current_datetime.date()
current_time = current_datetime.time()
  # %A gives the full weekday name (e.g., Monday, Tuesday)

# Print the results
print("Current Date:", current_date)
print("Current Time:", current_time)
print("Current Day:", current_day)

