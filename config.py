import os

class Config:
    DB_USERNAME = os.getenv('DB_USERNAME', 'root')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'kyzgax-wobgok')
    DB_HOST = os.getenv('DB_HOST', 'localhost')

class Timetable:
    DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    TIMES = [f"{hour}:00" for hour in range(9, 19)]