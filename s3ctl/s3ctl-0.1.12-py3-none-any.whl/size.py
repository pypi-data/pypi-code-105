import boto3
from name import bucket_name


def buckets_number_size(buckets):
    s3 = boto3.client('s3')
    bckt_size = []

    for i in buckets:
        size = s3.list_objects_v2(
            Bucket=i).get('Contents')[0]['Size']
        bckt_size.append(size)

    return bckt_size
