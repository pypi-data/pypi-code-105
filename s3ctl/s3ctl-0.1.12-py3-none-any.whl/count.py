import boto3

try:
    def buckets_number_obj(buckets):

        s3 = boto3.resource('s3')
        bucket_obj = []

        for bucket in buckets:
            count_obj = sum(1 for i in s3.Bucket(bucket).objects.all())
            bucket_obj.append(count_obj)

        return bucket_obj
except:
    print("error")
