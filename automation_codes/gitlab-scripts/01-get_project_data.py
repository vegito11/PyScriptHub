import os
import requests
import json
import math

base_git_url = 'http://git.shopcart.in/api/v4'
# base_git_url = 'http://git.shopcart.in/api/v4'
headers = {'PRIVATE-TOKEN': 'nvv_sdfdsfdffdsfsfd'}

data_map = {
    "users": {
       "fname": "user_data.json",
       "api_uri": "users",
     },
    "groups": {
       "fname": "groups_data.json",
       "api_uri": "groups",
     },
    "projects": {
       "fname": "projects_data.json",
       "api_uri": "projects",
     }   
}

#####---------------- Get User, Project, Group -------------------------- ####
def store_in_file(filename, json_data):
    with open(filename, "w") as jd:
        jd.write( json.dumps(json_data, indent = 2))

def update_user_data(xmap):

    url = f"{base_git_url}/{xmap['api_uri']}?per_page=1"
    response = requests.get(url, data={}, headers= headers)

    usr_cnt = response.headers["X-Total"]
    per_page  = 100
    pages = int(math.ceil(int(usr_cnt) / per_page) + 1)
    store_data = []

    for page in range(1, pages):

        url = f"{base_git_url}/{xmap['api_uri']}?per_page={per_page}&page={page}"
        response = requests.get(url, data={}, headers= headers)

        print(url)

        if response.status_code == 200 :
            store_data.extend(response.json())
        else:
            print(response)
               
    store_in_file(xmap["fname"], store_data)

def get_group_projects(group_name):
    
    pids = []
    frk_pid = []

    url = f"{base_git_url}/groups/{group_name}"

    response = requests.get(url, data={}, headers= headers)

    if response.status_code == 200 :
        data = response.json()
        # uid = user_id
        cnt = 1
        for proj in data["projects"]:
            print("-------"*15)
            print(f' {cnt} ) project name : {proj["web_url"]}')
            try :
                print(f'Forked project Name : {proj["forked_from_project"]["http_url_to_repo"]}')
                fpid = proj["forked_from_project"]["id"]
                pid = proj["id"]
                frk_pid.append(fpid)
                pids.append(pid)
            except KeyError:
                print(KeyError)
                continue

            # give_project_access(uid, fpid)
            print("======="*15)
            cnt += 1
            # break
    return pids

def get_group_id(group_name):

    with open(data_map["groups"]["fname"]) as f:
        data = json.load(f)
        for group in data:
            if group["name"] == group_name:
                return group["id"]


####---------------- Give Project Access --------------------------- #####

def update_project_access(user_id, project_id, group_id=None):
    
    url = f"{base_git_url}/projects/{project_id}/members/{user_id}"

    data = { "access_level": 40 }

    response = requests.put(url, data=data, headers= headers)
    print(url)
    if response.status_code == 201:
        print("Member successfully added to groups")
    elif response.status_code == 409:
        print("Member Already Exists")
    else:    
        print(response)
        print(json.dumps(response.json(), indent=2))

def give_project_access(user_id, project_id=None, group_id=None):

    if group_id:
        url = f"{base_git_url}/groups/{group_id}/members"
    else:
        url = f"{base_git_url}/projects/{project_id}/members"

    data = {
        "user_id": user_id,
        "access_level": 30 # developer
        # "access_level": 20 # reporter
        # "access_level": 40 # maintainer
    }

    response = requests.post(url, data=data, headers= headers)

    if response.status_code == 201:
        print("Member successfully added to groups")
    elif response.status_code == 409:
        print("Member Already Exists")
    else:
        print(url)
        print(response)
        print(json.dumps(response.json(), indent=2))

def list_access_req(project_id=3128):

    # url = f"{base_git_url}/projects/{project_id}/access_requests"
    # url = f"{base_git_url}/groups/{group_id}/access_requests"

    response = requests.get(url, data={}, headers= headers)

    print(response)
    print(json.dumps(response.json(), indent=2))

#### --------------------- Get Some Data --------------------------- ### 

def get_project_detail(prj):

    url = f"{base_git_url}/projects/{prj}"
    response = requests.get(url, data={}, headers= headers)

    if response.status_code == 200:
        data = response.json()
        print(data)

    else:
        print(response)

def get_user_id(email):

    username = email.split("@shopcart.com")[0].split("_ext")[0]

    url = f"{base_git_url}/users?username={username}"
    print(url)
    response = requests.get(url, data={}, headers=headers)

    if response.status_code == 200:
        data =  response.json()

        if len(data) == 1:
            return data[0]["id"]
        else:
            uname, lname = username.split(".")
            username = uname + "." + lname[0]
            url = f"{base_git_url}/users?username={username}"
            response = requests.get(url, data={}, headers= headers)

            if response.status_code == 200:
                data =  response.json()
                if len(data) == 1:
                    return data[0]["id"]
                else:
                    with open(data_map["users"]["fname"]) as f:
                        data = json.load(f)
                        for user in data:
                            if user["email"] == email:
                                return user["id"]

        return 

def give_grp_access():
  
    grpname = [
        "platform",
        "release",
    ]

    # get_user_id(779)
    uid = 896
    for grp in grpname:
        gid = get_group_id(grp)
        give_project_access(uid, group_id=gid)
        # print(gid)

def project_access():
    pids = [3052, 2992, 2869, 646, 460]
    uids = [ 78 ]

    for pid in pids:
        for uid in uids:
            give_project_access(uid, project_id=pid)
            # update_project_access(uid,project_id=pid)
        # print(pid)


# update_user_data(data_map["users"])
# update_user_data(data_map["projects"])    
# project_access()
give_grp_access()

# print(data)