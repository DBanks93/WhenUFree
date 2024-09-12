import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DB_USERNAME = 'root' #os.getenv('DB_USERNAME')
    DB_PASSWORD = 'kyzgax-wobgok' #os.getenv('DB_PASSWORD')
    DB_HOST = os.getenv('DB_HOST', 'localhost')

class Timetable:
    DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    TIMES = [f"{hour}:00" for hour in range(9, 19)]