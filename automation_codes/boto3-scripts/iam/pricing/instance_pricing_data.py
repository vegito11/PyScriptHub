import json
import requests

def store_instance_data(region="ap-south-1"):
	url = f"https://ec2.shop/?region={region}"
	headers = {"Accept": "application/vnd.github+json"}
	response = requests.get(url, headers=headers)
	data = json.dumps(response.json(), indent=2)

	filename = "instance_data.json"
	with open(filename, "w") as outfile:
	    outfile.write(data)

def sort_dict(in_dict):
	sorted_workers = sorted(in_dict.items(),key= lambda col : col[1])
	for item in sorted_workers:
		print(item[0], item[1])

def sort_workers():

	dict_data = {}
	filename = "pods_cnt.log"

	with open(filename) as f:		
		for line in f.read().split("\n"):
			if line.strip():
				itype, cnt = line.split(" ")
				dict_data[itype] = int(cnt)
				# print(cnt, itype)

	sort_dict(dict_data)

def show_instance_podcnt():

	filename = "instance_data.json"
	with open(filename) as f:
		data = json.load(f)

	filename = "pods_cnt.log"
	with open(filename) as f:
		for line in f.read().split("\n"):
			itype, icnt = line.split()
			for inst in data["Prices"]:
				if inst["InstanceType"] == itype and int(icnt) < 60 :
					# print(f'{itype.ljust(13)} - {icnt.rjust(3)} - {inst["Memory"].rjust(9)} - {str(inst["VCPUS"]).rjust(3)} - {inst["Cost"]} ')
					print(f'{itype.ljust(13)} \t {icnt.rjust(3)} \t {inst["Memory"].rjust(9)} \t {str(inst["VCPUS"]).rjust(3)} \t {inst["Cost"]} ')

# store_instance_data()
# sort_workers()
show_instance_podcnt()
# summary()

