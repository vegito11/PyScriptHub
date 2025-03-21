import json
import re
from utils import (
    logger,
    send_slack_message,
    is_skip_vm,
    sess,
    SLACK_CHANNEL
)

ec2_client = sess.client("ec2")
cnt = 1


def start_stop_vms(vms, operation=None, dry_run=False):
    """ --- start/stop instance
    Args:
        vms (dict): map of {vmid: [vm_status, vm_name] }
        operation (string, optional): stop/start. Defaults to None.
        dry_run (bool, False): True/False. Defaults to False.
    """

    result = ""

    for vmid, vmdata in vms.items():
        vmname, state = vmdata[1], vmdata[0]
        
        if not re.search(r'.*prod*|.*eks.*|worker-13', vmdata[1]):
        
            if operation == "stop" and state not in ["stopped", "stopping"]:
                msg = f'Stopping *{vmid}* - `{vmname}` ... '
                result += msg + "\n"
                logger.info(msg)
                response = ec2_client.stop_instances(InstanceIds=[ vmid ], DryRun=dry_run)
        
            elif operation == "start" and state not in ["running", "stopping"]:
        
                msg = f'Started *{vmid}* - `{vmname}` ... '
                result += msg + "\n"
                logger.info(msg)
                response = ec2_client.start_instances( InstanceIds=[vmid], DryRun=dry_run,)
        
            elif not operation:
                logger.info(f"No operation selected for {vm} - {vmname}")

    if operation == "stop":
        send_slack_message("STOPPING VM", result, color="#FFE57F", receiver=SLACK_CHANNEL)
    if operation == "start":
        send_slack_message("STARTING VM", result, color="#69F0AE", receiver=SLACK_CHANNEL)
            
# ---- 2) Filter the instances to stop/start

def process_instances(vms):

    global cnt
    result_vm = {}

    for vm in vms["Reservations"]:
        
        if is_skip_vm(vm["Instances"][0]):
            continue
        
        vm_id, state = vm["Instances"][0]["InstanceId"], vm["Instances"][0]["State"]["Name"]
        tags = vm["Instances"][0]["Tags"]
        
        # Convert [{Key: Name, Value: VM1}, ..] array to {Name:VM1} dict
        vmname =  [tag["Value"] for tag in tags if tag["Key"].lower() in ["name"]] 
        vmname =  vmname[0] if vmname else "UNKNOWN"
        
        logger.info(f' {cnt} ) {vm_id} - {state} - {vmname} ')
        result_vm[vm_id] = [state, vmname]

        cnt = cnt + 1

    return result_vm

# --- 1) get the instances from aws using sdk

def get_filtered_instances(vms="all"):

    paginator = ec2_client.get_paginator('describe_instances')
    pg_token, filterd_vms = None, {}

    filters = [{
        'Name': 'tag:environment',
        'Values': ['management']
    }]

    while True and pg_token != -1:

        
        if vms == "all" or len(vms) and vms[0] == "all":
            pass
        elif vms[0].startswith("i-0"):
            filters.append({ 'Name': 'instance-id', 'Values': vms})
        else:
            filters.append({ 'Name': 'tag:Name', 'Values': vms})

        ec2_paginator = paginator.paginate(
            Filters=filters,
            DryRun=False,
            PaginationConfig={
                'PageSize': 15,
                'StartingToken': pg_token
            }
        )
        for page in ec2_paginator:
            data = json.dumps(page, indent=2, default=str)
            result_vm = process_instances(page)
            filterd_vms.update(result_vm)
            pg_token = page.get("NextToken", -1)

    # logger.info(filterd_vms)
    return filterd_vms