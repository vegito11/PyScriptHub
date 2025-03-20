import requests
import urllib.parse
from packaging import version
from config import BASE_URL, HEADERS, REL_BRANCH_PATTERN

def get_rel_brs(proj_id):
	
	regex_pattern = REL_BRANCH_PATTERN
	encoded_regex = urllib.parse.quote(regex_pattern, safe='')
	url = f"{BASE_URL}/projects/{proj_id}/repository/branches?regex={encoded_regex}&per_page=100"
	
	print(f"Getting release branch for {proj_id}")
	resp = requests.get(url, data={}, headers=HEADERS)

	if str(resp.status_code).startswith("20"):
		rdata = resp.json()
		branches = [br["name"] for br in rdata]
		return branches
		
	else:
		print(resp.status_code)
		print(resp.text)

	return []

def get_fwd_brs(proj_id, start_br, include_br=False):
	
	print(f"Getting all forward branchs for {start_br}")
	brs = get_rel_brs(proj_id)
	
	sorted_brs = sorted(brs, key=lambda x: version.parse(x.split('/')[1]))
	if include_br:
		gt_brch = [br for br in sorted_brs if version.parse(br.split('/')[1]) >= version.parse(start_br.split('/')[1])]
	else:
		gt_brch = [br for br in sorted_brs if version.parse(br.split('/')[1]) > version.parse(start_br.split('/')[1])]
	fwd_br  = [ b.split('/')[1] for b in gt_brch ]
	
	print(f"All forward branches {', '.join(fwd_br)}")

	return gt_brch

def get_mrs(proj_id, payload={}):

	url = f"{BASE_URL}/projects/{proj_id}/merge_requests"
	params_all = {
		"labels": ",".join(mr_label),
		"state": "opened"
	}
	mrs = []

	print(f"Getting merge req for {proj_id}")
	resp = requests.get(url, json=payload, params=params_all, headers=HEADERS)

	if str(resp.status_code).startswith("20"):
		rdata = resp.json()
		for mr in rdata:
			mrs.append({
				"id": mr["id"],
				"iid": mr["iid"],
				"has_conflicts": mr["has_conflicts"],
				"merge_status": mr["merge_status"],
				"labels": mr["labels"]
			})
		return mrs
		print(json.dumps(mrs, indent=2))
	else:
	  print(f"{resp.status_code} - failed to create mr - {resp.text}")	  


def get_mr(proj_id, mr_iid):

	url = f"{BASE_URL}/projects/{proj_id}/merge_requests/{mr_iid}"

	print(f"Getting merge req !{mr_iid} details for {proj_id}")
	resp = requests.get(url, headers=HEADERS)

	if str(resp.status_code).startswith("20"):
		rdata = resp.json()
		mrdata = {
			"id": rdata["id"],
			"iid": rdata["iid"],
			"merge_status": rdata["merge_status"],
			"changes_count": rdata["changes_count"],
			"has_conflicts": rdata["has_conflicts"],
			"source_branch": rdata["source_branch"],
			"target_branch": rdata["target_branch"],
			"merge_error": rdata["merge_error"],
			"web_url": rdata["web_url"],
			"labels": rdata["labels"]
		}
		return mrdata

	else:
		print(f"{resp.status_code} - failed to create mr - {resp.text}")
		return {}