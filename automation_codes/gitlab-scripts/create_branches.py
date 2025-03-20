import requests
import os

GITLAB_API_URL = "https://gitlab.com/api/v4"
PROJECT_ID = "62057396"

# List of branches to create
branches = [
    "release/12.1", "release/12.2", "release/12.5", "release/13.1", "release/13.3",
    "release/13.4", "release/15.2", "release/15.5",  "release/15.3", "release/16.1",
    "release/16.3", "release/16.4", "release/16.7", "feature/catalog"
]

source_branch = "main"

headers = {
    "PRIVATE-TOKEN": os.getenv("CASCADE_API_TOKEN")
}

# Function to create a branch using GitLab API
def create_branch(branch_name):
    url = f"{GITLAB_API_URL}/projects/{PROJECT_ID}/repository/branches"
    data = {
        "branch": branch_name,
        "ref": source_branch
    }
    response = requests.post(url, headers=headers, data=data)
    
    if response.status_code == 201:
        print(f"Branch '{branch_name}' created successfully.")
    elif response.status_code == 400 and 'already exists' in response.text:
        print(f"Branch '{branch_name}' already exists.")
    else:
        print(f"Failed to create branch '{branch_name}': {response.text}")

# Loop through the list of branches and create them
for branch in branches:
    create_branch(branch)

print("All branch operations completed.")