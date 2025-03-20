import time
import os
import json
import sys
import re
import requests
from get_branches_mrs import get_fwd_brs
from mr_operations import create_mr, merge_mr, update_mr
from config import MR_LABELS, CONFLICT_LABELS, POST_RELEASE_TARGETS, REL_BRANCH_PATTERN, HEADERS, BASE_URL


def recheck_conflict(proj_id):
	
	url = f"{BASE_URL}/projects/{proj_id}/merge_requests?per_page=40"

	params_all = {
		"labels": ",".join(CONFLICT_LABELS),
		"state": "opened"
	}

	print(f"Getting conflicting merge req for {proj_id}")

	resp = requests.get(url, params=params_all, headers=HEADERS)


	if str(resp.status_code).startswith("20"):
		
		cdata = []
		if resp.json():
			print("waiting for 6 second to recalculate changes")
			time.sleep(6)
			resp = requests.get(url, params=params_all, headers=HEADERS)
			cdata = resp.json()

		for mr in cdata:
			
			print(f"!{mr['iid']} - {mr['has_conflicts']} - {mr['merge_status']}")

			if not mr['has_conflicts']:
				update_mr(proj_id, mr["iid"], {
					"remove_labels": ",".join(CONFLICT_LABELS),
					"add_labels": "conflict_resolved"
				})
				print(f"Removed conflicting labels for !{mr['iid']} due conflicts are resolved ")
				merge_mr(proj_id, mr["iid"])

	else:
	  print(f"{resp.status_code} - failed Getting conflicting merge req - {resp.text}")	