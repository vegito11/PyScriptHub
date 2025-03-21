# https://milvus.io/api-reference/pymilvus/v2.0.2/Collection/Collection().md
from pymilvus import Milvus, Collection, connections, utility
import os

milvus_host = os.getenv("MILVUS_HOST", "localhost")
milvus_port = os.getenv("MILVUS_PORT", "19530")
milvus_url  = f"{milvus_host}:{milvus_port}"

connections.connect(alias="default", host=milvus_host, port=milvus_port)


def take_snapshot(milvus_url, collection_name, snapshot_file_path):
    # Create Milvus client
    milvus_client = Milvus(milvus_url)

    # Create snapshot
    snapshot = milvus_client.snapshot(collection_name)
    snapshot_path = os.path.join(snapshot_file_path, f"{collection_name}.snapshot")

    # Save snapshot to file
    with open(snapshot_path, "wb") as f:
        for chunk in snapshot:
            f.write(chunk)

    # Release snapshot resources
    snapshot.release()

def restore_snapshot(milvus_url, collection_name, snapshot_file_path):
    # Create Milvus client
    milvus_client = Milvus(milvus_url)

    # Load snapshot file
    snapshot_path = os.path.join(snapshot_file_path, f"{collection_name}.snapshot")
    with open(snapshot_path, "rb") as f:
        snapshot_data = f.read()

    # Load snapshot into collection
    milvus_client.load_collection(collection_name, snapshot_data)

    # Release snapshot resources
    milvus_client.release_collection(collection_name)

def get_coll_details(name="llamalection"):
    
    coll = Collection(name)
    return coll.index()


def list_collections():
    
    return utility.list_collections()

def query_coll(coll_name="llamalection"):

    coll = Collection(coll_name)
    

    res = coll.query(
            expr = "Mandatory documents for export/import of goods from/into India",
            consistency_level="Strong"
        )

    print(res)


def delete_collection(name="llamalection"):
    
    utility.drop_collection(name)


x  = list_collections()
x  = delete_collection()
print(x)
# query_coll()

connections.disconnect("default")

# print(x)
