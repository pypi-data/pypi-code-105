import boto3


def bucket_name(buckets):

    s3 = boto3.resource('s3')
    bckt = []

    for bucket in buckets:
        bckt.append(bucket)

    return print(bckt)
