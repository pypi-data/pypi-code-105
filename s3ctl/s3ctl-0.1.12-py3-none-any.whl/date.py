import boto3

from name import bucket_name

client = boto3.client('s3')

try:
    def bucket_creation_date(buckets):

        dates = []

        for bucket in range(len(buckets)):
            dates.append(client.list_buckets()[
                "Buckets"][bucket]["CreationDate"].strftime('%Y-%m-%d-%H:%M:%S'))

        return dates
except client.exceptions.NoSuchEntityException as error:
    raise error
