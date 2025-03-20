import datetime
import boto3

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from botocore.signers import CloudFrontSigner

####----------------------------------
### openssl genrsa -out cloudfront_development_bucket.pem 2048
### openssl rsa -pubout -in cloudfront_development_bucket.pem -out cloudfront_development_bucket.pub
####----------------------------------

def rsa_signer(message):
    key_file_path = "cloudfront_development_bucket.pem"
    with open(key_file_path, 'rb') as key_file:
       private_key = serialization.load_pem_private_key(
           key_file.read(),
           password=None,
           backend=default_backend()
       )
    return private_key.sign(message, padding.PKCS1v15(), hashes.SHA1())


def get_signed_url(file_path):

    key_id = 'KV2XXXXXXXXXXXXXXX'
    cloudfront_url = "https://assests.shopkart.io"
    url = f'{cloudfront_url}/{file_path}'

    cloudfront_signer = CloudFrontSigner(key_id, rsa_signer)
    # Create a signed url that will be valid until the specific expiry date
    # provided using a canned policy.
    from datetime import datetime, timedelta
    import pytz

    expire_date = datetime.now(pytz.timezone('Asia/Kolkata')) + timedelta(minutes=4)

    signed_url = cloudfront_signer.generate_presigned_url(url, date_less_than=expire_date)
    print(url)
    print(signed_url)

file_path = "b013b4c0-b2ca-4c57-b2e7-979bdd4bfe0e/saCxC5099b.PNG"
# file_path = "b013b4c0-b2ca-4c57-b2e7-979bdd4bfe0e/thor.jpg"
# file_path = "b013b4c0-b2ca-4c57-b2e7-979bdd4bfe0e/messi.jpg?ver=1"
# file_path = "b013b4c0-b2ca-4c57-b2e7-979bdd4bfe0e/messi.jpg?versionId=D13zwclU.x.nj4TaPzpAoGQduDk_QuX6"
# file_path = "b013b4c0-b2ca-4c57-b2e7-979bdd4bfe0e/messi.jpg?versionId=63QvES._VI6n7o.D60QIsT9FcTRY3arZ"
# file_path = "img/LoginBack.png"

# url = 'http://d454gfdgfd344.cloudfront.net/hello.txt'

get_signed_url(file_path)

print()
