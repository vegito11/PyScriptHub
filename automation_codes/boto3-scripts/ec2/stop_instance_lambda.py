import json
from instance_processor import (
    start_stop_vms,
    get_filtered_instances
)
from eks_processor import update_cluster
from utils import logger, send_slack_message, SLACK_CHANNEL

def process_eks(cluster_info):
    cst, status = "", 100

    if cluster_info and True :
        for cluster in cluster_info:
            logger.info(f'Updating {cluster["name"]}, - {cluster["scale"]}')
            status = update_cluster(cluster["name"], cluster["scale"])
            cst += f'Perfoming `{cluster["scale"]}` on `{cluster["name"]}` cluster - {status} \n'

        send_slack_message("UPDATING EKS CLUSTERS", cst, color="#FFE57F", receiver=SLACK_CHANNEL)

def process_event(event):

    body = event
    if event.get("httpMethod") == "POST":

        ip1, ip2 = event["headers"]["X-Forwarded-For"], event["requestContext"]["identity"]["sourceIp"]
        allowed_ips = ["1.2.3.5", "3.2.19.7"]

        logger.info(f"Message is requested from {ip1} - {ip2} ")
        
        if ip1 in allowed_ips or ip2 in allowed_ips:
            body = json.loads(event.get("body"))
        else:
            errmsg = {"msg": f"{ip1} - {ip2} is not allowed  "}
            return 401, errmsg

    OPERATION = body.get("operation")
    TARGET    = body.get("targets")
    vm_to_prc = {}

    if OPERATION and TARGET:
        vm_to_prc = get_filtered_instances(TARGET)
        # vm_to_prc = {'i-63463454334': ['stopped', 'worker-1']}
        
        start_stop_vms(vm_to_prc, OPERATION, False)

    process_eks(body.get("eks"))
    

    result = { "msg": f" performed {OPERATION} operation successfully for {TARGET}", "vms": vm_to_prc}

    return 200, result

def lambda_handler(event, context):
    
    status, msg = process_event(event)
    
    return { 'statusCode': status, 'body': json.dumps(msg) }

if __name__ == '__main__':
    test_event = {
        # "operation": "stop",
        # "targets": ["all"],
        "eks": [
            {"name": "development", "scale": "downscale"},
        ]
    }
    # lambda_handler(test_event, {})