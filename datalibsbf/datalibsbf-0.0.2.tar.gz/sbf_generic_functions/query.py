import logging
from google.cloud import bigquery

def running_bq (**kwargs):
    """Running query on BigQuery
    For example:

    >>> query.running_bq(sql="select * from cnto-data-lake.raw.cnt_ora_0000_kill_wms_prev_transito", project="cnto-data-lake")
    True
    """
    sql = kwargs['sql']
    project = kwargs['project']

    client = bigquery.Client(project=project)

    job = client.query(sql)
    logging.info('api request')
    job.result()
    logging.info('job finish')
    return True