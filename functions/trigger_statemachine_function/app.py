import boto3
import json
import os
import uuid
import datetime
from urllib.parse import unquote_plus

dynamodb = boto3.resource('dynamodb')
job_table = dynamodb.Table(os.environ['JOB_TABLE'])
create_hls = os.environ['ENABLE_HLS']
sfn_client = boto3.client('stepfunctions')


def lambda_handler(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = unquote_plus(record['s3']['object']['key'])
        object_prefix = key[:key.rfind('/') + 1]
        object_name = key[key.rfind('/') + 1:]

        # create a job item in dynamodb
        job_id = str(uuid.uuid4())
        job_table.put_item(
            Item={
                'id': job_id,
                'bucket': bucket,
                'key': key,
                'object_prefix': object_prefix,
                'object_name': object_name,
                'created_at': datetime.datetime.now().isoformat()
            }
        )

        # kick start the main statemachine for transcoding
        response = sfn_client.start_execution(
            stateMachineArn=os.environ['SFN_ARN'],
            input= json.dumps({
                'job_id': job_id,
                'bucket': bucket,
                'key': key,
                'object_prefix': object_prefix,
                'object_name': object_name,
                'create_hls': create_hls
            })
        )
