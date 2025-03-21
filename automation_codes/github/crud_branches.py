import json
import requests
from utilities import *


def create_branch(repo_name, new_brch, src_brch="main"):
	
	create_api_url = f"{base_api_url}/{OWNER}/{repo_name}/git/refs"
	get_api_url = f"{base_api_url}/{OWNER}/{repo_name}/branches/{src_brch}"
	
	headers["Accept"] = "application/vnd.github+json"

	response = requests.get(get_api_url, headers=headers, data=json.dumps({}))

	if str(response.status_code).startswith("2"):
		
		sha = response.json()["commit"]["sha"]
		
		payload = {
			"ref" : f"refs/heads/{new_brch}",
			"sha" : sha
		}

		## create new branch
		response = requests.post(create_api_url, headers=headers, data=json.dumps(payload))

def delete_branch(repo_name, brnch_nm):
	
	if brnch_nm == "main":
		return

	del_api_url = f"{base_api_url}/{OWNER}/{repo_name}/git/refs/heads/{brnch_nm}"
	
	headers["Accept"] = "application/vnd.github+json"

	## delete branch new branch
	response = requests.delete(del_api_url, headers=headers)

	if response.status_code in [200, 204]:
		print(f"Delete Branch protection for {br_nm}")
	else:
		print(response.status_code, " -- " , response.text)
		
def set_brh_prot_rule(repo_name, br_nm):
	
	## add branch protection
	prot_api_url = f"{base_api_url}/{OWNER}/{repo_name}/branches/{br_nm}/protection"
	payload = {
		"required_status_checks": {
		  "strict": True,
		  "contexts": []
		},
		"required_signatures": False,
		"restrictions": None,
		"enforce_admins": False,
		"required_pull_request_reviews": {
		  "dismiss_stale_reviews": False,
		  "require_code_owner_reviews": False,
		  "required_approving_review_count": 1,
		  "bypass_pull_request_allowances": {
		  	"users": ["akshaymhetre"]
		  }
		},
		"required_linear_history":False,
		"allow_force_pushes": False,
		"allow_deletions": False,
		"block_creations": False,
		"required_conversation_resolution": False
	}
	
	response = requests.put(prot_api_url, headers=headers, data=json.dumps(payload))

	if response.status_code == 200:
		print(f"Added Branch protection for {br_nm}")
	else:
		print(json.dumps(response.json(), indent=2))

def get_prot_rule(repo_name, br_nm):
	get_api_url = f"{base_api_url}/{OWNER}/{repo_name}/branches/{br_nm}/protection"
	response = requests.get(get_api_url, headers=headers, data=json.dumps({}))
	data = response.json()
	print(json.dumps(data, indent=2))

def remove_prot_rule(repo_name, br_nm):
	if br_nm == "main":
		return

	prot_api_url = f"{base_api_url}/{OWNER}/{repo_name}/branches/{br_nm}/protection"

	response = requests.delete(prot_api_url, headers=headers)

	if response.status_code == 200:
		print(f"Delete Branch protection for {br_nm}")
	else:
		# print(json.dumps(response.text, indent=2))
		print(response.text)

if __name__ == '__main__':
	pass
	# create_branch("sample_app", "develop", "alpha")
	# set_brh_prot_rule("sample_app", "develop")
	# get_prot_rule("sample_app", "main")
