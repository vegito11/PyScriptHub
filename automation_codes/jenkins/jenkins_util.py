import jenkins as jen
import json
import requests
from utilities import get_config_var

def get_conn():

	secret_filepath = "configs/secrets.json"
	url = get_config_var(secret_filepath, "jenkins", "url")
	username = get_config_var(secret_filepath, "jenkins", "username")
	password = get_config_var(secret_filepath, "jenkins", "password")

	server = jen.Jenkins(url, username=username, password=password)
	user = server.get_whoami()
	version = server.get_version()
	print('Hello %s from Jenkins %s' % (user['fullName'], version))
	return server

def get_api_session(ssl_verify=True, ssl_cert=None):
	
    secret_filepath = "../configs/secrets.json"
    url = get_config_var(secret_filepath, "jenkins", "url")
    username = get_config_var(secret_filepath, "jenkins", "username")
    password = get_config_var(secret_filepath, "jenkins", "password")

    # response = requests.post(url, auth = (username, password),verify=False)
    # if response.status_code != 200:
    # 	print(f" not able to connect to jenkins - {response.status_code} ")
    # 	return None, url

    session = get_session(username, password, ssl_verify, ssl_cert)

    crumb = session.get(url + '/crumbIssuer/api/xml?xpath=concat(//crumbRequestField,":",//crumb)')
	
    if crumb.status_code == 200:
        head = crumb.text.split(':')
        session.headers = {str(head[0]): str(head[1])}

    return session, url


def get_session(login, password, ssl_verify, ssl_cert, header=None):
    session 		= requests.Session()
    session.auth 	= (login, password)
    session.cert 	= ssl_cert
    session.verify 	= ssl_verify
    session.headers = header
    return session

# get_conn()

get_api_session()