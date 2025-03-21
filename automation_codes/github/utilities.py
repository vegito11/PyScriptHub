import json
import os

def get_config_var(filepath, section, varname, envname=None):
	with open(filepath) as f:
		data = json.load(f)
		if data[section].get(varname):
			return data[section].get(varname)
		else:
			if envname:
				return os.getenv(envname.upper())
			else:	
				return os.getenv(f'{section}_{varname}'.upper())


secret_filepath = "../configs/secrets.json"
OWNER = get_config_var(secret_filepath, "github", "orgname")
WEBHOOK_TOKEN = get_config_var(secret_filepath, "github", "webhook_token")
base_api_url = "https://api.github.com/repos"
headers = {
	'Authorization': 'token ' + WEBHOOK_TOKEN,
	"Accept" : "application/vnd.github.v3+json"
}


if __name__ == '__main__':
	filename = "./configs/secrets.json"
	section = "jenkins"
	varname = "my"
	value = get_var(filename, section, varname)
	print(value)