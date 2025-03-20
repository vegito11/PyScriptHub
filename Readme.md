# Python Scripts Repository

This repository contains a collection of Python scripts for various tasks, including interacting with the GitLab API, AWS automation using Boto3, and connecting to various databases.

## Table of Contents

- [AWS Automation (Boto3)](#aws-automation-boto3)

    -  <details>
        <summary> <b> VPC,Security Group, Networking etc </b> </summary>

         - get vpc info

        </details>
    
    -  **IAM, Secret Manager, Pricing**

        - [Delete Inactive users](./automation_codes/boto3-scripts/iam/inactive-users/delete_inactive_users.py)

        - [Get EC2 instance ](./automation_codes/boto3-scripts/iam/pricing/instance_pricing_data.py)

        - [Rotate User Keys](automation_codes/boto3-scripts/iam/inactive-users/rotate_keys.py)

        - [Add Cognito User](automation_codes/boto3-scripts/cognito/adduser.py)
    
    - **Cloudfront**

        - [Update Distros](./automation_codes/boto3-scripts/cloudfront/update_ditros.py)

        - [Get Signed URL for S3](./automation_codes/boto3-scripts/cloudfront/signed-url.py)

    - **Dynamodb**
        
        - [Dynamodb Crud](./automation_codes/boto3-scripts/dynamodb/db_utils.py)
    
    - **ECR**

        - [Remove Unused Images](automation_codes/boto3-scripts/ecr/remove_unused_images.py)

- [GitLab API Scripts](#gitlab-api-scripts)

    - [Get Branches, MR, Forward Branches](./automation_codes/gitlab-scripts/get_branches_mrs.py)

    - [Check Conflicts](./automation_codes/gitlab-scripts/check_conflicts.py)
    
    - [Create, Get, Delete MR](./automation_codes/gitlab-scripts/mr_operations.py)

    - [Create Branches](./automation_codes/gitlab-scripts/create_branches.py)

    - [Get Project, Group, User Data](./automation_codes/gitlab-scripts/01-get_project_data.py)

    - [List and Give user Access](./automation_codes/gitlab-scripts/02-list_give_access.py)

    - [Clone repo and Commit to Repo](./automation_codes/gitlab-scripts/03-clone-repo-commit.py)

- [Database Connections](#database-connections)

    1. [Postgres](./automation_codes/databases/postgres_qry.py)

    2. [Rabbitmq](./automation_codes/databases/rmq.py)
    
    2. [ActiveMq Producer](./automation_codes/databases/amq_producer.py)

- [Jenkins](./automation_codes/jenkins)

- [Github](./automation_codes/Github)