# Python Scripts Repository

This repository contains a collection of Python scripts for various tasks, including interacting with the GitLab API, AWS automation using Boto3, and connecting to various databases.

## Table of Contents

- [AWS Automation (Boto3)](automation_codes/boto3-scripts/)

    -  <details>
        <summary> <b> VPC,Security Group, Networking etc </b> </summary>

         - get vpc info

        </details>
    
    - **Compute, EKS**

        - [Start and Stop Vms](./automation_codes/boto3-scripts/ec2/stop_instance.py)

        - [Update EKS Nodegroup](./automation_codes/boto3-scripts/eks/upgrade_nodegroup.py)
    
    -  **IAM, Secret Manager, Pricing**

        - [Delete Inactive users](./automation_codes/boto3-scripts/iam/inactive-users/delete_inactive_users.py)

        - [Get EC2 instance ](./automation_codes/boto3-scripts/iam/pricing/instance_pricing_data.py)

        - [Rotate User Keys](automation_codes/boto3-scripts/iam/inactive-users/rotate_keys.py)

        - [Add Cognito User](automation_codes/boto3-scripts/cognito/adduser.py)

        - [Configuring AWS profile creadenials with MFA](bash_scripts/aws/mfa_cli.sh)
    
    - **Cloudfront**

        - [Update Distros](./automation_codes/boto3-scripts/cloudfront/update_ditros.py)

        - [Get Signed URL for S3](./automation_codes/boto3-scripts/cloudfront/signed-url.py)

    - **Dynamodb**
        
        - [Dynamodb Crud](./automation_codes/boto3-scripts/dynamodb/db_utils.py)
    
    - **ECR**

        - [Remove Unused Images](automation_codes/boto3-scripts/ecr/remove_unused_images.py)


- [Azure](./automation_codes/azure)

    - [Get logged azure user](./automation_codes/azure/get-auth-user.py)

    - [List azure vms](./automation_codes/azure/azure_services/list-azure-vms.py)
    
    - [Get and Set KeyVault secret](./automation_codes/azure/azure_services/get-set-secret.py)
    
    - [Azure Blob storage operations](./automation_codes/azure/azure_services/retrive-upload-files.py)

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

    2. [Milvus snapshot backup and restore](./automation_codes/databases/milvus-snapshot.py)

- [Jenkins](./automation_codes/jenkins/)

    - [Jenkins connection](automation_codes/jenkins/jenkins_util.py)

    - [create jenkins job](./automation_codes/jenkins/jenkin/jobs.py)
    
    - [Get Job,Node,Cred Permissions](./automation_codes/jenkins/jenkin/permissions.py)
    
    - [Create, Delete, Map, Remove Role, User Class](./automation_codes/jenkins/jenkin/roles.py)
    
    - [Create, Delete, Map, Remove Role, User](./automation_codes/jenkins/jenkin/rbac.py)
    

- [Github](./automation_codes/github/)
    
    - [Create, Delete branches, set protection rule](./automation_codes/github/crud_branches.py)
    
    - [CRUD webhook](./automation_codes/github/webhook_crud.py)

- [Get Transcript from video](./automation_codes/gcp/get_transcribe.py)
