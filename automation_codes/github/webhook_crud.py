# https://docs.github.com/en/rest/webhooks/repo-config
import json
import requests
from utilities import *

def create_webhook(repo_name):
	webhook_url = f"{JENKINS_URL}/multibranch-webhook-trigger/invoke?token={JOB_TRIGGER_TOKEN}"
	hook_api_url = f"{base_api_url}/{OWNER}/{repo_name}/hooks"

	payload = {
	  "name": 'web',
	  "active": True,
	  "events": [
	    'push',
	    'create',
	    'delete',
	    'pull_request',
	  ],
	  "config": {
	    "url": webhook_url,
	    "content_type": 'json',
	    "insecure_ssl": '0'
	  }
	}

	response = requests.post(hook_api_url, headers=headers, data=json.dumps(payload))
	print(response.status_code)
	
	if response.json().get("errors", []):
		print("=============!!!!!!!!!!==============")
		print(json.dumps(response.json()["errors"], indent=2))
	else:
		print(json.dumps(response.json(), indent=2))

def delete_webhook(repo_name, old_jurl):
	
	hook_api_url = f"{base_api_url}/{OWNER}/{repo_name}/hooks"

	hook_data = get_webhook(repo_name, old_jurl)
	if hook_data:
		hook_id = hook_data["id"]
	
		delete_hook = requests.delete(f"{hook_api_url}/{hook_id}", headers=headers)
		if delete_hook.status_code == 204:
			print(f" Deleted the Hook {hook_id} !!")
		else:
			print(f"Failed to delete the hook - {hook_id} ")
			print(json.dumps(delete_hook.json(), indent=2))

def update_webhook(repo_name, old_jurl):
	webhook_url = f"{JENKINS_URL}/multibranch-webhook-trigger/invoke?token={JOB_TRIGGER_TOKEN}"
	hook_api_url = f"{base_api_url}/{OWNER}/{repo_name}/hooks"
		
	payload = {	
	  "config": {
	    "url": webhook_url,
	    "content_type": 'json',
	    "insecure_ssl": '0'
	  }
	}	

	hook_data = get_webhook(repo_name, old_jurl)

	if hook_data:
		hook_id = hook_data["id"]
		update_hook = requests.post(f"{hook_api_url}/{hook_id}", headers=headers, data=json.dumps(payload))
		if update_hook.status_code == 200:
			print(f" Updated the Hook {hook_id} !!")
		else:
			print(f"Failed to Update the hook {hook_id} - {update_hook.status_code}")
			print(json.dumps(update_hook.json(), indent=2))

def get_webhook(repo_name, old_jurl):

	hook_api_url = f"{base_api_url}/{OWNER}/{repo_name}/hooks"
	all_hooks = requests.get(hook_api_url, headers=headers)
	all_hooks_json = all_hooks.json()

	if str(all_hooks.status_code).startswith(old_jurl):
		print(all_hooks.json())
	else:
		for hook in all_hooks_json:
			if hook["config"]["url"].find(old_jurl) != -1 :
				hook_id = hook["id"]
				# print(json.dumps(hook, indent=2))
				return hook
	print(f"No Hook matched the {old_jurl}")		

secret_filepath = "/configs/secrets.json"
config_filepath = "/configs/vars.json"

JENKINS_URL = get_config_var(secret_filepath, "jenkins", "url")
JOB_TRIGGER_TOKEN = get_config_var(secret_filepath, "github", "trigger_token")

if __name__ == '__main__':
	
	repos = get_config_var(secret_filepath, "github", "code_repo_name")

	for repo in repos:
		print(repo)
		break
		# get_webhook(repo, "backend-service")
	create_webhook("client-dashboard")
	