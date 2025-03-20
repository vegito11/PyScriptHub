import os
import requests
import json

base_git_url = 'http://git.shopcart.in/api/v4'
headers = {'PRIVATE-TOKEN': 'nvv_XXXXXXXXXXXXXXXXX'}

user_id = 174
project_id = 3128

def get_group_projects(group_name):
    
    projects = []

    url = f"{base_git_url}/groups/{group_name}"

    response = requests.get(url, data={}, headers= headers)

    if response.status_code == 200 :
        data = response.json()
        uid = user_id
        cnt = 1
        for proj in data["projects"]:
            print("-------"*15)
            print(f' {cnt} ) project name : {proj["web_url"]}')
            try :
                print(f'Forked project Name : {proj["forked_from_project"]["http_url_to_repo"]}')
                fpid = proj["forked_from_project"]["id"]
                pid = proj["id"]
            except KeyError:
                print(KeyError)
                continue

            give_project_access(uid, fpid)
            print("======="*15)
            cnt += 1
            # break

def give_project_access(user_id, project_id, group_id=None):
    
    url = f"{base_git_url}/projects/{project_id}/members/{user_id}"
    # url = f"{base_git_url}/projects/{project_id}/members"

    data = {
        # "user_id": user_id,
        "access_level": 20
    }

    response = requests.put(url, data=data, headers= headers)

    if response.status_code == 201:
        print("Member successfully added to groups")
    elif response.status_code == 409:
        print("Member Already Exists")
    else:    
        print(response)
        print(json.dumps(response.json(), indent=2))

def list_access_req(project_id=3128):

    # url = f"{base_git_url}/projects/{project_id}/access_requests"
    # url = f"{base_git_url}/groups/{group_id}/access_requests"

    response = requests.get(url, data={}, headers= headers)

    print(response)
    print(json.dumps(response.json(), indent=2))


def store_in_file(filename, json_data):
    with open(filename, "w") as jd:
        jd.write( json.dumps(json_data, indent = 2))

def get_project_detail(prj):

    url = f"{base_git_url}/projects/{prj}"
    response = requests.get(url, data={}, headers= headers)

    if response.status_code == 200:
        data = response.json()
        print(data)

    else:
        print(response)


def update_data():


    data_map = {
        # "groups": "groups_data.json",
        "users": "user_data.json",
    }

    for key, file in data_map.items():
        print(key)
        print(file)

        url = f"{base_git_url}/{key}/"
        response = requests.get(url, data={}, headers= headers)

        if response.status_code == 200 and True :
            
            store_in_file(file, response.json())
            with open (file, "r") as f:
                data = f.read()
                print(data)
        else:
            print(response)


def get_user_id(email):

    username = email.split("@shopcart.com")[0].split("_ext")[0]
    url = f"{base_git_url}/users?username={username}"
    response = requests.get(url, data={}, headers= headers)

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
                    pass


        return 

# get_group_projects("certificate")
# list_access_req()
# give_project_access(user_id, project_id)


# update_data()
# get_gid("certificate")

emails = [
    "fname.asd@shopcart.com",
    "fistname.asdd@shopcart.com",
    "asde.dfgerr@shopcart.com",
]


pids = [ 2675, 2676, ]

for email in emails:
    username = email.split("@shopcart.com")[0].split("_ext")[0]

    uid = get_user_id(username)

    if uid:
        for pid in pids:
            # print(f" {pid} : {uid} ")
            give_project_access(uid, pid)

    else:
        print(f" !!! {username} don't have any PID !!! ")

    print("----"*21)

