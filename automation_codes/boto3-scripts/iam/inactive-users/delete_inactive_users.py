from datetime import datetime
from dateutil.tz import tzutc
import json
from utils import (
	get_all_users,
	get_inactive_cli_users, 
	get_inactive_console_users,
	deactivate_console_user,
	deactivate_cli_user
)


if __name__ == '__main__':
	# all_users = get_all_users()
	
	all_users = {'john.doe': datetime(2021, 7, 29, 10, 12, 29, tzinfo=tzutc()), 
				  # 'remote_logger': -1,
				  'akshay.karan': -1,
				  'jason.lee': datetime(2021, 2, 9, 20, 47, 13, tzinfo=tzutc()),
				  'JeanDev': -1,
				  # 'nat.meo': datetime(2021, 8, 11, 18, 51, 44, tzinfo=tzutc()),
    		}
    
	cli_user, infreq_cli_user =  get_inactive_cli_users(all_users)
	password_user, infreq_console_user =  get_inactive_console_users(all_users)

	print("----------------- 1) Console Users ---------------------------------")
	print(json.dumps(password_user, indent=2))
	print(json.dumps(infreq_console_user, indent=2))
	print("----------------- 2) CLI User---------------------------------")
	print(json.dumps(cli_user, indent=2))
	print(json.dumps(infreq_cli_user, indent=2))
	print("================== END ===================")
	deactivate_console_user(password_user, infreq_console_user)
	deactivate_cli_user(cli_user, infreq_cli_user)
	

######============================
# Permissions:

# iam:readalluser
# iam:getLastUsedPassword
# iam:getUser
# iam:deletepassword
# iam:deactive_key

##################################