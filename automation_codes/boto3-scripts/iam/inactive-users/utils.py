import boto3
import botocore
from botocore.exceptions import ClientError
import json
from datetime import datetime
from dateutil.tz import tzutc
import os
import requests

skip_password_user = [""]
skip_cli_user = [""]

CLI_INACTIVE_DAYS = os.getenv("CLI_INACTIVE_DAYS", 30)
PASSWORD_INACTIVE_DAYS = os.getenv("PASSWORD_INACTIVE_DAYS", 30)
ENV = os.getenv("ENV", "staging")
SLACK_CHANNEL = os.getenv("CHANNEL", "#devops-notification")

stg_sesstion = boto3.Session(profile_name='prod_mfa')
iam_client = stg_sesstion.client('iam')

##-------------------------------------- Slack Functions -------------------------------------
def get_bot_token(srt_id="slack_bot_token"):
	client = stg_sesstion.client("secretsmanager")
	response = client.get_secret_value(SecretId=srt_id)
	json_res = json.loads(response["SecretString"])
	return json_res["bot_token"]

def get_slack_member_ids():
        
    SLACK_BOT_TOEKN = get_bot_token() # xob-XXXXXXXXXXXXX
    headers = {
        "Content-type": "application/json",
        "Authorization": "Bearer "+ SLACK_BOT_TOEKN
    }

    member_ids = {}
    url = "https://slack.com/api/users.list"
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise Exception(response.status_code, response.text)

    else:
        response = response.json()
        if response["ok"] == True:
            for member in response["members"]:
                member_ids[member["name"]] = member["id"]

    # member_ids = {'slackbot': 'INTSD423', 'travis': 'INRROS3'}

    return member_ids	
	
def send_slack_message(title, message, color="#B71C1C", receiver=None):
	SLACK_BOT_TOEKN = get_bot_token()
	headers = {
	    "Content-type": "application/json",
	    "Authorization": "Bearer "+ SLACK_BOT_TOEKN
	}

	if receiver == None:
		receiver = SLACK_CHANNEL
	else:
		print(receiver)	
		receiver = "@UJFDN@)#"
	url = "https://slack.com/api/chat.postMessage"
	slack_data = {  
	                "channel": receiver,
	                "text": title,
	                "attachments": [
	                    {"text": message,
	                    "fallback":"..",
	                    "color": color,
	                }]
	            }
	print("Sending Slack Message to user "+ receiver)
	response = requests.post(url, data=json.dumps(slack_data), headers=headers)
	if response.status_code != 200:
	    raise Exception(response.status_code, response.text)

slack_member_ids = get_slack_member_ids()

def get_slack_uid(username):
	fname = username.split(".")[0]
	fullname = "".join(username.split("."))

	if slack_member_ids.get(username, None):
		return "@" + slack_member_ids.get(username, None)
	
	elif slack_member_ids.get(fname, None):
		return "@" + slack_member_ids.get(fname, None)
	
	elif slack_member_ids.get(fullname, None):
		return "@" + slack_member_ids.get(fullname, None)

	return SLACK_CHANNEL	

######-------------------------------------------- Delete Inactive Users ----------------------------------

def get_inactive_days(last_date):
	
	if not last_date or type(last_date) == int:
		return -1
	else:	
		epoch_diff = int(datetime.utcnow().strftime("%s")) - int(last_date.strftime("%s"))
		days = epoch_diff // 86400
		return days

#= 3) Deactivate aws cli key of user
def delete_inactive_key(user,acc_id):
	print(f" Deactivating {acc_id} access key of {user} ...")
	# response = client.update_access_key(UserName=user, AccessKeyId=acc_id, Status='Inactive')

def deactivate_cli_user(users, infrequent_users):
	"""
		users: {  "john.doe": "ACCESS_KEY", "jane.doe": "ACCESS_KEY" }
		infrequent_users: { "JeanDev": -1, "rio.nose": -1, "yatika.pandiya": -1 }
	"""
	for inactive_user, access_key_id in users.items():
		msg = f"""	Hi *{inactive_user}* :wave: , \n Your {ENV} AWS IAM *cli* credentials has been `expired` :no_entry: due to inactivity. \n Please contact the admin if you need aws acccess in future"""
		# print(msg)
		receiver = get_slack_uid(inactive_user)
		send_slack_message(":pushpin: *Inactive AWS CLI User :keyboard: * :pushpin: ", msg, receiver=receiver)
		
		delete_inactive_key(inactive_user, access_key_id)	

	for user,days in infrequent_users.items():
		msg = f""" Hi {user} :wave: , \n Your {ENV} AWS CLI credentials are going to `expire in {days} days` :hourglass: !!!. \n It will be `deleted` automatically if you don't login to aws console in `{days} days` ."""
		# print(msg)
		receiver = get_slack_uid(user)
		send_slack_message("*Infrequent AWS CLI User :keyboard: * :alarm_clock: ", msg, "#FFC107", receiver=receiver)

