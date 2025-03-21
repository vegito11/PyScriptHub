# Role-based Authorization Strategy
import jenkins
import json
from ..jenkins_util import get_api_session
from ..utilities import get_config_var
from permissions import Permissions

class Roles(object):

    def __init__(self, ssl_verify=True, ssl_cert=None):
        self.session, self.url = get_api_session(ssl_verify, ssl_cert)
        self.url = self.url + '/role-strategy/strategy'

    def get_all_roles(self):
        api_url = self.url + "/getAllRoles"
        data = self.session.get(api_url, params={})
        return data.json()
        # print(data.json())

    @staticmethod
    def get_true_permission(perm_list=[{}, {}]):
        
        result = []
        for perm_map in perm_list:
            for perm in perm_map:
                if perm_map[perm]:
                    result.append(perm)

        return result

    def create_role(self, rolename, permissions, type="globalRoles", pattern=None):
        '''	
            type: [globalRoles, projectRoles, slaveRoles]
            pattern: job pattern like .*-ci
        '''

        api_url = self.url + '/addRole'

        permids = self.get_true_permission(permissions)	
        perm_str = ','.join(permids)

        data = {
            "type": type,
            "roleName": rolename,
            "permissionIds": perm_str,
            "overwrite": True
        }    

        if pattern:
            data['pattern'] = pattern

        # print(data)

        response = self.session.post(api_url, data=data)

        if response.status_code == 200:
            print(f" {rolename} Role created successfully - {pattern}")
	
    def delete_role(self, rolename, type="globalRoles"):

        api_url = self.url + '/removeRoles'

        data = {
            "type": type,
            "roleNames": rolename,
        }

        response = self.session.post(api_url, data=data)

        if response.status_code == 200:
            print(f" {rolename} Role deleted successfully")

        # print(response)

    def assign_role_to_user(self, rolename, username, type="globalRoles"):

        api_url = self.url + '/assignRole'

        data = {
            "type": type,
            "roleName": rolename,
            "sid": username
        }

        # print(data)
        response = self.session.post(api_url, data=data)

        if response.status_code == 200:
            print(f"Role {rolename} has been assigned to user {username} successfully")

        # print(response)

    def remove_role_from_user(self, rolename, username, type="globalRoles"):

        api_url = self.url + '/unassignRole'

        data = {
            "type": type,
            "roleName": rolename,
            "sid": username
        }

        response = self.session.post(api_url, data=data)

        if response.status_code == 200:
            print(f"Role {rolename} has been Removed from user {username} successfully")

        # print(response)

class Users:

	def __init__(self, ssl_verify=True, ssl_cert=None):
		self.session, self.url = get_api_session(ssl_verify, ssl_cert)
		self.url = self.url

	def get_all_roles(self):
		api_url = self.url + "/getAllRoles"
		data = self.session.get(api_url, params={})
		return data.json()

	def create_user(self, username, email, password):

		api_url = self.url + 'securityRealm/createAccountByAdmin'
		fname = username.split("_")[0].capitalize()
		lname = username.split("_")[-1].capitalize()
		
		if fname != lname:
			fullname = fname + " " + lname 
		else:
			fullname = fname

		data = {
			"username": username,
			"password1": password,
			"password2": password,
			"fullname": fullname,
			"email": email,
			# "Jenkins-Crumb": self.session.headers["Jenkins-Crumb"],
		}
		
		response = self.session.post(api_url, data=data)

		if response.status_code == 200:
			print(f" {username} user has been created")


if __name__ == '__main__':
	pass