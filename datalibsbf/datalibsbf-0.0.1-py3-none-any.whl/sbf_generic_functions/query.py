import logging
from google.cloud import bigquery

def running_bq (**kwargs):

    sql = kwargs['sql']
    project = kwargs['project']

    client = bigquery.Client(project=project)

    job = client.query(sql)
    logging.info('api request')
    job.result()
    logging.info('job finish')
    return True