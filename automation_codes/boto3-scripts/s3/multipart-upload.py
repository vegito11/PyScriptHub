import os
import boto3
from boto3.s3.transfer import TransferConfig

def resumable_upload(file_path, bucket_name, object_name=None):
    """
    Upload a large file to S3 with resumable capability using multipart upload
    
    :param file_path: Path to the file to upload
    :param bucket_name: Target S3 bucket name
    :param object_name: S3 object name (if None, use file name)
    """
    # Initialize S3 client
    session = boto3.Session(profile_name="one_terra")
    s3 = session.client('s3')
    
    # If object_name was not specified, use file name
    if object_name is None:
        object_name = os.path.basename(file_path)
    
    # Configure multipart upload
    config = TransferConfig(
        multipart_threshold=1024 * 25,  # 25MB
        max_concurrency=10,
        multipart_chunksize=1024 * 25,  # 25MB
        use_threads=True
    )
    
    try:
        # Start/resume the upload
        s3.upload_file(
            file_path,
            bucket_name,
            object_name,
            Config=config,
            Callback=ProgressPercentage(file_path)
        )
        print("\nUpload completed successfully!")
    except Exception as e:
        print(f"\nUpload failed: {str(e)}")
        # The upload can be resumed later as the parts are stored in S3
        # Just run the script again to resume

class ProgressPercentage(object):
    """Callback class to display upload progress"""
    def __init__(self, filename):
        self._filename = filename
        self._size = float(os.path.getsize(filename))
        self._seen_so_far = 0
        self._lock = threading.Lock()
    
    def __call__(self, bytes_amount):
        with self._lock:
            self._seen_so_far += bytes_amount
            percentage = (self._seen_so_far / self._size) * 100
            print(
                f"\rUploading {self._filename}: {self._seen_so_far} / {self._size} "
                f"({percentage:.2f}%)",
                end=""
            )

if __name__ == "__main__":
    import threading
    
    file_path = "C:\\Users\\Testing\\Downloads\\Large_Video.mp4"
    bucket_name = "temp-testing-demo-bucket.demo.io"
    object_name = "videos/large_video.mp4"
    
    # Start the upload
    resumable_upload(file_path, bucket_name, object_name)