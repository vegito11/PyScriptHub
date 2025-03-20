'''

aws cloudfront --update-distribution --distribution-id E11A56BU8CYDSF --paths '/blueprint/

Specifies the event type that triggers a Lambda@Edge function invocation. You can specify the following values:

viewer-request : The function executes when CloudFront receives a request from a viewer and before it checks to see whether the requested object is in the edge cache.
origin-request : The function executes only when CloudFront sends a request to your origin. When the requested object is in the edge cache, the function doesn't execute.
origin-response : The function executes after CloudFront receives a response from the origin and before it caches the object in the response. When the requested object is in the edge cache, the function doesn't execute.
viewer-response : The function executes before CloudFront returns the requested object to the viewer. The function executes regardless of whether the object was already in the edge cache. If the origin returns an HTTP status code other than HTTP 200 (OK), the function doesn't execute.
'''


import boto3
import json
import os

cf_client = boto3.client('cloudfront')

### -------------- Set Variables --------------------------------- ###
LAMBDA_FUNCTION_ARN = ''
MAINTAINS_ON = os.environ.get('MAINTAINS_ON', "no")
ENVIRONMENT = os.environ.get('ENVIRONMENT', "demo")

#### ------------ Operational function -------------------------- ###
def get_cfront_config(cfront_id):
	data = cf_client.get_distribution_config(Id=cfront_id)
	return data['ETag'], data['DistributionConfig']

def associate_lambda_function(payload, paths):
	'''
		This function Associate the the lambda function to given path of cloudfront distribution,
		Only if that path does not have any Lamdafunction associated with it and that path
		present in list provided by user
	'''
	for path in payload:
		need_to_update = False
		if path['LambdaFunctionAssociations']['Quantity'] == 0 and path['PathPattern'] in paths:
			print(f" {path['PathPattern']} will be updated ")
			need_to_update = True
			path['LambdaFunctionAssociations'] = {
				    "Quantity": 1,
				    "Items": [{
				        "LambdaFunctionARN": LAMBDA_FUNCTION_ARN,
				        "EventType": "viewer-request",
				        "IncludeBody": False
				    }]
			}

		else:
			print(f" {path['PathPattern']} path Will be ignored ")
	return need_to_update		
			
def remove_lambda_function(payload, paths):
	need_to_update = False
	for path in payload:
		if path['LambdaFunctionAssociations']['Quantity'] != 0 and path['PathPattern'] in paths:
			need_to_update = True
			print(f" Removing lamdba function from - {path['PathPattern']} - path  ")
			path['LambdaFunctionAssociations'] = { "Quantity": 0 }		
	return need_to_update		

def turn_on_maintenance_mode(cfront_distri_id, paths):
	
	etag, distr_conf = get_cfront_config(cfront_distri_id)
	items = distr_conf['CacheBehaviors']['Items']
	
	need_to_update = associate_lambda_function(items, paths)
	
	if need_to_update:
		print(f" Associating the lambda function to the {cfront_distri_id} distribution  ... ")
		response = cf_client.update_distribution(DistributionConfig=distr_conf, Id=cfront_distri_id,IfMatch=etag)
		print(f" Distribution Status : {response['Distribution']['Status']} - Last Modification Time {response['Distribution']['LastModifiedTime']} ")
		
	else:
		print(f"No Updation required for {cfront_distri_id} distribution --")	

def turn_off_maintenance_mode(cfront_distri_id, paths):
	print(cfront_distri_id, paths)
	etag, distr_conf = get_cfront_config(cfront_distri_id)
	items = distr_conf['CacheBehaviors']['Items']
	
	need_to_update = remove_lambda_function(items, paths)
	
	if need_to_update:
		print(f" !! Removing a lambda function from the {cfront_distri_id} distribution  ... ")
		response = cf_client.update_distribution(DistributionConfig=distr_conf, Id=cfront_distri_id, IfMatch=etag)
		print(f" Distribution Status : {response['Distribution']['Status']} - Last Modification Time {response['Distribution']['LastModifiedTime']} ")
	
	else:
		print(f"No Updation required for {cfront_distri_id} distribution --")

def do_operations(distro_map):

	if MAINTAINS_ON.lower() == "yes":
		print(" 🕓 each cloudfront Distro endpoint will be diverted to the maintenance page... 🕓")
		for cf_distro_id, paths in distro_map.items():
			
			print("++","--"*18,cf_distro_id,"--"*20,"++")
			turn_on_maintenance_mode(cf_distro_id, paths)

	else:
		print(" ⭐ Removing maintenance page redirection from each cloudfront Distro endpoint ... ⭐ ")
		for cf_distro_id, paths in distro_map.items():
			
			print("##","--"*18,cf_distro_id,"--"*18,"##")
			turn_off_maintenance_mode(cf_distro_id, paths)



def lambda_handler(event, context):
    
    staging_distro_map = { "SDUWRYASIFIS31": ['/login*', "/status*"], "9484NDWN21NDFN": ["/something"] } 
    print("On Main",MAINTAINS_ON)
    try:
        
        status = 200
        content = "Updated the given cloudfront distributions successfully"
        if ENVIRONMENT == "staging":
            do_operations(staging_distro_map)

        elif ENVIRONMENT == "production":
            # do_operations(prod_distro_map)
            pass
        else:
            print("Invalid Environment Name ")
        
    except Exception as e:
        status = 200
        content = "failed to update given cloudfront distributions"
        print(e)


    print("------------------ END -----------------------")

    # TODO implement
    return {
        'statusCode': status,
        'body': json.dumps(content)
    }
