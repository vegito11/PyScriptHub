import hmac
import hashlib
import base64
import boto3
import json

REGION="us-east-1"
session = boto3.Session(profile_name='dev', region_name=REGION)
client = session.client('cognito-idp')

# CLIENTSECRET="XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXx"
clientId = "XXXXXXXXXXXXXXXXXXXXXXXXXX"

CLIENTSECRET=""


# Function used to calculate SecretHash value for a given client
def getSecretHash(client_id, client_secret, username):
    if client_secret:
        key = bytes(client_secret, 'utf-8')
        message = bytes(f'{username}{client_id}', 'utf-8')
        return base64.b64encode(hmac.new(key, message, digestmod=hashlib.sha256).digest()).decode()
    else:
        return ""

def confirmUser(email, otp):

	response = client.confirm_sign_up(
		ClientId=clientId,
		# SecretHash=getSecretHash(clientId, CLIENTSECRET, email),
		Username=email,
	    ConfirmationCode=otp,
	    ForceAliasCreation=False,
	)
	print(json.dumps(response, indent=2))

def createUser(email, tenid):

	response = client.sign_up(
	    ClientId=clientId,
	    # SecretHash=getSecretHash(clientId, CLIENTSECRET, email),
	    Username=email,
	    Password='sdfdfg#t45asr32',
	    UserAttributes=[
	        {
	            'Name': 'custom:tenant_id',
	            'Value': tenid
	        },
	        {
	            'Name': 'email',
	            'Value': email
	        },
	    ]
	   )

	print(json.dumps(response, indent=2))

def deleteUser(poolId, email):
	response = client.admin_disable_user(
    	UserPoolId=poolId,
    	Username=email
	)
	response = client.admin_delete_user(
    	UserPoolId=poolId,
    	Username=email
	)

email = "vegito@shopkart.io"
createUser(email, "greenFresh")
# confirmUser(email, "510820")
# deleteUser("ap-south-1_6ZrHTlScM", email)

# createUser("vegito@gmail.com", "greenFresh")
# createUser("automation@shopkart.io", "greenFresh")