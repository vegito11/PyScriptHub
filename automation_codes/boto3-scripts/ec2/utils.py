import json
import os
import logging
import boto3

import sys
sys.path.append("libs")
import requests
#### ----- global vars
skip_ids = ["ii-0123454324"]
skip_ips = ["192.0.0.100", "192.0.0.11"]
skip_name = ["worker-1"]
skip_tags = [{"environment": ["production"]}]

AWS_REGION_NAME = "ap-south-1"

# sess = boto3.Session(region_name=AWS_REGION_NAME, profile_name="terra")
# SLACK_CHANNEL = "#testing-alerts"

sess = boto3.Session(region_name=AWS_REGION_NAME)
SLACK_CHANNEL = "#k8s-nonprod-alerts"


#### ----- logger
logger = logging.getLogger("lambda_logger")
logger.setLevel(logging.INFO)
formatter = '[%(levelname)s] [%(asctime)s] %(lineno)d - %(message)s'
logging.basicConfig(level=logging.INFO, format=formatter)

def get_bot_token(srt_id="slack_bot_token"):
    
    logger.debug("Getting slack bot token ")    
    client = sess.client("secretsmanager")
    response = client.get_secret_value(SecretId=srt_id)
    json_res = json.loads(response["SecretString"])
    return json_res["monitoring_bot_token"]

def send_slack_message(title, message, color="#B71C1C", receiver=None):

    SLACK_BOT_TOKEN = get_bot_token()
    headers = {
        "Content-type": "application/json",
        "Authorization": "Bearer "+ SLACK_BOT_TOKEN
    }

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
    
    try:
        response = requests.post(url, data=json.dumps(slack_data), headers=headers)
        if response.status_code != 200:
            raise Exception(response.status_code, response.text)
    except Exception as e:
        logger.exception(e) 

# ----- 3) should we skip vm

def is_skip_vm(vm):

    ip, vmid, tags = vm.get("PrivateIpAddress"), vm.get(
        "InstanceId"), vm.get("Tags")
    tags = {item["Key"].lower(): item["Value"].lower() for item in tags}

    # logger.debug(ip, vmid, tags.get("name"), tags)

    # If vmid, Name and IPS exists in skip return True
    if vmid in skip_tags or ip in skip_ips or tags.get("name") in skip_name:
        logger.debug(f'Skipping {vmid} - {tags.get("name")}')
        return True

    for item in skip_tags:
        for key, value in item.items():
            if tags.get(key) and tags.get(key) in value:
                logger.debug(f'Skipping {vmid} - {tags.get("name")} for {key} - {tags.get(key)} ')
                return True

    return False



def get_config_var(key, subkey=None):
    file_path = "config.json"
    with open(file_path) as f:
        data = json.load(f)
        value = data.get(key, {})

        if subkey:
            value = value.get(subkey)

    return value