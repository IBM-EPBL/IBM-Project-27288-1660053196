import ibm_boto3
from ibm_botocore.client import Config, ClientError

COS_ENDPOINT="https://s3.jp-tok.cloud-object-storage.appdomain.cloud"
COS_API_KEY_ID="cVWZ4RVLsIGhnc7FwrQxiF_AQ4PpCrTjnU5BCrJyAmQm"
COS_INSTANCE_CRN="crn:v1:bluemix:public:cloud-object-storage:global:a/702af44240f54d66ba7adebefb61dd74:21d01580-e4e2-41a3-8589-ef29aaacb70d::"
COS_BUCKET_LOCATION="jp-tok-smart"

cos = ibm_boto3.resource("s3",
    ibm_api_key_id=COS_API_KEY_ID,
    ibm_service_instance_id=COS_INSTANCE_CRN,
    config=Config(signature_version="oauth"),
    endpoint_url=COS_ENDPOINT
)
def get_buckets():
    print("Retrieving list of buckets")
    try:
        buckets = cos.buckets.all()
        print(buckets)
        for bucket in buckets:
            print("Bucket Name: {0}".format(bucket.name))
    except ClientError as be:
        print("CLIENT ERROR: {0}\n".format(be))
    except Exception as e:
        print("Unable to retrieve list buckets: {0}".format(e))

get_buckets()
