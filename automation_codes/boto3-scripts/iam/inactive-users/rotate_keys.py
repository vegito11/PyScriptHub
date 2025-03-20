import boto3
import json
from datetime import datetime, timezone
import csv
import datetime as dt
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart


AWS_REGION_NAME = "us-east-2"
sess = boto3.Session(region_name=AWS_REGION_NAME, profile_name="terra")
from_email = "vegito@test.com"
# sess = boto3.Session(region_name=AWS_REGION_NAME)

skip_users = ["terrauser", "devops", "john.doe"]
iam_client = boto3.client("iam")
ses_client = boto3.client("ses")

ROTATION_PERIOD = "30"

def send_email_to_user(to_email, filepath):

	message = MIMEMultipart()
	message['Subject'] = 'New AWS CLI Creds'
	message['From'] = from_email
	message['To'] = ', '.join([to_email, 'recipient2@domain.com'])
	
	# message body
	part = MIMEText(f'Your Access Key has been changed due to it was created {ROTATION_PERIOD}+ days ago ', 'html')
	message.attach(part)

	part = MIMEApplication(open(filepath, 'rb').read())
	part.add_header('Content-Disposition', 'attachment', filename=f'{to_email}.csv')
	message.attach(part)
	
	response = ses_client.send_raw_email(
	
		Source=message['From'],
		Destinations=[to_email, 'recipient2@domain.com'],
		RawMessage={
	    	'Data': message.as_string()
		}
	)


def save_row_to_csv(access_keys, secret_id, file_path="credentials.csv"):

    data = [
        {"username": access_keys, "password": secret_id},
    ]

    with open(file_path, 'w', newline='') as file:
        
        writer = csv.DictWriter(file, fieldnames=["username", "password"])

        writer.writeheader()

        for row in data:
            writer.writerow(row)

def get_user_email(uname, keyname="TEAM"):

	tags = iam_client.list_user_tags(UserName=uname).get("Tags")

	for tag in tags:
		if tag.get("Key") == keyname:
			email = tag.get("Value")
			print(f" \t\t User email is {email}")
			return email

def get_inactive_days(in_date):
	
	in_date_utc = in_date.replace(tzinfo=timezone.utc)
		
	if not in_date or type(in_date) == int:
		return -1
	else:	
		epoch_diff = int(datetime.now(timezone.utc).timestamp()) - int(in_date_utc.timestamp())
		# epoch_diff = int(datetime.utcnow().strftime("%s")) - int(in_date.strftime("%s"))
		days = epoch_diff // 86400
		return days

def rotate_access_key(key_metadata):
	
	# return
	uname = key_metadata.get("UserName")
	creation_time = key_metadata.get("CreateDate")
	keyid = key_metadata.get("AccessKeyId")

	print(f"\t Rotating {uname} user key - {keyid} ")
	
	if uname in skip_users:
		print(f" \t\t Skipping roation due to {uname} user is whitelisted")
		return

	if key_metadata.get("Status") == "Active":
		
		creation_days = get_inactive_days(creation_time)
		
		## 1) Verifying if User Key >= Rotation Period 
		# if creation_days >= int(ROTATION_PERIOD):
		if creation_days <= int(ROTATION_PERIOD): ### comment this and uncomment above!!!
			
			## 2) Inactivating User Key
			inactive_rep = iam_client.update_access_key(UserName=uname, 
				AccessKeyId=keyid, Status='Inactive')
			if str(inactive_rep["ResponseMetadata"]["HTTPStatusCode"]) == "200":
				print(f" \t\t !!! Deactivated {keyid} as it created {creation_days} days ago  !!!!")
			else:
				print(f" \t\t !!! Failed to Deactivated access key {keyid} for user {uname} !!!! ")
				return

			## 3) Deleting User Key
			delete_key_resp = iam_client.delete_access_key(UserName=uname, AccessKeyId=keyid)
			if str(delete_key_resp["ResponseMetadata"]["HTTPStatusCode"]) == "200":
				print(f" \t\t Deleted access key {keyid} for user {uname} !!!! ")
			else:
				print(f" \t\t !!! Failed to Delete access key {keyid} for user {uname} !!!! ")
				return

			## 4) Creating New Access key
			print(f" \t\t Creating new access key for {uname} ....")
			create_key_resp = iam_client.create_access_key(UserName=uname)
			
			if str(create_key_resp["ResponseMetadata"]["HTTPStatusCode"]) == "200":
				
				new_access_key = create_key_resp["AccessKey"]["AccessKeyId"]
				new_secret_key = create_key_resp["AccessKey"]["SecretAccessKey"]

				to_email = get_user_email(uname)
				save_row_to_csv(new_access_key, new_secret_key, f"/tmp/{to_email}.csv")
				send_email_to_user(to_email, f"/tmp/{to_email}.csv")

				
			else:
				print(f" \t\t !!! Failed to Create new access key {keyid} for user {uname} !!!! ")
				return
			
		else:
			print(f" \t\t Skipping rotation as key is just {creation_days} days old ")

	else:
		print(f" \t\t Skipping roation due to {keyid} for {uname} user is alrady Inactive")

def check_users():

	users = iam_client.list_users()

	for user in users.get("Users"):

		username = user.get("UserName")
		access_keys = iam_client.list_access_keys(UserName="chandrakant.khadse")
		# access_keys = iam_client.list_access_keys(UserName=username)
		num_acc_keys = len(access_keys.get("AccessKeyMetadata"))

		
		if num_acc_keys == 1:
			
			key1 = access_keys.get('AccessKeyMetadata')[0]
			rotate_access_key(key1)
		
		if num_acc_keys == 2:
			
			key1 = access_keys.get('AccessKeyMetadata')[0]
			key2 = access_keys.get('AccessKeyMetadata')[1]
			
			rotate_access_key(key1)
			rotate_access_key(key2)
		
		print("----------------------------------------------------")
		break

# check_users()