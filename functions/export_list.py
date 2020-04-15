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

    for message in records:
        sqs.send_message(
            QueueUrl=queue_url,
            MessageBody=json.dumps(message)
        )

