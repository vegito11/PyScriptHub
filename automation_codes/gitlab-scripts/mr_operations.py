import requests
from config import BASE_URL, HEADERS, MR_LABELS
from get_branches_mrs import get_mr

import re

def delete_mr(proj_id, mr_iid):
	
	url = f"{BASE_URL}/projects/{proj_id}/merge_requests/{mr_iid}"

	print(f"Deleting merge req {mr_iid} for {proj_id} ")
	resp = requests.delete(url, headers=HEADERS)

	if str(resp.status_code).startswith("20"):
		print(f" Successfully deleted mr {mr_iid}")
	else:
	  print(f"{resp.status_code} - failed to delete mr - {resp.text}")	  

def create_mr(proj_id, src_br, tg_br):

	url = f"{BASE_URL}/projects/{proj_id}/merge_requests"

	payload = {
		"source_branch": src_br,
		"target_branch": tg_br,
		"title": f"[cascade_bot] Automatic merge: {src_br} -> {tg_br} ",
		"labels": ",".join(MR_LABELS),
		"squash": False
	}

	print(f"Creating merge req for {proj_id} , {src_br} => {tg_br} ")
	resp = requests.post(url, json=payload, headers=HEADERS)

	if str(resp.status_code) == "409":
		
		rdata = resp.json()
		
		for err_msg in rdata["message"]:
			
			if err_msg.startswith("Another open merge request already exists for this source branch:"):
				matches = re.findall(r'!(\d+)', err_msg)
				if matches:
					return matches[-1]
				break

	elif str(resp.status_code).startswith("20"):
		rdata = resp.json()
		cg_cnt = rdata['changes_count']
		print(f"created mr with id {rdata['iid']} - with {cg_cnt} changes ")

		if cg_cnt == "0":
			print("deleting MR with 0 Changes")
			# delete_mr(proj_id, rdata["iid"])
		elif rdata["merge_status"] == "cannot_be_merged":
			update_mr(proj_id, rdata["iid"], {"add_labels": ",".join(conflict_label)})
		
		return rdata["iid"]

	else:
		print(f"{resp.status_code} - failed to create mr - {resp.text}")

def update_mr(proj_id, mr_iid, payload):
	url = f"{BASE_URL}/projects/{proj_id}/merge_requests/{mr_iid}"

	print(f"Updating merge req !{mr_iid} for {proj_id}")
	resp = requests.put(url, json=payload, headers=HEADERS)

	if str(resp.status_code).startswith("20"):
		print(f"Updated merge req !{mr_iid} with conflict label for {proj_id} ")
	else:
		print(f"{resp.status_code} - failed to Update MR - {resp.text}")

def merge_mr(proj_id, mr_iid):

	url = f"{BASE_URL}/projects/{proj_id}/merge_requests/{mr_iid}/merge"

	mr_dtl = get_mr(proj_id, mr_iid)

	if mr_dtl:
		
		if mr_dtl["changes_count"] == 0 or mr_dtl["changes_count"] == None:
			delete_mr(proj_id, mr_iid)
			return True
		
		elif mr_dtl["has_conflicts"]:
			print(f" MR {mr_dtl['web_url']} has merge conflicts {mr_dtl['merge_error']} ")
			update_mr(proj_id, mr_iid, {"add_labels": ",".join(conflict_label)})
			
		else:
			print(f"Merging !{mr_iid} Merge req for {proj_id}")
			resp = requests.put(url, headers=HEADERS)

			if str(resp.status_code).startswith("20"):
				print(f"Merged MR with id {mr_iid}")
				return True
			elif str(resp.status_code).startswith("422"):
				sleep(3)
				print(f"Retrying Merging for MR with id {mr_iid}")
				resp = requests.put(url, headers=HEADERS)
				if str(resp.status_code).startswith("20"):
					return True
			else:
				print(f"{resp.status_code} - failed to Merge mr - {resp.text}")

	else:
		print(f" No details found for mr !{mr_iid}")

	return False

def delete_conflict_mr(proj_id):

	url = f"{BASE_URL}/projects/{proj_id}/merge_requests"

	params_all = {
		# "labels": ",".join(["cascade"]),
		"state": "merged"
	}
	# params_all = {
	# 	"labels": ",".join(["merge_conflict", "automerge_bot"]),
	# 	"state": "opened"
	# }


	mrs = []

	print(f"Getting merge req for {proj_id}")
	resp = requests.get(url, params=params_all, headers=HEADERS)

	if str(resp.status_code).startswith("20"):
		rdata = resp.json()
		for mr in rdata:
			delete_mr(proj_id, mr["iid"])
	else:
	  print(f"{resp.status_code} - failed to create mr - {resp.text}")	  