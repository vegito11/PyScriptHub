#!/bin/bash
BASE_PROFILE="qa"
MFA_PROFILE="qa_mfa"
MFA_DEVICE_ARN="arn:aws:iam::1234567899:mfa/poc"
DEFAULT_REGION="us-east-1"
DEFAULT_OUTPUT="json"
# DURATION=129600 ## 36 hours
DURATION=900  ## 15 min

function generate_session_token(){
	echo -e "\033[1;36m Generating new IAM STS Token \033[0m"
	read -r AWS_ACCESS_KEY_ID AWS_ACCESS_KEY AWS_SESSION_TOKEN EXPIRATION < <(aws sts get-session-token --serial-number $MFA_DEVICE_ARN --token-code $MFA_OTP \
		--profile $BASE_PROFILE \
		--duration $DURATION  \
		--output text \
		--query 'Credentials.*')
}

function update_sts_profile(){
	echo -e "\033[1;36m Setting up the MFA_PROFILE with name $MFA_PROFILE \033[0m"
	aws configure set aws_secret_access_key "$AWS_ACCESS_KEY" --profile $MFA_PROFILE
	aws configure set aws_session_token "$AWS_SESSION_TOKEN" --profile $MFA_PROFILE
	aws configure set aws_access_key_id "$AWS_ACCESS_KEY_ID" --profile $MFA_PROFILE
	aws configure set expiration "$EXPIRATION" --profile $MFA_PROFILE
	aws configure set region "$DEFAULT_REGION" --profile $MFA_PROFILE
	aws configure set output "$DEFAULT_OUTPUT" --profile $MFA_PROFILE
	echo -e "\033[1;32m STS token updated successfully !! \033[0m"
}

if [ ${#} -eq 0 ]; then
	echo -e "\033[1;31m Please provide OTP from MFA device as arg to script \033[0m"
else
	MFA_OTP=$1
	generate_session_token
	
	if [ $? -ne 0 ]; then
		echo -e "\033[1;31m Failed to generate SessionToken , Please verify the OTP or other configuration again \033[0m"
	else
		update_sts_profile
		# echo -e -e "$AWS_ACCESS_KEY -1- \n $AWS_SESSION_TOKEN -2- \n $EXPIRATION -3- \n $AWS_ACCESS_KEY_ID"
		echo -e "aws sts get-caller-identity --profile $MFA_PROFILE \033[0m"
	fi
fi


# aws configure --profile qa
# bash mfa_cli.sh <6 DIGIT OTP>