#= 2) Delete console password of user 
def delete_console_password_key(user):
	print(f" Deleting console password of {user}")
	# client.delete_login_profile(UserName=user)

def deactivate_console_user(users, infrequent_users):
	"""
		params: user => { "fname.lname": 187, "john.doe": 432 }
		params: infrequent_users => { "fname.lname": 35, "john.doe": 31 }
		
	"""

	for inactive_user, days in users.items():
		msg = f"Hi *{inactive_user}* :wave: , \n Your `{ENV}` aws console password has been `expired` :no_entry: due to inactivity. \n Please contact the admin if you need aws acccess in future"		
		# print(msg)
		receiver = get_slack_uid(inactive_user)
		send_slack_message(":red_circle: * :computer: Inactive Console User * :red_circle: ", msg, receiver=receiver)
		
		delete_console_password_key(inactive_user)

	for user, days in infrequent_users.items():
		msg = f"Hi {user} :wave: , \n Your `{ENV}` aws console password is going to expire in `{days} days` :hourglass: !!!. \n It will be `deleted automatically` if you don't login to aws console in {days} days ."
		# print(msg)
		receiver = get_slack_uid(user)
		send_slack_message("* :computer: Infrequent Console User* :alarm_clock: ", msg, receiver=receiver)

######-------------------------------------------- Get Inactive Users ----------------------------------

#### 1.3) filter inactive cli and console users
def get_inactive_cli_users(users):
	potential_inactive_cli_usr = {}
	cli_usr_to_inactivate = {}
	
	print(f"Getting All users who hasn't used there to CLI keys since {CLI_INACTIVE_DAYS} days ...")
	
	for user in users:

		if user in skip_cli_user:
			continue

		access_keys = iam_client.list_access_keys(UserName=user)
		for key in access_keys["AccessKeyMetadata"]:
			
			if key.get("Status") == "Inactive":
				continue
			else:
				last_used_date = iam_client.get_access_key_last_used(AccessKeyId=key["AccessKeyId"]).get("AccessKeyLastUsed").get("LastUsedDate")
				inactive_days = get_inactive_days(last_used_date)
				
				if inactive_days >= CLI_INACTIVE_DAYS:
					cli_usr_to_inactivate[user] = key["AccessKeyId"]
				
				elif inactive_days >= (CLI_INACTIVE_DAYS - 5) and  inactive_days < CLI_INACTIVE_DAYS or inactive_days == -1:
					potential_inactive_cli_usr[user] = (CLI_INACTIVE_DAYS - inactive_days)

	return cli_usr_to_inactivate, potential_inactive_cli_usr,

# 1.1)	
def get_inactive_console_users(users):
	
	inactive_user = {}
	infrequent_inactive_user = {}

	print(f"Getting All users who hasn't login to aws console since {PASSWORD_INACTIVE_DAYS} ...")

	for username, lastpass_use_date in users.items():
		
		if username in skip_password_user:
			continue

		inactive_days = get_inactive_days(lastpass_use_date)
		if inactive_days > PASSWORD_INACTIVE_DAYS:
			inactive_user[username] = inactive_days
		if inactive_days >= (PASSWORD_INACTIVE_DAYS - 5) and inactive_days <= PASSWORD_INACTIVE_DAYS:
			infrequent_inactive_user[username] = (PASSWORD_INACTIVE_DAYS - inactive_days)

	return inactive_user, infrequent_inactive_user

# 1.0) Get all users and there last password used date
def get_all_users():
	'''
		Get all users and there Last Password Used Date mapping
		{"user1": 13, "user2": 34}
	'''
	paginator = iam_client.get_paginator('list_users')
	all_users = {}
	print("Get All Users and there last used password date ....")
	# for page in paginator.paginate(PaginationConfig={'MaxItems': 2}):
	for page in paginator.paginate():
		for user in page["Users"]:
			if user.get("UserName") in skip_password_user:
				continue
			all_users[user.get("UserName")] = user.get("PasswordLastUsed", -1)

	return all_users

if __name__ == '__main__':

	pass