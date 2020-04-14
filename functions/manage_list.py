import boto3
import json
import re


dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('klaviyo-user-data')


def lambda_handler(event, context):

    response = write_entry(json.loads(event['body']))

    if response:
        return {
            'statusCode': 200,
            'body': json.dumps({
                'status': 200,
                'message': 'Processed Successfully'
            })
        }
    else:
        return {
            'statusCode': 422,
            'body': json.dumps({
                'status': 422,
                'message': 'Invalid Input'
            })
        }



def write_entry(unsafe_data):
    validated_data = validate_data(unsafe_data)

    if validated_data:
        return table.put_item(Item=validated_data)

    return False


def validate_data(data):
    if 'email_address' in data and 'location' in data:
        regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'

        if (re.search(regex, data['email_address'])):
            return {
                'email_address': data['email_address'],
                'location': data['location'],
                'email-location': data['email_address'] + "-" + data['location']
            }

    return False
