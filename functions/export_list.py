import boto3
import json
import time

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('klaviyo-user-data')
sqs = boto3.client('sqs')

def lambda_handler(event, context):
    export_data(fetch_dynamo_data())

def fetch_dynamo_data():
    return table.scan()['Items']

def export_data(records):
    queue_url = "https://sqs.us-east-1.amazonaws.com/114147430656/klaviyo-mailer"
    sub_array = []
    for i in range(0, len(records)):
        sub_array.append({
            'Id': str(i),
            'MessageBody': json.dumps(records[i])
        })

        if i % 10 == 0 or i == len(records):
            sqs.send_message_batch(
                QueueUrl=queue_url,
                Entries=sub_array,
            )
            sub_array = []

