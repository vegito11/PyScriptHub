import boto3, json
stg_sesstion = boto3.Session(profile_name='staging')
client = stg_sesstion.client('vpc')

def get_vpc_info(vpc_data):
	vpc_info = {}
	vpc_info['cidr'] = vpc_data["CidrBlock"]
	vpc_info['vpcid'] = vpc_data["VpcId"]
	for tag in vpc_data["Tags"]:
		if tag.get("Key").lower() == "name":
			vpc_info['vpc_name'] = tag.get("Value")
		if tag.get("Key").lower() == "environment":
			vpc_info['vpc_env'] = tag.get("Value")

		if tag.get("Key").lower() == "owner":
			vpc_info['vpc_owner'] = tag.get("Value")

	return vpc_info		

def get_subnet_within_vpc(vpc_id):
	vpc = ec2.Vpc(vpc_id)

def get_all_vpc():
	# all_vpc_response = ec2.describe_vpcs()
	# for vpc in all_vpc_response["Vpcs"]:
	# 	print(get_vpc_info(vpc))

	test_vpc = {'cidr': '13.0.0.0/16', 'vpcid': 'vpc-04baadb2896da7903', 'vpc_owner': 'terraform', 'vpc_env': 'staging', 'vpc_name': 'staging-vpc'}
	get_subnet_within_vpc(test_vpc['vpc_id'])


get_all_vpc()