import pandas as pd
import base64
import os

def get_file_path(file_name):
	""" Get the file full path for LEI-Data.xlsx Excel file
	"""
	base_path = os.path.dirname(os.getcwd())
	file_path = os.path.join(base_path, file_name)
	return file_path

def clean_data(data_frame):
	""" Remove columns which do not have any values
	"""
	# data_frame.dropna(axis="columns", how="all", inplace=True)
	data_frame.fillna("", inplace=True)

def rename_cols(data_frame, rename_col_mapping):
	data_frame.rename(columns=rename_col_mapping, inplace=True)

def merge_region_country(region_country):
	region, country = region_country[0], region_country[1]
	if pd.isnull(region):
		region = ""
	if pd.isnull(country):
		country = ""
		
	result, region = "", str(region)	
	
	if country == "US":
		if len(region)>3 and region[2] == "-":
			result = ","+region
	elif region and not pd.isnull(region):
		if region[2] != "-":
			result = ","+region
			print(region,type(region))
		if country:
			result += ","+country

	return result	

def return_not_na_val(col_value, sep=","):
	col_value = col_value
	if pd.isnull(col_value) or not str(col_value):
		return ""
	else:
		return sep+str(col_value)

if __name__ == "__main__":
	insert_to_dynamodb()

