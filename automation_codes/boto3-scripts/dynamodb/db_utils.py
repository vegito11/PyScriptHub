import boto3
import math
from botocore.exceptions import ClientError
data_list = [{'lei_number': 'qweqwerqwrqwedqwe', 'company_name': 'FIDELITY ADVISOR SERIES I - Fidelity Advisor Leveraged Company Stock Fund', 'native_language': '', 'legal_address_country': 'US', 'hq_address_country': 'US', 'legal_address': '245 SUMMER STREET,BOSTON,US-MA,2110', 'head_quarter_address': '245 Summer Street,Boston,US-MA,2210'}, 
     {'lei_number': asdasfqewrfqwe, 'company_name': "The Greater Morristown Young Men's Christian Association, Inc.", 'native_language': '', 'legal_address_country': 'US', 'hq_address_country': 'US', 'legal_address': '79 Horsehill Road,Cedar Knolls,US-NJ,07927-2003', 'head_quarter_address': '79 Horsehill Road,Cedar Knolls,US-NJ,07927-2003'}]


def get_dynamo_session():
	ddb = boto3.resource('dynamodb',
	                     endpoint_url='http://localhost:8000',
	                     region_name="dummy",
	                     aws_access_key_id="dummy",
	                     aws_secret_access_key="dummy")
	return ddb

dynamo_session = get_dynamo_session()

def create_table(table_name):
    db_client = get_dynamo_session()
    table = db_client.create_table(
		        TableName=table_name,
		        KeySchema=[
		            {
		                'AttributeName': 'lei_number',
		                'KeyType': 'HASH'  # Partition key
		            }
		        ],
		        AttributeDefinitions=[
		            {
		                'AttributeName': 'lei_number',
		                'AttributeType': 'S'
		            }
		        ],
		        ProvisionedThroughput={
		            'ReadCapacityUnits': 10,
		            'WriteCapacityUnits': 10
		        }
   			)

def insert_row_to_table(table_name, data):
	
	table = dynamo_session.Table(table_name)
	try:
		table.put_item(Item=row)
	except:
		print(" Unable to insert record in table" , table_name,"\n\n")
		print(e)
		return False
	return True

def batch_insert_to_table(table_name, data, batch_size=50):

	start, end = 0, batch_size  ## initialize start and end index for list
	batches = math.ceil(len(data) / 3)  ## 1-50 , 50-100 , 100-150 = 3 batches
	record_count, fail_count = 0, 0

	table = dynamo_session.Table(table_name)

	## iterate from 1, 2, 3, 4, 5 (batches)
	for round in range(1, batches+1):
		# initially data[0:50] next data[50:100]	
		current_chunk = data[start:end]
		
		##### Insert One Batch to Dynamodb #####
		with table.batch_writer() as batch:
			for record in current_chunk:
				try:
					batch.put_item(Item=record)
					record_count += 1  ## Increment if successfully inserted record
				except Exception as e:
					print(e)
					print("\n\n =========================== \n ")
					fail_count += 1
		#######################################

		## Update index for next iteration
		start = end  # start = 50, then 100
		end += batch_size  ## end = 100 then 150

	return record_count, True

def get_record(table_name, key, key_value):
    table = dynamo_session.Table(table_name)
    try:
        response = table.get_item(
            Key={
                key: key_value
            }
        )
    except ClientError as e:
        return {'message': e.response['Error']['Message']}, False
    else:
        if response.get('Item'):
            return response['Item'], True
        else:
            return {'message': 'No data for the given key'}, False

def get_records(table_name,):
	table = dynamo_session.Table(table_name)
	scan_response = table.scan(TableName=table_name)
	items = scan_response['Items']
	return items

def delete_table(table_name):
	try:
		table = dynamo_session.Table(table_name)
		table.delete()
	except Exception as e:
		return False
	return True

def main():
	# create_table()
	db = get_dynamo_session()
	print(db.tables)
	print("Hello")

if __name__ == '__main__':
	# TABLE_NAME = 'LeiTable'
	# batch_insert_to_table(TABLE_NAME,data_list, 3)
	# print(delete_table(TABLE_NAME))
	# print(create_table(TABLE_NAME))
	pass