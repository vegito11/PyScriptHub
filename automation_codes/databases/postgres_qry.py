import random
import string
import psycopg2

def get_random_pass():
	
	characters = string.digits + "#%$^@_-" + string.ascii_letters
	password = ''.join(random.choice(characters) for i in range(12))

	return password

# print(get_random_pass())

def get_conn():
	
	username = "vegito"
	password = "XXXXX"
	dbname = "shopkart"
	endpoint = "localhost"
	port = "33060"
	# port = "35432"

	conn = psycopg2.connect(database=dbname, host=endpoint, user=username, password=password, port=port)
	# print(help(psycopg2.connect))
	print(conn)

get_conn()

# ALTER USER readonly WITH PASSWORD 'wvEk%q8n58OA';
# CREATE USER readonly WITH PASSWORD 'wvEk%q8n58OA';


##-------------------------------------------------------------###

from datetime import datetime
import pytz


def get_ist_date(dt_str):

	dt_obj = datetime.strptime(dt_str.strip(), "%Y-%m-%d %H:%M:%S,%f")
	ist = pytz.timezone('Asia/Kolkata')
	ist_dt_obj = ist.localize(dt_obj)

	return ist_dt_obj.strftime("%Y-%m-%d %H:%M:%S")

def utc_to_ist(utc_time_string):
	
	# Define the UTC timezone
	utc_timezone = pytz.timezone('UTC')

	# Define the IST timezone
	ist_timezone = pytz.timezone('Asia/Kolkata')

	# Convert the input UTC time string to a datetime object
	utc_datetime = datetime.strptime(utc_time_string, '%Y-%m-%d %H:%M:%S,%f')

	# Set the timezone of the datetime object to UTC
	utc_datetime = utc_timezone.localize(utc_datetime)

	# Convert the datetime object to IST timezone
	ist_datetime = utc_datetime.astimezone(ist_timezone)

	# Format the IST datetime string
	ist_time_string = ist_datetime.strftime('%Y-%m-%d %H:%M:%S')	
	return ist_time_string