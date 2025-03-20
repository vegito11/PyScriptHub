import os
import requests
import json
import sys
import gitlab
import subprocess
import git 

def copy_integration_to_release(dev_repo_path, release_repo_path):
	
	# Remove everything from tmp branch of release repo
	results = subprocess.run(f"rm -r {release_repo_path}/* ", 
		shell=True, universal_newlines=True, check=True)

	print(results.stdout)
	
	# Remove .git repo from integration branch and copy all its code to release
	results = subprocess.run(f"rm -r {dev_repo_path}/.git ; cp -r {dev_repo_path}/* {release_repo_path}/ ",
		 shell=True, universal_newlines=True, check=True)
	print(results.stdout)

def push_to_release(release_repo):
	
	COMMIT_MESSAGE = "Copied code of intergration to release repo"
	release_repo.git.add(update=True)
	release_repo.index.commit(COMMIT_MESSAGE)

	origin = release_repo.remote(name='origin')
	result = origin.push()
	print(result)

def clone_repos():

	gl = gitlab.Gitlab('http://git.shopcart.in', private_token = 'nvv_XXXXXXXXXXXXXXXX')
	
	int_project = gl.projects.get(2997)
	release_project = gl.projects.get(2996)

	print(f" 1) Cloning Integration Repo {int_project.ssh_url_to_repo} ...")
	int_repo = git.Repo.clone_from(int_project.ssh_url_to_repo , "intergration_" + int_project.name)

	print(f" 2) Cloning Release Repo {int_project.ssh_url_to_repo} ...")
	release_repo = git.Repo.clone_from(release_project.ssh_url_to_repo , release_project.name)
	release_repo.git.checkout('temp')
	
	print(f" 3) Copying data from intergration to release temp branch")
	copy_integration_to_release("intergration_" + int_project.name, release_project.name)

	push_to_release(release_repo)

clone_repos()
# push_to_release()