import json
from db_utils import insert_row_to_table, get_record, get_records, create_table, batch_insert_to_table
import time
from LEILevelOne import LEILevelOne

TABLE_NAME = 'MyTabel'

def lambda_handler(event=None, context=None):
    
	ob = LEILevelOne("LEI-Data.xlsx", "excel")

	delete_table(TABLE_NAME)
	create_table(TABLE_NAME)
	start_time = time.time()
	insert_data_to_table(TABLE_NAME, ob.data_frame.to_dict(orient='records'))
	result = batch_insert_to_table(TABLE_NAME, ob.data_frame.head(10).to_dict(orient='records'))
	print(result)
	print("--- %s seconds ---" % (time.time() - start_time))
	
	ob.data_frame.to_excel("result.xlsx")
	print(ob.data_frame.count())
	print(get_records(TABLE_NAME))
	
	return {
	    'statusCode': 200,
	    'body': json.dumps('Hello from Lambda!')
	}

lambda_handler()