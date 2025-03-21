import json
import random
import string
from utils.utilities import get_config_var
from permissions import Permissions
from roles import Roles, Users

def createRoles(role):

	for group in userdata:

		per = Permissions(group)

		perm_map = [
			per.get_job_permission(),
			per.get_cred_permission(),
			per.get_node_permission(),
			per.get_view_permission(),
			per.run_job_permission(),
			per.misc_job_permission()
		]

		grp_data = userdata[group]
		role.create_role(grp_data["rolename"], perm_map, "globalRoles")

		if group != "devops":
			role.create_role(grp_data["rolename"], perm_map, "projectRoles", grp_data["pattern"])

		print("-----" * 15)		

def deleteRoles(role):

	for group in userdata:
		role.delete_role(userdata[group]["rolename"], "globalRoles")
		role.delete_role(userdata[group]["rolename"], "projectRoles")

def MapRoles(role):

	for group in userdata:
		grp_data = userdata[group]
		for user in grp_data["users"]:
			username = grp_data["users"][user]["username"]
			role.assign_role_to_user(grp_data["rolename"], username, "globalRoles")
			role.assign_role_to_user(grp_data["rolename"], username, "projectRoles")
	
def RemoveMapping(role):

	for group in userdata:
		grp_data = userdata[group]
		for user in grp_data["users"]:
			username = grp_data["users"][user]["username"]
			role.remove_role_from_user(grp_data["rolename"], username, "globalRoles")
			role.remove_role_from_user(grp_data["rolename"], username, "projectRoles")

def get_random_pass():
	
	characters = string.digits + "#%$^@_-" + string.ascii_letters
	password = ''.join(random.choice(characters) for i in range(12))

	return password

def createUsers(user):
	
	for group in userdata:
		grp_data = userdata[group]
		for key, udata in grp_data["users"].items():
			passwd = get_random_pass()
			email = udata["email"]
			username = udata["username"]
			user.create_user(username, email, passwd)
			print(f" Jenkins {username} - created with password - {passwd} ")			

role = Roles()
user = Users()
secret_filepath = "../configs/secrets.json"
userdata = get_config_var(secret_filepath, "teams")

if __name__ == '__main__':

	# data = role.get_all_roles()
	# print(data)
	
	# createRoles(role)
	# deleteRoles(role)
	MapRoles(role)
	# RemoveMapping(role)
	# print(user)
	createUsers(user)
