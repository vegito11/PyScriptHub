import json
import re
from utils import (
    logger,
    send_slack_message,
    get_config_var,
    sess,
)

eks_client = sess.client("eks")

def update_nodegroup_config(clt_nm, ng_nm, config):
    
    response = eks_client.update_nodegroup_config(
        clusterName=clt_nm,
        nodegroupName=ng_nm,
        scalingConfig=config
    )
    logger.info(f' Scaling Operation Response is - {response["ResponseMetadata"].get("HTTPStatusCode")}')
    # logger.info(response)
    return response["ResponseMetadata"].get("HTTPStatusCode")

def update_cluster(clt_nm, type="upscale"):
    
    clt = get_config_var("clusters", clt_nm)

    if clt and clt.get("desired_config"):
        ngname = clt.get("ng_name")
        node_config = clt.get("desired_config")

        if type == "upscale":
            logger.info(f" Autoscaling Cluster {clt_nm} {node_config} ")
            return update_nodegroup_config(clt_nm, ngname, node_config)
            
        
        elif type == "downscale":
            logger.info(f" Downscaling Cluster {clt_nm} ")
            node_config = {
                "minSize": 0,
                "maxSize": 1,
                "desiredSize": 0
            }
            return update_nodegroup_config(clt_nm, ngname, node_config)

    else:
        logger.info(f"Invalid Cluster Name {clt_nm}  ...")

if __name__ == '__main__':
    # update_cluster("development")
    pass