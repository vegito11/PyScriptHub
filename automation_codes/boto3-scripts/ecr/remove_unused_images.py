import boto3
import datetime
import json
import os

boto_session = boto3.Session(profile_name='jenkins_ecr', region_name="ap-south-1")
ecr_client = boto_session.client('ecr')


def get_days_diff(dt):
	today = datetime.date.today()
	dt = datetime.datetime.strptime(dt,"%Y-%m-%d").date()
	return (today - dt).days

def get_older_images(img_name, img_ids):

	# 1) Add untagged image Digest in delete image array
	del_img_ids = [ {"imageDigest": img["imageDigest"]} for img in img_ids if not img.get("imageTags")]

	num_of_imgs = len(img_ids) - len(del_img_ids)
	
	print("\t Number of images available are ", num_of_imgs)
	# 2) If images are less than 10 skip further processing
	if num_of_imgs <= MIN_IMG_TO_KEEP:
		return del_img_ids

	# 3) Add all image which are older than 60 days
	else:
		for img in img_ids:
			
			if img.get("imageTags"):
				img_created_at = str(img["imagePushedAt"]).split()[0]
				old_days = get_days_diff(img_created_at)

				# if days greater than THRESHOLD_DAYS (like 30 days )  add it to delete array
				if old_days >= THRESHOLD_DAYS and num_of_imgs > MIN_IMG_TO_KEEP:
					del_img_ids += [{"imageDigest": img["imageDigest"], "imageTag": tag} for tag in img["imageTags"] if tag not in skip_tags]
					num_of_imgs -= 1
					print(f"\t Number of images available are {num_of_imgs}, we need to keep minimum {MIN_IMG_TO_KEEP}")
			
	return del_img_ids

def delete_tags(img_name, img_ids, dry_run=False):
	
	print("\t Getting tags/hash of images to be deleted  .... ")
	tag_to_delete = get_older_images(img_name, img_ids)
	
	if tag_to_delete:
		str_list = [ tag.get("imageTag","") for tag in tag_to_delete ]
		print("\t !!! Deleting following tags of",img_name,(" -- ".join(str_list)))

		if not dry_run:
			for item in tag_to_delete:
				print(f" \t {item}")

			try:
				response = ecr_client.batch_delete_image(repositoryName=img_name, imageIds=tag_to_delete)
				print(json.dumps(response["ResponseMetadata"], indent=2))
				if response["ResponseMetadata"]["HTTPStatusCode"] != 200:
					print(response['failures'])
				pass
			except Exception as e:
				print("\t Error in deleting images", e)
				raise e
	
	else:
		print("\t Hurray !! You don't have any older tags to delete :) ")

def clean_ecr_repo():
	cnt=0
	for svc_name in service_names:
		cnt += 1
		print(f" \n =============== {cnt}) Deleting image of service {svc_name} =============== \n ")
		IMG_NAME = REPO_PREFIX + "/" + svc_name
		try:
			images_info = ecr_client.describe_images(repositoryName=IMG_NAME)
			# delete_tags(IMG_NAME, images_info["imageDetails"])
			delete_tags(IMG_NAME, images_info["imageDetails"], DRY_RUN)
		
		except Exception as e:
			print("\t !!! Error occurred while fetching image tags", e)

if __name__ == '__main__':
	
	AWS_ACCOUNT_ID = "69678532XXXX"
	REPO_PREFIX = "saas"
	ECR_REPO = AWS_ACCOUNT_ID + ".dkr.ecr.ap-south-1.amazonaws.com/"
	THRESHOLD_DAYS = 30  # All images who are greater than threshould days will be removed
	MIN_IMG_TO_KEEP = 2 # min number of tags to keep
	DRY_RUN = True # True/ False

	service_names = [ "platform", "document-gen",
	  					"frontend"
					]	

	skip_tags = ["master_185-alpine", "master_55-alpine"]
	
	clean_ecr_repo()
